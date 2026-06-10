"""
BeanBotics Data Models

Data structures for the BeanBotics coffee ordering system.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


MILK_ALTERNATIVES = {"none", "oat", "almond", "soy"}


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


@dataclass
class MenuItem:
    id: str
    name: str
    description: str
    category: str
    sizes: Dict[str, Dict[str, Any]]


@dataclass
class OrderCustomizations:
    extra_shot: bool = False
    milk_alternative: str = "none"
    whipped_cream: bool = False

    def validate(self) -> None:
        if self.milk_alternative not in MILK_ALTERNATIVES:
            raise ValueError(
                "Invalid milk alternative. Must be one of: none, oat, almond, soy"
            )


@dataclass
class ReceiptLineItem:
    label: str
    price: float


@dataclass
class OrderReceipt:
    base_item: ReceiptLineItem
    customization_items: List[ReceiptLineItem] = field(default_factory=list)
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_with_tax: float = 0.0


@dataclass
class Order:
    order_id: int
    items: List[str]
    total_price: float
    customizations: OrderCustomizations = field(default_factory=OrderCustomizations)
    receipt: Optional[OrderReceipt] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
