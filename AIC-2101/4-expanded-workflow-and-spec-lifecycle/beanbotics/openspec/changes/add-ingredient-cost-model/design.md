## Context

BeanBotics is a vanilla FastAPI + JavaScript coffee ordering app with menu browsing, order placement, and an order queue. The existing system stores menu items in JSON, keeps orders in memory, and calculates order totals from drink sizes and customization surcharges.

This change introduces a financial layer that tracks ingredient COGS alongside customer revenue so the product can display gross margin for each order and across the current order queue.

## Goals / Non-Goals

**Goals:**
- Define base ingredient unit costs for espresso ($0.40/shot), milk ($0.05/oz), chocolate ($0.08/oz), whipped cream ($0.25/serving), and alternative milk ($0.15/oz).
- Define drink recipes by size and calculate COGS from ingredient quantities using the formula sum(quantity × unit cost).
- Ensure customization surcharges also contribute to COGS by adding their ingredient costs separately from customer surcharge revenue.
- Expose order financial details via the backend API.
- Add a live financial dashboard next to the order board with total revenue, total COGS, and gross margin.
- Show a per-order financial breakdown for each order.

**Non-Goals:**
- Inventory tracking, supplier management, purchase ordering, or historical accounting.
- Multi-location support.
- Fully persistent financial history beyond the in-memory order list.

## Decisions

### 1. Use immutable backend configuration for ingredient costs and recipes

- Store ingredient unit costs in a centralized backend configuration module.
- Store drink recipe definitions in a centralized backend config structure keyed by `item_id` and `size`.
- Include size-dependent recipe mappings so that large drinks use two espresso shots while small and medium drinks use one.
- This keeps recipe data in code, avoids a new data store, and fits the current JSON/config-driven architecture.

Alternatives considered:
- Persisting recipes in a separate JSON file. Rejected because the project is small and the current menu is already driven by code-defined structures.
- Building a generic recipe engine. Rejected as overkill for the current scope.

### 2. Extend the order model with COGS and margin fields

- Add `cogs`, `revenue`, and `margin` fields to the `Order` dataclass (or equivalent order object).
- `revenue` should equal the existing customer-facing price for the order, including base size price and customization surcharges.
- `cogs` should equal the sum of each ingredient quantity multiplied by its unit cost for the drink recipe, plus any ingredient cost contributions from customizations.
  - For example, an extra espresso shot shall add the cost of one espresso shot to the order COGS in addition to the $0.75 customer surcharge for the extra shot.
- `margin` should equal `revenue - cogs`.

This makes financial values explicit in the order object and avoids repeated recomputation in the dashboard.

### 3. Calculate customization COGS from ingredient costs, not from surcharge values

- Define customization ingredient contributions in the backend, e.g. `extra-shot` adds 1 espresso shot, `oat-milk` adds alternative milk volume, `whipped-cream` adds one serving.
- Keep customer surcharge prices separate from ingredient cost contributions.

This preserves the ability to have different customer-facing surcharges than ingredient costs while still calculating true COGS.

### 4. Expose order financials in API responses

- Update `POST /api/orders` and `GET /api/orders` to include a `financials` or `order_finance` object with `revenue`, `cogs`, and `margin`.
- The order response should also continue to expose existing fields such as `total_price` for backward compatibility.

This avoids requiring the frontend to infer costs from menu data and keeps financial logic server-side.

### 5. Render the dashboard from the current in-memory order list

- Compute dashboard totals from all active orders returned by `GET /api/orders`.
- Recalculate dashboard totals whenever the frontend receives an updated order list, including after order creation, cancellation, or refresh.
- Use the existing frontend order list state to keep metrics live as orders are placed, completed, or removed.
- Show per-order revenue, COGS, and margin within the order queue.

This avoids introducing historical storage or a separate analytics backend. For this simple in-memory app, live updates are implemented by recalculating totals on render after order state changes rather than adding polling or server-sent events.

## Risks / Trade-offs

- [Risk] Recipe quantities are hard-coded and may not reflect real barista practices.
  → Mitigation: choose sensible defaults and keep recipe data centralized so it can be updated easily.

- [Risk] Customizations that add ingredient cost may not match current surcharge semantics.
  → Mitigation: define customization ingredient contributions explicitly and document the mapping.

- [Risk] In-memory order state means financial totals are not persistent across server restarts.
  → Mitigation: acknowledge it as an acceptable limitation for the current scope.

- [Risk] Adding financial UI may clutter the order board if not designed carefully.
  → Mitigation: keep the dashboard compact and place it alongside the order board with clear labels.

## Migration Plan

1. Add the cost model constants and recipe definitions in `backend/models.py`.
2. Extend the order model and order creation logic to compute `cogs`, `revenue`, and `margin`.
3. Update `POST /api/orders` and `GET /api/orders` to include financial data in order responses.
4. Add frontend dashboard components and order row breakdown rendering.
5. Validate with orders that include customizations and verify live dashboard totals update.

If a rollback is needed, remove the financial dashboard UI and revert order response changes while leaving the existing ordering flow intact.

## Open Questions

- Should `revenue` be presented as the pre-tax subtotal or include tax? The current system uses pre-tax totals, so this change should align with that convention.
- Should margins be shown for all orders in the queue, or only for completed orders? The current spec favors a live dashboard for orders as they are placed and completed.
