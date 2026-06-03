from decimal import Decimal

import pytest

from orders.shipping import (
    FREE_SHIPPING_THRESHOLD,
    ZONE_RATES,
    base_rate,
    estimate,
    expedited_surcharge,
)


class TestBaseRate:
    @pytest.mark.parametrize("zone", sorted(ZONE_RATES.keys()))
    def test_multiplies_weight_by_zone_rate(self, zone):
        weight = Decimal("4")
        result = base_rate(weight, zone)
        expected = (weight * ZONE_RATES[zone]).quantize(Decimal("0.01"))
        assert result == expected

    def test_zero_weight_raises(self):
        with pytest.raises(ValueError):
            base_rate(Decimal("0"), "domestic")

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError):
            base_rate(Decimal("-1"), "domestic")

    def test_unknown_zone_raises_keyerror(self):
        with pytest.raises(KeyError):
            base_rate(Decimal("1"), "moon")


class TestExpeditedSurcharge:
    def test_half_of_base_when_above_minimum(self):
        assert expedited_surcharge(Decimal("20.00")) == Decimal("10.00")

    def test_clamps_to_five_dollar_minimum(self):
        assert expedited_surcharge(Decimal("4.00")) == Decimal("5.00")

    def test_exact_minimum_is_five(self):
        assert expedited_surcharge(Decimal("10.00")) == Decimal("5.00")


class TestEstimate:
    def test_free_shipping_at_threshold_non_expedited(self):
        result = estimate(
            weight_lbs=Decimal("10"),
            zone="domestic",
            subtotal=FREE_SHIPPING_THRESHOLD,
            expedited=False,
        )
        assert result == Decimal("0")

    def test_free_shipping_does_not_apply_to_expedited(self):
        result = estimate(
            weight_lbs=Decimal("10"),
            zone="domestic",
            subtotal=FREE_SHIPPING_THRESHOLD,
            expedited=True,
        )
        assert result > Decimal("0")

    def test_below_threshold_returns_base_rate(self):
        result = estimate(
            weight_lbs=Decimal("4"),
            zone="domestic",
            subtotal=Decimal("10.00"),
            expedited=False,
        )
        assert result == Decimal("2.00")

    def test_expedited_adds_surcharge_to_base(self):
        base = base_rate(Decimal("20"), "domestic")
        result = estimate(
            weight_lbs=Decimal("20"),
            zone="domestic",
            subtotal=Decimal("10.00"),
            expedited=True,
        )
        assert result == (base + expedited_surcharge(base)).quantize(Decimal("0.01"))
