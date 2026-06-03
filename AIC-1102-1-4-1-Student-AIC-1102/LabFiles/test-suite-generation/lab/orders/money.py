from decimal import Decimal, ROUND_HALF_UP


def round_cents(amount: Decimal) -> Decimal:
    """Round a Decimal to two decimal places using half-up rounding."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_usd(amount: Decimal) -> str:
    """Format a Decimal as a USD currency string with a dollar sign."""
    return f"${round_cents(amount)}"


def parse_amount(value: str) -> Decimal:
    """Parse a monetary string into a Decimal. Accepts an optional ``$`` prefix."""
    value = value.strip().lstrip("$")
    return Decimal(value)
