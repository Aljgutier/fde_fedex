## 1. Backend pricing and receipt data model

- [x] 1.1 Add order model fields for receipt breakdown (base line item, customization line items, subtotal, tax amount, total including tax) while keeping existing fields backward compatible
- [x] 1.2 Implement a single backend pricing helper that builds receipt line items from selected size and customizations using existing surcharge constants
- [x] 1.3 Add fixed server-side tax constant of 8.25% and compute `subtotal`, rounded `tax_amount`, and rounded `total_with_tax` in the pricing helper
- [x] 1.4 Add unit tests that verify tax is applied to subtotal (pre-tax) and that `total_with_tax = subtotal + tax_amount` after rounding rules
- [x] 1.5 Update order creation/list service flow to persist and return receipt breakdown data for each order

## 2. API and lifecycle integration

- [x] 2.1 Ensure completed orders returned by `GET /api/orders` include receipt breakdown fields required by the receipt view
- [x] 2.2 Verify status transition flow to `completed` remains unchanged while exposing receipt data in completed-order payloads
- [x] 2.3 Add/adjust backend tests for receipt payload shape, line-item values, and tax-inclusive totals

## 3. Frontend order confirmation step

- [x] 3.1 Add Review Your Order UI state in menu card flow with drink name, selected size, base line item, selected customization line items, and pre-tax total
- [x] 3.2 Implement Confirm and Back actions so confirm submits `POST /api/orders` and back returns to editable selections without creating an order
- [x] 3.3 Reuse existing surcharge values in review rendering so card totals and review line-item pricing remain consistent
- [x] 3.4 Add frontend checks/tests to ensure confirmation line items only include selected customizations and match surcharge constants

## 4. Frontend completed-order receipt rendering

- [x] 4.1 Extend completed order card rendering to show receipt breakdown (base line item, customization line items, subtotal, tax, total including tax)
- [x] 4.2 Keep active/completed grouping behavior and action-button visibility unchanged while adding receipt details only for completed orders
- [x] 4.3 Ensure receipt omits customization lines when no extras are selected and preserves current customization summary text behavior
- [x] 4.4 Add frontend checks/tests to keep confirmation flow and receipt rendering distinct (pre-submit review vs completed-order display)

## 5. End-to-end validation and polish

- [x] 5.1 Add/update frontend tests (or deterministic UI checks) for review flow, confirm/back behavior, and completed receipt display
- [x] 5.2 Validate rounding consistency between backend response totals and rendered frontend receipt values
- [x] 5.3 Run full project tests and manual smoke checks for placing customized orders through completion and viewing receipt breakdown
