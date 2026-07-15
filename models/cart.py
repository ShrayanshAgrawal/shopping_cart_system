import json
import os
from models.linked_list import CartLinkedList
from models.product import Product


class Cart:
    """High level shopping cart, backed by a linked list of items."""

    TAX_RATE = 0.08  # 8% flat tax

    COUPONS = {
        "SAVE10": 0.10,
        "WELCOME5": 0.05,
        "MEGA20": 0.20,
    }

    def __init__(self, catalog):
        self.catalog = catalog
        self.items = CartLinkedList()
        self.applied_coupon = None

    # ---------- Core operations ----------

    def add_item(self, product_id, quantity):
        product = self.catalog.find_by_id(product_id)
        if not product:
            return False, "Product not found."
        if quantity <= 0:
            return False, "Quantity must be positive."
        if product.stock < quantity:
            return False, f"Only {product.stock} unit(s) in stock."

        self.catalog.reduce_stock(product_id, quantity)
        self.items.add(product, quantity)
        return True, f"Added {quantity} x {product.name} to cart."

    def update_item(self, product_id, new_quantity):
        node = self.items.find(product_id)
        if not node:
            return False, "Item not in cart."
        if new_quantity <= 0:
            return False, "Use remove instead of setting quantity to 0."

        diff = new_quantity - node.quantity
        if diff > 0:
            if node.product.stock < diff:
                return False, f"Only {node.product.stock} more unit(s) available."
            self.catalog.reduce_stock(product_id, diff)
        elif diff < 0:
            self.catalog.restore_stock(product_id, -diff)

        self.items.update_quantity(product_id, new_quantity)
        return True, "Quantity updated."

    def remove_item(self, product_id):
        node = self.items.remove(product_id)
        if not node:
            return False, "Item not in cart."
        self.catalog.restore_stock(product_id, node.quantity)
        return True, f"Removed {node.product.name} from cart."

    def clear_cart(self):
        for product, qty in self.items.to_list():
            self.catalog.restore_stock(product.product_id, qty)
        self.items.clear()
        self.applied_coupon = None

    # ---------- Pricing ----------

    def get_subtotal(self):
        return sum(p.price * qty for p, qty in self.items.to_list())

    def get_bulk_discount_rate(self, subtotal):
        """Tiered discount purely based on cart subtotal."""
        if subtotal >= 10000:
            return 0.15
        elif subtotal >= 5000:
            return 0.10
        elif subtotal >= 2000:
            return 0.05
        return 0.0

    def apply_coupon(self, code):
        code = code.upper().strip()
        if code in self.COUPONS:
            self.applied_coupon = code
            return True, f"Coupon '{code}' applied ({int(self.COUPONS[code]*100)}% off)."
        return False, "Invalid coupon code."

    def remove_coupon(self):
        self.applied_coupon = None

    def calculate_totals(self):
        subtotal = self.get_subtotal()
        bulk_rate = self.get_bulk_discount_rate(subtotal)
        bulk_discount = subtotal * bulk_rate

        coupon_rate = self.COUPONS.get(self.applied_coupon, 0.0)
        coupon_discount = subtotal * coupon_rate

        taxable_amount = subtotal - bulk_discount - coupon_discount
        taxable_amount = max(taxable_amount, 0)
        tax = taxable_amount * self.TAX_RATE

        total = taxable_amount + tax

        return {
            "subtotal": subtotal,
            "bulk_discount_rate": bulk_rate,
            "bulk_discount": bulk_discount,
            "coupon": self.applied_coupon,
            "coupon_discount": coupon_discount,
            "tax_rate": self.TAX_RATE,
            "tax": tax,
            "total": total,
        }

    # ---------- Display ----------

    def display_cart(self):
        if self.items.is_empty():
            print("\nYour cart is empty.\n")
            return

        print("\n" + "=" * 78)
        print(f"{'ID':<6}{'Name':<25}{'Price':>10}{'Qty':>6}{'Line Total':>15}")
        print("-" * 78)
        for product, qty in self.items.to_list():
            line_total = product.price * qty
            print(f"{product.product_id:<6}{product.name:<25}{product.price:>10.2f}{qty:>6}{line_total:>15.2f}")
        print("=" * 78)

        totals = self.calculate_totals()
        print(f"{'Subtotal':>63}: Rs.{totals['subtotal']:>10.2f}")
        if totals["bulk_discount"] > 0:
            print(f"{'Bulk Discount (' + str(int(totals['bulk_discount_rate']*100)) + '%)':>63}: -Rs.{totals['bulk_discount']:>9.2f}")
        if totals["coupon_discount"] > 0:
            print(f"{'Coupon ' + str(totals['coupon']):>63}: -Rs.{totals['coupon_discount']:>9.2f}")
        print(f"{'Tax (' + str(int(totals['tax_rate']*100)) + '%)':>63}: Rs.{totals['tax']:>10.2f}")
        print(f"{'GRAND TOTAL':>63}: Rs.{totals['total']:>10.2f}")
        print("=" * 78 + "\n")

    # ---------- Persistence ----------

    def save_cart(self, filepath="data/saved_cart.json"):
        data = {
            "applied_coupon": self.applied_coupon,
            "items": [
                {"product_id": p.product_id, "quantity": qty}
                for p, qty in self.items.to_list()
            ],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        return True

    def load_cart(self, filepath="data/saved_cart.json"):
        if not os.path.exists(filepath):
            return False, "No saved cart found."

        # Restore stock for whatever is currently in the cart before loading
        self.clear_cart()

        with open(filepath, "r") as f:
            data = json.load(f)

        for entry in data.get("items", []):
            product = self.catalog.find_by_id(entry["product_id"])
            if product:
                qty = entry["quantity"]
                if product.stock >= qty:
                    self.catalog.reduce_stock(product.product_id, qty)
                    self.items.add(product, qty)

        self.applied_coupon = data.get("applied_coupon")
        return True, "Cart loaded successfully."