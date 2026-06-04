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

    def test_adding_zero_quantity_raises(self, cart):
        with pytest.raises(ValueError):
            cart.add("SKU-1", "Widget", Decimal("9.99"), quantity=0)

    def test_adding_negative_quantity_raises(self, cart):
        with pytest.raises(ValueError):
            cart.add("SKU-1", "Widget", Decimal("9.99"), quantity=-1)


class TestRemove:
    def test_remove_returns_true_for_existing_sku(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        assert cart.remove("SKU-1") is True

    def test_remove_returns_false_for_missing_sku(self, cart):
        assert cart.remove("nope") is False

    def test_remove_drops_line_from_subtotal(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        cart.add("SKU-2", "Gadget", Decimal("5.00"))
        cart.remove("SKU-1")
        assert cart.subtotal() == Decimal("5.00")


class TestSetQuantity:
    def test_sets_quantity_on_existing_line(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        line = cart.set_quantity("SKU-1", 7)
        assert line.quantity == 7

    def test_missing_sku_raises_keyerror(self, cart):
        with pytest.raises(KeyError):
            cart.set_quantity("nope", 1)

    def test_zero_quantity_raises_valueerror(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        with pytest.raises(ValueError):
            cart.set_quantity("SKU-1", 0)


class TestSubtotal:
    def test_empty_cart_returns_zero(self, cart):
        assert cart.subtotal() == Decimal("0.00")

    def test_sums_lines_with_quantity(self, cart):
        cart.add("A", "Widget", Decimal("10.00"), quantity=2)
        cart.add("B", "Gadget", Decimal("3.50"), quantity=4)
        assert cart.subtotal() == Decimal("34.00")

    def test_rounds_to_cents(self, cart):
        cart.add("A", "Odd", Decimal("0.333"), quantity=3)
        assert cart.subtotal() == Decimal("1.00")


class TestLinesAndIsEmpty:
    def test_empty_cart_is_empty(self, cart):
        assert cart.is_empty() is True
        assert cart.lines() == []

    def test_cart_with_line_is_not_empty(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        assert cart.is_empty() is False
        assert len(cart.lines()) == 1

    def test_lines_returns_copy_not_reference(self, cart):
        cart.add("SKU-1", "Widget", Decimal("9.99"))
        snapshot = cart.lines()
        snapshot.clear()
        assert len(cart.lines()) == 1
