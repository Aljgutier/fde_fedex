from decimal import Decimal

from orders.discounts import percentage_discount


class TestPercentageDiscount:
    def test_ten_percent_off_100(self):
        assert percentage_discount(Decimal("100.00"), Decimal("10")) == Decimal("10.00")
