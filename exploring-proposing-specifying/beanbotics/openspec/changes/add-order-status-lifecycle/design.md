## Context

The current order flow supports creating pending orders and cancelling pending orders, but does not support progressing orders through preparation and completion. The `Order` model already documents lifecycle statuses, creating a mismatch between the documented domain and runtime behavior. The change must fit the existing FastAPI service-layer backend and vanilla JavaScript queue UI without introducing a separate staff interface or automated timers.

## Goals / Non-Goals

**Goals:**
- Implement a validated order lifecycle with explicit states and allowed transitions.
- Provide one backend endpoint for all manual status transitions.
- Preserve current cancellation policy: cancellation is allowed only while pending.
- Update the existing queue board to provide inline progression actions per order.
- Keep completed orders visible in a dedicated Completed group.

**Non-Goals:**
- Separate staff dashboard or role-based access model.
- Automatic progression via timers/background workers.
- Real-time push updates (WebSocket/SSE).
- Persistence redesign beyond current in-memory storage.

## Decisions

1. Canonical status lifecycle in backend
- Decision: Centralize lifecycle state and transition rules in backend service logic.
- Rationale: The backend is the source of truth and can enforce valid transitions consistently for all clients.
- Alternatives considered:
  - Frontend-driven transition rules: rejected because it allows divergence and invalid updates from non-UI clients.
  - Multiple endpoint-per-transition API: rejected to avoid route sprawl and duplicated validation.

2. Single transition endpoint
- Decision: Add one endpoint (for example `PATCH /api/orders/{order_id}/status`) accepting target status.
- Rationale: Simplifies API surface and supports future lifecycle adjustments without adding new routes.
- Alternatives considered:
  - Keep DELETE for cancel and add multiple action endpoints: rejected because behavior becomes fragmented.

3. Explicit transition map
- Decision: Validate moves using a strict transition map:
  - `pending -> preparing`
  - `pending -> cancelled`
  - `preparing -> ready`
  - `ready -> completed`
- Rationale: Encodes workflow rules clearly and makes invalid moves deterministic.
- Alternatives considered:
  - Allow arbitrary forward movement (e.g., pending to ready): rejected because it weakens workflow integrity.

4. Inline queue controls in existing UI
- Decision: Add per-order inline action buttons based on current status.
- Rationale: Matches operator workflow with minimal UI disruption and no new surface area.
- Alternatives considered:
  - New staff-only page: rejected as out of scope.
  - Automatic timers: rejected per product decision.

5. Completed group visibility
- Decision: Keep completed orders visible in a dedicated Completed group on the queue board.
- Rationale: Preserves short-term fulfillment visibility without mixing completed orders into active workflow.
- Alternatives considered:
  - Hide completed orders from queue entirely: rejected because it reduces operational traceability.

## Risks / Trade-offs

- [Concurrent updates may fail] -> Mitigation: backend rejects stale/invalid transitions; frontend reloads queue after each action and shows server error feedback.
- [Client/server lifecycle drift] -> Mitigation: backend transition map remains canonical; frontend only renders allowed next actions from current status.
- [Queue clutter from completed orders] -> Mitigation: show completed in a separate group and keep active statuses visually distinct.
- [Regression risk in existing cancel flow] -> Mitigation: preserve pending-only cancel as an explicit transition and add tests for legacy behavior.

## Migration Plan

1. Introduce status value validation and transition-map logic in `OrderService`.
2. Add single status transition API route and response/error contract.
3. Update frontend queue rendering to grouped sections and inline action controls.
4. Keep existing cancel affordance behavior aligned with pending-only rule.
5. Add/adjust tests for allowed transitions, rejected transitions, and queue grouping behavior.
6. Rollback strategy: remove new transition route and restore previous pending/cancelled-only rendering if deployment issues occur.

## Open Questions

- Should cancelled orders remain hidden (current behavior) or appear in a separate Cancelled group?
- Should status values be implemented as a strict enum in the model layer now, or validated only in service for the first iteration?
