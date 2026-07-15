import json
import os
from models.product import Product


class Catalog:
    """Array-based product catalog (Python list acts as the array)."""

    def __init__(self, filepath="data/catalog.json"):
        self.filepath = filepath
        self.products = []  # <-- the "array" of Product objects
        self.load_catalog()

    def load_catalog(self):
        if not os.path.exists(self.filepath):
            self.products = []
            return
        with open(self.filepath, "r") as f:
            raw = json.load(f)
        self.products = [Product.from_dict(p) for p in raw]

    def save_catalog(self):
        with open(self.filepath, "w") as f:
            json.dump([p.to_dict() for p in self.products], f, indent=2)

    def get_all(self):
        return self.products

    def find_by_id(self, product_id):
        for p in self.products:
            if p.product_id.upper() == product_id.upper():
                return p
        return None

    def search_by_name(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.products if keyword in p.name.lower()]

    def filter_by_category(self, category):
        category = category.lower()
        return [p for p in self.products if p.category.lower() == category]

    def get_categories(self):
        return sorted(set(p.category for p in self.products))

    def reduce_stock(self, product_id, qty):
        p = self.find_by_id(product_id)
        if p and p.stock >= qty:
            p.stock -= qty
            return True
        return False

    def restore_stock(self, product_id, qty):
        p = self.find_by_id(product_id)
        if p:
            p.stock += qty