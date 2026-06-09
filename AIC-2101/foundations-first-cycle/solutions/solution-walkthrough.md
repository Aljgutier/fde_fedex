# Solution Walkthrough: Foundations & First Cycle Lab

This walkthrough describes the step-by-step journey from the starter state to the completed state for the Foundations & First Cycle lab.

## Starting State

The BeanBotics starter app with:
- 5 AI-themed coffee drinks displayed in a menu grid
- Order placement hardcoded to medium size only
- Order queue with place/cancel functionality
- Backend already supports all three sizes (small, medium, large)

## Exercise 1: Set Up the Starter App

**Steps:**
1. Open the lab folder in VS Code: `code supporting/labs/foundations-first-cycle/files/beanbotics`
2. Create a virtual environment: `uv venv`
3. Install dependencies: `uv pip install -r requirements.txt`
4. Run the app: `uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000`
5. Open `http://localhost:8000` — verify menu loads, orders work

**Expected result:** App runs, all 5 drinks visible, can place and cancel orders (medium only).

## Exercise 2: Initialize OpenSpec

**Steps:**
1. Verify OpenSpec is installed (pre-installed by lab VM setup): `openspec --version` should report `1.2.0`
2. Run `openspec init` — select your agent (core profile is the default)
   - After init: reload the VS Code window (Ctrl+Shift+P → *Developer: Reload Window*) so your agent picks up the newly generated commands
   - The reload stops the server (it runs in the integrated terminal); restart it with `uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000` in a new terminal
3. Examine generated structure:
   - `openspec/` directory with `specs/` and `changes/` subdirectories
   - Your agent's config directory (e.g., `.claude/`, `.cursor/`, `.amazonq/`) with skill and command definitions
4. Edit `openspec/config.yaml` (created by `openspec init`) with project context

**Expected config.yaml:**

```yaml
schema: spec-driven

context: |
  BeanBotics is an AI-themed coffee ordering web application.
  Tech stack: Python 3.10+, FastAPI, vanilla HTML/CSS/JavaScript frontend.
  Backend: FastAPI app in backend/ with service layer pattern.
  Frontend: Single-page app in frontend/ using fetch API for all server calls.
  Data: Menu items loaded from backend/data/menu.json. Orders stored in memory.
  No database, no authentication, no payment processing.
  API endpoints: GET /api/menu, POST /api/orders, GET /api/orders, DELETE /api/orders/{id}.
```

**Expected result:** OpenSpec initialized. `openspec/` and your agent's config directory exist. `config.yaml` in place.

## Exercise 3: Explore the Codebase

**Exploration prompts used:**

```
What does this project do? Walk me through the main files and architecture.
```

```
Look at the menu data in backend/data/menu.json. What drink sizes are available, and how does the frontend currently handle size selection?
```

```
What would need to change to let customers choose between small, medium, and large sizes when ordering?
```

**Key discoveries:**
- `backend/data/menu.json` — Each item has `sizes` with small, medium, large and respective prices
- `backend/app.py` — `OrderRequest` already accepts a `size` field
- `backend/services/orders.py` — `place_order()` already looks up the price by size and formats the display name as "Size DrinkName"
- `frontend/script.js` — Hardcodes `size: "medium"` in `placeOrder()` and only shows medium price
- **Conclusion:** This is primarily a frontend change. The backend is already ready.

**Context clearing:** Clear your agent's context (or start a new session) after exploration, before proposing.

## Exercise 4: First Propose-Apply-Archive Cycle

### Propose

Pass `add-drink-size-selection` to *propose*, with the following lead-in prompt:

```
Add a size selector (small, medium, large) to the order form so
customers can choose a size before placing an order. The selected
size should drive the displayed price and be sent with the order.

Out of scope: drink customizations (milk, flavor, extra shots),
menu changes, new backend endpoints, and any UI changes beyond
the size selector and its price display.
```

The scope block is essential here. Invoking *propose* with just `add-drink-size-selection` and no lead-in leaves the agent to infer intent from the codebase — and `menu.json` plus the existing model hint at more features than this change should deliver, so the agent often over-scopes into drink customizations. Feeding intent and out-of-scope boundaries up front keeps the generated proposal focused on what was actually asked for.

**Expected artifacts generated in `openspec/changes/add-drink-size-selection/`:**

- `proposal.md` — Describes adding size selection to the ordering UI. Scope: frontend changes to show all sizes and let users pick. Out of scope: backend changes (already supports sizes), drink customizations, menu changes.
- `specs/` — Delta specs with ADDED requirements for size selector UI, price display per size, and selected size sent to API.
- `design.md` — Technical approach: modify `script.js` to render size radio buttons, update `placeOrder()` to read selected size, add CSS for size selector.
- `tasks.md` — Checklist of implementation steps.

### Apply

Invoke the *apply* command.

**What changes in the code:**

The AI agent modifies the frontend files. The key changes are:

**`frontend/script.js`** — Three modifications:
1. `loadMenu()` now renders size radio buttons (small, medium, large) for each drink instead of a single "Order (Medium)" button. Medium is pre-selected.
2. The order button shows the currently selected price and updates dynamically when a different size is chosen.
3. `placeOrder()` reads the selected radio button value instead of hardcoding "medium".

**`frontend/style.css`** — New CSS rules:
1. `.size-selector` — Flex container for the three size options
2. `.size-option` — Individual size button styling with hover and selected states
3. `.size-label` and `.size-price` — Typography for size name and price
4. Updated `.order-btn` to be full-width

**`frontend/index.html`** — No structural changes required (the HTML is generated dynamically by JavaScript).

### Verify

After applying, refresh the browser at `http://localhost:8000`:
- Each menu card shows three size options (Small, Medium, Large) with prices
- Medium is pre-selected by default
- Clicking a different size updates the price on the order button
- Placing an order sends the selected size to the API
- The order queue shows the size in the order name (e.g., "Large Neural Network Latte")
- Price in the order matches the selected size's price

### Archive

Invoke the *archive* command.

**Expected result:**
- `openspec/specs/` now contains specification file(s) describing current system behavior including size selection
- `openspec/changes/archive/` contains a timestamped folder with the completed change artifacts
- `openspec/changes/` is clean (no active changes)

## Final State

The completed BeanBotics app with:
- Size selection UI on each menu card (small, medium, large radio buttons)
- Dynamic price display that updates when size changes
- Orders placed with the selected size
- Order queue showing size in order name and correct price
- OpenSpec initialized with config.yaml, one archived change, and specs describing current behavior
