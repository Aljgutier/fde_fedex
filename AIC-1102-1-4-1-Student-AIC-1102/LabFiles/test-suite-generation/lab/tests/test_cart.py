from decimal import Decimal

import pytest

from orders.cart import Cart


@pytest.fixture
def cart():
    return Cart()


class TestAdd:
    def test_new_line_is_stored(self, cart):
        line = cart.add("SKU-1", "Widget", Decimal("9.99"))
        assert line.sku == "SKU-1"
        assert line.quantity == 1

    def test_adding_existing_sku_increments_quantity(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"), quantity=2)
        line = cart.add("SKU-1", "Widget", Decimal("9.99"), quantity=3)
        assert line.quantity == 5


class TestRemove:
    def test_remove_returns_true_for_existing_sku(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        assert cart.remove("SKU-1") is True

    def test_remove_returns_false_for_missing_sku(self, cart):
        assert cart.remove("nope") is False
