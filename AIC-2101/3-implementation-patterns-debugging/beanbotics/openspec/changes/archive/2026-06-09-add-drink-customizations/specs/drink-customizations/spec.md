## ADDED Requirements

### Requirement: Menu cards expose customization options
Each menu card SHALL provide customization controls for optional extras: extra espresso shot, milk alternative selection (none, oat, almond, soy), and whipped cream.

#### Scenario: Customization controls are visible on load
- **WHEN** the menu page loads
- **THEN** each menu card shows controls for extra espresso shot, milk alternative, and whipped cream

#### Scenario: Milk alternative defaults to none
- **WHEN** a menu card first renders
- **THEN** milk alternative SHALL default to `none`

### Requirement: Dynamic total includes selected customizations
The displayed order total on each menu card SHALL include the selected size price plus surcharges for selected customizations: extra shot +$0.75, milk alternative +$0.60 when not `none`, whipped cream +$0.50.

#### Scenario: Single customization updates total
- **WHEN** the customer enables extra espresso shot on a medium drink priced $5.50
- **THEN** the order button total SHALL update to $6.25

#### Scenario: Multiple customizations update total
- **WHEN** the customer selects milk alternative `oat` and whipped cream on a large drink priced $6.50
- **THEN** the order button total SHALL update to $7.60

### Requirement: Submitted orders include customization payload
When an order is placed, the system SHALL submit selected customization values in the order request.

#### Scenario: Submit with all customizations selected
- **WHEN** the customer enables extra shot, selects milk alternative `soy`, enables whipped cream, and clicks order
- **THEN** the system SHALL send `POST /api/orders` with `customizations` containing `{ "extra_shot": true, "milk_alternative": "soy", "whipped_cream": true }`

#### Scenario: Submit with defaults
- **WHEN** the customer places an order without selecting extras
- **THEN** the system SHALL send `customizations` containing `{ "extra_shot": false, "milk_alternative": "none", "whipped_cream": false }`

### Requirement: Order records persist customizations and total
The backend SHALL persist selected customizations and computed final total in each order record returned by order APIs.

#### Scenario: API returns persisted customizations
- **WHEN** an order is created with milk alternative `almond`
- **THEN** subsequent `GET /api/orders` responses SHALL include the same customization values for that order

#### Scenario: Backend computes authoritative total
- **WHEN** an order is submitted with selected extras
- **THEN** the backend SHALL compute final total from base size price plus fixed surcharges before storing and returning the order
