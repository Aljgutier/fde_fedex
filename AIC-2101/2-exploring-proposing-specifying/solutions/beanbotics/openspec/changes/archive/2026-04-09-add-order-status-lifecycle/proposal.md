## Why

The Order model defines five statuses (`pending`, `preparing`, `ready`, `completed`, `cancelled`) but only two are reachable. Orders are created as `pending` and can only become `cancelled` via the DELETE endpoint. There is no way to advance an order through the preparation lifecycle, and the status field is an unvalidated string with no enforcement of valid transitions.

## What Changes

- Replace the bare `status: str` on the Order model with a proper `OrderStatus` enum
- Add a server-side transition map encoding which status changes are valid
- Add a `PATCH /api/orders/{id}` endpoint to advance order status through the lifecycle
- Add a service method `update_order_status()` to validate and apply transitions
- Display status-colored badges on the frontend (amber/cyan/green/grey)
- Add inline "advance" buttons on each non-terminal order (e.g., "Start Preparing", "Mark Ready", "Complete")
- Split the orders display into grouped sections: **Active Orders** and **Completed**

## Capabilities

### New Capabilities

- `order-status-lifecycle`: Server-side state machine with enum, transition map, PATCH endpoint, and service method for advancing orders through pending -> preparing -> ready -> completed (with cancellation from pending only)
- `order-status-ui`: Frontend status badges with color coding, inline advance buttons, and grouped order display (active vs. completed)

### Modified Capabilities

*(none — no existing specs are being changed)*

## Impact

- **Backend**: `models.py` (new enum), `services/orders.py` (new method, possible refactor of `cancel_order`), `app.py` (new PATCH route and request model)
- **Frontend**: `script.js` (advance button logic, grouped rendering), `style.css` (status badge classes)
- **API**: New `PATCH /api/orders/{id}` endpoint; existing endpoints unchanged
- **Dependencies**: None — uses only Python stdlib `enum` module
