"""
BeanBotics Data Models

Data structures for the BeanBotics coffee ordering system.
"""

from dataclasses import dataclass, field
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

CUSTOMIZATIONS: Dict[str, Dict[str, Any]] = {
    "extra-shot": {"name": "Extra Espresso Shot", "price": 0.75},
    "oat-milk": {"name": "Oat Milk", "price": 0.60},
    "almond-milk": {"name": "Almond Milk", "price": 0.60},
    "soy-milk": {"name": "Soy Milk", "price": 0.60},
    "whipped-cream": {"name": "Whipped Cream", "price": 0.50},
}

# Ingredient unit costs (immutable configuration)
INGREDIENT_UNIT_COSTS: Dict[str, float] = {
    "espresso_shot": 0.40,
    "milk": 0.05,
    "chocolate": 0.08,
    "whipped_cream": 0.25,
    "alternative_milk": 0.15,
}

# Recipes: ingredient quantities by `item_id` and `size` (units are per-drink)
# Small/medium use 1 espresso shot, large uses 2 espresso shots where applicable.
RECIPES: Dict[str, Dict[str, Dict[str, float]]] = {
    "neural-latte": {
        "small": {"espresso_shot": 1, "milk": 6.0},
        "medium": {"espresso_shot": 1, "milk": 8.0},
        "large": {"espresso_shot": 2, "milk": 10.0},
    },
    "machine-mocha": {
        "small": {"espresso_shot": 1, "milk": 5.0, "chocolate": 1.0},
        "medium": {"espresso_shot": 1, "milk": 7.0, "chocolate": 1.5},
        "large": {"espresso_shot": 2, "milk": 9.0, "chocolate": 2.0},
    },
    "transformer-white": {
        "small": {"espresso_shot": 1, "milk": 5.5},
        "medium": {"espresso_shot": 1, "milk": 7.0},
        "large": {"espresso_shot": 2, "milk": 9.0},
    },
    "deep-doppio": {
        "small": {"espresso_shot": 1},
        "medium": {"espresso_shot": 2},
        "large": {"espresso_shot": 2},
    },
    "gan-cappuccino": {
        "small": {"espresso_shot": 1, "milk": 4.0, "whipped_cream": 0.5},
        "medium": {"espresso_shot": 1, "milk": 5.5, "whipped_cream": 0.75},
        "large": {"espresso_shot": 2, "milk": 7.0, "whipped_cream": 1.0},
    },
}

# Map customizations to ingredient contributions for COGS calculation
CUSTOMIZATION_INGREDIENTS: Dict[str, Dict[str, float]] = {
    "extra-shot": {"espresso_shot": 1},
    "oat-milk": {"alternative_milk": 2.0},
    "almond-milk": {"alternative_milk": 2.0},
    "soy-milk": {"alternative_milk": 2.0},
    "whipped-cream": {"whipped_cream": 1.0},
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
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # Financial fields (calculated at order placement)
    revenue: float = 0.0
    cogs: float = 0.0
    margin: float = 0.0
