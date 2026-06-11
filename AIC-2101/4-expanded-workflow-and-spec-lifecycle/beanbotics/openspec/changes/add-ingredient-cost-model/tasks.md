## 1. Backend recipe and ingredient cost configuration

- [x] 1.1 Add immutable ingredient unit cost definitions in the backend configuration: espresso $0.40/shot, milk $0.05/oz, chocolate $0.08/oz, whipped cream $0.25/serving, alternative milk $0.15/oz.
- [x] 1.2 Add drink recipe definitions keyed by `item_id` and `size`, including size-dependent quantities (small/medium 1 espresso shot, large 2 espresso shots).
- [x] 1.3 Add customization ingredient cost contributions separately from customer surcharge pricing.

## 2. Order model and financial calculation

- [x] 2.1 Extend the backend order model to store `revenue`, `cogs`, and `margin` for each order.
- [x] 2.2 Calculate order revenue as the base drink price plus customization surcharges.
- [x] 2.3 Calculate order COGS from recipe ingredient quantities and unit costs, including customization ingredient costs.
- [x] 2.4 Calculate order margin as `revenue - cogs`.

## 3. API response updates

- [x] 3.1 Update `POST /api/orders` to return the order financial data.
- [x] 3.2 Update `GET /api/orders` to include financial values for all active orders.
- [x] 3.3 Preserve existing order response fields for backward compatibility while exposing the new financial fields.

## 4. Frontend dashboard and order breakdown

- [x] 4.1 Add a financial dashboard component next to the order board.
- [x] 4.2 Render total revenue, total COGS, and gross margin in the dashboard.
- [x] 4.3 Render per-order revenue, COGS, and margin as part of the order queue.
- [x] 4.4 Recalculate dashboard metrics whenever the frontend order list updates.

## 5. Validation and manual checks

- [x] 5.1 Verify that large drink orders use 2 espresso shots in the recipe-based COGS calculation.
- [x] 5.2 Verify that extra shot customizations add espresso cost to COGS and a surcharge to revenue.
- [x] 5.3 Verify the dashboard updates correctly when orders are placed and removed.
