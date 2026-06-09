# Explore Status Lifecycle

## Problem

The Order model documents a multi-step lifecycle (`pending`, `preparing`, `ready`, `completed`, `cancelled`), but the current implementation only uses `pending` and `cancelled`.

Current behavior:
- New orders are always created as `pending`.
- Orders can only be cancelled while `pending`.
- There is no way to move an order through `preparing`, `ready`, and `completed`.
- The queue UI cannot represent in-progress or fulfilled states beyond pending/cancelled.

This leaves a gap between the documented domain model and actual runtime behavior, and limits operational visibility for order progress.

## Proposed Solution

Implement a validated, manual order lifecycle across backend and frontend using a single transition endpoint and inline controls in the existing queue UI.

Decisions applied:
- Add inline advance buttons on each order in the existing UI (no separate staff view, no automatic timers).
- Keep cancellation restricted to pending only.
- Keep completed orders visible in a dedicated Completed group on the queue board.
- Use one endpoint for all status transitions, with a backend transition map that validates and rejects invalid moves.

Lifecycle rules (server-side source of truth):
- `pending -> preparing`
- `pending -> cancelled`
- `preparing -> ready`
- `ready -> completed`
- All other transitions rejected.

## Scope

### Backend

- Standardize lifecycle statuses and enforce them as valid values.
- Add transition-map validation in order service.
- Add a single status transition endpoint (for example `PATCH /api/orders/{id}/status`).
- Return clear errors for not found orders, invalid status values, and invalid transitions.
- Preserve cancel restriction by allowing cancel only from `pending`.
- Ensure list responses support queue grouping so completed orders remain visible in a Completed section.

### Frontend

- Update queue rendering to group orders by status, including a visible Completed group.
- Add inline status action buttons per order:
  - `pending`: advance to preparing, cancel
  - `preparing`: mark ready
  - `ready`: mark completed
  - `completed`: no advance actions
- Keep status badges/labels readable and distinct by state.
- Wire all status actions through the single transition endpoint.

### Validation and UX Behavior

- Backend remains the authoritative validator for lifecycle transitions.
- Frontend only presents valid next-step actions based on current status.
- UI refreshes order list after transitions and handles rejected transitions gracefully.

## Out of Scope

- Separate staff dashboard/view.
- Automatic status progression timers/background jobs.
- Role-based permissions for status changes.
- Real-time push updates (WebSocket/SSE).
- Broader persistence redesign or analytics/reporting expansions.

## Risks

- **Stale UI / concurrency conflicts:** Two operators may act on the same order simultaneously.
  - Mitigation: refresh queue after every mutation and surface transition errors clearly.

- **Rule drift between client and server:** UI assumptions can diverge from backend lifecycle logic.
  - Mitigation: keep transition map canonical on backend; frontend remains display/action guidance only.

- **Behavioral compatibility changes:** Existing consumers may depend on current order-list filtering.
  - Mitigation: preserve response shape and introduce additive filtering/grouping behavior where needed.

- **Testing gaps:** Lifecycle transitions can regress without dedicated tests.
  - Mitigation: add service/API tests for allowed transitions, blocked transitions, and terminal-state behavior.
