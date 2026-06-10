## ADDED Requirements

### Requirement: Size-specific drink recipes
Each menu item SHALL have a recipe for each of its available sizes. A recipe maps ingredient identifiers to quantities consumed to produce that drink at that size. Recipes SHALL be defined within `menu.json` as a `recipe` field nested under each size.

#### Scenario: Latte recipe varies by size
- **WHEN** the menu is loaded
- **THEN** the Neural Network Latte has a recipe for small, medium, and large, each specifying espresso shots and milk ounces

#### Scenario: Large drinks use more espresso
- **WHEN** a large-size recipe is defined for a standard espresso drink
- **THEN** it typically specifies 2 espresso shots, while small and medium specify 1 (except where the drink's identity requires otherwise, e.g. a doppio)

#### Scenario: Mocha recipes include chocolate
- **WHEN** the Machine Learning Mocha recipe is defined
- **THEN** each size includes espresso, chocolate, and milk quantities

### Requirement: All menu items have complete recipes
Every drink/size combination present in the menu SHALL have a corresponding recipe. The system SHALL NOT allow a menu item to be served without a recipe.

#### Scenario: Menu item missing recipe
- **WHEN** a menu item size entry lacks a `recipe` field
- **THEN** the system raises an error at startup identifying the incomplete item

#### Scenario: Recipe references valid ingredients
- **WHEN** a recipe references an ingredient identifier
- **THEN** that identifier SHALL correspond to an ingredient defined in `ingredients.json`

### Requirement: Recipe ingredient quantities are positive
All ingredient quantities in a recipe SHALL be positive numbers.

#### Scenario: Zero or negative quantity
- **WHEN** a recipe specifies an ingredient quantity that is zero or negative
- **THEN** the system raises an error at startup identifying the invalid recipe entry
