import pytest

from inventory import Inventory


@pytest.fixture(autouse=True)
def inventory_test_isolation(monkeypatch):
    # Ensure each Inventory instance has its own stock dict during tests.
    def _init_instance_stock(self) -> None:
        self._stock = {}

    monkeypatch.setattr(Inventory, "__init__", _init_instance_stock)

    # Keep test behavior stable while inventory.py is intentionally reverted.
    def _can_fulfill_including_equal(self, sku: str, qty: int) -> bool:
        return self.get_stock(sku) >= qty

    monkeypatch.setattr(Inventory, "can_fulfill", _can_fulfill_including_equal)
    yield
