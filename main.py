from models.catalog import Catalog
from models.cart import Cart
from utils.helpers import (
    clear_screen,
    print_header,
    pause,
    get_int_input,
    get_nonempty_input,
    print_products,
)

CATALOG_PATH = "data/catalog.json"
SAVED_CART_PATH = "data/saved_cart.json"


def show_menu():
    print_header("SHOPPING CART SYSTEM")
    print("""
 1. View Product Catalog
 2. Search Products
 3. Filter by Category
 4. Add Item to Cart
 5. Update Item Quantity
 6. Remove Item from Cart
 7. View Cart
 8. Apply Coupon
 9. Remove Coupon
10. Checkout (View Totals)
11. Save Cart
12. Load Cart
13. Clear Cart
 0. Exit
""")


def main():
    catalog = Catalog(CATALOG_PATH)
    cart = Cart(catalog)

    while True:
        clear_screen()
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print_products(catalog.get_all())
            pause()

        elif choice == "2":
            keyword = get_nonempty_input("Search keyword: ")
            print_products(catalog.search_by_name(keyword))
            pause()

        elif choice == "3":
            print("Categories:", ", ".join(catalog.get_categories()))
            category = get_nonempty_input("Enter category: ")
            print_products(catalog.filter_by_category(category))
            pause()

        elif choice == "4":
            print_products(catalog.get_all())
            pid = get_nonempty_input("\nEnter Product ID to add: ")
            qty = get_int_input("Enter quantity: ", min_value=1)
            ok, msg = cart.add_item(pid, qty)
            print(("\n[OK] " if ok else "\n[ERROR] ") + msg)
            pause()

        elif choice == "5":
            cart.display_cart()
            pid = get_nonempty_input("Enter Product ID to update: ")
            qty = get_int_input("Enter new quantity: ", min_value=1)
            ok, msg = cart.update_item(pid, qty)
            print(("\n[OK] " if ok else "\n[ERROR] ") + msg)
            pause()

        elif choice == "6":
            cart.display_cart()
            pid = get_nonempty_input("Enter Product ID to remove: ")
            ok, msg = cart.remove_item(pid)
            print(("\n[OK] " if ok else "\n[ERROR] ") + msg)
            pause()

        elif choice == "7":
            cart.display_cart()
            pause()

        elif choice == "8":
            print("Available coupons:", ", ".join(Cart.COUPONS.keys()))
            code = get_nonempty_input("Enter coupon code: ")
            ok, msg = cart.apply_coupon(code)
            print(("\n[OK] " if ok else "\n[ERROR] ") + msg)
            pause()

        elif choice == "9":
            cart.remove_coupon()
            print("\n[OK] Coupon removed.")
            pause()

        elif choice == "10":
            cart.display_cart()
            pause()

        elif choice == "11":
            cart.save_cart(SAVED_CART_PATH)
            print("\n[OK] Cart saved successfully.")
            pause()

        elif choice == "12":
            ok, msg = cart.load_cart(SAVED_CART_PATH)
            print(("\n[OK] " if ok else "\n[ERROR] ") + msg)
            pause()

        elif choice == "13":
            confirm = input("Are you sure you want to clear the cart? (y/n): ").strip().lower()
            if confirm == "y":
                cart.clear_cart()
                print("\n[OK] Cart cleared.")
            pause()

        elif choice == "0":
            print("\nThank you for shopping with us. Goodbye!\n")
            break

        else:
            print("\nInvalid choice. Try again.")
            pause()


if __name__ == "__main__":
    main()