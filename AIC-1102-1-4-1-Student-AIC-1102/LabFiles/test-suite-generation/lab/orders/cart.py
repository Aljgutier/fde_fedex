from dataclasses import dataclass
from decimal import Decimal

from orders.money import round_cents


@dataclass
class Line:
    sku: str
    description: str
    unit_price: Decimal
    quantity: int


class Cart:
    """In-memory shopping cart."""

    def __init__(self) -> None:
        self._lines: dict[str, Line] = {}

    def add(self, sku: str, description: str, unit_price: Decimal, quantity: int = 1) -> Line:
        """Add a line. If ``sku`` already exists, increment its quantity."""
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        if sku in self._lines:
            self._lines[sku].quantity += quantity
            return self._lines[sku]
        line = Line(sku=sku, description=description, unit_price=unit_price, quantity=quantity)
        self._lines[sku] = line
        return line

    def remove(self, sku: str) -> bool:
        """Remove the line for ``sku``. Return True if removed, False if not present."""
        return self._lines.pop(sku, None) is not None

    def set_quantity(self, sku: str, quantity: int) -> Line:
        """Set the quantity of an existing line. Raise ``KeyError`` if ``sku`` is unknown."""
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        if sku not in self._lines:
            raise KeyError(sku)
        self._lines[sku].quantity = quantity
        return self._lines[sku]

    def lines(self) -> list[Line]:
        return list(self._lines.values())

    def subtotal(self) -> Decimal:
        """Return the sum of ``unit_price * quantity`` across all lines, rounded to cents."""
        total = sum((line.unit_price * line.quantity for line in self._lines.values()), Decimal("0"))
        return round_cents(total)

    def is_empty(self) -> bool:
        return not self._lines
