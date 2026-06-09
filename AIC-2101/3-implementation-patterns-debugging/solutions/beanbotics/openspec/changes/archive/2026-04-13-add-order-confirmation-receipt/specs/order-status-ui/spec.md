## MODIFIED Requirements

### Requirement: Grouped order display

The orders section SHALL split into two groups:
- **Active Orders**: orders with status `pending`, `preparing`, or `ready` — displayed with action controls
- **Completed**: orders with status `completed` — displayed below active orders with a "View Receipt" button on each order

If either group is empty, it SHALL not render a heading or empty container.

#### Scenario: Mixed orders display in groups
- **WHEN** the order list contains orders in various statuses
- **THEN** active orders (`pending`, `preparing`, `ready`) SHALL appear under an "Active Orders" heading
- **AND** completed orders SHALL appear under a "Completed" heading below

#### Scenario: No completed orders hides completed section
- **WHEN** all orders are in active statuses (none completed)
- **THEN** the "Completed" section SHALL not be rendered

#### Scenario: No active orders shows only completed
- **WHEN** all orders are completed
- **THEN** only the "Completed" section SHALL be rendered

#### Scenario: No orders at all
- **WHEN** there are no orders
- **THEN** the empty state message SHALL be displayed (no group headings)

#### Scenario: Completed order shows View Receipt button
- **WHEN** a completed order is displayed
- **THEN** a "View Receipt" button SHALL be shown on the order
- **AND** no advance or cancel buttons SHALL be shown
