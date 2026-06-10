## Why

BeanBotics uses fixed pricing regardless of time of day. Coffee shops typically offer off-peak discounts to attract customers during slow periods. Dynamic pricing lets the business run full prices during peak hours and discount during off-peak. This can increase sales volume and revenue without changing the underlying menu or product offerings. 

## What Changes

- Pricing tier definitions (peak and off-peak)
- Time simulation for testing
- Modified menu display to show current prices based on time of day
- Modified order pricing to calculate based on current prices (peak and off-peak) instead of fixed price
- Modified receipts to show current prices at the time the order was placed
- Modified financial dashboard to reflect revenue based on dynamic pricing instead of fixed prices
- `POST /api/orders` accepts a new optional `pricing_tier` field (`"peak"` or `"off-peak"`, defaults to `"peak"` for backward compatibility)

## Capabilities

### New Capabilities
- `pricing-tiers`: Defines peak/off-peak pricing tiers, discount rules, and the time simulation slider for testing

### Modified Capabilities
- `menu-display`: Size options show strikethrough + discounted prices during off-peak; pricing tier indicator added
- `order-pricing`: Order placement sends simulated time; backend calculates tier-based price; customization surcharges exempt from discount
- `order-confirmation`: Overlay total uses tier-adjusted base price; no additional discount indicators needed
- `order-receipt`: Off-peak receipts include discount line item; base_price reflects active tier at time of order
- `financial-dashboard`: Aggregate metrics add peak vs. off-peak revenue breakdown; per-order table adds pricing tier column

## Impact

- **API**: `POST /api/orders` request body gains a time field for tier determination. Response `items_detail.base_price` now reflects tier-adjusted price.
- **Backend**: `OrderService` price calculation changes from fixed lookup to tier-aware. Order model needs to store which pricing tier applied.
- **Frontend**: Menu cards, order button, and receipt rendering all become tier-aware. New time simulation slider component added to UI.
- **Data**: No changes to `menu.json`. Menu prices continue to represent full (peak) prices; discounts are computed at runtime.

## Scope Boundaries

- More complex pricing logic beyond peak and off-peak
- Per-drink discount overrides
- Customer-facing tier schedule
- Historical pricing data

