import asyncio
import unittest

from fastapi import HTTPException

from backend.app import (
    menu_service,
    order_service,
    OrderRequest,
    StatusUpdateRequest,
    place_order,
    update_order_status,
    list_orders,
    cancel_order,
)


class ApiStatusLifecycleTests(unittest.TestCase):
    def setUp(self):
        order_service.orders = []
        order_service._next_id = 1
        self.item_id = menu_service.get_all_items()[0].id

    def _create_order(self):
        payload = OrderRequest(item_id=self.item_id, size="medium")
        response = asyncio.run(place_order(payload))
        return response["order"]["order_id"]

    def _patch(self, order_id, status):
        try:
            response = asyncio.run(
                update_order_status(order_id, StatusUpdateRequest(status=status))
            )
            return 200, response
        except HTTPException as exc:
            return exc.status_code, {"detail": exc.detail}

    def test_patch_status_success_and_conflict(self):
        order_id = self._create_order()

        status_code, body = self._patch(order_id, "preparing")
        self.assertEqual(status_code, 200)
        self.assertEqual(body["order"]["status"], "preparing")

        status_code, _ = self._patch(order_id, "completed")
        self.assertEqual(status_code, 409)

    def test_patch_invalid_status_returns_400(self):
        order_id = self._create_order()

        status_code, _ = self._patch(order_id, "confirmed")
        self.assertEqual(status_code, 400)

    def test_patch_missing_order_returns_404(self):
        status_code, _ = self._patch(9999, "preparing")
        self.assertEqual(status_code, 404)

    def test_get_orders_includes_completed_orders(self):
        order_id = self._create_order()

        self.assertEqual(self._patch(order_id, "preparing")[0], 200)
        self.assertEqual(self._patch(order_id, "ready")[0], 200)
        self.assertEqual(self._patch(order_id, "completed")[0], 200)

        response = asyncio.run(list_orders())
        statuses = [order["status"] for order in response["orders"]]
        self.assertIn("completed", statuses)

    def test_delete_cancel_remains_pending_only(self):
        pending_order_id = self._create_order()
        response = asyncio.run(cancel_order(pending_order_id))
        self.assertEqual(response["message"], f"Order {pending_order_id} cancelled")

        active_order_id = self._create_order()
        self.assertEqual(self._patch(active_order_id, "preparing")[0], 200)

        with self.assertRaises(HTTPException) as context:
            asyncio.run(cancel_order(active_order_id))
        self.assertEqual(context.exception.status_code, 409)


if __name__ == "__main__":
    unittest.main()
