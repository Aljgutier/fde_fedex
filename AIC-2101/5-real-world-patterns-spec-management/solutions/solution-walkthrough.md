# Lab 5 Solution Walkthrough: Real-World Patterns & Spec Management

> Step-by-step journey from the Lab 5 checkpoint to the completed state.
> Use this alongside the solution `beanbotics/` directory for reference.

---

## Starting State

The checkpoint is the completed Lab 4 solution:
- BeanBotics app with size selection, order lifecycle, customizations, confirmation/receipts, ingredient cost model, and financial dashboard
- 11 spec files in `openspec/specs/` across 5 domain areas
- 5 archived changes in `openspec/changes/archive/`
- Expanded profile commands installed in your agent's command directory (propose, explore, apply, archive, new, continue, ff, verify)

---

## Exercise 1: Set Up Working Copy

Open the lab folder in VS Code, create a venv, install dependencies, and run the app.

```bash
code supporting/labs/real-world-patterns-spec-management/files/beanbotics
```

Then in the VS Code integrated terminal:

```bash
uv venv
uv pip install -r requirements.txt
uv run uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

Verify at http://localhost:8000 — full BeanBotics UI with menu, customizations, confirmation, status board, receipts, and financial dashboard.

Check starting state:
```bash
ls openspec/specs/
# cogs-calculation/  drink-customizations/  drink-customizations-ui/
# drink-recipe-mapping/  drink-size-selection/  financial-dashboard/
# ingredient-cost-model/  order-confirmation/  order-receipt/
# order-status-lifecycle/  order-status-ui/

ls openspec/changes/archive/
# 2026-04-08-add-drink-size-selection/
# 2026-04-09-add-order-status-lifecycle/
# 2026-04-13-add-drink-customizations/
# 2026-04-13-add-order-confirmation-receipt/
# 2026-04-14-add-ingredient-cost-model/

# List your agent's command directory (e.g., .claude/commands/opsx/,
# .cursor/commands/, .amazonq/prompts/, etc.)
# Expected files: apply  archive  continue  explore  ff  new  propose  verify
```

---

## Exercise 2: Fix Without SDD

Find a small cosmetic issue in the app and fix it conversationally — no spec workflow.

**Example issue:** Drink name titles on the menu cards are slightly small relative to the surrounding UI.

**Prompt to your agent:**

```
The drink name titles on the menu cards (like "Neural Network Latte") are a bit
small. Increase the font size from 1rem to 1.1rem.
```

The agent edits `frontend/style.css`, changing `.menu-card h3` font-size from `1rem` to `1.1rem`.

**Verify:** Hard refresh (Ctrl+Shift+R). Titles should appear slightly larger.

**Why no spec?** The intent is self-evident, no behavioral requirement changed, and no spec in `openspec/specs/` needs updating. This is a cosmetic-only change.

---

## Exercise 3: Identify Pricing Assumptions in the Spec Suite

Read the specs that touch pricing and note fixed-price assumptions:

```bash
cat openspec/specs/drink-size-selection/spec.md
cat openspec/specs/order-receipt/spec.md
cat openspec/specs/financial-dashboard/spec.md
```

**Key findings:**
- `drink-size-selection` — menu displays prices per size, assumed fixed from `menu.json`
- `order-receipt` — `items_detail.base_price` is the static size price
- `financial-dashboard` — revenue computed from order totals with no tier distinction

These are the specs that will need MODIFIED sections in the delta specs.

---

## Exercise 4: Write Specs by Hand

### Step 1: Scaffold the Change

Invoke the **new** command with `add-dynamic-pricing` as the argument.

Creates `openspec/changes/add-dynamic-pricing/` with empty structure.

### Step 2: Write the Proposal

Hand-write `openspec/changes/add-dynamic-pricing/proposal.md`:

**Key sections in the solution proposal:**
- **Why:** Fixed pricing regardless of time of day; coffee shops typically discount during slow periods
- **What changes:** Pricing tier definitions, time simulation, modified menu display, modified order pricing, modified receipts, modified financial dashboard
- **New capability:** `pricing-tiers` — peak/off-peak definitions, discount rules, time simulation toggle
- **Modified capabilities:** `menu-display` (strikethrough + discounted prices), `order-pricing` (tier-based calculation, customizations exempt), `order-confirmation` (tier-adjusted totals), `order-receipt` (discount line item), `financial-dashboard` (peak vs. off-peak breakdown)
- **Scope boundaries:** No per-drink discount overrides, no customer-facing tier schedule, no historical pricing data

### Step 3: Create Delta Spec Scaffolding

```bash
mkdir -p openspec/changes/add-dynamic-pricing/specs/pricing-tiers
mkdir -p openspec/changes/add-dynamic-pricing/specs/menu-display
mkdir -p openspec/changes/add-dynamic-pricing/specs/order-pricing
mkdir -p openspec/changes/add-dynamic-pricing/specs/order-receipt
mkdir -p openspec/changes/add-dynamic-pricing/specs/financial-dashboard

