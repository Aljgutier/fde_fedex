# Lab 4 Solution Walkthrough: Expanded Workflow & Spec Lifecycle

> Step-by-step journey from the Lab 4 checkpoint to the completed state.
> Use this alongside the solution `beanbotics/` directory for reference.

---

## Starting State

The checkpoint is the completed Lab 3 solution:
- BeanBotics app with size selection, order lifecycle, customizations, confirmation/receipt
- 7 spec files in `openspec/specs/` across 4 domain areas
- 4 archived changes in `openspec/changes/archive/`
- Core profile commands in your agent's command directory (propose, explore, apply, archive)

---

## Exercise 1: Set Up Working Copy

Open the lab's folder in VS Code, create a venv, install dependencies, and run the app.

```bash
code supporting/labs/expanded-workflow-spec-lifecycle/files/beanbotics
```

Then in the VS Code terminal:

```bash
uv venv
uv pip install -r requirements.txt
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Verify at http://localhost:8000 — full BeanBotics UI with menu, customizations, confirmation step, status board, and receipts.

Check starting state:
```bash
ls openspec/specs/
# drink-customizations/  drink-customizations-ui/  drink-size-selection/
# order-confirmation/  order-receipt/  order-status-lifecycle/  order-status-ui/

ls openspec/changes/archive/
# 2026-04-08-add-drink-size-selection/
# 2026-04-09-add-order-status-lifecycle/
# 2026-04-13-add-drink-customizations/
# 2026-04-13-add-order-confirmation-receipt/

ls .claude/commands/opsx/      # Claude Code (other agents: see your agent's command directory)
# apply.md  archive.md  explore.md  propose.md
```

---

## Exercise 2: Switch to the Expanded Profile

### Profile Switch

```bash
openspec config profile
```

1. Select **Workflows only**
2. Toggle on: **New change**, **Continue change**, **Fast-forward**, **Verify change** (in addition to the 4 already enabled)
3. Press Enter to confirm
4. Select **Yes** when prompted "Apply changes to this project now?"

OpenSpec regenerates your agent's command files automatically (e.g., `.claude/commands/opsx/` for Claude Code, `.cursor/commands/` for Cursor, `.amazonq/prompts/` for Amazon Q — see the agent-config table in Lab 1).

### Verify New Commands

```bash
ls .claude/commands/opsx/      # Claude Code example — check your agent's command directory
# apply.md  archive.md  continue.md  explore.md  ff.md  new.md  propose.md  verify.md
```

The new commands (`new.md`, `continue.md`, `ff.md`, `verify.md`) appear alongside the core ones.

---

## Exercise 3: Scaffold and Build the Proposal

### Step 1: Scaffold the Change

In your agent's chat panel, invoke the **new** command with `add-ingredient-cost-model` as the argument.

This creates `openspec/changes/add-ingredient-cost-model/` with `.openspec.yaml` but no artifacts.

### Step 2: Generate the Proposal

Send your agent the following prompt:

```
Read the specs in openspec/specs/ for context on the current system.

This change adds an ingredient cost model and financial dashboard.

Ingredient cost model:
- Define base ingredients with unit costs (espresso per shot,
  milk per oz, chocolate per oz, whipped cream per serving,
  alternative milk per oz)
- Map each drink/size to ingredient quantities — e.g., a Large
  Neural Network Latte uses 2 espresso shots + 12oz milk. Small and
  medium drinks typically use 1 shot; large drinks use 2.
- Calculate COGS per order from the recipe ingredients
- Customization surcharges (like extra shot) must also add their
  ingredient cost to COGS, not just the customer price

Financial dashboard:
- Display alongside the order board showing total revenue,
  total COGS, and gross margin (revenue minus COGS)
- Per-order breakdown showing revenue, COGS, and margin per order
- Updates live as orders are placed and completed

