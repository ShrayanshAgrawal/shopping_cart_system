class CartNode:
    """A single node in the cart's singly linked list."""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.next = None


class CartLinkedList:
    """Singly linked list that stores cart items dynamically."""

    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def find(self, product_id):
        current = self.head
        while current:
            if current.product.product_id.upper() == product_id.upper():
                return current
            current = current.next
        return None

    def add(self, product, quantity):
        """Add a product, or increase quantity if it already exists."""
        existing = self.find(product.product_id)
        if existing:
            existing.quantity += quantity
            return existing

        new_node = CartNode(product, quantity)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        return new_node

    def update_quantity(self, product_id, quantity):
        node = self.find(product_id)
        if node:
            node.quantity = quantity
            return True
        return False

    def remove(self, product_id):
        current = self.head
        prev = None
        while current:
            if current.product.product_id.upper() == product_id.upper():
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                self.size -= 1
                return current
            prev = current
            current = current.next
        return None

    def total_items(self):
        current = self.head
        total = 0
        while current:
            total += current.quantity
            current = current.next
        return total

    def to_list(self):
        """Return cart items as a plain Python list of (product, qty) tuples."""
        items = []
        current = self.head
        while current:
            items.append((current.product, current.quantity))
            current = current.next
        return items

    def clear(self):
        self.head = None
        self.size = 0