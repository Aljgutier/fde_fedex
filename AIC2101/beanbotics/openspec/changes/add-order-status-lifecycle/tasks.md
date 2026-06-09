## 1. Backend lifecycle model and transition API

- [x] 1.1 Add explicit lifecycle status validation for orders (`pending`, `preparing`, `ready`, `completed`, `cancelled`).
- [x] 1.2 Implement a canonical transition map in `OrderService` and enforce allowed transitions only.
- [x] 1.3 Add a single status transition service method that returns clear outcomes for success, invalid transition, invalid status, and missing order.
- [x] 1.4 Add `PATCH /api/orders/{order_id}/status` request/response handling and map service outcomes to stable HTTP errors.
- [x] 1.5 Keep pending-only cancellation behavior aligned with transition rules (including existing cancel route behavior).

## 2. Frontend queue lifecycle UX

- [x] 2.1 Update queue rendering to group orders into Active (`pending`, `preparing`, `ready`) and Completed (`completed`).
- [x] 2.2 Add inline action controls per status (pending: prepare/cancel, preparing: ready, ready: complete, completed: no advance).
- [x] 2.3 Route all status actions through the single status transition endpoint and reload queue state after mutations.
- [x] 2.4 Add or update status badge styling for each lifecycle state and preserve clear visual distinction between groups.
- [x] 2.5 Handle transition failures gracefully in UI (invalid move/not found) with operator-visible feedback.

## 3. Verification and regression coverage

- [x] 3.1 Add backend tests for allowed transitions and blocked transitions.
- [x] 3.2 Add backend tests for pending-only cancellation and not-found order transition behavior.
- [x] 3.3 Add API tests for invalid status value rejection and error-code consistency.
- [x] 3.4 Validate frontend queue behavior for grouped rendering and status-specific inline actions.
- [x] 3.5 Run project checks/tests and confirm lifecycle behavior matches spec scenarios.
