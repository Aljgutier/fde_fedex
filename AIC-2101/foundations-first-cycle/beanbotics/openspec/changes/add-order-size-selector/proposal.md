## Why

Customers can currently place an order without explicitly selecting a size, which makes price expectations unclear at the point of purchase. Adding an explicit size selector now improves ordering clarity and prevents mismatch between displayed pricing and submitted order data.

## What Changes

- Add a size selector to the frontend order form with `small`, `medium`, and `large` options for each menu item.
- Update the order UI so the displayed price reflects the currently selected size before submission.
- Include the selected size in the order payload sent to the existing `POST /api/orders` endpoint.
- Keep scope limited to the size selector and size-based price display; no drink customization, menu structure changes, endpoint additions, or unrelated UI redesign.

## Capabilities

### New Capabilities
- `order-size-selection`: Allow customers to choose drink size in the order form, see size-based pricing, and submit orders with the selected size.

### Modified Capabilities
- None.

## Impact

- Affected frontend files: `frontend/index.html`, `frontend/script.js`, `frontend/style.css`.
- Existing backend API usage remains the same (`POST /api/orders` already accepts `size`); no new endpoints required.
- No new third-party dependencies.