Out of scope: supplier management, ingredient inventory tracking,
purchase ordering, historical reporting, multi-location support.
```

Then invoke **continue**. The agent generates `proposal.md` only.

### Step 3: Review Gate — The Proposal

**What the generated proposal covers:**
- Why: BeanBotics lacks visibility into production costs
- What changes: ingredient definitions, recipe mappings, COGS calculation, financial dashboard
- 4 capabilities: ingredient-cost-model, drink-recipe-mapping, cogs-calculation, financial-dashboard
- Impact: backend (new data/services), frontend (dashboard), data (new JSON file), API (extended responses + new endpoint)

**What to check:**
- Customization COGS is explicitly mentioned: "Ensure customization surcharges contribute both customer price markup and ingredient cost to COGS" ✓
- Scope is one change (not split into ingredients and dashboard separately) ✓
- No scope creep (no inventory tracking, supplier management, etc.) ✓

No edits needed — the proposal matched the intent.

---

## Exercise 4: Build Specs and Design with Review Gates

### Specs (second **continue**)

The agent generated 4 spec files:
- `ingredient-cost-model/spec.md` — Base ingredient definitions, customization mappings, data validation
- `drink-recipe-mapping/spec.md` — Size-specific recipes in menu.json, validation rules
- `cogs-calculation/spec.md` — COGS formula (recipe costs + customization costs), stored on Order model
- `financial-dashboard/spec.md` — Aggregate metrics (revenue, COGS, margin), per-order breakdown, live updates

**What to check:**
- COGS calculation explicitly includes customization ingredient costs ✓ ("COGS equals the sum of ingredient costs for all ingredients in the drink recipe, plus the sum of ingredient costs from any applied customizations")
- "Gross margin" is defined as revenue minus COGS ✓
- Revenue is pre-tax (order total before tax) — implied by "sum of all order totals" referring to the pre-tax price
- Recipe mappings specify concrete structure (recipe field nested per size in menu.json) ✓
- Validation rules for ingredients (no negative costs) and recipes (positive quantities, valid ingredient IDs) ✓

### Design (third **continue**)

**Key decisions in the generated design:**
- **Ingredient data**: New `ingredients.json` file with unit costs, separate from menu pricing
- **Recipe mapping**: Recipe field added to each size entry in `menu.json` (co-located with menu items)
- **COGS calculation**: Added to `OrderService.place_order()`, result stored on Order model
- **Customization cost mapping**: Defined in `ingredients.json` as `customization_mappings` section
- **Financial dashboard**: Frontend component alongside order board, fetches from new `/api/financials` endpoint
- **Order model extension**: New `cogs` field on Order dataclass

**What to check:**
- Size-dependent recipes handled (recipe per size in menu.json) ✓
- Recipe data lives alongside menu items (reasonable for this project) ✓
- Dashboard updates via re-fetching after order state changes ✓
- No implementation-level detail leaking into design (no variable names or type signatures) ✓

### Tasks (fourth **continue**)

**Generated task structure (6 groups, 18 tasks):**

1. **Ingredient Data** — Create ingredients.json, add customization mappings, create IngredientService
2. **Drink Recipes** — Add recipe field to menu.json, validate recipes in MenuService
3. **COGS Calculation** — Add cogs field to Order model, implement calculation in OrderService, wire services
4. **API Integration** — Verify cogs in API responses, add GET /api/financials endpoint
5. **Financial Dashboard Frontend** — HTML structure, CSS styling, loadFinancials() function, per-order table, live updates
6. **Validation and Testing** — Manual verification of COGS values, dashboard totals, live updates

**What to check:**
- Tasks ordered by dependency (ingredients → recipes → COGS → API → frontend → testing) ✓
- Dashboard tasks come after COGS calculation tasks ✓
- Each task is independently verifiable ✓

---

## Exercise 5: Implement and Verify

### Clear context and apply

Clear your agent's context (use your agent's clear/reset command — for example, `/clear` in Claude Code), then invoke the **apply** command.

The agent works through all 18 tasks, creating:

**New files:**
- `backend/data/ingredients.json` — 7 base ingredients with unit costs + 5 customization mappings
- `backend/services/ingredients.py` — IngredientService class (load, validate, calculate costs)

**Modified files:**
- `backend/data/menu.json` — Added `recipe` field to each size entry (ingredient quantities per drink/size)
- `backend/models.py` — Added `cogs` field to Order dataclass (float, default None)
- `backend/services/menu.py` — Added recipe validation (all items have recipes, all recipe IDs reference valid ingredients)
- `backend/services/orders.py` — COGS calculation in place_order() using IngredientService
- `backend/app.py` — New IngredientService initialization, new GET /api/financials endpoint, recipe validation at startup
- `frontend/index.html` — Financial dashboard section with metric cards and per-order table
- `frontend/script.js` — loadFinancials() function, called after order/status/cancel events
- `frontend/style.css` — Dashboard styling (metric cards, breakdown table)

### Verify in browser

After hard refresh (Ctrl+Shift+R):
- Financial dashboard visible alongside order board
- Three metric cards: Total Revenue, Total COGS, Gross Margin
- Per-order breakdown table below metrics

### Run verify

Invoke the **verify** command. Verify checks completeness, correctness, and coherence against the specs.

### The Customization COGS Test

Place a Large Neural Network Latte ($6.50) with extra shot (+$0.75).

**Hand calculation with actual ingredient values:**

```
Base recipe COGS (Large Neural Network Latte):
  2 espresso shots x $0.40/shot   = $0.80
  16oz milk x $0.08/oz            = $1.28
  Base COGS                       = $2.08

