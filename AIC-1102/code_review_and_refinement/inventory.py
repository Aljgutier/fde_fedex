class Inventory:
    def __init__(self, items=[]):
        self.items = items

    def add_item(self, name, qty):
        self.items.append({"name": name, "qty": qty})

    def get_stock(self, name):
        """Get current quantity for a named item.

        Args:
            name: Item name to look up.

        Returns:
            The item quantity if found, otherwise None.
        """
        for item in self.items:
            if item["name"] == name:
                return item["qty"]
        return None

    def updateStock(self, name, qty):
        """Set quantity for a named item.

        Args:
            name: Item name to update.
            qty: New quantity to assign.

        Returns:
            True if the item exists and was updated, otherwise False.
        """
        for item in self.items:
            if item["name"] == name:
                item["qty"] = qty
                return True
        return False
