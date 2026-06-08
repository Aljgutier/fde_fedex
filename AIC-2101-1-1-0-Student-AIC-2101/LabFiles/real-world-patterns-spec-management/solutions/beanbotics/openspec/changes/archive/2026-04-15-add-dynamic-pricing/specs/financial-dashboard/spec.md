# Delta Spec: Financial Dashboard — Dynamic Pricing

## MODIFIED

### Requirement: Aggregate financial metrics display

**Previous:** The frontend SHALL display a financial dashboard showing three aggregate metrics: total revenue (sum of all order totals), total COGS (sum of all order COGS), and gross margin (revenue minus COGS). The dashboard SHALL appear alongside the order board.

**Updated:** The financial dashboard SHALL display aggregate metrics broken down by pricing tier. The dashboard SHALL show: total revenue, total COGS, and gross margin as before, plus a breakdown showing peak revenue vs. off-peak revenue. This allows the business to see the impact of off-peak discounting on overall revenue and margins.

#### Scenario: Dashboard distinguishes peak and off-peak revenue
- **WHEN** orders have been placed during both peak and off-peak hours
- **THEN** the dashboard displays total revenue with a breakdown showing peak revenue and off-peak revenue separately

#### Scenario: Off-peak margins are lower than peak margins
- **WHEN** the same drink is ordered during peak and off-peak hours
- **THEN** the off-peak order shows lower revenue but the same COGS
- **AND** the off-peak gross margin is lower than the peak gross margin

### Requirement: Per-order financial breakdown

**Previous:** The dashboard SHALL include a per-order breakdown table showing each order's revenue (order total), COGS, and margin (revenue minus COGS).

**Updated:** The per-order breakdown table SHALL include a pricing tier column indicating whether each order was placed during peak or off-peak hours. For off-peak orders, the revenue column reflects the discounted price.

#### Scenario: Per-order row shows pricing tier
- **WHEN** an order was placed during off-peak hours
- **THEN** the per-order row displays "Off-Peak" in the pricing tier column
- **AND** the revenue reflects the discounted base price plus any full-price customization surcharges