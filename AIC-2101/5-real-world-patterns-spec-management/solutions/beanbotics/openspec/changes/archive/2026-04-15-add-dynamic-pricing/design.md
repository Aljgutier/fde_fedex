## Context

BeanBotics currently uses fixed pricing loaded from `menu.json`. The `MenuService` serves prices as-is, `OrderService.place_order()` looks up the base price by size, adds customization surcharges, and computes tax and COGS. The frontend renders prices from the menu response and submits orders with `{ item_id, size, customizations }`.

This change introduces a peak/off-peak pricing tier system. Since there's no real clock to drive tier changes (the app is a demo), a UI toggle simulates the active tier. The discount applies only to base drink prices — customizations and COGS are unaffected.

## Goals / Non-Goals

**Goals:**
- Allow the business to offer 20% off-peak discounts on base drink prices
- Keep the backend as the single source of truth for all price calculations
- Maintain backward compatibility on POST /api/orders (omitting `pricing_tier` defaults to peak)
- Show pricing tier impact on the financial dashboard

**Non-Goals:**
- Variable discount rates per drink or per tier
- More than two pricing tiers
- Customer-facing schedule of when tiers apply
- Historical pricing data or analytics over time

## Decisions

### 1. Backend owns all price calculations

The backend computes both the menu display prices and order prices. `GET /api/menu` returns `price` (peak) and `off_peak_price` (base x 0.80) for each size. The frontend never applies the 20% discount itself — it picks the right price field based on the toggle state.

**Why:** Single source of truth. If the discount rate changes, it changes in one place. No risk of frontend and backend diverging on a calculated price.

**Alternative considered:** Frontend applies 20% client-side. Simpler API, but creates two independent implementations of the same business logic.

### 2. Frontend sends `pricing_tier` enum, not a timestamp

`POST /api/orders` accepts `pricing_tier: "peak" | "off-peak"` (optional, defaults to `"peak"`). The backend doesn't need to know what time it is — the toggle state is the only input.

**Why:** The time simulation is a UI concern. Since the toggle has only two states, sending the tier directly is simpler and more explicit than sending a timestamp that the backend would have to re-interpret. It also keeps backward compatibility clean — the field is optional with a sensible default.

**Alternative considered:** Send a simulated timestamp, let the backend derive the tier. Adds unnecessary coupling to the peak/off-peak hour definitions on both sides.

### 3. `items_detail` carries a `discount` object

For off-peak orders, the API response includes `discount: { "label": "Off-Peak Discount (20%)", "amount": -0.85 }`. For peak orders, `discount: null`. The `base_price` field always holds the full (peak) price.

**Why:** The frontend needs structured data to render the discount line on receipts. Keeping `base_price` as the full price means the receipt can show both the original price and the discount amount without the frontend having to reverse-calculate anything. The `label` field lets the backend control the display text.

**Alternative considered:** Pre-discount `base_price` (set to the already-discounted value). Simpler response, but then the frontend can't show the original price or the discount amount without fetching it separately from the menu.

### 4. Order model stores `pricing_tier`

The `Order` dataclass gets a `pricing_tier: str` field (default `"peak"`). Set at creation, immutable after that.

**Why:** The financial dashboard needs to show per-order tier breakdown. Without persisting it, the dashboard would need to re-derive the tier from timestamps or other indirect signals. Storing it directly is cheap and unambiguous.

### 5. Toggle, not slider

The UI uses a two-state toggle ("Peak" / "Off-Peak") instead of a continuous time slider. Defaults to "Peak" on page load.

**Why:** There are only two pricing states. A continuous slider would add complexity (time parsing, boundary detection) with no additional capability. A toggle is immediately understandable and maps 1:1 to the pricing tiers.

### 6. `GET /api/menu` always returns both price points

Every size object includes both `price` and `off_peak_price`. No query parameter needed.

**Why:** The frontend needs both prices for the strikethrough display (showing original + discounted). Returning both unconditionally keeps the API stateless and avoids the frontend making two requests or caching prices across toggle changes.

### 7. Confirmation overlay live-updates on toggle change

If the toggle changes while the confirmation overlay is open, the overlay re-renders with the new tier's prices.

**Why:** The overlay reads from the same pricing state as the menu. Making it reactive avoids a stale-price edge case where the customer confirms at a price that no longer matches the active tier. Simpler than snapshot-and-lock.

## Risks / Trade-offs

**Frontend trust** — The frontend sends `pricing_tier` and the backend trusts it. A caller could send `"off-peak"` at any time to get the discount. This is acceptable because BeanBotics has no authentication and the toggle is a simulation feature, not a security boundary. If this ever moved to production with a real clock, the backend would derive the tier from server time instead of accepting it from the client.

**Hardcoded 20%** — The discount rate is embedded in the backend calculation, not configurable. This matches the scope boundary (no variable rates). If rates need to change later, it's a single constant to update.

**`total_price` semantics shift** — The existing `total_price` field on Order represents the pre-tax subtotal. With dynamic pricing, this subtotal will reflect the discounted base price for off-peak orders. Existing consumers (the financial dashboard) already use this field as revenue, so the change flows through correctly. But any future consumer expecting `total_price` to match the menu's base price will be surprised.
