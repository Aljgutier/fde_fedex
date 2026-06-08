"""
BeanBotics Data Models

Data structures for the BeanBotics coffee ordering system.
"""

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


VALID_TRANSITIONS: Dict[OrderStatus, List[OrderStatus]] = {
    OrderStatus.PENDING: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    OrderStatus.PREPARING: [OrderStatus.READY],
    OrderStatus.READY: [OrderStatus.COMPLETED],
    OrderStatus.COMPLETED: [],
    OrderStatus.CANCELLED: [],
}


TAX_RATE = 0.085

OFF_PEAK_DISCOUNT = 0.20


def compute_off_peak_price(base_price: float) -> float:
    discounted = Decimal(str(base_price)) * Decimal(str(1 - OFF_PEAK_DISCOUNT))
    return float(discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

CUSTOMIZATIONS: Dict[str, Dict[str, Any]] = {
    "extra-shot": {"name": "Extra Espresso Shot", "price": 0.75},
    "oat-milk": {"name": "Oat Milk", "price": 0.60},
    "almond-milk": {"name": "Almond Milk", "price": 0.60},
    "soy-milk": {"name": "Soy Milk", "price": 0.60},
    "whipped-cream": {"name": "Whipped Cream", "price": 0.50},
}


@dataclass
class MenuItem:
    id: str
    name: str
    description: str
    category: str
    sizes: Dict[str, Dict[str, Any]]


@dataclass
class Order:
    order_id: int
    items: List[str]
    total_price: float
    status: OrderStatus = OrderStatus.PENDING
    customizations: List[str] = field(default_factory=list)
    items_detail: Optional[Dict[str, Any]] = None
    cogs: Optional[float] = None
    pricing_tier: str = "peak"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
