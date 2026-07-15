class Product:
    """Represents a single product in the catalog."""

    def __init__(self, product_id, name, category, price, stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.stock = int(stock)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["category"],
            data["price"],
            data["stock"],
        )

    def __str__(self):
        return f"{self.product_id} | {self.name:<25} | {self.category:<12} | Rs.{self.price:>9.2f} | Stock: {self.stock}"