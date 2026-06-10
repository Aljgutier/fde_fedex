## Why

Customers can currently place customized drink orders immediately, which increases accidental submissions and does not provide a final pre-submit verification step. Completed orders also lack a standardized receipt breakdown, making it hard for customers to validate how base price, customizations, and tax contributed to the final amount.

## What Changes

- Add a pre-submit order confirmation step in the frontend flow: after selecting size and customizations, customers see a Review Your Order summary before final confirmation.
- Show line-item pricing in the confirmation view, including base drink/size price, each selected customization surcharge, and pre-tax order total.
- Make the confirmation step explicitly depend on current customization selection and pricing rules so reviewed line items always reflect selected extras and existing surcharge constants.
- Add receipt data and a receipt presentation for completed orders, including base price line, customization line items, subtotal, and tax-inclusive total.
- Keep confirmation and receipt as distinct features: confirmation is a pre-submit review/decision step, while receipt is a post-completion order record view.
- Extend backend order representation to include receipt-friendly pricing breakdown fields computed from authoritative backend pricing rules.
- Keep existing out-of-scope items unchanged: no print/email receipts, no receipt history page, and no tax configuration UI.

## Capabilities

### New Capabilities
- `order-confirmation-review`: Pre-submit review step that depends on selected customizations and current surcharge rules, and summarizes selected drink, customizations, and pre-tax total before order creation.
- `order-receipt-breakdown`: Post-completion receipt view for completed orders with line-item breakdown, subtotal, tax, and final total.

### Modified Capabilities
- `drink-customizations`: Clarify and enforce consistent customization line-item and surcharge values across confirmation and receipt displays.
- `order-status-ui`: Extend completed-order presentation to include receipt details when status is `completed`.

## Impact

- Frontend: [frontend/index.html](frontend/index.html), [frontend/script.js](frontend/script.js), and [frontend/style.css](frontend/style.css) will gain confirmation and receipt UI states/components.
- Backend: [backend/models.py](backend/models.py), [backend/services/orders.py](backend/services/orders.py), and [backend/app.py](backend/app.py) may require response-shape updates for receipt breakdown fields.
- Tests: Add and update backend and frontend behavior coverage for review-step flow and completed-order receipt rendering.
- APIs: Existing order creation/list endpoints remain in place; response payloads for orders may be extended with receipt breakdown fields.
