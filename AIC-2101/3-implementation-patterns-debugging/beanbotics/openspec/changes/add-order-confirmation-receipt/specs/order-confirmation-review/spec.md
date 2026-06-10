## ADDED Requirements

### Requirement: Review step appears before order submission
The system SHALL present a Review Your Order step after the customer selects drink size and customizations and before `POST /api/orders` is sent.

#### Scenario: Review step opens from menu card
- **WHEN** the customer clicks order on a configured menu card
- **THEN** the UI SHALL show a Review Your Order summary for that selection
- **AND** no order SHALL be created until the customer confirms

### Requirement: Review summary includes itemized pre-tax pricing
The Review Your Order step SHALL show the selected drink name and size, base price line item, each selected customization as a separate line item with surcharge,sand a pre-tax total.

### Requirement: Tax calculation
Tax MUST be calculated at a rate of 8.5%, applied to the order
subtotal (base price plus all customizations). The tax amount
MUST be rounded to the nearest cent using standard rounding
(half-up). Tax MUST appear as a separate line item on the receipt.

#### Scenario: Review summary shows selected customizations only
- **WHEN** the customer selects large Transformer Flat White with extra shot and oat milk
- **THEN** the review summary SHALL show base line for large size price
- **AND** line items for Extra shot (+$0.75) and Oat milk (+$0.60)
- **AND** no line item for unselected whipped cream
- **AND** the pre-tax total SHALL equal base plus selected surcharges

### Requirement: Customer can confirm or return to edit
The review step SHALL provide both Confirm and Back actions.

#### Scenario: Confirm submits reviewed order
- **WHEN** the customer clicks Confirm in Review Your Order
- **THEN** the system SHALL send `POST /api/orders` using the reviewed size and customizations
- **AND** the created order SHALL use backend-authoritative pricing

#### Scenario: Back returns without creating order
- **WHEN** the customer clicks Back in Review Your Order
- **THEN** the system SHALL return to the same menu card with prior selections preserved
- **AND** no order SHALL be created



