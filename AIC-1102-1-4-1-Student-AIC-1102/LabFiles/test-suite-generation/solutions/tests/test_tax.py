from decimal import Decimal

import pytest

from orders.tax import STATE_RATES, calculate_tax, is_tax_exempt, rate_for_state


class TestRateForState:
    @pytest.mark.parametrize("state", sorted(STATE_RATES.keys()))
    def test_known_state_returns_configured_rate(self, state):
        assert rate_for_state(state) == STATE_RATES[state]

    def test_lowercase_state_normalizes(self):
        assert rate_for_state("ca") == STATE_RATES["CA"]

    def test_unknown_state_raises_keyerror(self):
        with pytest.raises(KeyError):
            rate_for_state("XX")


class TestCalculateTax:
    def test_general_category_multiplies_by_state_rate(self):
        result = calculate_tax(Decimal("100.00"), "CA", "general")
        assert result == Decimal("7.25")

    def test_rounds_to_cents(self):
        result = calculate_tax(Decimal("12.345"), "NY", "general")
        assert result == Decimal("0.99")

    @pytest.mark.parametrize("category", ["groceries", "prescription_drugs"])
    def test_exempt_category_returns_zero(self, category):
        assert calculate_tax(Decimal("100.00"), "CA", category) == Decimal("0")

    def test_unknown_state_raises_keyerror(self):
        with pytest.raises(KeyError):
            calculate_tax(Decimal("100.00"), "XX", "general")

    def test_default_category_is_general(self):
        with_default = calculate_tax(Decimal("100.00"), "CA")
        with_explicit = calculate_tax(Decimal("100.00"), "CA", "general")
        assert with_default == with_explicit


class TestIsTaxExempt:
    @pytest.mark.parametrize("category,expected", [
        ("groceries", True),
        ("prescription_drugs", True),
        ("general", False),
        ("electronics", False),
        ("", False),
    ])
    def test_category_membership(self, category, expected):
        assert is_tax_exempt(category) is expected
