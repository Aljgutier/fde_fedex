## MODIFIED Requirements

### Requirement: Grouped order display
The orders section SHALL continue to split into two groups:
- **Active Orders**: orders with status `pending`, `preparing`, or `ready` - displayed with action controls
- **Completed**: orders with status `completed` - displayed below active orders with no action buttons

Each displayed order card SHALL include selected customization details when present. Completed order cards SHALL include a receipt breakdown showing base price line item, selected customization line items, subtotal, tax, and total including tax.

If either group is empty, it SHALL not render a heading or empty container.

#### Scenario: Mixed orders display in groups with customizations and receipts
- **WHEN** the order list contains orders in various statuses and some orders have customizations
- **THEN** active orders (`pending`, `preparing`, `ready`) SHALL appear under an "Active Orders" heading
- **AND** completed orders SHALL appear under a "Completed" heading below
- **AND** active order cards SHALL display selected customizations when present
- **AND** completed order cards SHALL display selected customizations and receipt breakdown details

#### Scenario: No completed orders hides completed section
- **WHEN** all orders are in active statuses (none completed)
- **THEN** the "Completed" section SHALL not be rendered

#### Scenario: No active orders shows only completed
- **WHEN** all orders are completed
- **THEN** only the "Completed" section SHALL be rendered

#### Scenario: No orders at all
- **WHEN** there are no orders
- **THEN** the empty state message SHALL be displayed (no group headings)

### Requirement: Order cards display customization summary
Both queue and status board order cards SHALL render a human-readable summary of selected customizations for each order. For completed orders, the receipt breakdown SHALL present each selected customization as a separate priced line item.

#### Scenario: Order card displays multiple selected extras
- **WHEN** an order has extra shot enabled and milk alternative `soy`
- **THEN** the order card SHALL show labels for "Extra shot" and "Soy milk"
- **AND** if the order is completed, the receipt breakdown SHALL include separate line items for each selected customization

#### Scenario: Order card omits unselected extras
- **WHEN** an order has no optional extras selected
- **THEN** the order card SHALL omit customization labels and display only existing order details
- **AND** if the order is completed, the receipt SHALL not include customization line items
