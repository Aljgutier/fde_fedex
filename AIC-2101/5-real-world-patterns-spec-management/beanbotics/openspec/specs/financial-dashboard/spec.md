## ADDED Requirements

### Requirement: Aggregate financial metrics display
The frontend SHALL display a financial dashboard showing three aggregate metrics: total revenue (sum of all order totals), total COGS (sum of all order COGS), and gross margin (revenue minus COGS). The dashboard SHALL appear alongside the order board.

#### Scenario: Dashboard shows totals with orders present
- **WHEN** orders exist in the system
- **THEN** the dashboard displays total revenue, total COGS, and gross margin computed from all orders

#### Scenario: Dashboard shows zero state
- **WHEN** no orders have been placed
- **THEN** the dashboard displays $0.00 for revenue, COGS, and margin

### Requirement: Per-order financial breakdown
The dashboard SHALL include a per-order breakdown table showing each order's revenue (order total), COGS, and margin (revenue minus COGS).

#### Scenario: Per-order row displayed
- **WHEN** orders exist
- **THEN** each order appears as a row with its order ID, drink name, revenue, COGS, and margin

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
