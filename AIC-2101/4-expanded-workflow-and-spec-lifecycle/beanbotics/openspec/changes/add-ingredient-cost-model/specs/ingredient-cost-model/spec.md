## ADDED Requirements

### Requirement: Ingredient cost model defines base ingredient unit costs
The system SHALL define base ingredient unit costs for espresso ($0.40/shot), milk ($0.05/oz), chocolate ($0.08/oz), whipped cream ($0.25/serving), and alternative milk ($0.15/oz).

#### Scenario: Ingredient unit costs are available
- **WHEN** the system requests ingredient unit costs
- **THEN** it SHALL return espresso, milk, chocolate, whipped cream, and alternative milk with numeric unit costs

### Requirement: Drink recipes map each drink and size to ingredient quantities
The system SHALL define recipe ingredient quantities for each drink and size in concrete units: espresso shots, ounces of milk, ounces of chocolate, servings of whipped cream, and ounces of alternative milk. Small and medium drinks SHALL typically use 1 espresso shot, while large drinks SHALL use 2 espresso shots.

#### Scenario: Recipe quantities are available for a drink size
- **WHEN** the system requests the recipe for a specific drink and size
- **THEN** it SHALL return the ingredient quantities required for that drink and size in concrete units

### Requirement: Order COGS is computed from recipe ingredient costs
The system SHALL calculate cost of goods sold (COGS) for each order as the sum of each ingredient quantity multiplied by its unit cost, using the drink recipe quantities plus any selected customizations.

#### Scenario: Base order COGS is calculated from recipe ingredients
- **WHEN** an order is placed for a drink with a selected size
- **THEN** the system SHALL calculate COGS from the recipe ingredient quantities and unit costs

#### Scenario: Customization ingredient costs contribute to COGS
- **WHEN** an order includes customizations such as an extra shot, alternative milk, or whipped cream
- **THEN** the system SHALL add the ingredient cost of those customizations to the order COGS, not just their customer surcharge price

#### Scenario: Extra espresso shot adds cost and surcharge
- **WHEN** an order includes an extra espresso shot customization
- **THEN** the system SHALL add the cost of one espresso shot to the order COGS in addition to applying the $0.75 customer surcharge for the extra shot
