## Requirements

### Requirement: Pricing tier definitions
The system MUST define two pricing tiers:
- Peak: 7:00am-9:00am and 11:30am-1:30pm — full menu prices
- Off-peak: all other hours — 20% discount on base drink prices

Customization surcharges (extra shot, milk alternatives, whipped cream) MUST NOT be discounted. Only the base drink price is affected. Discounted prices SHALL be rounded to 2 decimal places (half-up).

### Requirement: GET /api/menu returns both peak and off-peak prices
The `GET /api/menu` response SHALL include both the base price and the off-peak price for each size of every menu item. The base price is the full (peak) price from menu.json. The off-peak price is the base price with the 20% discount applied (base x 0.80). The frontend uses these to render the appropriate display based on the active toggle state.

#### Scenario: Menu response includes both price points
- **WHEN** `GET /api/menu` is called
- **THEN** each size object SHALL include `price` (the base/peak price) and `off_peak_price` (the discounted price)
- **AND** for a Neural Network Latte large: `price` is 6.50 and `off_peak_price` is 5.20

### Requirement: Time simulation toggle
The UI MUST include a toggle switch with two states: "Peak" and "Off-Peak". The toggle MUST default to "Peak" on page load. The system MUST use the toggle's value to determine the active pricing tier. The menu and pricing MUST update immediately when the toggle value changes.
