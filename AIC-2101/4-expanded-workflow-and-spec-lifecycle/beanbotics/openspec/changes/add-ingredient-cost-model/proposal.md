## Why

BeanBotics needs a clearer financial view of drink profitability. The current system only tracks customer prices and surcharges, so it cannot calculate cost of goods sold (COGS) or gross margin per order.

This change combines ingredient cost definitions and size-based drink recipes into a single COGS model because the financial dashboard requires both pieces to calculate accurate order-level margins.

## What Changes

- Add an ingredient cost model that defines base ingredient unit costs and recipes for each drink size, including espresso ($0.40/shot), milk ($0.05/oz), chocolate ($0.08/oz), whipped cream ($0.25/serving), and alternative milk ($0.15/oz).
- Map each drink and size to ingredient quantities and calculate order-level COGS from those recipes.
- Include customization ingredient costs in COGS, not just customer surcharge prices.
- Add a financial dashboard alongside the order board showing total revenue, total COGS, and gross margin.
- Add a per-order financial breakdown showing revenue, COGS, and margin for each order.

## Capabilities

### New Capabilities
- `ingredient-cost-model`: Define base ingredient unit costs, map drink/size recipes to ingredient quantities, and calculate per-order COGS from recipe ingredients and customizations.
- `financial-dashboard`: Display a live dashboard alongside the order board with total revenue, total COGS, gross margin, and per-order revenue/COGS/margin breakdown.

### Modified Capabilities
- None: this change introduces new requirements without changing existing spec-level behavior.

## Impact

- Backend: extend the pricing/order model to include ingredient cost data and COGS calculations, including customization contributions.
- Backend API: expose order financial details and ensure order responses include revenue, COGS, and margin data for live dashboard rendering.
- Frontend: add the financial dashboard UI next to the order board, update order display to include per-order financial breakdown, and update live totals when orders are placed or completed.
- Services: ensure order creation and completion logic maintains accurate financial metrics for each order and the dashboard summary.
