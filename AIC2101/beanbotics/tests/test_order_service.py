import unittest

from backend.services.menu import MenuService
from backend.services.orders import OrderService


class OrderServiceLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.menu_service = MenuService()
        self.order_service = OrderService(self.menu_service)
        self.item_id = self.menu_service.get_all_items()[0].id

    def _place_order(self):
        order = self.order_service.place_order(self.item_id, "medium")
        self.assertIsNotNone(order)
        return order

    def test_valid_transition_sequence(self):
        order = self._place_order()

        outcome, updated, _ = self.order_service.update_order_status(order.order_id, "preparing")
        self.assertEqual(outcome, "ok")
        self.assertEqual(updated.status, "preparing")

        outcome, updated, _ = self.order_service.update_order_status(order.order_id, "ready")
        self.assertEqual(outcome, "ok")
        self.assertEqual(updated.status, "ready")

        outcome, updated, _ = self.order_service.update_order_status(order.order_id, "completed")
        self.assertEqual(outcome, "ok")
        self.assertEqual(updated.status, "completed")

    def test_invalid_transition_is_rejected(self):
        order = self._place_order()

        outcome, updated, message = self.order_service.update_order_status(order.order_id, "completed")
        self.assertEqual(outcome, "invalid_transition")
        self.assertIsNone(updated)
        self.assertIn("Cannot transition", message)

    def test_invalid_status_value_is_rejected(self):
        order = self._place_order()

        outcome, updated, message = self.order_service.update_order_status(order.order_id, "confirmed")
        self.assertEqual(outcome, "invalid_status")
        self.assertIsNone(updated)
        self.assertIn("Unknown status", message)

    def test_cancel_allowed_only_from_pending(self):
        pending_order = self._place_order()
        outcome, updated, _ = self.order_service.update_order_status(pending_order.order_id, "cancelled")
        self.assertEqual(outcome, "ok")
        self.assertEqual(updated.status, "cancelled")

        active_order = self._place_order()
        outcome, _, _ = self.order_service.update_order_status(active_order.order_id, "preparing")
        self.assertEqual(outcome, "ok")

        outcome, updated, _ = self.order_service.update_order_status(active_order.order_id, "cancelled")
        self.assertEqual(outcome, "invalid_transition")
        self.assertIsNone(updated)

    def test_missing_order_returns_not_found(self):
        outcome, updated, message = self.order_service.update_order_status(9999, "preparing")
        self.assertEqual(outcome, "not_found")
        self.assertIsNone(updated)
        self.assertEqual(message, "Order not found")


if __name__ == "__main__":
    unittest.main()
