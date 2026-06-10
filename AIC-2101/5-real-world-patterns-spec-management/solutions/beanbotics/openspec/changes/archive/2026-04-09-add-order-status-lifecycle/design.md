## Context

BeanBotics orders currently have a `status: str` field that is set to `"pending"` at creation and can only transition to `"cancelled"` via `DELETE /api/orders/{id}`. The three intermediate statuses (`preparing`, `ready`, `completed`) mentioned in the model comment are unreachable. The frontend only renders a cancel button for pending orders — there are no controls to advance an order.

## Goals / Non-Goals

**Goals:**
- Enforce valid status transitions server-side so invalid state changes are impossible
- Provide a single PATCH endpoint for all status transitions (including cancellation)
- Display order status visually with color-coded badges
- Give the operator inline buttons to advance orders through the lifecycle
- Group orders into active vs. completed sections in the UI

**Non-Goals:**
- Authentication, roles, or staff-vs-customer views
- Automatic timers or background progression
- Persistent storage or order history beyond the in-memory list
- WebSocket/SSE real-time updates
- Cancellation from any status other than `pending`

## Decisions

### 1. OrderStatus as a Python `str` enum

Use `class OrderStatus(str, Enum)` so enum values serialize directly to JSON strings without a custom encoder. This avoids changing FastAPI's default serialization and keeps `asdict()` output clean.

**Alternative considered:** Plain string constants or a separate validation function. Rejected because an enum gives type safety, IDE autocomplete, and prevents typos at the model level.

### 2. Transition map as a module-level dict

Define `VALID_TRANSITIONS: dict[OrderStatus, list[OrderStatus]]` in `models.py` alongside the enum. This keeps the lifecycle rules co-located with the data model and easily testable in isolation.

**Alternative considered:** Encoding transitions as methods on the Order class. Rejected because a declarative dict is simpler to read and extend.

### 3. Single PATCH endpoint for all transitions

`PATCH /api/orders/{id}` with body `{ "status": "<next>" }` handles both advancing and cancelling. The existing `DELETE /api/orders/{id}` route is kept for backward compatibility but delegates to the same service method internally.

**Alternative considered:** Separate endpoints per transition (e.g., `POST /api/orders/{id}/advance`). Rejected because a single PATCH with the target status is more RESTful and reduces route proliferation.

### 4. Keep `get_all_orders()` returning non-cancelled orders

The current filter (`status != "cancelled"`) remains unchanged. Completed orders appear in the response so the frontend can render the "Completed" group. Cancelled orders stay hidden.

### 5. Frontend grouping via JS filter, not separate API calls

The frontend fetches all orders from `GET /api/orders` and splits them client-side into active (`pending`, `preparing`, `ready`) and completed groups. No new API endpoint needed.

**Alternative considered:** Server-side filtering with query params. Rejected as unnecessary complexity for an in-memory store with a small order list.

## Risks / Trade-offs

- **No concurrency protection** — Two browser tabs could advance the same order simultaneously. Acceptable for a demo app with in-memory storage. → Document as a known limitation.
- **DELETE endpoint duplication** — Keeping DELETE alongside PATCH means two ways to cancel. → DELETE delegates to the same service logic, so behavior stays consistent.
- **Enum is a minor breaking change** — If anything serializes `status` expecting a raw string, the `str` base class on the enum ensures compatibility. → No impact for in-memory-only storage.