touch openspec/changes/add-dynamic-pricing/specs/pricing-tiers/spec.md
touch openspec/changes/add-dynamic-pricing/specs/menu-display/spec.md
touch openspec/changes/add-dynamic-pricing/specs/order-pricing/spec.md
touch openspec/changes/add-dynamic-pricing/specs/order-receipt/spec.md
touch openspec/changes/add-dynamic-pricing/specs/financial-dashboard/spec.md
```

### Step 4: Fill in the Specs

Three specs are provided in the lab instructions (menu-display, order-pricing, financial-dashboard). Students write two themselves (pricing-tiers, order-receipt).

**The lab also generated an `order-confirmation` delta spec** during the test run (the AI review identified that the confirmation overlay needed updating too). The lab instructions don't explicitly scaffold this, but the AI may suggest it during the review step.

#### `pricing-tiers/spec.md` (student writes)

All ADDED — entirely new requirements:
- Two pricing tiers: peak (7-9am, 11:30am-1:30pm) at full price, off-peak (all other hours) at 20% off
- Customization surcharges NOT discounted — only base drink price affected
- Discounted prices rounded to 2 decimal places (half-up)
- `GET /api/menu` returns both `price` (peak) and `off_peak_price` for each size
- Time simulation toggle: two states (Peak/Off-Peak), defaults to Peak, updates immediately

#### `order-receipt/spec.md` (student writes)

MODIFIED — changes existing receipt behavior:
- **Previous:** `items_detail` includes `base_price` as the static size price
- **Updated:** `items_detail` includes a `discount` field (object with `label` and `amount` for off-peak, `null` for peak); `base_price` always shows the full peak price; `subtotal` = `base_price + discount.amount + customizations`
- Off-peak receipts show "Off-Peak Discount (20%)" line item between base price and customizations
- Peak receipts display unchanged

#### `menu-display/spec.md` (provided)

MODIFIED — menu cards show strikethrough + discounted price during off-peak, pricing tier indicator.

#### `order-pricing/spec.md` (provided)

MODIFIED — backend calculates tier-based price, customization surcharges exempt. REMOVED — fixed-price assumption.

#### `financial-dashboard/spec.md` (provided)

MODIFIED — aggregate metrics include peak vs. off-peak revenue breakdown; per-order table gains pricing tier column.

### Step 5: AI Review

```
Read the proposal and delta specs I wrote in
openspec/changes/add-dynamic-pricing/. Compare them
against the existing specs in openspec/specs/.

Review for:
- Gaps: requirements I missed or scenarios I didn't cover
- Ambiguities: language that could be interpreted multiple ways
- Conflicts: new requirements that contradict existing ones
- Edge cases: boundary conditions I didn't address

Tell me what's missing or unclear.
```

**Typical AI review findings:**
- Order confirmation overlay needs to reflect tier-adjusted prices (may suggest adding an `order-confirmation` delta spec)
- Rounding strategy should be explicit (round the discounted price, not the discount amount)
- Default pricing tier on page load should be specified
- `pricing_tier` field should be stored on the Order model for historical tracking

Edit specs based on feedback.

---

## Exercise 5: Implement Dynamic Pricing

### Generate Design and Tasks

Invoke the **ff** command.

The agent reads the hand-written proposal and specs and generates `design.md` and `tasks.md`.

**Generated task structure (11 groups, ~25 tasks):**

1. Backend — Pricing tier foundation (discount constant, compute helper, pricing_tier on Order model)
2. Backend — Menu API (enrich sizes with off_peak_price)
3. Backend — Order placement (accept pricing_tier, apply discount, update items_detail with discount field)
4. Backend — Financials API (peak/off-peak revenue breakdown, pricing tier per order)
5. Frontend — Pricing toggle (peak/off-peak switch, shared state, tier indicator)
6. Frontend — Menu display (strikethrough + discounted prices, order button reflects tier)
7. Frontend — Order confirmation (tier-adjusted totals, reactive to toggle changes)
8. Frontend — Order submission (include pricing_tier in POST body)
9. Frontend — Receipt display (discount line item for off-peak)
10. Frontend — Financial dashboard (peak/off-peak breakdown, tier column in table)
11. End-to-end verification

### Clear Context and Apply

Clear your agent's context (use your agent's clear-context mechanism — for example, `/clear` in Claude Code, or start a fresh session).

Then invoke the **apply** command.

### What the Implementation Changed

**Modified files:**
- `backend/models.py` — Added `OFF_PEAK_DISCOUNT` constant (0.20), `compute_off_peak_price()` helper, `pricing_tier` field on Order
- `backend/app.py` — `OrderRequest` gains `pricing_tier` field (optional, default "peak"); `/api/menu` enriches sizes with `off_peak_price`; `/api/financials` includes peak/off-peak breakdown
- `backend/services/orders.py` — `place_order()` accepts `pricing_tier`, applies discount to base price when off-peak, adds `discount` field to `items_detail`
- `frontend/index.html` — Pricing toggle switch added to UI
- `frontend/script.js` — Toggle state management, menu/confirmation/receipt rendering updated for tier awareness, `pricing_tier` included in POST body
- `frontend/style.css` — Toggle styling, strikethrough price styling, tier indicator styling

### Verify in Browser

Hard refresh (Ctrl+Shift+R).

**Peak mode (toggle set to Peak):**
- Menu shows normal prices, no discount indicators
- "Peak Pricing" indicator visible
- Order a Large Neural Network Latte ($6.50) + extra shot ($0.75) = $7.25 subtotal

**Off-peak mode (toggle set to Off-Peak):**
- Menu shows original prices with strikethrough and discounted prices
- "Off-Peak Pricing — 20% Off" indicator visible
- Large Neural Network Latte shows ~~$6.50~~ $5.20
- Order with extra shot: $5.20 + $0.75 = $5.95 subtotal

**Expected receipt for off-peak order (Large Neural Network Latte + extra shot):**

```
Neural Network Latte (Large) .......... $6.50
  Off-Peak Discount (20%) ............. -$1.30
  Extra Espresso Shot ................. $0.75
                          Subtotal      $5.95
                        Tax (8.5%)      $0.51
                             Total      $6.46
