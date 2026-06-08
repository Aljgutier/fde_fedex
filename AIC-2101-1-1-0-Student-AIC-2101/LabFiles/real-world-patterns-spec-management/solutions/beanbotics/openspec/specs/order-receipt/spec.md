## ADDED Requirements

### Requirement: Backend returns itemized pricing in order responses

The backend SHALL include an `items_detail` object in every order returned by `POST /api/orders` and `GET /api/orders`. The `items_detail` object SHALL contain:
- `base_price`: the full (peak) price of the drink at the selected size
- `discount`: for off-peak orders, an object with `label` (string) and `amount` (negative number); for peak orders, `null`
- `customizations`: an array of objects, each with `name` and `price`
- `subtotal`: base_price + discount.amount (if present) + sum of customization prices
- `tax_rate`: the tax rate applied (0.085)
- `tax`: the tax amount (subtotal x tax_rate, rounded to 2 decimal places)
- `total`: subtotal + tax

The existing `total_price` field SHALL continue to represent the pre-tax subtotal for backward compatibility.

#### Scenario: Peak order — no discount field
- **WHEN** a customer places an order for a Medium Neural Network Latte ($4.25) with Extra Espresso Shot ($0.75) and Oat Milk ($0.60) during peak hours
- **THEN** the order response SHALL include `items_detail` with:
  - `base_price`: 4.25
  - `discount`: null
  - `customizations`: [{"name": "Extra Espresso Shot", "price": 0.75}, {"name": "Oat Milk", "price": 0.60}]
  - `subtotal`: 5.60
  - `tax_rate`: 0.085
  - `tax`: 0.48
  - `total`: 6.08

#### Scenario: Off-peak order — discount field present
- **WHEN** a customer places an order for a Medium Neural Network Latte ($4.25) with Extra Espresso Shot ($0.75) and Oat Milk ($0.60) during off-peak hours
- **THEN** the order response SHALL include `items_detail` with:
  - `base_price`: 4.25
  - `discount`: {"label": "Off-Peak Discount (20%)", "amount": -0.85}
  - `customizations`: [{"name": "Extra Espresso Shot", "price": 0.75}, {"name": "Oat Milk", "price": 0.60}]
  - `subtotal`: 4.75
  - `tax_rate`: 0.085
  - `tax`: 0.40
  - `total`: 5.15

#### Scenario: Order without customizations includes itemized detail
- **WHEN** a customer places an order for a Small GAN Cappuccino ($4.00) with no customizations
- **THEN** the order response SHALL include `items_detail` with:
  - `base_price`: 4.00
  - `discount`: null
  - `customizations`: []
  - `subtotal`: 4.00
  - `tax_rate`: 0.085
  - `tax`: 0.34
  - `total`: 4.34

#### Scenario: GET /api/orders returns itemized detail for all orders
- **WHEN** `GET /api/orders` is called
- **THEN** every order in the response SHALL include the `items_detail` object

### Requirement: Receipt view for completed orders

Completed orders SHALL display a receipt with a line-item breakdown. The receipt SHALL show:
1. **Base item**: drink name, size, and base price (always the full peak price)
2. **Discount** (off-peak only): "Off-Peak Discount (20%)" line item with negative amount, shown between base price and customizations
3. **Customizations**: each customization on its own line with its price (omitted if none)
4. **Subtotal**: base price + discount (if any) + customization prices
5. **Tax**: labeled "Tax (8.5%)" with the tax amount
6. **Total**: final amount including tax, visually emphasized

Peak orders display without a discount line. Off-peak orders MUST include the discount line.

#### Scenario: Receipt for peak order with customizations
- **WHEN** a completed peak order for Medium Neural Network Latte with Extra Espresso Shot and Oat Milk is displayed
- **THEN** the receipt SHALL show:
  - "Neural Network Latte (Medium)" — $4.25
  - "Extra Espresso Shot" — $0.75
  - "Oat Milk" — $0.60
  - Subtotal — $5.60
  - Tax (8.5%) — $0.48
  - Total — $6.08

#### Scenario: Receipt for off-peak order with customizations
- **WHEN** a completed off-peak order for Medium Neural Network Latte with Extra Espresso Shot and Oat Milk is displayed
- **THEN** the receipt SHALL show:
  - "Neural Network Latte (Medium)" — $4.25
  - "Off-Peak Discount (20%)" — -$0.85
  - "Extra Espresso Shot" — $0.75
  - "Oat Milk" — $0.60
  - Subtotal — $4.75
  - Tax (8.5%) — $0.40
  - Total — $5.15

#### Scenario: Receipt for order without customizations
- **WHEN** a completed order for Small GAN Cappuccino with no customizations is displayed
- **THEN** the receipt SHALL show:
  - "GAN Cappuccino (Small)" — $4.00
  - Subtotal — $4.00
  - Tax (8.5%) — $0.34
  - Total — $4.34
- **AND** no customization lines SHALL appear

### Requirement: Receipt is toggled inline on completed orders

Each completed order SHALL display a "View Receipt" button. Clicking it SHALL expand an inline receipt panel below the order. Clicking again (or a "Hide Receipt" toggle) SHALL collapse it.

#### Scenario: Expanding a receipt
- **WHEN** the customer clicks "View Receipt" on a completed order
- **THEN** the receipt panel SHALL expand below the order showing the line-item breakdown
- **AND** the button text SHALL change to "Hide Receipt"

#### Scenario: Collapsing a receipt
- **WHEN** the customer clicks "Hide Receipt" on an expanded receipt
- **THEN** the receipt panel SHALL collapse
- **AND** the button text SHALL change back to "View Receipt"

#### Scenario: Multiple receipts can be open simultaneously
- **WHEN** the customer expands receipts on two different completed orders
- **THEN** both receipt panels SHALL be visible at the same time
