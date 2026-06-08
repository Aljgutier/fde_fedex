# Solution Walkthrough: Implementation Patterns & Debugging Lab

This walkthrough describes the step-by-step journey from the starter state to the completed state for the Implementation Patterns & Debugging lab.

## Starting State

BeanBotics with the completed Lab 2 features:
- 5 AI-themed coffee drinks with size selection (small, medium, large)
- Order status lifecycle with forward-only transitions (pending → preparing → ready → completed)
- Status-grouped queue board with color-coded badges and advance buttons
- Cancel restricted to pending orders
- OpenSpec initialized with `config.yaml`, two archived changes, and three merged spec files (`drink-size-selection`, `order-status-lifecycle`, `order-status-ui`)

## Exercise 1: Set Up Your Working Copy

**Steps:**
1. Stop any running server from an earlier lab (`Ctrl+C` or `kill` the process on port 8000)
2. Open the lab folder in VS Code: `code supporting/labs/implementation-patterns-debugging/files/beanbotics`
3. Set up environment (open a terminal inside the VS Code window):
   ```bash
   uv venv
   uv pip install -r requirements.txt
   uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```
4. Verify at `http://localhost:8000` — menu with size selection, status-grouped order queue working
5. Review starting state:
   - `openspec/specs/` — three spec files: `drink-size-selection`, `order-status-lifecycle`, `order-status-ui`
   - `openspec/changes/archive/` — two archived changes

**Expected result:** App running. OpenSpec commands available in your agent (starter state already includes all seven supported agent config trees).

## Exercise 2: Drink Customizations — The Fast Cycle

### Step 1: Propose

Invoke the **propose** command with the change name `add-drink-customizations` and the following prompt body:

```
Customers should be able to add optional extras when ordering any drink:
- Extra espresso shot: +$0.75
- Milk alternative (oat, almond, or soy): +$0.60
- Whipped cream: +$0.50

Customization options should appear on each menu card. The order total
should update dynamically as customizations are selected. The order queue
and status board should display any customizations on each order.

Out of scope: per-drink customization restrictions (all options available
for all drinks), customization inventory tracking, recurring/saved
customization preferences.
```

**Expected artifacts in `openspec/changes/add-drink-customizations/`:**

- `proposal.md` — Problem: no customization options. Solution: optional extras with fixed prices. Clear scope boundaries.
- `specs/` — Spec files covering: customization options with prices, dynamic price updates in UI, customization details on order cards and status board.
- `design.md` — Technical approach: customizations defined as a constant in the backend, new `/api/customizations` endpoint, checkbox UI on menu cards, order model extended to carry customization data.
- `tasks.md` — Implementation checklist: backend model changes → API endpoint → frontend customization UI → dynamic pricing → order display updates.

### Step 2: Quick scan

Review artifacts with a light touch:
- Verify prices are correct ($0.75, $0.60, $0.50)
- Check scope matches intent — no feature creep
- Skim scenarios for obvious gaps

**Issue found during testing:** `design.md` contained implementation-level details (variable names, type signatures, file paths) that belong in specs or tasks. Example: "Define CUSTOMIZATIONS: dict[str, float] in models.py" — corrected to describe the decision and rationale without naming specific code constructs. See the extra material section in the lab for full details.

### Step 3: Apply

Invoke the **apply** command.

**Observation questions while watching the agent:**
- Does it follow task order from `tasks.md`? (Yes — backend before frontend)
- Does it check off tasks as it goes? (Yes)
- Does it reference specs/design? (Varies by run)

### What changed in the code

**`backend/models.py`** — Two additions:
1. `CUSTOMIZATIONS` dict mapping option IDs to names and prices (extra-shot, oat-milk, almond-milk, soy-milk, whipped-cream)
2. `Order` dataclass gains `customizations: List[str]` field (default empty list)

**`backend/app.py`** — Two additions:
1. `OrderRequest` gains `customizations: list[str] = []` field
2. `GET /api/customizations` endpoint returning available options with IDs, names, and prices

**`backend/services/orders.py`** — Updated `place_order()`:
1. Accepts optional `customizations` parameter
2. Validates each customization ID against `CUSTOMIZATIONS`
3. Calculates surcharge from customization prices
4. Includes customization names in the display string

**`frontend/script.js`** — Multiple additions:
1. `loadCustomizations()` fetches available options on page load
2. Checkbox UI rendered on each menu card
3. `updatePrice()` recalculates displayed price when size or customizations change
4. `placeOrder()` collects selected customization IDs and sends with order

**`frontend/style.css`** — New rules for customization checkboxes and labels.

### Step 4: Verify

After hard refresh (`Ctrl+Shift+R`):
- Customization checkboxes appear on each menu card (extra shot, oat/almond/soy milk, whipped cream)
- Selecting customizations updates the displayed price dynamically
- Placing an order with customizations shows them on the order card
- Customization details visible at all status stages

### Step 5: Archive

Invoke the **archive** command.

New spec files merged into `openspec/specs/`. Archive now contains three changes.

### Step 6: Clear context

Clear your agent's chat context (e.g., `/clear` in Claude Code, or your agent's equivalent reset/new-session command).

## Exercise 3: Order Confirmation & Receipt — Dependency Handling

### Step 1: Reference existing specs when proposing

Invoke the **propose** command with the change name `add-order-confirmation-receipt` and the following prompt body:

