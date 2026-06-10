## ADDED Requirements

### Requirement: Base ingredient definitions
The system SHALL maintain a set of base ingredients, each with a unique identifier, a display name, a unit of measure, and a cost per unit. Ingredients SHALL be loaded from a JSON data file (`backend/data/ingredients.json`) at application startup.

#### Scenario: Ingredient data loaded at startup
- **WHEN** the application starts
- **THEN** all ingredients defined in `ingredients.json` are available for recipe and COGS lookups

#### Scenario: Ingredient structure
- **WHEN** an ingredient is defined
- **THEN** it SHALL have fields: `id` (string), `name` (string), `unit` (string, e.g. "shot", "oz", "serving"), and `cost_per_unit` (number, dollars)

### Requirement: Customization ingredient mappings
Each customization option SHALL have an associated ingredient mapping that defines which ingredients it consumes and in what quantity. These mappings SHALL be defined in `ingredients.json` alongside the base ingredient costs.

#### Scenario: Extra shot customization has ingredient cost
- **WHEN** the "extra-shot" customization is applied to an order
- **THEN** its ingredient mapping specifies additional espresso shot(s) consumed

#### Scenario: Alternative milk customization has ingredient cost
- **WHEN** an alternative milk customization (e.g. "oat-milk") is applied
- **THEN** its ingredient mapping specifies the quantity of alternative milk ingredient consumed

#### Scenario: Whipped cream customization has ingredient cost
- **WHEN** the "whipped-cream" customization is applied
- **THEN** its ingredient mapping specifies the whipped cream servings consumed

### Requirement: Ingredient data validation
The system SHALL validate ingredient data on load. If an ingredient entry is missing required fields or has a negative cost, the system SHALL raise an error at startup.

#### Scenario: Missing cost field
- **WHEN** an ingredient entry in `ingredients.json` is missing the `cost_per_unit` field
- **THEN** the system raises a startup error identifying the invalid entry

#### Scenario: Negative cost
- **WHEN** an ingredient entry has a `cost_per_unit` less than zero
- **THEN** the system raises a startup error identifying the invalid entry