Customization COGS:
  1 extra espresso shot x $0.40   = $0.40

Total COGS:                       = $2.48

Revenue (pre-tax subtotal):
  Large Neural Network Latte        $6.50
  Extra shot surcharge            + $0.75
  Revenue                         = $7.25

Gross margin: $7.25 - $2.48 = $4.77
```

**Key verification:** The COGS on the dashboard should be $2.48 (includes the extra shot ingredient cost), not $2.08 (base recipe only). If the spec and implementation are correct, customization ingredients are included in COGS.

### Actual ingredient costs in this solution

| Ingredient | Unit | Cost |
|-----------|------|------|
| Espresso | shot | $0.40 |
| Whole Milk | oz | $0.08 |
| Chocolate Syrup | oz | $0.15 |
| Whipped Cream | serving | $0.30 |
| Oat Milk | oz | $0.15 |
| Almond Milk | oz | $0.12 |
| Soy Milk | oz | $0.10 |

### Customization ingredient mappings

| Customization | Ingredients Consumed |
|--------------|---------------------|
| Extra Shot | 1 espresso shot |
| Oat Milk | 8oz oat milk |
| Almond Milk | 8oz almond milk |
| Soy Milk | 8oz soy milk |
| Whipped Cream | 1 serving |

### Sample recipe: Neural Network Latte

| Size | Espresso | Milk |
|------|----------|------|
| Small | 1 shot | 8oz |
| Medium | 1 shot | 12oz |
| Large | 2 shots | 16oz |

---

## Exercise 6: Archive and Review

Invoke the **archive** command.

### Final spec suite

```bash
ls openspec/specs/
# cogs-calculation/           # NEW — Lab 4
# drink-customizations/       # Lab 3
# drink-customizations-ui/    # Lab 3
# drink-recipe-mapping/       # NEW — Lab 4
# drink-size-selection/       # Lab 1
# financial-dashboard/        # NEW — Lab 4
# ingredient-cost-model/      # NEW — Lab 4
# order-confirmation/         # Lab 3
# order-receipt/              # Lab 3
# order-status-lifecycle/     # Lab 2
# order-status-ui/            # Lab 2
```

11 spec files covering 5 domain areas. The ingredient cost model added 4 new specs.

### Final archive

```bash
ls openspec/changes/archive/
# 2026-04-08-add-drink-size-selection/
# 2026-04-09-add-order-status-lifecycle/
# 2026-04-13-add-drink-customizations/
# 2026-04-13-add-order-confirmation-receipt/
# 2026-04-14-add-ingredient-cost-model/     # NEW
```

5 archived changes documenting the full evolution of BeanBotics.

---

## Key Files Changed (Summary)

| File | Change |
|------|--------|
| `backend/data/ingredients.json` | NEW — ingredient definitions and customization mappings |
| `backend/data/menu.json` | MODIFIED — added recipe field per size entry |
| `backend/models.py` | MODIFIED — added cogs field to Order |
| `backend/services/ingredients.py` | NEW — IngredientService |
| `backend/services/menu.py` | MODIFIED — recipe validation |
| `backend/services/orders.py` | MODIFIED — COGS calculation in place_order() |
| `backend/app.py` | MODIFIED — IngredientService init, /api/financials endpoint, recipe validation |
| `frontend/index.html` | MODIFIED — financial dashboard section |
| `frontend/script.js` | MODIFIED — loadFinancials(), live update wiring |
| `frontend/style.css` | MODIFIED — dashboard styling |
| Your agent's command directory (e.g., `.claude/commands/opsx/`, `.cursor/commands/`, `.amazonq/prompts/`) | MODIFIED — expanded profile commands added |
| `openspec/specs/` | 4 new spec files (ingredient-cost-model, drink-recipe-mapping, cogs-calculation, financial-dashboard) |
| `openspec/changes/archive/` | 1 new archived change |
