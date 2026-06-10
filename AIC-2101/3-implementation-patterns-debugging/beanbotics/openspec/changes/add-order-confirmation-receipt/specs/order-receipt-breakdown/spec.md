## ADDED Requirements

### Requirement: Completed orders include structured receipt breakdown
Orders that reach `completed` status SHALL include receipt breakdown fields with base price line, customization line items, subtotal, tax amount, and total including tax.

#### Scenario: Completed order payload includes receipt fields
- **WHEN** an order transitions to `completed`
- **THEN** subsequent `GET /api/orders` responses SHALL include receipt data containing base line item, customization line items, subtotal, tax amount, and total including tax

### Requirement: Receipt totals use fixed server-side tax rate
The system SHALL compute receipt tax using a fixed server-side tax rate and SHALL return tax and total values rounded to two decimal places.

#### Scenario: Tax is applied to subtotal
- **WHEN** a completed order has subtotal $7.60
- **THEN** the system SHALL calculate tax from the fixed tax rate
- **AND** total including tax SHALL equal subtotal plus tax
- **AND** returned tax and total values SHALL be rounded to two decimals

### Requirement: Completed-order receipt view shows line-item breakdown
The completed-order UI SHALL render a receipt view that displays base line item, each selected customization as separate lines, subtotal, tax, and total including tax.

#### Scenario: Receipt view renders all required lines
- **WHEN** a completed order has extra shot and whipped cream selected
- **THEN** the receipt view SHALL show separate lines for base price, Extra shot, and Whipped cream
- **AND** the receipt SHALL show subtotal, tax, and total including tax
