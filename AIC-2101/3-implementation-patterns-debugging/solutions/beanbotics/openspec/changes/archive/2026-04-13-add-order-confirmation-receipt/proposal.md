## Why

Customers currently place orders with a single click and have no way to review what they selected before it's submitted. There's also no receipt or price breakdown once an order completes. Adding a confirmation step reduces ordering mistakes, and a receipt view gives customers a clear record of what they paid and why.

## What Changes

- After clicking the order button, a confirmation overlay appears showing the drink name, selected size, each customization with its price, and the order total. The customer can confirm or go back to make changes.
- Completed orders display a receipt with a line-item breakdown: base drink price, each customization as a separate line, subtotal, tax at 8.5%, and final total.
- The backend order response includes itemized pricing data (base price, customization line items, subtotal, tax, total) so the frontend can render breakdowns without recalculating.

## Capabilities

### New Capabilities
- `order-confirmation`: Pre-submission review step that shows a summary of the order (drink, size, customizations, total) and lets the customer confirm or go back.
- `order-receipt`: Line-item receipt view for completed orders showing base price, customization surcharges, subtotal, tax, and total.

### Modified Capabilities
- `order-status-ui`: Completed orders gain a "View Receipt" action that opens the receipt view.

## Impact

- **Backend**: `POST /api/orders` response adds itemized pricing fields (base price, customization details, tax, total). New `GET /api/orders/{id}` endpoint or enriched order data to support receipt retrieval.
- **Frontend**: New confirmation overlay component in the ordering flow. New receipt view component for completed orders. Updates to order rendering for the "View Receipt" button.
- **No new dependencies**: Uses existing tech stack. No database changes (order data already in memory).
