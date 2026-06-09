"""
Order Service

Manages the BeanBotics order queue — placing, listing, and cancelling orders.
"""

from typing import List, Optional

from backend.models import Order, OrderStatus, VALID_TRANSITIONS
from backend.services.menu import MenuService


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
        )
        self.orders.append(order)
        self._next_id += 1
        return order

    def get_all_orders(self) -> List[Order]:
        return [o for o in self.orders if o.status != "cancelled"]

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def update_order_status(self, order_id: int, new_status: OrderStatus) -> Order:
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        allowed = VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from '{order.status.value}' to '{new_status.value}'"
            )
        order.status = new_status
        return order

    def cancel_order(self, order_id: int) -> bool:
        try:
            self.update_order_status(order_id, OrderStatus.CANCELLED)
            return True
        except ValueError:
            return False
