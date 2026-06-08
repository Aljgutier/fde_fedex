## ADDED Requirements

### Requirement: Customization options constant

The system SHALL define a `CUSTOMIZATIONS` constant mapping option IDs to their display names and prices:
- `extra-shot`: "Extra Espresso Shot", $0.75
- `oat-milk`: "Oat Milk", $0.60
- `almond-milk`: "Almond Milk", $0.60
- `soy-milk`: "Soy Milk", $0.60
- `whipped-cream`: "Whipped Cream", $0.50

All options SHALL be available for all drinks with no per-drink restrictions.

#### Scenario: Options constant is accessible
- **WHEN** the customization options are queried
- **THEN** the system SHALL return all five options with their IDs, names, and prices

### Requirement: Order model includes customizations

The `Order` model SHALL include a `customizations` field containing a list of customization IDs selected for the order. The field SHALL default to an empty list.

#### Scenario: Order created without customizations
- **WHEN** an order is placed with no customizations specified
- **THEN** the order SHALL have an empty `customizations` list and `total_price` equal to the base size price

#### Scenario: Order created with customizations
- **WHEN** an order is placed with customizations `["extra-shot", "oat-milk"]`
- **THEN** the order SHALL store `["extra-shot", "oat-milk"]` in its `customizations` field

### Requirement: Price calculation includes customization surcharges

The order `total_price` SHALL equal the base size price plus the sum of all selected customization surcharges.

#### Scenario: Single customization adds to price
- **WHEN** an order is placed for a medium Neural Network Latte ($5.50) with `["extra-shot"]`
- **THEN** `total_price` SHALL be $6.25 ($5.50 + $0.75)

#### Scenario: Multiple customizations add to price
- **WHEN** an order is placed for a small Deep Learning Doppio ($3.50) with `["extra-shot", "whipped-cream", "almond-milk"]`
- **THEN** `total_price` SHALL be $5.35 ($3.50 + $0.75 + $0.50 + $0.60)

#### Scenario: No customizations means base price only
- **WHEN** an order is placed with no customizations
- **THEN** `total_price` SHALL equal the base size price

### Requirement: POST /api/orders accepts customizations

The `POST /api/orders` endpoint SHALL accept an optional `customizations` field in the request body — a list of customization IDs. If omitted, it SHALL default to an empty list.

#### Scenario: Valid customizations accepted
- **WHEN** a POST request includes `{ "item_id": "neural-latte", "size": "medium", "customizations": ["extra-shot"] }`
- **THEN** the system SHALL create the order with the customization and return HTTP 200 with the order including customizations and adjusted total price

#### Scenario: Invalid customization ID rejected
- **WHEN** a POST request includes a customization ID not in the known options (e.g., `"double-whip"`)
- **THEN** the system SHALL return HTTP 400 with an error describing the invalid customization

#### Scenario: No customizations field defaults to empty
- **WHEN** a POST request omits the `customizations` field
- **THEN** the system SHALL create the order with an empty customizations list (backward compatible)

### Requirement: GET /api/customizations endpoint

The system SHALL expose `GET /api/customizations` returning all available customization options with their IDs, display names, and prices.

#### Scenario: Retrieve all customization options
- **WHEN** a GET request is sent to `/api/customizations`
- **THEN** the system SHALL return a JSON response with all five customization options, each including `id`, `name`, and `price`

### Requirement: Order display name includes customizations

The order `items` list SHALL include the drink name followed by customization names for display purposes. Customizations SHALL appear as a parenthetical suffix, e.g., "Medium Neural Network Latte (Extra Espresso Shot, Oat Milk)".

#### Scenario: Display name with customizations
- **WHEN** an order for a medium Neural Network Latte with `["extra-shot", "oat-milk"]` is created
- **THEN** the `items` list SHALL contain `"Medium Neural Network Latte (Extra Espresso Shot, Oat Milk)"`

#### Scenario: Display name without customizations
- **WHEN** an order with no customizations is created
- **THEN** the `items` list SHALL contain the drink name without a parenthetical suffix