```
Read the specs in openspec/specs/ for context on the current system,
especially the customization pricing model.

This change adds two things:
1. An order confirmation step: after selecting a drink and customizations,
   the customer sees a "Review Your Order" summary before confirming.
   The summary shows the drink name and size, each selected customization
   with its price, and the order total. The customer can confirm or go back.
2. A receipt view for completed orders: when an order reaches "completed"
   status, it has a receipt showing a line-item breakdown:
   - Base price (drink name, size, price)
   - Each customization as a separate line item with its price
   - Subtotal
   - Total including tax

Out of scope: printing receipts, emailing receipts, receipt history page,
tax configuration UI.
```

Note: The proposal deliberately says "total including tax" without specifying the tax rate, application method, or rounding strategy. This sets up the debugging exercise in Exercise 4.

**Expected artifacts in `openspec/changes/add-order-confirmation-receipt/`:**

- `proposal.md` — Acknowledges dependency on customization pricing. Two features: confirmation step and receipt view.
- `specs/` — Spec files covering: confirmation summary with customization line items, receipt with line-item breakdown, tax calculation (may or may not specify rate/rounding — this is the intentional gap).
- `design.md` — Technical approach: confirmation overlay/modal in frontend, receipt panel on completed orders, `items_detail` data structure for line-item breakdown, tax calculation in the backend.
- `tasks.md` — Confirmation step tasks before receipt tasks.

### Step 2: Review artifacts — focus on the dependency

Review in order: proposal → specs → design → tasks.

Key checks:
- Does the proposal acknowledge the customization dependency?
- Do receipt scenarios reference customization line items?
- Is the tax rate specified in the specs? Note what is present and what is missing.
- Are confirmation tasks before receipt tasks?

### Step 3: Apply

Invoke the **apply** command.

### What changed in the code

**`backend/models.py`** — One addition:
1. `TAX_RATE = 0.085` constant
2. `Order` dataclass gains `items_detail: Optional[Dict[str, Any]]` field for line-item breakdown

**`backend/services/orders.py`** — Updated `place_order()`:
1. Calculates tax: `round(subtotal * TAX_RATE, 2)`
2. Builds `items_detail` dict with: item_name, size, base_price, customizations (list of name/price dicts), subtotal, tax_rate, tax, total

**`frontend/script.js`** — Multiple additions:
1. `pendingOrder` state variable for confirmation flow
2. `placeOrder()` now shows confirmation instead of submitting immediately
3. `showConfirmation()` renders overlay with drink name, size, customizations, and total
4. `submitPendingOrder()` sends order on confirm, `closeConfirmation()` on cancel/back
5. `renderReceipt()` builds line-item display: base price, each customization, subtotal, tax (8.5%), total
6. `toggleReceipt()` show/hide on completed orders
7. `renderOrder()` adds "View Receipt" button for completed orders

**`frontend/index.html`** — Confirmation overlay markup added.

**`frontend/style.css`** — New rules for confirmation overlay, receipt panel, and receipt line items.

### Step 4: Verify confirmation step

After hard refresh (`Ctrl+Shift+R`):
- Select a drink and customizations, click Order
- "Review Your Order" overlay appears with drink name, size, customizations with prices, and total
- Confirm places the order; Back dismisses without ordering

## Exercise 4: Debugging Spec Ambiguity

### Step 1: Create a test order

Place: Large Neural Network Latte ($6.50) with extra shot (+$0.75).

### Step 2: Hand calculation

```
Large Neural Network Latte .......... $6.50
  Extra espresso shot ............... $0.75
                          Subtotal    $7.25
                        Tax (8.5%)    $0.62
                             Total    $7.87
```

Tax: $7.25 × 0.085 = $0.61625, rounded to $0.62.

### Step 3: Advance and check receipt

Advance: pending → preparing → ready → completed. Click "View Receipt."

### Step 4: Diagnose

During testing, the AI chose 8.5% tax applied to the subtotal with standard rounding — matching the hand calculation. However, the spec did not explicitly specify the tax rate. The AI made a reasonable assumption that happened to match.

The teaching moment: even when the numbers match, check whether the spec actually specified the details. If not, a different AI session could produce a different rate. Add the explicit requirement:

```
### Requirement: Tax calculation
Tax MUST be calculated at a rate of 8.5%, applied to the order
subtotal (base price plus all customizations). The tax amount
MUST be rounded to the nearest cent using standard rounding
(half-up). Tax MUST appear as a separate line item on the receipt.
```

### Step 6: Archive

Invoke the **archive** command.

## Exercise 5: Review the Accumulated System

### Final OpenSpec state

- `openspec/specs/` — 7 spec files covering 4 feature areas:
  - `drink-size-selection` (Lab 1)
  - `order-status-lifecycle`, `order-status-ui` (Lab 2)
  - `drink-customizations`, `drink-customizations-ui` (Lab 3, Change 1)
  - `order-confirmation`, `order-receipt` (Lab 3, Change 2)
- `openspec/changes/archive/` — 4 archived changes:
  - `2026-04-08-add-drink-size-selection`
  - `2026-04-09-add-order-status-lifecycle`
  - `2026-04-13-add-drink-customizations`
  - `2026-04-13-add-order-confirmation-receipt`
- `openspec/changes/` — empty (no active changes)

## Final State

BeanBotics with:
- Size selection (from Lab 1)
- Order status lifecycle with forward-only transitions (from Lab 2)
- Drink customizations: extra shot ($0.75), oat/almond/soy milk ($0.60), whipped cream ($0.50)
- Dynamic price updates on menu cards when selecting size or customizations
- Order confirmation step ("Review Your Order") before placing
- Receipt view on completed orders with line-item breakdown: base price, customizations, subtotal, tax (8.5%), total
- Customization details visible on order cards at all status stages
- OpenSpec with 7 merged spec files and 4 archived changes
