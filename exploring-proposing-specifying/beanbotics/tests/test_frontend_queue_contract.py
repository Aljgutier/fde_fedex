import unittest
from pathlib import Path


class FrontendQueueContractTests(unittest.TestCase):
    def test_queue_groups_and_inline_actions_are_defined(self):
        script_path = Path("frontend/script.js")
        source = script_path.read_text(encoding="utf-8")

        self.assertIn('const ACTIVE_STATUSES = ["pending", "preparing", "ready"]', source)
        self.assertIn("const STATUS_ACTIONS = {", source)
        self.assertIn('pending: [', source)
        self.assertIn('preparing: [{ label: "Mark Ready"', source)
        self.assertIn('ready: [{ label: "Mark Completed"', source)
        self.assertIn("function renderOrderGroup(title, orders, emptyMessage)", source)
        self.assertIn('renderOrderGroup(\n                "Active"', source)
        self.assertIn('renderOrderGroup(\n                "Completed"', source)
        self.assertIn('method: "PATCH"', source)


if __name__ == "__main__":
    unittest.main()
