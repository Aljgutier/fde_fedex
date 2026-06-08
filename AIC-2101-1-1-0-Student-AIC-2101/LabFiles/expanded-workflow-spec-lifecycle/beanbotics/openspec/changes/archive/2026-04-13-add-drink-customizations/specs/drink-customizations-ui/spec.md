## ADDED Requirements

### Requirement: Customization checkboxes on menu cards

Each menu card SHALL display a set of checkboxes for available customization options. Options SHALL be loaded from `GET /api/customizations`. Each checkbox SHALL show the option name and surcharge price (e.g., "Extra Espresso Shot +$0.75").

#### Scenario: Menu card displays customization options
- **WHEN** the menu loads
- **THEN** each menu card SHALL show checkboxes for all available customizations with their names and prices

#### Scenario: Checkboxes are unchecked by default
- **WHEN** a menu card is rendered
- **THEN** all customization checkboxes SHALL be unchecked

### Requirement: Dynamic price update

The order button price SHALL update dynamically as customization checkboxes are toggled or the size selection changes. The displayed price SHALL equal the selected size price plus the sum of all checked customization surcharges.

#### Scenario: Checking a customization updates the price
- **WHEN** a customer checks "Extra Espresso Shot" on a card with medium ($5.50) selected
- **THEN** the order button SHALL display $6.25

#### Scenario: Unchecking a customization updates the price
- **WHEN** a customer unchecks "Extra Espresso Shot" (previously checked) on a card with medium ($5.50) selected
- **THEN** the order button SHALL display $5.50

#### Scenario: Changing size recalculates with customizations
- **WHEN** a customer has "Extra Espresso Shot" checked and changes size from medium ($5.50) to large ($6.50)
- **THEN** the order button SHALL display $7.25 ($6.50 + $0.75)

### Requirement: Order submission includes selected customizations

When the order button is clicked, the `POST /api/orders` request SHALL include the IDs of all checked customizations in the `customizations` field.

#### Scenario: Order placed with customizations
- **WHEN** a customer checks "Oat Milk" and "Whipped Cream" then clicks Order
- **THEN** the request body SHALL include `"customizations": ["oat-milk", "whipped-cream"]`

#### Scenario: Order placed without customizations
- **WHEN** a customer clicks Order with no checkboxes checked
- **THEN** the request body SHALL include `"customizations": []`

### Requirement: Customization checkboxes reset after ordering

After a successful order placement, the customization checkboxes on the menu card that was ordered from SHALL reset to unchecked, and the displayed price SHALL revert to the base size price.

#### Scenario: Checkboxes reset after order
- **WHEN** an order is successfully placed from a menu card
- **THEN** all customization checkboxes on that card SHALL be unchecked and the price SHALL show the base size price

### Requirement: Order queue displays customizations

Each order in the order queue SHALL display its customizations. If an order has customizations, they SHALL be visible as part of the order details.

#### Scenario: Order with customizations shown in queue
- **WHEN** an order with customizations is displayed in the order queue
- **THEN** the customization names SHALL be visible in the order details

#### Scenario: Order without customizations shows no extras
- **WHEN** an order with no customizations is displayed in the order queue
- **THEN** no customization detail SHALL be shown
