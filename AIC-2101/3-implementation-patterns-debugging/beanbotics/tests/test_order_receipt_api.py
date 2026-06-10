import asyncio
import unittest

from backend.app import (
    OrderCustomizationRequest,
    OrderRequest,
    StatusUpdateRequest,
    list_orders,
    order_service,
    place_order,
    update_order_status,
)
from backend.models import OrderStatus


class OrderReceiptApiTests(unittest.TestCase):
    def setUp(self):
        order_service.orders.clear()
        order_service._next_id = 1

    def _create_order(self):
        response = asyncio.run(
            place_order(
                OrderRequest(
                    item_id="transformer-white",
                    size="large",
                    customizations=OrderCustomizationRequest(
                        extra_shot=True,
                        milk_alternative="oat",
                        whipped_cream=False,
                    ),
                )
            )
        )
        return response["order"]

    def test_order_payload_contains_receipt_fields(self):
        order = self._create_order()

        self.assertIn("receipt", order)
        receipt = order["receipt"]
        self.assertEqual(receipt["base_item"]["label"], "Large Transformer Flat White")
        self.assertEqual(receipt["subtotal"], order["total_price"])
        self.assertEqual(receipt["total_with_tax"], round(receipt["subtotal"] + receipt["tax_amount"], 2))

    def test_completed_orders_include_receipt_in_list(self):
        order = self._create_order()
        order_id = order["order_id"]

        for status in [OrderStatus.PREPARING, OrderStatus.READY, OrderStatus.COMPLETED]:
            updated = asyncio.run(
                update_order_status(
                    order_id,
                    StatusUpdateRequest(status=status),
                )
            )
            self.assertEqual(updated["order"]["status"], status.value)

        listed = asyncio.run(list_orders())
        order_row = next((o for o in listed["orders"] if o["order_id"] == order_id), None)
        self.assertIsNotNone(order_row)
        self.assertEqual(order_row["status"], "completed")
        self.assertIn("receipt", order_row)
        self.assertIn("customization_items", order_row["receipt"])


if __name__ == "__main__":
    unittest.main()
