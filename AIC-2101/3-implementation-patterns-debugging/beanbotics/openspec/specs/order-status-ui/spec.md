## ADDED Requirements

### Requirement: Status-colored badges

Each order SHALL display its status as a colored badge. The badge colors SHALL be:
- `pending` — amber/yellow
- `preparing` — cyan/blue
- `ready` — green
- `completed` — muted grey
- `cancelled` — muted grey

Each status MUST be visually distinct. The badge color MUST clearly differentiate pending, preparing, ready,
completed, and cancelled orders.

#### Scenario: Pending order shows amber badge
- **WHEN** an order with status `pending` is displayed
- **THEN** the status badge SHALL have the `.status-pending` class and appear in amber/yellow

#### Scenario: Preparing order shows cyan badge
- **WHEN** an order with status `preparing` is displayed
- **THEN** the status badge SHALL have the `.status-preparing` class and appear in cyan/blue

#### Scenario: Ready order shows green badge
- **WHEN** an order with status `ready` is displayed
- **THEN** the status badge SHALL have the `.status-ready` class and appear in green

#### Scenario: Completed order shows grey badge
- **WHEN** an order with status `completed` is displayed
- **THEN** the status badge SHALL have the `.status-completed` class and appear in muted grey

### Requirement: Advance buttons

Each non-terminal order SHALL display an inline button to advance it to the next status. The button label SHALL reflect the target action:
- `pending` → "Start Preparing"
- `preparing` → "Mark Ready"
- `ready` → "Complete"

Terminal orders (`completed`, `cancelled`) SHALL NOT display an advance button.

#### Scenario: Pending order shows advance button
- **WHEN** an order with status `pending` is displayed
- **THEN** an "Start Preparing" button SHALL be shown
- **AND WHEN** the button is clicked
- **THEN** the system SHALL send `PATCH /api/orders/{id}` with `{ "status": "preparing" }` and refresh the order list

#### Scenario: Preparing order shows advance button
- **WHEN** an order with status `preparing` is displayed
- **THEN** a "Mark Ready" button SHALL be shown
- **AND WHEN** the button is clicked
- **THEN** the system SHALL send `PATCH /api/orders/{id}` with `{ "status": "ready" }` and refresh the order list

#### Scenario: Ready order shows advance button
- **WHEN** an order with status `ready` is displayed
- **THEN** a "Complete" button SHALL be shown
- **AND WHEN** the button is clicked
- **THEN** the system SHALL send `PATCH /api/orders/{id}` with `{ "status": "completed" }` and refresh the order list

#### Scenario: Completed order has no action buttons
- **WHEN** an order with status `completed` is displayed
- **THEN** no advance or cancel buttons SHALL be shown

### Requirement: Cancel button restricted to pending

The cancel button SHALL only appear on orders with status `pending`. Once an order advances to `preparing` or beyond, cancellation is no longer available in the UI.

#### Scenario: Pending order shows cancel button
- **WHEN** an order with status `pending` is displayed
- **THEN** a "Cancel" button SHALL be shown alongside the "Start Preparing" button

#### Scenario: Non-pending order hides cancel button
- **WHEN** an order with status `preparing`, `ready`, or `completed` is displayed
- **THEN** no cancel button SHALL be shown

### Requirement: Grouped order display

The orders section SHALL continue to split into two groups:
- **Active Orders**: orders with status `pending`, `preparing`, or `ready` - displayed with action controls
- **Completed**: orders with status `completed` - displayed below active orders with no action buttons

Each displayed order card SHALL include selected customization details when present.

If either group is empty, it SHALL not render a heading or empty container.

#### Scenario: Mixed orders display in groups with customizations
- **WHEN** the order list contains orders in various statuses and some orders have customizations
- **THEN** active orders (`pending`, `preparing`, `ready`) SHALL appear under an "Active Orders" heading
- **AND** completed orders SHALL appear under a "Completed" heading below
- **AND** each order card SHALL display its selected customizations

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
Both queue and status board order cards SHALL render a human-readable summary of selected customizations for each order.

#### Scenario: Order card displays multiple selected extras
- **WHEN** an order has extra shot enabled and milk alternative `soy`
- **THEN** the order card SHALL show labels for "Extra shot" and "Soy milk"

#### Scenario: Order card omits unselected extras
- **WHEN** an order has no optional extras selected
- **THEN** the order card SHALL omit customization labels and display only existing order details
