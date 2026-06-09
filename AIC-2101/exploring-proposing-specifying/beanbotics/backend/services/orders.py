"""
Order Service

Manages the BeanBotics order queue — placing, listing, and cancelling orders.
"""

from typing import List, Optional, Dict, Set, Tuple, Literal

from backend.models import Order, OrderStatus
from backend.services.menu import MenuService


VALID_STATUSES: Set[str] = {"pending", "preparing", "ready", "completed", "cancelled"}
ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
    "pending": {"preparing", "cancelled"},
    "preparing": {"ready"},
    "ready": {"completed"},
    "completed": set(),
    "cancelled": set(),
}
TransitionOutcome = Literal["ok", "not_found", "invalid_status", "invalid_transition"]


class OrderService:
    def __init__(self, menu_service: MenuService):
        self.menu_service = menu_service
        self.orders: List[Order] = []
        self._next_id = 1

    def place_order(self, item_id: str, size: str) -> Optional[Order]:
        item = self.menu_service.get_item_by_id(item_id)
        if not item:
            return None
        if size not in item.sizes:
            return None

        price = item.sizes[size]["price"]
        display_name = f"{size.capitalize()} {item.name}"

        order = Order(
            order_id=self._next_id,
            items=[display_name],
            total_price=price,
            status="pending",
        )
        self.orders.append(order)
        self._next_id += 1
        return order

    def is_valid_status(self, status: str) -> bool:
        return status in VALID_STATUSES

    def get_all_orders(self) -> List[Order]:
        return [o for o in self.orders if o.status != "cancelled"]

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def cancel_order(self, order_id: int) -> bool:
        outcome, _, _ = self.update_order_status(order_id, "cancelled")
        return outcome == "ok"

    def update_order_status(self, order_id: int, new_status: str) -> Tuple[TransitionOutcome, Optional[Order], str]:
        if not self.is_valid_status(new_status):
            return "invalid_status", None, f"Unknown status '{new_status}'"

        order = self.get_order_by_id(order_id)
        if not order:
            return "not_found", None, "Order not found"

        current_status = order.status
        if new_status not in ALLOWED_TRANSITIONS[current_status]:
            return (
                "invalid_transition",
                None,
                f"Cannot transition from '{current_status}' to '{new_status}'",
            )

        order.status = new_status  # type: ignore[assignment]
        return "ok", order, ""
