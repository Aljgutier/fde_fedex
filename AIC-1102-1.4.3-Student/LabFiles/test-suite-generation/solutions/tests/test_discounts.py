from decimal import Decimal

import pytest

from orders.discounts import bulk_discount, fixed_amount_discount, percentage_discount


class TestPercentageDiscount:
    @pytest.mark.parametrize(
        "subtotal,percent,expected",
        [
            (Decimal("100.00"), Decimal("10"), Decimal("10.00")),
            (Decimal("100.00"), Decimal("0"), Decimal("0.00")),
            (Decimal("100.00"), Decimal("100"), Decimal("100.00")),
            (Decimal("33.33"), Decimal("15"), Decimal("5.00")),
        ],
    )
    def test_returns_expected_discount(self, subtotal, percent, expected):
        assert percentage_discount(subtotal, percent) == expected

    @pytest.mark.parametrize("percent", [Decimal("-1"), Decimal("101")])
    def test_out_of_range_percent_raises(self, percent):
        with pytest.raises(ValueError):
            percentage_discount(Decimal("100.00"), percent)


class TestFixedAmountDiscount:
    def test_amount_less_than_subtotal_returns_amount(self):
        assert fixed_amount_discount(Decimal("100.00"), Decimal("10.00")) == Decimal("10.00")

    def test_amount_greater_than_subtotal_is_capped(self):
        assert fixed_amount_discount(Decimal("5.00"), Decimal("10.00")) == Decimal("5.00")

    def test_amount_equal_to_subtotal_returns_subtotal(self):
        assert fixed_amount_discount(Decimal("5.00"), Decimal("5.00")) == Decimal("5.00")

    def test_zero_amount_returns_zero(self):
        assert fixed_amount_discount(Decimal("100.00"), Decimal("0")) == Decimal("0.00")

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            fixed_amount_discount(Decimal("100.00"), Decimal("-1"))


class TestBulkDiscount:
    @pytest.mark.parametrize(
        "quantity,expected_percent",
        [
            (0, Decimal("0")),
            (9, Decimal("0")),
            (10, Decimal("0.05")),
            (24, Decimal("0.05")),
            (25, Decimal("0.10")),
            (49, Decimal("0.10")),
            (50, Decimal("0.15")),
            (1000, Decimal("0.15")),
        ],
    )
    def test_tier_boundaries(self, quantity, expected_percent):
        subtotal = Decimal("100.00")
        expected = (subtotal * expected_percent).quantize(Decimal("0.01"))
        assert bulk_discount(subtotal, quantity) == expected

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            bulk_discount(Decimal("100.00"), -1)
