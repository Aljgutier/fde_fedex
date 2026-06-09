## 1. Backend Model Layer

- [x] 1.1 Add `OrderStatus(str, Enum)` to `backend/models.py` with values: `pending`, `preparing`, `ready`, `completed`, `cancelled`
- [x] 1.2 Add `VALID_TRANSITIONS` dict to `backend/models.py` mapping each `OrderStatus` to its list of allowed next statuses
- [x] 1.3 Update the `Order` dataclass to use `OrderStatus` for the `status` field (default: `OrderStatus.PENDING`)

## 2. Backend Service Layer

- [x] 2.1 Add `update_order_status(order_id, new_status)` method to `OrderService` that validates the transition against `VALID_TRANSITIONS` and updates the order
- [x] 2.2 Refactor `cancel_order()` to delegate to `update_order_status()` with `OrderStatus.CANCELLED`

## 3. Backend API Layer

- [x] 3.1 Add `StatusUpdateRequest` Pydantic model to `backend/app.py` with a `status` field
- [x] 3.2 Add `PATCH /api/orders/{order_id}` route that calls `order_service.update_order_status()` — return 200 on success, 400 on invalid transition, 404 on missing order
- [x] 3.3 Verify existing `POST /api/orders` and `DELETE /api/orders/{id}` still work correctly with the enum-based status

## 4. Frontend Status Badges

- [x] 4.1 Add CSS classes `.status-pending` (amber), `.status-preparing` (cyan), `.status-ready` (green), `.status-completed` (grey), `.status-cancelled` (grey) to `frontend/style.css`
- [x] 4.2 Update `loadOrders()` in `frontend/script.js` to apply the appropriate status class to the order status span

## 5. Frontend Advance Controls

- [x] 5.1 Add `advanceOrder(orderId, nextStatus)` function to `frontend/script.js` that sends `PATCH /api/orders/{id}` with the target status and refreshes the order list
- [x] 5.2 Update order rendering to show the correct advance button per status: "Start Preparing" (pending), "Mark Ready" (preparing), "Complete" (ready)
- [x] 5.3 Restrict cancel button to `pending` orders only (already the case — verify after refactor)

## 6. Frontend Grouped Display

- [x] 6.1 Update `loadOrders()` to split orders into active (`pending`, `preparing`, `ready`) and completed groups
- [x] 6.2 Render "Active Orders" heading and items, then "Completed" heading and items — hide either section if its group is empty
- [x] 6.3 Show the empty-state message only when there are zero orders total
