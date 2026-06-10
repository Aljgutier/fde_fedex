import unittest
from pathlib import Path


class FrontendOrderReviewContractTests(unittest.TestCase):
    def test_review_modal_and_receipt_contract_present(self):
        root = Path(__file__).resolve().parents[1]
        html = (root / "frontend" / "index.html").read_text(encoding="utf-8")
        script = (root / "frontend" / "script.js").read_text(encoding="utf-8")

        self.assertIn('id="review-modal"', html)
        self.assertIn('id="review-confirm-btn"', html)
        self.assertIn('id="review-back-btn"', html)

        self.assertIn("function startOrderReview", script)
        self.assertIn("function confirmReviewOrder", script)
        self.assertIn("function renderReceipt", script)
        self.assertIn("if (order.status !== \"completed\" || !order.receipt)", script)
        self.assertIn("Review Your Order", script)


if __name__ == "__main__":
    unittest.main()
