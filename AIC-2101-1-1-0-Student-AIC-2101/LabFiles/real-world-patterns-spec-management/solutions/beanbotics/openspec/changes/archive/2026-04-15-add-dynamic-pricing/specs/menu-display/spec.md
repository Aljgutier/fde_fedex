# Delta Spec: Menu Display — Dynamic Pricing

## MODIFIED

### Requirement: Menu cards display size options with prices

**Previous:** Each menu card SHALL display a size selector showing all available sizes (small, medium, large) with their corresponding prices.

**Updated:** Each menu card SHALL display a size selector showing all available sizes (small, medium, large) with pricing that reflects the active pricing tier. During peak hours, prices display normally. During off-peak hours, each size option SHALL show the original price with a strikethrough and the discounted price beside it. A pricing tier indicator SHALL be visible on the menu showing whether peak or off-peak pricing is active.

#### Scenario: Menu during peak hours
- **WHEN** the active time is within a peak window (7:00am-9:00am or 11:30am-1:30pm)
- **THEN** each size option shows its base price normally with no discount indicators
- **AND** the menu displays a "Peak Pricing" indicator

#### Scenario: Menu during off-peak hours
- **WHEN** the active time is outside all peak windows
- **THEN** each size option shows the original base price with a strikethrough and the discounted price (base price minus 20%) beside it
- **AND** the menu displays an "Off-Peak Pricing — 20% Off" indicator

### Requirement: Order button reflects tier-adjusted price

**Previous:** The order button on each menu card SHALL display the currently selected size name and price.

**Updated:** The order button price SHALL reflect the active pricing tier. During off-peak hours, the button SHALL show the discounted base price plus any full-price customization surcharges.

#### Scenario: Order button during peak hours
- **WHEN** the customer selects "Large" on Neural Network Latte during peak hours with Extra Espresso Shot checked
- **THEN** the order button reads "Order — $7.25" ($6.50 + $0.75)

#### Scenario: Order button during off-peak hours
- **WHEN** the customer selects "Large" on Neural Network Latte during off-peak hours with Extra Espresso Shot checked
- **THEN** the order button reads "Order — $5.95" ($5.20 + $0.75)

#### Scenario: Prices update when time changes
- **WHEN** the customer adjusts the time simulation slider from a peak time to an off-peak time
- **THEN** the menu prices update immediately to show strikethrough and discounted prices without a page reload