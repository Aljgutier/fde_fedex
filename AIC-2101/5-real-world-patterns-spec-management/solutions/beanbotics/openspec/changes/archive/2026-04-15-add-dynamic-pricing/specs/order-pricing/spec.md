# Delta Spec: Order Pricing — Dynamic Pricing

## MODIFIED

### Requirement: Order is placed with the selected size

**Previous:** When the customer clicks the order button, the system SHALL send the selected size to the API instead of always sending "medium".

**Updated:** When the customer clicks the order button, the system SHALL send the selected size and `pricing_tier` (`"peak"` or `"off-peak"`) to the API. If `pricing_tier` is omitted, the backend SHALL default to `"peak"` for backward compatibility. The backend SHALL calculate the base drink price according to the tier: full price for peak, 20% off for off-peak. Customization surcharges (extra shot, milk alternatives, whipped cream) SHALL NOT be discounted — only the base drink price is affected.

#### Scenario: Order placed during peak hours
- **WHEN** the customer places an order for a Large Neural Network Latte ($6.50) at 8:00am (peak)
- **THEN** the backend uses $6.50 as the base price
- **AND** the order total reflects the full base price plus any customization surcharges

#### Scenario: Order placed during off-peak hours
- **WHEN** the customer places an order for a Large Neural Network Latte ($6.50) at 3:00pm (off-peak)
- **THEN** the backend applies a 20% discount to the base price: $6.50 × 0.80 = $5.20
- **AND** the order total reflects $5.20 plus any customization surcharges at full price

#### Scenario: Customization surcharges are not discounted
- **WHEN** the customer places an order at 3:00pm (off-peak) for a Large Neural Network Latte with an extra espresso shot (+$0.75)
- **THEN** the base price is discounted to $5.20 but the extra shot remains $0.75
- **AND** the pre-tax subtotal is $5.95

#### Scenario: Price is locked at order placement time
- **WHEN** the customer places an order at 8:59am (peak) and the time crosses into off-peak (9:01am) before the order is completed
- **THEN** the order retains the peak price from when it was placed

## ADDED

### Requirement: Pricing tier stored on Order model
The Order model SHALL include a `pricing_tier` field storing the tier active at order placement: `"peak"` or `"off-peak"`. This field SHALL be set at creation and SHALL NOT change after placement.

#### Scenario: Peak order stores tier
- **WHEN** an order is placed during peak hours
- **THEN** the order's `pricing_tier` field is `"peak"`

#### Scenario: Off-peak order stores tier
- **WHEN** an order is placed during off-peak hours
- **THEN** the order's `pricing_tier` field is `"off-peak"`

#### Scenario: Pricing tier included in API responses
- **WHEN** `POST /api/orders` or `GET /api/orders` returns an order
- **THEN** the response SHALL include the `pricing_tier` field

## REMOVED

### Assumption: Drink prices are always the base size price
**Reason:** Drink prices now vary by time of day. The base size price in menu.json represents the full (peak) price. During off-peak hours, a 20% discount is applied to the base drink price. The fixed-price assumption is replaced by tier-based pricing.