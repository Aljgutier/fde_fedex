## 1. Ingredient Data

- [x] 1.1 Create `backend/data/ingredients.json` with base ingredient definitions (espresso, milk, chocolate, whipped cream, oat milk, almond milk, soy milk) — each with id, name, unit, and cost_per_unit
- [x] 1.2 Add customization-to-ingredient mappings in `ingredients.json` mapping each customization id to ingredient quantities consumed
- [x] 1.3 Create `IngredientService` in `backend/services/ingredients.py` that loads and validates ingredient data at startup (reject missing fields, negative costs)

## 2. Drink Recipes

- [x] 2.1 Add `recipe` field to each size entry in `backend/data/menu.json` mapping ingredient ids to quantities (e.g. small latte: 1 espresso shot, 8oz milk)
- [x] 2.2 Update `MenuService` to validate that every drink/size has a recipe and all recipe ingredient ids exist in the ingredient data
- [x] 2.3 Validate recipe quantities are positive numbers at load time

## 3. COGS Calculation

- [x] 3.1 Add `cogs` field (float, default None) to the `Order` dataclass in `backend/models.py`
- [x] 3.2 Implement COGS calculation in `OrderService.place_order()` — sum recipe ingredient costs plus customization ingredient costs
- [x] 3.3 Wire `IngredientService` into `OrderService` (pass via constructor, initialize in `app.py`)

## 4. API Integration

- [x] 4.1 Verify `cogs` field is included in POST /api/orders and GET /api/orders responses (dataclass serialization)
- [x] 4.2 Add GET /api/financials endpoint returning aggregate totals: revenue, cogs, margin computed from all non-cancelled orders

## 5. Financial Dashboard Frontend

- [x] 5.1 Add dashboard HTML section in `index.html` alongside the order board with placeholders for revenue, COGS, and margin
- [x] 5.2 Add dashboard styling in `style.css` — layout, metric cards, per-order breakdown table
- [x] 5.3 Implement `loadFinancials()` in `script.js` that fetches GET /api/financials and renders aggregate metrics
- [x] 5.4 Add per-order breakdown table in the dashboard showing order id, drink name, revenue, COGS, and margin per order
- [x] 5.5 Call `loadFinancials()` after order placement, status changes, and cancellations so the dashboard updates live

## 6. Validation and Testing

- [x] 6.1 Start the server and place orders with various drink/size/customization combinations — verify COGS values are reasonable
- [x] 6.2 Verify the financial dashboard totals match the sum of individual order financials
- [x] 6.3 Verify dashboard updates live after placing a new order and after cancelling an order
