from decimal import Decimal

from orders.money import round_cents


def percentage_discount(subtotal: Decimal, percent: Decimal) -> Decimal:
    """Return the discount amount for a percentage off the subtotal.

    ``percent`` is expressed as a whole number: 10 means 10%.
    """
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    return round_cents(subtotal * percent / Decimal("100"))


def fixed_amount_discount(subtotal: Decimal, amount: Decimal) -> Decimal:
    """Return a fixed discount capped at the subtotal (never negative)."""
    if amount < 0:
        raise ValueError("discount amount must be non-negative")
    return round_cents(min(subtotal, amount))


def bulk_discount(subtotal: Decimal, quantity: int) -> Decimal:
    """Tiered bulk discount:

    * < 10 items -> 0%
    * 10-24 items -> 5%
    * 25-49 items -> 10%
    * 50+ items -> 15%
    """
    if quantity < 0:
        raise ValueError("quantity must be non-negative")
    if quantity >= 50:
        rate = Decimal("0.15")
    elif quantity >= 25:
        rate = Decimal("0.10")
    elif quantity >= 10:
        rate = Decimal("0.05")
    else:
        rate = Decimal("0")
    return round_cents(subtotal * rate)
