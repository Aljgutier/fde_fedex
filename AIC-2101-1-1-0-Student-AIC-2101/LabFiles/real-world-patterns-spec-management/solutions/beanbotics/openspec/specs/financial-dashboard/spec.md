## ADDED Requirements

### Requirement: Aggregate financial metrics display
The financial dashboard SHALL display aggregate metrics broken down by pricing tier. The dashboard SHALL show: total revenue, total COGS, and gross margin as before, plus a breakdown showing peak revenue vs. off-peak revenue. This allows the business to see the impact of off-peak discounting on overall revenue and margins.

#### Scenario: Dashboard shows totals with orders present
- **WHEN** orders exist in the system
- **THEN** the dashboard displays total revenue, total COGS, and gross margin computed from all orders

#### Scenario: Dashboard distinguishes peak and off-peak revenue
- **WHEN** orders have been placed during both peak and off-peak hours
- **THEN** the dashboard displays total revenue with a breakdown showing peak revenue and off-peak revenue separately

#### Scenario: Dashboard shows zero state
- **WHEN** no orders have been placed
- **THEN** the dashboard displays $0.00 for revenue, COGS, and margin

### Requirement: Per-order financial breakdown
The per-order breakdown table SHALL include a pricing tier column indicating whether each order was placed during peak or off-peak hours. For off-peak orders, the revenue column reflects the discounted price.

#### Scenario: Per-order row displayed
- **WHEN** orders exist
- **THEN** each order appears as a row with its order ID, drink name, pricing tier, revenue, COGS, and margin

#### Scenario: Per-order row shows pricing tier
- **WHEN** an order was placed during off-peak hours
- **THEN** the per-order row displays "Off-Peak" in the pricing tier column
- **AND** the revenue reflects the discounted base price plus any full-price customization surcharges

#### Scenario: Order with positive margin
- **WHEN** an order has revenue of $6.00 and COGS of $1.50
- **THEN** the row shows margin as $4.50

### Requirement: Live dashboard updates
The financial dashboard SHALL update in real time as orders are placed and as order statuses change. The frontend SHALL re-render the dashboard whenever the order list is refreshed.

#### Scenario: New order updates totals
- **WHEN** a new order is placed
- **THEN** the dashboard totals immediately reflect the additional revenue and COGS

#### Scenario: Dashboard reflects current order list
- **WHEN** an order is cancelled (removed from the active order list)
- **THEN** the dashboard totals update to exclude the cancelled order's financials

### Requirement: Dashboard positioned alongside order board
The financial dashboard SHALL be displayed in the application layout alongside the existing order board, visible without requiring navigation or toggling.

#### Scenario: Dashboard visible on page load
- **WHEN** the page loads
- **THEN** the financial dashboard section is visible alongside the order board
