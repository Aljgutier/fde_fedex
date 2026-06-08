## MODIFIED Requirements

### Requirement: Receipt line items

**Previous:** The `items_detail` object includes `base_price` as the price of the drink at the selected size.

**Updated:** The `items_detail` object SHALL include a `discount` field for off-peak orders. The `discount` field SHALL be an object with `label` (string) and `amount` (negative number). For peak orders, `discount` SHALL be `null`. The `base_price` SHALL always be the full (peak) price. The `subtotal` SHALL equal `base_price + discount.amount + sum of customization prices`.

Off-peak orders MUST include an "Off-Peak Discount (20%)" line item on the receipt between the base price and the customizations. Peak orders display as they do today (no changes).

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

