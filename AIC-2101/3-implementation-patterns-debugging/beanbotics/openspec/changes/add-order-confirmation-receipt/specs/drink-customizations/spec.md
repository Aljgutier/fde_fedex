## MODIFIED Requirements

### Requirement: Dynamic total includes selected customizations
The displayed order total on each menu card SHALL include the selected size price plus surcharges for selected customizations: extra shot +$0.75, milk alternative +$0.60 when not `none`, whipped cream +$0.50. The same surcharge values SHALL be used in the Review Your Order line items and in completed-order receipt customization line items.

#### Scenario: Single customization updates total
- **WHEN** the customer enables extra espresso shot on a medium drink priced $5.50
- **THEN** the order button total SHALL update to $6.25
- **AND** the review summary customization line item SHALL show Extra shot at +$0.75

#### Scenario: Multiple customizations update total
- **WHEN** the customer selects milk alternative `oat` and whipped cream on a large drink priced $6.50
- **THEN** the order button total SHALL update to $7.60
- **AND** the review summary SHALL show line items for Oat milk (+$0.60) and Whipped cream (+$0.50)

### Requirement: Order records persist customizations and total
The backend SHALL persist selected customizations and computed final total in each order record returned by order APIs. For completed orders, the backend SHALL also persist and return receipt line-item data that includes base price details, selected customization line items with surcharge amounts, subtotal, tax amount, and total including tax.

#### Scenario: API returns persisted customizations
- **WHEN** an order is created with milk alternative `almond`
- **THEN** subsequent `GET /api/orders` responses SHALL include the same customization values for that order

#### Scenario: Backend computes authoritative total
- **WHEN** an order is submitted with selected extras
- **THEN** the backend SHALL compute final total from base size price plus fixed surcharges before storing and returning the order

#### Scenario: Completed order includes receipt line items
- **WHEN** an order with selected extras reaches `completed`
- **THEN** `GET /api/orders` SHALL return receipt data with base price line item, selected customization line items, subtotal, tax amount, and total including tax
