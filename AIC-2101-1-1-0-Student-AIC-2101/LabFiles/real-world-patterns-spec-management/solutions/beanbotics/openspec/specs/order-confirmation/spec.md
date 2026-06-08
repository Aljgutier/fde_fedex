## ADDED Requirements

### Requirement: Confirmation overlay appears before order submission

When the customer clicks the Order button on a menu card, the system SHALL display a confirmation overlay instead of immediately submitting the order. The overlay SHALL appear on top of the current page with a dimmed backdrop.

#### Scenario: Clicking Order opens confirmation overlay
- **WHEN** the customer clicks the Order button on a menu card
- **THEN** a modal overlay SHALL appear with the title "Review Your Order"
- **AND** the order SHALL NOT be submitted to the backend

#### Scenario: Overlay has dimmed backdrop
- **WHEN** the confirmation overlay is displayed
- **THEN** a semi-transparent dark backdrop SHALL cover the page behind the overlay

### Requirement: Confirmation overlay shows order summary

The confirmation overlay SHALL display the order total using the active pricing tier's base price. During off-peak hours, the base price reflects the 20% discount. Customization surcharges remain at full price. No additional discount indicators or strikethrough treatment is needed — the customer has already seen the pricing context on the menu.

If no customizations are selected, the customizations section SHALL be omitted.

#### Scenario: Order with customizations shows full breakdown
- **WHEN** the customer orders a Medium Neural Network Latte with Extra Espresso Shot and Oat Milk
- **THEN** the overlay SHALL show:
  - "Neural Network Latte — Medium" as the drink line
  - "Extra Espresso Shot" with "$0.75"
  - "Oat Milk" with "$0.60"
  - Total: "$5.60" (base $4.25 + $0.75 + $0.60)

#### Scenario: Order without customizations omits customization section
- **WHEN** the customer orders a Large Deep Learning Doppio with no customizations
- **THEN** the overlay SHALL show:
  - "Deep Learning Doppio — Large" as the drink line
  - Total matching the base large price
- **AND** no customization line items SHALL appear

#### Scenario: Confirmation overlay during peak hours
- **WHEN** the customer opens the confirmation overlay for a Medium Neural Network Latte ($5.50) with Extra Espresso Shot ($0.75) during peak hours
- **THEN** the overlay shows the total as $6.25 ($5.50 + $0.75)

#### Scenario: Confirmation overlay during off-peak hours
- **WHEN** the customer opens the confirmation overlay for a Medium Neural Network Latte ($5.50) with Extra Espresso Shot ($0.75) during off-peak hours
- **THEN** the overlay shows the total as $5.15 ($4.40 + $0.75)
- **AND** no strikethrough or discount label is displayed

#### Scenario: Toggle changes while overlay is open
- **WHEN** the confirmation overlay is open showing peak prices
- **AND** the customer toggles to off-peak
- **THEN** the overlay SHALL re-render with the off-peak discounted prices

### Requirement: Confirm button submits the order

The confirmation overlay SHALL include a "Confirm Order" button. Clicking it SHALL submit the order to the backend via `POST /api/orders` with the selected item, size, and customizations, then close the overlay.

#### Scenario: Confirming submits and closes overlay
- **WHEN** the customer clicks "Confirm Order" on the overlay
- **THEN** the system SHALL send `POST /api/orders` with the selected item_id, size, and customizations
- **AND** the overlay SHALL close
- **AND** the order list SHALL refresh to show the new order
- **AND** the menu card's customization checkboxes SHALL reset to unchecked

### Requirement: Go Back button dismisses without ordering

The confirmation overlay SHALL include a "Go Back" button. Clicking it SHALL close the overlay without submitting an order, preserving the customer's current selections on the menu card.

#### Scenario: Going back preserves selections
- **WHEN** the customer clicks "Go Back" on the confirmation overlay
- **THEN** the overlay SHALL close
- **AND** no order SHALL be submitted
- **AND** the menu card's size selection and customization checkboxes SHALL remain unchanged

### Requirement: Backdrop click dismisses overlay

Clicking the dimmed backdrop area outside the overlay content SHALL dismiss the overlay, behaving the same as clicking "Go Back."

#### Scenario: Clicking backdrop dismisses overlay
- **WHEN** the confirmation overlay is displayed
- **AND** the customer clicks the dimmed backdrop area
- **THEN** the overlay SHALL close without submitting an order
- **AND** the menu card selections SHALL remain unchanged
