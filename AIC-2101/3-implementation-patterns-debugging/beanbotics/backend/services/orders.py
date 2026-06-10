"""
Order Service

Manages the BeanBotics order queue — placing, listing, and cancelling orders.
"""

from typing import List, Optional

from backend.models import (
    Order,
    OrderCustomizations,
    OrderReceipt,
    OrderStatus,
    ReceiptLineItem,
    VALID_TRANSITIONS,
)
from backend.services.menu import MenuService


EXTRA_SHOT_PRICE = 0.75
MILK_ALTERNATIVE_PRICE = 0.60
WHIPPED_CREAM_PRICE = 0.50
TAX_RATE = 0.0825


class OrderService:
    def __init__(self, menu_service: MenuService):
        self.menu_service = menu_service
        self.orders: List[Order] = []
        self._next_id = 1

    def _build_receipt(
        self,
        item_name: str,
        size: str,
        base_price: float,
        customizations: OrderCustomizations,
    ) -> OrderReceipt:
        customization_items: List[ReceiptLineItem] = []

        if customizations.extra_shot:
            customization_items.append(ReceiptLineItem(label="Extra shot", price=EXTRA_SHOT_PRICE))

        if customizations.milk_alternative != "none":
            milk = customizations.milk_alternative.capitalize()
            customization_items.append(
                ReceiptLineItem(label=f"{milk} milk", price=MILK_ALTERNATIVE_PRICE)
            )

        if customizations.whipped_cream:
            customization_items.append(
                ReceiptLineItem(label="Whipped cream", price=WHIPPED_CREAM_PRICE)
            )

        subtotal = round(base_price + sum(i.price for i in customization_items), 2)
        tax_amount = round(subtotal * TAX_RATE, 2)
        total_with_tax = round(subtotal + tax_amount, 2)

        return OrderReceipt(
            base_item=ReceiptLineItem(
                label=f"{size.capitalize()} {item_name}",
                price=round(base_price, 2),
            ),
            customization_items=customization_items,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_with_tax=total_with_tax,
        )

    def place_order(
        self,
        item_id: str,
        size: str,
        customizations: Optional[OrderCustomizations] = None,
    ) -> Optional[Order]:
        item = self.menu_service.get_item_by_id(item_id)
        if not item:
            return None
        if size not in item.sizes:
            return None

        normalized_customizations = customizations or OrderCustomizations()
        normalized_customizations.validate()

        base_price = item.sizes[size]["price"]
        receipt = self._build_receipt(item.name, size, base_price, normalized_customizations)
        total_price = receipt.subtotal
        display_name = f"{size.capitalize()} {item.name}"

        order = Order(
            order_id=self._next_id,
            items=[display_name],
            total_price=total_price,
            customizations=normalized_customizations,
            receipt=receipt,
        )
        self.orders.append(order)
        self._next_id += 1
        return order

    def get_all_orders(self) -> List[Order]:
        return [o for o in self.orders if o.status != OrderStatus.CANCELLED]

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
