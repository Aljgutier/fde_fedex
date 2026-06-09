"""
BeanBotics Data Models

Data structures for the BeanBotics coffee ordering system.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Literal
from datetime import datetime, timezone


OrderStatus = Literal["pending", "preparing", "ready", "completed", "cancelled"]


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
    status: OrderStatus
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
