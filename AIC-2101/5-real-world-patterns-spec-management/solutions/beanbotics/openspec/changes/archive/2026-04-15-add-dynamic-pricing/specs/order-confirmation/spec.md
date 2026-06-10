# Delta Spec: Order Confirmation — Dynamic Pricing

## MODIFIED

### Requirement: Confirmation overlay shows order summary

**Previous:** The confirmation overlay SHALL display a complete summary of the pending order: drink name and selected size, each selected customization with its individual price, and order total (base price + customization surcharges).

**Updated:** The confirmation overlay SHALL display the order total using the active pricing tier's base price. During off-peak hours, the base price reflects the 20% discount. Customization surcharges remain at full price. No additional discount indicators or strikethrough treatment is needed — the customer has already seen the pricing context on the menu.

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
