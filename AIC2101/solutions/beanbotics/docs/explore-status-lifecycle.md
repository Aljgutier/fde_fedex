# Order Status Lifecycle — Draft Proposal Summary

## Problem

The Order model defines five statuses (`pending`, `preparing`, `ready`, `completed`, `cancelled`) but only two are implemented. Orders are created as `pending` and can only become `cancelled` — there is no way to advance an order through the preparation lifecycle. The status field is an unvalidated string with no enforcement of valid transitions.

## Proposed Solution

Activate the full order lifecycle with inline controls and a validated state machine.

### State machine

```
place order
    │
    ▼
┌─────────┐
│ pending  │──── cancel ────► cancelled
└────┬─────┘
     │ advance
     ▼
┌──────────┐
│preparing │
└────┬─────┘
     │ advance
     ▼
┌─────────┐
│  ready   │
└────┬─────┘
     │ advance
     ▼
┌──────────┐
│completed │
└──────────┘
```

### Valid transitions (enforced server-side)

| Current Status | Allowed Next Statuses       |
|----------------|-----------------------------|
| pending        | preparing, cancelled        |
| preparing      | ready                       |
| ready          | completed                   |
| completed      | *(terminal — no transitions)* |
| cancelled      | *(terminal — no transitions)* |

Cancellation is restricted to `pending` only. Once preparation starts, the order cannot be cancelled.

### Backend changes

1. **OrderStatus enum** — Replace the bare `status: str` on the Order model with a proper enum. Validates at creation time and prevents typos.

2. **Transition map** — A dictionary encoding the valid-transitions table above. Single source of truth for lifecycle rules.

3. **`PATCH /api/orders/{id}`** — New endpoint accepting `{ "status": "<next_status>" }`. Validates the requested transition against the map; returns 400 on invalid transitions, 404 on missing orders.

4. **`OrderService.update_order_status()`** — New service method that looks up the order, checks the transition map, updates the status, and returns the result. The existing `cancel_order()` method either delegates to this or is retired in favor of the PATCH endpoint.

### Frontend changes

5. **Status-colored badges** — CSS classes (`.status-pending`, `.status-preparing`, `.status-ready`, `.status-completed`) with distinct colors. Suggested palette within the existing dark theme:
   - `pending` — amber/yellow
   - `preparing` — cyan/blue
   - `ready` — green
   - `completed` — muted grey

6. **Advance button** — Each non-terminal order gets an inline button labeled with the next status (e.g., "Start Preparing", "Mark Ready", "Complete"). Calls `PATCH /api/orders/{id}` and refreshes the order list.

7. **Grouped order queue** — The orders section splits into two groups:
   - **Active Orders** — `pending`, `preparing`, `ready` (with advance/cancel controls)
   - **Completed** — `completed` orders displayed below, no action buttons

## Scope

- Backend: enum, transition map, PATCH endpoint, service method
- Frontend: status badges, advance buttons, grouped display
- Validation: invalid transitions return clear error responses

## Out of Scope

- Authentication or role-based access (no staff vs. customer distinction)
- Automatic timers or background status progression
- Order history persistence (orders remain in-memory)
- Cancellation from non-pending statuses
- WebSocket/SSE push updates (manual refresh after each action is sufficient)

## Risks

| Risk | Mitigation |
|------|------------|
| Advance buttons could confuse users expecting a customer-only UI | Label buttons clearly; consider a small "barista mode" toggle if feedback warrants it |
| No concurrency protection — two tabs could advance the same order simultaneously | Acceptable for a demo app with in-memory storage; note as a limitation |
| Adding an enum is a small breaking change if anything persists raw status strings | Not a concern today (in-memory only), but worth noting if persistence is added later |
