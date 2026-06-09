## Why

Customers have no way to personalize their drinks. Every order is the base drink at the selected size — there are no add-ons like an extra shot, milk alternatives, or whipped cream. Adding optional extras increases order value and makes the ordering experience more realistic.

## What Changes

- Define a set of customization options (extra shot, milk alternatives, whipped cream) with fixed add-on prices
- Add a customizations section to each menu card with checkbox toggles
- Update the displayed order price dynamically as customizations are toggled
- **BREAKING**: Extend `POST /api/orders` to accept an optional `customizations` list
- Store customizations on the Order model and include them in API responses
- Add customization surcharges to the order total price calculation
- Display customizations alongside each order in the order queue and status board

## Capabilities

### New Capabilities

- `drink-customizations`: Backend support for customization options — data model, price calculation, and API contract for submitting and displaying customizations with orders
- `drink-customizations-ui`: Frontend customization picker on menu cards, dynamic price updates, and customization display in the order queue

### Modified Capabilities

*(none — existing specs are not changing at the requirement level)*

## Impact

- **Backend**: `models.py` (new `customizations` field on Order), `services/orders.py` (price calculation with add-ons, display name includes extras), `app.py` (extend `OrderRequest` to accept customizations)
- **Frontend**: `script.js` (customization checkboxes, price recalculation, order display), `style.css` (customization picker and order detail styling)
- **API**: `POST /api/orders` request body gains an optional `customizations` array; response includes customizations. All other endpoints unchanged.
- **Data**: Customization options and prices can be hardcoded (not in `menu.json`) since they apply universally to all drinks
