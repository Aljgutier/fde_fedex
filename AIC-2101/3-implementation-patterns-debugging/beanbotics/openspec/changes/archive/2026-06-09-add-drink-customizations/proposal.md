## Why

Customers currently can only choose drink size, which blocks common cafe personalization needs and makes order totals less transparent. Adding optional extras now improves ordering flexibility while preserving the app's existing in-memory and no-auth architecture.

## What Changes

- Add optional drink customizations to ordering: extra espresso shot (+$0.75), milk alternative selection (oat, almond, or soy; +$0.60), and whipped cream (+$0.50).
- Show customization controls directly on each menu card so customers can select options before placing an order.
- Update order total dynamically on each card as size and customizations change.
- Extend order creation payload and backend order model to persist selected customizations and computed total.
- Render selected customizations in both the order queue and status board views.
- Keep all customization options available for all drinks (no per-drink restrictions) and exclude inventory/preference features from this change.

## Capabilities

### New Capabilities
- `drink-customizations`: Optional add-ons can be selected per menu card and are included in order pricing and submission.

### Modified Capabilities
- `drink-size-selection`: The order button price behavior expands from size-only to size-plus-customizations dynamic totals.
- `order-status-ui`: Order displays are updated to include selected customizations in queue and status board cards.

## Impact

- Backend:
  - Update order request/response handling in `backend/app.py`.
  - Extend order data structures in `backend/models.py` and order logic in `backend/services/orders.py`.
- Frontend:
  - Update menu card rendering, interaction state, and total calculation in `frontend/script.js`.
  - Add customization control and display styling in `frontend/style.css`.
- API contract:
  - `POST /api/orders` request and order response schema gain customization fields.
- Data and dependencies:
  - No new external dependencies.
  - No changes to menu source data format required for this scope.
