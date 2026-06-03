from decimal import Decimal

from orders.money import round_cents

FREE_SHIPPING_THRESHOLD = Decimal("75.00")

ZONE_RATES: dict[str, Decimal] = {
    "domestic": Decimal("0.50"),
    "continental": Decimal("0.75"),
    "international": Decimal("2.25"),
}


def base_rate(weight_lbs: Decimal, zone: str) -> Decimal:
    """Return the base shipping rate in dollars.

    Rate is ``weight_lbs * zone_rate``, rounded to cents. Raises
    ``KeyError`` for unknown zones and ``ValueError`` for non-positive
    weight.
    """
    if weight_lbs <= 0:
        raise ValueError("weight_lbs must be positive")
    return round_cents(weight_lbs * ZONE_RATES[zone])


def expedited_surcharge(base: Decimal) -> Decimal:
    """Return the surcharge for expedited shipping: 50% of base, minimum $5.00."""
    surcharge = base * Decimal("0.5")
    return round_cents(max(surcharge, Decimal("5.00")))


def estimate(
    weight_lbs: Decimal,
    zone: str,
    subtotal: Decimal,
    expedited: bool = False,
) -> Decimal:
    """Estimate the shipping cost for an order.

    Returns Decimal("0") if ``subtotal`` meets the free shipping threshold
    and the order is not expedited. Otherwise returns the base rate plus,
    if applicable, the expedited surcharge.
    """
    if not expedited and subtotal >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0")
    base = base_rate(weight_lbs, zone)
    if expedited:
        return round_cents(base + expedited_surcharge(base))
    return base
