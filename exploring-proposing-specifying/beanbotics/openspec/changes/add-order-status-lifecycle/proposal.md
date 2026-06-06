## Why

The `Order` model documents a multi-step lifecycle, but the application currently only uses `pending` and `cancelled`. This mismatch limits operational visibility and prevents staff from tracking order progress from in-queue to fulfilled.

## What Changes

- Introduce a validated order status lifecycle with explicit transition rules.
- Add one status transition API endpoint that accepts a target status and rejects invalid state moves.
- Keep cancellation restricted to pending orders.
- Update the queue UI to show lifecycle progression with inline action buttons on each order.
- Keep fulfilled orders visible in a dedicated Completed group on the queue board.

## Capabilities

### New Capabilities
- `order-status-lifecycle`: Define lifecycle states, allowed transitions, validation behavior, and queue presentation for active and completed orders.

### Modified Capabilities
- (none)

## Impact

- Backend model/service changes in `backend/models.py` and `backend/services/orders.py`.
- New/updated API route behavior in `backend/app.py` for status transitions and validation errors.
- Frontend queue rendering and action controls in `frontend/script.js` and status styling in `frontend/style.css`.
- Additional tests for transition validity and API error handling.
