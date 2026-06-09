# Solution Walkthrough: Exploring, Proposing & Specifying Lab

This walkthrough describes the step-by-step journey from the starter state to the completed state for the Exploring, Proposing & Specifying lab.

## Starting State

BeanBotics with the completed Lab 1 features:
- 5 AI-themed coffee drinks with size selection (small, medium, large)
- Order placement with selected size, order queue with cancel
- OpenSpec initialized with `config.yaml`, one archived change (drink-size-selection), and merged specs

## Exercise 1: Open This Lab's BeanBotics Folder

**Steps:**
1. Open the lab folder in VS Code: `code supporting/labs/exploring-proposing-specifying/files/beanbotics`
2. Create a virtual environment: `uv venv`
3. Install dependencies: `uv pip install -r requirements.txt`
4. Stop any server using port 8000 from a prior session if needed (Ctrl+C in its terminal, or restart your terminal session)
5. Run the app: `uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000`
6. Verify at `http://localhost:8000` — menu with size selection, order queue working

**Expected result:** App running. OpenSpec commands available (this lab's folder already includes the agent config directories with commands pre-installed for all supported agents).

## Exercise 2: Explore the Order System

### Step 1: Start exploration

Invoke the **explore** command, then ask:

```
Look at the Order model in the backend. What status values does it define?
How are those statuses actually used in the codebase? Is anything defined
but not implemented?
```

### Step 2: Key discovery

The agent discovers:
- `backend/models.py` — `Order` has `status: str` with a comment listing 5 values: pending, preparing, ready, completed, cancelled
- `backend/services/orders.py` — `place_order()` sets status to `"pending"`, `cancel_order()` sets to `"cancelled"`
- **No code path** reaches preparing, ready, or completed — 3 of 5 statuses are unreachable

### Step 3: Think through the solution

```
If we wanted to activate the full order lifecycle. Pending through
preparing, ready, and completed. What would need to change? Think
about both the backend (API, validation) and the frontend (how would
the order queue display different statuses?).
```

The agent presents design options. Key decision points surfaced (may be organized differently each run):
- **Who triggers transitions?** Options: separate staff view, automatic timers, or inline advance buttons
- **When can orders be cancelled?** Only from pending, or from any non-terminal state?
- **What happens to completed orders?** Disappear, separate group, or accumulate?
- **API design:** Single endpoint for all transitions, or separate endpoints per action?

### Step 4: Draft a proposal summary

```
Good analysis. Let's capture this as a draft proposal summary.
Here are my decisions on the open questions:

- Advance buttons inline on each order in the existing UI (no separate
  staff view, no automatic timers)
- Cancel from pending only (keep the current restriction)
- Completed orders stay visible in a "Completed" group on the queue board
- Single endpoint for all status transitions with a transition map
  that validates and rejects invalid moves

Write a draft proposal summary with these decisions baked in.
Include: the problem, proposed solution, scope, out of scope, and risks.
Save it to docs/explore-status-lifecycle.md.
```

**Expected result:** `docs/explore-status-lifecycle.md` created with problem statement, proposed solution (state machine, transition map, advance buttons, grouped display), scope boundaries, and risks.

### Step 5: Clear context

Reset your agent's context so the next exercise starts clean. In Claude Code, type `/clear`; in other agents, open a new chat (or use the equivalent context-reset action).

## Exercise 3: Propose the Order Status Lifecycle

### Step 1: Run the proposal

Pass `add-order-status-lifecycle` to the **propose** command, with the following lead-in prompt:

```
Read docs/explore-status-lifecycle.md for context on what we want to build,
then propose the change add-order-status-lifecycle.
```

**Expected artifacts in `openspec/changes/add-order-status-lifecycle/`:**

- `proposal.md` — Problem: 3 of 5 statuses unreachable. Solution: enum, transition map, PATCH endpoint, status-grouped UI with advance buttons. Out of scope: auth/roles, timers, persistence.
- `specs/` — Two spec files generated:
  - `order-status-lifecycle/spec.md` — Backend requirements: forward-only transitions, cancellation restricted to pending, invalid transitions rejected
  - `order-status-ui/spec.md` — Frontend requirements: status badges, advance buttons per status, cancel restricted to pending, grouped display (active vs completed)
- `design.md` — Technical approach: `OrderStatus(str, Enum)`, `VALID_TRANSITIONS` dict, `PATCH /api/orders/{id}` endpoint, `update_order_status()` service method, frontend grouping via JS filter
- `tasks.md` — Implementation checklist ordered by dependency: model layer → service layer → API layer → frontend badges → frontend controls → frontend grouping

## Exercise 4: Review and Refine the Artifacts

### Spec review findings (representative)

The AI-generated specs were mostly solid but contained implementation details that should be behavioral. Example found during testing:

**Original (implementation detail):**
```
Badge styles SHALL be implemented as CSS classes:
`.status-pending`, `.status-preparing`, `.status-ready`,
`.status-completed`, `.status-cancelled`.
```

**Corrected (behavioral requirement):**
```
Each status MUST be visually distinct. The badge color
MUST clearly differentiate pending, preparing, ready,
completed, and cancelled orders.
```

Other review actions:
- Verified RFC 2119 keywords used consistently (MUST, SHALL)
- Confirmed edge case scenarios present: cannot advance cancelled/completed orders, cannot cancel non-pending orders
- Confirmed design.md follows existing service layer pattern
- Verified tasks ordered correctly (backend before frontend)

## Exercise 5: Apply, Verify, and Archive

### Apply

Invoke the **apply** command to drive implementation from the specs.

### What changed in the code

**`backend/models.py`** — Two additions:
1. `OrderStatus(str, Enum)` with 5 values: PENDING, PREPARING, READY, COMPLETED, CANCELLED
2. `VALID_TRANSITIONS` dict mapping each status to its allowed next statuses
3. `Order.status` field changed from `str` to `OrderStatus` with default `OrderStatus.PENDING`

**`backend/services/orders.py`** — Two changes:
1. New `update_order_status(order_id, new_status)` method that validates transitions against the map and raises `ValueError` on invalid moves
2. `cancel_order()` refactored to delegate to `update_order_status(OrderStatus.CANCELLED)`

**`backend/app.py`** — Two additions:
1. `StatusUpdateRequest` Pydantic model with `status: OrderStatus` field
2. `PATCH /api/orders/{order_id}` route calling `update_order_status()`, returning 400 for invalid transitions and 404 for missing orders

**`frontend/script.js`** — Three additions:
1. `advanceOrder(orderId, nextStatus)` — sends PATCH request and refreshes order list
2. `getAdvanceButton(order)` — returns the correct button per status ("Start Preparing", "Mark Ready", "Complete") or empty string for terminal states
3. `loadOrders()` rewritten to split orders into active (pending/preparing/ready) and completed groups with headings; empty state shows only when zero orders total

**`frontend/style.css`** — New rules:
1. `.status-pending` (amber), `.status-preparing` (cyan), `.status-ready` (green), `.status-completed` (grey), `.status-cancelled` (grey)
2. `.advance-btn` styled to match theme (cyan outline, hover fills)
3. `.order-group-heading` for Active Orders / Completed section headers

### Verify

After hard refresh (`Ctrl+Shift+R`):
- Menu unchanged — size selection still works
- Order queue now shows "Active Orders" and "Completed" groups
- Each pending order has "Start Preparing" and "Cancel" buttons
- Each preparing order has "Mark Ready" button (no cancel)
- Each ready order has "Complete" button
- Completed orders show in their own section with no action buttons
- Color-coded badges: amber (pending), cyan (preparing), green (ready), grey (completed)
- Invalid transitions are rejected (tested by inspecting that completed/cancelled orders have no advance buttons)

### Archive

Invoke the **archive** command to move the completed change into the archive.

### Final OpenSpec state

- `openspec/specs/` — 3 domain areas: `drink-size-selection/`, `order-status-lifecycle/`, `order-status-ui/`
- `openspec/changes/archive/` — 2 archived changes: `2026-04-08-add-drink-size-selection/`, `2026-04-09-add-order-status-lifecycle/`
- `openspec/changes/` — empty (no active changes)
- `docs/explore-status-lifecycle.md` — draft proposal summary from exploration (kept as a project artifact)

## Final State

BeanBotics with:
- Size selection (from Lab 1)
- Order status lifecycle with forward-only transitions (pending → preparing → ready → completed)
- Cancel restricted to pending orders only
- Status-grouped queue board with color-coded badges
- Inline advance buttons per status (Start Preparing, Mark Ready, Complete)
- Active Orders / Completed visual grouping
- OpenSpec with 3 merged spec domains and 2 archived changes
