## 1. Backend — Pricing Tier Foundation

- [x] 1.1 Add `OFF_PEAK_DISCOUNT` constant (0.20) and a `compute_off_peak_price(base_price)` helper to `models.py` that applies the discount and rounds to 2 decimal places (half-up)
- [x] 1.2 Add `pricing_tier` field to the `Order` dataclass (str, default `"peak"`)

## 2. Backend — Menu API

- [x] 2.1 Update `MenuService.get_all_items()` (or the `/api/menu` route) to enrich each size object with an `off_peak_price` field computed via the discount helper

## 3. Backend — Order Placement

- [x] 3.1 Add `pricing_tier` (optional, default `"peak"`) to the `OrderRequest` Pydantic model in `app.py`
- [x] 3.2 Update `OrderService.place_order()` to accept `pricing_tier`, apply the discount to `base_price` when tier is `"off-peak"`, and store the tier on the Order
- [x] 3.3 Update `items_detail` construction: keep `base_price` as the full peak price, add `discount` object (`{"label": "Off-Peak Discount (20%)", "amount": <negative>}` or `null`), and compute `subtotal` as `base_price + discount.amount + surcharges`
- [x] 3.4 Pass `pricing_tier` through the route in `app.py` to `order_service.place_order()`

## 4. Backend — Financials API

- [x] 4.1 Update `/api/financials` to include `pricing_tier` per order row and add `peak_revenue` / `off_peak_revenue` to the aggregate response

## 5. Frontend — Pricing Toggle

- [x] 5.1 Add a peak/off-peak toggle switch to the UI (default: peak) with a visible tier indicator label ("Peak Pricing" or "Off-Peak Pricing — 20% Off")
- [x] 5.2 Wire the toggle to a shared state variable that the menu, order button, confirmation overlay, and order submission logic can all read

## 6. Frontend — Menu Display

- [x] 6.1 Update menu card rendering to read `off_peak_price` from the menu response and show strikethrough + discounted price when the toggle is set to off-peak
- [x] 6.2 Update the order button price to reflect the tier-adjusted base price plus full customization surcharges
- [x] 6.3 Ensure prices update immediately when the toggle changes (no page reload)

## 7. Frontend — Order Confirmation Overlay

- [x] 7.1 Update the confirmation overlay to display the tier-adjusted total (discounted base + full surcharges during off-peak, no strikethrough or discount label)
- [x] 7.2 Make the overlay reactive to toggle changes while open — re-render prices if the tier changes

## 8. Frontend — Order Submission

- [x] 8.1 Include the current `pricing_tier` value in the `POST /api/orders` request body

## 9. Frontend — Receipt Display

- [x] 9.1 Update receipt rendering to show the "Off-Peak Discount (20%)" line item (from `items_detail.discount`) between the base price and customizations when present
- [x] 9.2 Verify subtotal, tax, and total reflect the discounted amounts for off-peak orders

## 10. Frontend — Financial Dashboard

- [x] 10.1 Add peak/off-peak revenue breakdown to the aggregate metrics display
- [x] 10.2 Add a "Pricing Tier" column to the per-order breakdown table

## 11. End-to-End Verification

- [x] 11.1 Place orders in both peak and off-peak modes, verify prices, receipts, and dashboard reflect correct tier-based calculations
- [x] 11.2 Toggle between peak and off-peak with the menu open — confirm prices update immediately
- [x] 11.3 Toggle while the confirmation overlay is open — confirm the overlay re-renders
- [x] 11.4 Verify backward compatibility: submit an order without `pricing_tier` in the request body and confirm it defaults to peak pricing
