## ADDED Requirements

### Requirement: COGS calculated on order placement
The system SHALL calculate the Cost of Goods Sold (COGS) for each order when it is placed. COGS equals the sum of (ingredient quantity x ingredient unit cost) for all ingredients in the drink recipe, plus the sum of ingredient costs from any applied customizations.

#### Scenario: Order with no customizations
- **WHEN** an order is placed for a medium Neural Network Latte with no customizations
- **THEN** the order's COGS equals the sum of the medium latte recipe's ingredient costs (espresso shots x espresso cost + milk oz x milk cost)

#### Scenario: Order with customizations adds ingredient cost
- **WHEN** an order is placed for a large Machine Learning Mocha with an extra shot
- **THEN** the order's COGS includes the large mocha recipe's ingredient costs plus the extra shot's ingredient cost from its mapping

#### Scenario: Multiple customizations stack
- **WHEN** an order includes both oat-milk and whipped-cream customizations
- **THEN** the COGS includes ingredient costs from both customization mappings added to the base recipe cost

### Requirement: COGS stored on Order model
The Order model SHALL include a `cogs` field (numeric, dollars) that stores the calculated COGS. This field SHALL be populated at order creation and SHALL NOT change after placement.

#### Scenario: COGS persists on order
- **WHEN** an order is placed and its COGS is calculated
- **THEN** the `cogs` value is stored on the Order object and remains constant regardless of status changes

#### Scenario: COGS included in order API response
- **WHEN** a client requests GET /api/orders
- **THEN** each order in the response includes a `cogs` field with the calculated cost

### Requirement: COGS included in order creation response
The POST /api/orders response SHALL include the `cogs` field so the frontend can display cost data immediately after order placement.

#### Scenario: Order creation response includes COGS
- **WHEN** POST /api/orders succeeds
- **THEN** the response body includes the `cogs` value for the newly created order
