from decimal import Decimal

from orders.money import round_cents

STATE_RATES: dict[str, Decimal] = {
    "CA": Decimal("0.0725"),
    "NY": Decimal("0.08"),
    "TX": Decimal("0.0625"),
    "WA": Decimal("0.065"),
}

TAX_EXEMPT_CATEGORIES = {"groceries", "prescription_drugs"}


def rate_for_state(state: str) -> Decimal:
    """Return the base sales tax rate for a US state code.

    Raises ``KeyError`` for states not listed in ``STATE_RATES``.
    """
    return STATE_RATES[state.upper()]


def calculate_tax(subtotal: Decimal, state: str, category: str = "general") -> Decimal:
    """Compute sales tax for a subtotal.

    Returns Decimal("0") if the category is tax-exempt. Otherwise multiplies
    the subtotal by the rate for the given state, rounded to cents.
    """
    if category in TAX_EXEMPT_CATEGORIES:
        return Decimal("0")
    return round_cents(subtotal * rate_for_state(state))


def is_tax_exempt(category: str) -> bool:
    """Return True if the category is in the tax-exempt set."""
    return category in TAX_EXEMPT_CATEGORIES