```

### Run Verify

Invoke the **verify** command.

Checks implementation against the hand-written specs.

### Financial Dashboard Check

Place orders in both tiers and verify:
- Dashboard shows peak revenue and off-peak revenue separately
- Per-order table includes a "Pricing Tier" column (Peak/Off-Peak)
- Off-peak orders show lower revenue but identical COGS → lower margin
- Totals are correct across both tiers

---

## Exercise 6: Archive and Review

Invoke the **archive** command.

### Final Spec Suite

```bash
ls openspec/specs/
# cogs-calculation/           # Lab 4
# drink-customizations/       # Lab 3
# drink-customizations-ui/    # Lab 3
# drink-recipe-mapping/       # Lab 4
# drink-size-selection/       # Lab 1
# financial-dashboard/        # Lab 4 (MODIFIED in Lab 5)
# ingredient-cost-model/      # Lab 4
# menu-display/               # NEW — Lab 5
# order-confirmation/         # Lab 3 (MODIFIED in Lab 5)
# order-pricing/              # NEW — Lab 5
# order-receipt/              # Lab 3 (MODIFIED in Lab 5)
# order-status-lifecycle/     # Lab 2
# order-status-ui/            # Lab 2
# pricing-tiers/              # NEW — Lab 5
```

14 spec files covering 6 domain areas. Lab 5 added 3 new specs (pricing-tiers, menu-display, order-pricing) and modified 3 existing ones (financial-dashboard, order-confirmation, order-receipt).

### Final Archive

```bash
ls openspec/changes/archive/
# 2026-04-08-add-drink-size-selection/
# 2026-04-09-add-order-status-lifecycle/
# 2026-04-13-add-drink-customizations/
# 2026-04-13-add-order-confirmation-receipt/
# 2026-04-14-add-ingredient-cost-model/
# 2026-04-15-add-dynamic-pricing/              # NEW
```

6 archived changes documenting the complete evolution of BeanBotics across all 5 labs.

---

## Key Files Changed (Summary)

| File | Change |
|------|--------|
| `backend/models.py` | MODIFIED — `OFF_PEAK_DISCOUNT` constant, `compute_off_peak_price()` helper, `pricing_tier` field on Order |
| `backend/app.py` | MODIFIED — `pricing_tier` on OrderRequest, `/api/menu` returns `off_peak_price`, `/api/financials` includes tier breakdown |
| `backend/services/orders.py` | MODIFIED — tier-based pricing in `place_order()`, `discount` field in `items_detail` |
| `frontend/index.html` | MODIFIED — pricing toggle switch |
| `frontend/script.js` | MODIFIED — toggle state, tier-aware rendering for menu/confirmation/receipt, `pricing_tier` in POST |
| `frontend/style.css` | MODIFIED — toggle styling, strikethrough prices, tier indicator, menu card h3 font-size bump |
| `openspec/specs/` | 3 new specs (pricing-tiers, menu-display, order-pricing), 3 modified (financial-dashboard, order-confirmation, order-receipt) |
| `openspec/changes/archive/` | 1 new archived change (add-dynamic-pricing) |

---

> Your work in `supporting/labs/real-world-patterns-spec-management/files/beanbotics/` is preserved after the lab. If you want to restart from the clean starting state, re-extract the course materials ZIP (or copy the pristine folder from a fresh extract).

---

## Delta Spec Summary

This is the first lab where delta specs include all three section types:

| Spec File | Sections Used |
|-----------|---------------|
| `pricing-tiers` | ADDED (new domain) |
| `menu-display` | MODIFIED (price display behavior) |
| `order-pricing` | MODIFIED (price calculation), ADDED (pricing_tier field on Order), REMOVED (fixed-price assumption) |
| `order-receipt` | MODIFIED (discount line item in items_detail) |
| `order-confirmation` | MODIFIED (tier-adjusted overlay totals) |
| `financial-dashboard` | MODIFIED (peak/off-peak revenue breakdown) |
