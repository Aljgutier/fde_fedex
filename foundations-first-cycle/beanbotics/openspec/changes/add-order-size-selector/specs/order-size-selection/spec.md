## ADDED Requirements

### Requirement: Customer can select drink size before ordering
The system SHALL provide a size selector in the order form for each selectable menu item, with options constrained to `small`, `medium`, and `large` when those sizes are available for that item.

#### Scenario: Size options shown for selected item
- **WHEN** a customer selects a menu item in the order form
- **THEN** the system shows size options available for that item and allows choosing one before placing the order

### Requirement: Price display reflects selected size
The system SHALL display the order price based on the currently selected menu item and size, and SHALL update the displayed price whenever size selection changes.

#### Scenario: Price updates on size change
- **WHEN** a customer changes the size selection for the current menu item
- **THEN** the displayed price updates to the corresponding size price before the order is submitted

### Requirement: Order submission includes selected size
The system SHALL send the selected size with the order payload when placing an order through the existing order creation flow.

#### Scenario: Payload includes size
- **WHEN** a customer submits an order after choosing a size
- **THEN** the request payload includes both the selected item identifier and the selected size
