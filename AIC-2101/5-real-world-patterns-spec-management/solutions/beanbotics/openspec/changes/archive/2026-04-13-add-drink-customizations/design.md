## Context

BeanBotics orders currently track a drink name, size, and price. There is no concept of add-ons or modifiers — every order is the base drink at the selected size.

Customization options are universal — they apply to every drink identically with fixed prices:
- Extra espresso shot: +$0.75
- Milk alternative (oat, almond, soy): +$0.60
- Whipped cream: +$0.50

## Goals / Non-Goals

**Goals:**
- Allow customers to select optional extras when ordering any drink
- Calculate the correct total including base price + all selected customization surcharges
- Show customizations in the order queue so the barista knows what was ordered
- Update the displayed price on the menu card dynamically as checkboxes are toggled

**Non-Goals:**
- Per-drink customization restrictions (all options available for all drinks)
- Customization inventory tracking
- Recurring or saved customization preferences
- Customization options served from `menu.json` or a separate data file
- Mutually exclusive option groups (e.g., "pick one milk" — multiple selections are fine)

## Decisions

### 1. Customization options as a backend constant, not a data file

The set of options is small (five items), universal across all drinks, and unlikely to change frequently. Defining them as a constant in the backend keeps them co-located with the data model and avoids a separate data file.

**Alternative considered:** Adding customizations to `menu.json`. Rejected because the menu file describes drinks, not universal modifiers.

### 2. Client sends option IDs, server resolves prices

The frontend sends only customization IDs in the order request. The backend validates each ID and calculates surcharges from its own constant — the server is the sole source of truth for pricing.

**Alternative considered:** Sending full objects with name/price from the frontend. Rejected because it would let the client dictate prices.

### 3. Customizations stored as raw IDs on the order

Orders store the selected customization IDs as a simple list. Display names are derived from the options constant at render time rather than duplicated in each order.

**Alternative considered:** Storing structured objects with name and price per order. Rejected as unnecessary for in-memory storage — the constant provides lookups when needed.

### 4. Dedicated API endpoint for available options

A dedicated endpoint serves the customization catalog to the frontend, keeping the JS decoupled from option definitions. Changes to available options or prices only require a backend update.

**Alternative considered:** Hardcoding options in the frontend JS. Rejected because it duplicates pricing logic and could drift from the backend.

### 5. Shared price recalculation on any input change

A single recalculation function fires whenever a size radio or customization checkbox changes. It reads the current size price plus all checked surcharges and updates the order button display.

## Risks / Trade-offs

- **Milk alternatives are not mutually exclusive** — A customer could select both oat and almond milk. This is intentional per the out-of-scope statement (no per-drink restrictions). If confusing, a future change could add option groups.
- **Single extra shot only** — The checkbox model allows one extra shot, not multiples. Acceptable for the current scope; a quantity selector would be a separate enhancement.
- **Breaking API change** — The order API contract changes, but the new field is optional so existing callers are unaffected.
