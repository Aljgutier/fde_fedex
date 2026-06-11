## ADDED Requirements

### Requirement: Financial dashboard displays revenue, COGS, and gross margin
The system SHALL display a financial dashboard alongside the order board that shows total revenue, total COGS, and gross margin.

#### Scenario: Dashboard displays financial totals
- **WHEN** the order board is visible
- **THEN** the dashboard SHALL display the current total revenue, total COGS, and gross margin

### Requirement: Gross margin is defined as revenue minus COGS
The system SHALL define gross margin as revenue minus COGS and display it as a dollar amount. The dashboard MAY also show gross margin as a percentage, but the dollar amount is required.

#### Scenario: Gross margin is calculated correctly
- **WHEN** an order has known revenue and COGS values
- **THEN** the system SHALL display gross margin equal to revenue minus COGS

### Requirement: Dashboard updates live as orders change
The financial dashboard SHALL update live as orders are placed, updated, or completed.

#### Scenario: Dashboard updates when an order is placed
- **WHEN** a new order is placed
- **THEN** the financial dashboard SHALL refresh to reflect the updated total revenue, total COGS, and gross margin

#### Scenario: Dashboard updates when an order is completed
- **WHEN** an order is completed or removed
- **THEN** the financial dashboard SHALL refresh to reflect the updated totals

### Requirement: Per-order financial breakdown is visible
The system SHALL show each order’s revenue, COGS, and margin as part of the order queue or order details.

#### Scenario: Order list shows financial breakdown
- **WHEN** orders are displayed in the order queue
- **THEN** each order SHALL show its revenue, COGS, and margin values
