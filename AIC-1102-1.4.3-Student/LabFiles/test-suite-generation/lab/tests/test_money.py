from decimal import Decimal

import pytest

from orders.money import format_usd, parse_amount, round_cents


class TestRoundCents:
    @pytest.mark.parametrize(
        "amount,expected",
        [
            (Decimal("1.234"), Decimal("1.23")),
            (Decimal("1.235"), Decimal("1.24")),
            (Decimal("1.00"), Decimal("1.00")),
            (Decimal("0.005"), Decimal("0.01")),
            (Decimal("-1.235"), Decimal("-1.24")),
        ],
    )
    def test_rounds_to_two_places_half_up(self, amount, expected):
        assert round_cents(amount) == expected


class TestFormatUsd:
    def test_prefixes_with_dollar_sign(self):
        assert format_usd(Decimal("10.50")) == "$10.50"

    def test_rounds_to_cents_before_formatting(self):
        assert format_usd(Decimal("10.506")) == "$10.51"

    def test_handles_zero(self):
        assert format_usd(Decimal("0")) == "$0.00"

    def test_pads_single_digit_cents(self):
        assert format_usd(Decimal("10.5")) == "$10.50"


class TestParseAmount:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("10.50", Decimal("10.50")),
            ("$10.50", Decimal("10.50")),
            ("  $10.50  ", Decimal("10.50")),
            ("0", Decimal("0")),
            ("-1.23", Decimal("-1.23")),
        ],
    )
    def test_parses_valid_strings(self, value, expected):
        assert parse_amount(value) == expected

    def test_rejects_non_numeric(self):
        with pytest.raises(Exception):
            parse_amount("not a number")

    def test_rejects_empty_string(self):
        with pytest.raises(Exception):
            parse_amount("")
