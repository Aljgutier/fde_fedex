## 1. Backend — Itemized Pricing

- [x] 1.1 Add `items_detail` dict to the Order dataclass (base_price, customizations list, subtotal, tax_rate, tax, total)
- [x] 1.2 Update `OrderService.place_order()` to compute and store `items_detail` when creating an order
- [x] 1.3 Update `POST /api/orders` and `GET /api/orders` responses to include `items_detail` in serialized output

## 2. Frontend — Confirmation Overlay

- [x] 2.1 Add confirmation modal HTML structure to `index.html` (overlay backdrop, content container, title, summary area, Confirm Order and Go Back buttons)
- [x] 2.2 Add CSS for the confirmation overlay (modal positioning, backdrop, content styling, button styles)
- [x] 2.3 Refactor `placeOrder()` in `script.js` to open the confirmation overlay instead of immediately submitting
- [x] 2.4 Build `showConfirmation()` function that populates the overlay with drink name, size, customization line items with prices, and total
- [x] 2.5 Wire Confirm Order button to submit the order via `POST /api/orders`, close overlay, reset card, and refresh orders
- [x] 2.6 Wire Go Back button and backdrop click to close overlay without submitting

## 3. Frontend — Receipt View

- [x] 3.1 Add CSS for the inline receipt panel (line-item layout, subtotal/tax/total styling, expand/collapse transition)
- [x] 3.2 Update `renderOrder()` to add a "View Receipt" button on completed orders
- [x] 3.3 Build `renderReceipt()` function that creates the receipt panel from `items_detail` (base item, customizations, subtotal, tax, total)
- [x] 3.4 Wire View Receipt / Hide Receipt toggle to expand and collapse the receipt panel

## 4. Integration Testing

- [x] 4.1 Manually test the full flow: select drink with customizations → confirmation overlay → confirm → order appears → advance to completed → view receipt → verify line items and math
- [x] 4.2 Test edge cases: order with no customizations, Go Back preserves selections, backdrop click dismisses, multiple receipts open simultaneously
