import unittest

from backend.models import OrderCustomizations, OrderStatus
from backend.services.menu import MenuService
from backend.services.orders import OrderService, TAX_RATE


class OrderCustomizationTests(unittest.TestCase):
    def setUp(self):
        self.service = OrderService(MenuService())

    def test_place_order_defaults_customizations_when_omitted(self):
        order = self.service.place_order("neural-latte", "medium")

        self.assertIsNotNone(order)
        self.assertFalse(order.customizations.extra_shot)
        self.assertEqual(order.customizations.milk_alternative, "none")
        self.assertFalse(order.customizations.whipped_cream)
        self.assertEqual(order.total_price, 5.50)
        self.assertIsNotNone(order.receipt)
        self.assertEqual(order.receipt.subtotal, 5.50)

    def test_place_order_computes_total_with_multiple_customizations(self):
        order = self.service.place_order(
            "transformer-white",
            "large",
            OrderCustomizations(
                extra_shot=True,
                milk_alternative="oat",
                whipped_cream=False,
            ),
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 8.10)
        self.assertIsNotNone(order.receipt)
        self.assertEqual(order.receipt.base_item.label, "Large Transformer Flat White")
        self.assertEqual(order.receipt.subtotal, 8.10)
        self.assertEqual(order.receipt.tax_amount, round(8.10 * TAX_RATE, 2))
        self.assertEqual(order.receipt.total_with_tax, round(8.10 + round(8.10 * TAX_RATE, 2), 2))
        self.assertEqual(len(order.receipt.customization_items), 2)

    def test_place_order_computes_total_with_single_customization(self):
        order = self.service.place_order(
            "machine-mocha",
            "medium",
            OrderCustomizations(
                extra_shot=False,
                milk_alternative="none",
                whipped_cream=True,
            ),
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 6.50)
        self.assertEqual(order.receipt.subtotal, 6.50)
        self.assertEqual(len(order.receipt.customization_items), 1)

    def test_invalid_milk_alternative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.service.place_order(
                "neural-latte",
                "small",
                OrderCustomizations(milk_alternative="coconut"),
            )

    def test_completed_order_retains_receipt_data(self):
        order = self.service.place_order(
            "neural-latte",
            "small",
            OrderCustomizations(extra_shot=True, milk_alternative="none", whipped_cream=False),
        )

        self.service.update_order_status(order.order_id, OrderStatus.PREPARING)
        self.service.update_order_status(order.order_id, OrderStatus.READY)
        updated = self.service.update_order_status(order.order_id, OrderStatus.COMPLETED)

        self.assertEqual(updated.status, OrderStatus.COMPLETED)
        self.assertIsNotNone(updated.receipt)
        self.assertEqual(updated.receipt.subtotal, updated.total_price)
        self.assertEqual(updated.receipt.total_with_tax, round(updated.receipt.subtotal + updated.receipt.tax_amount, 2))


if __name__ == "__main__":
    unittest.main()
