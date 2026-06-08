## 1. Backend Data Model

- [x] 1.1 Add `CUSTOMIZATIONS` dict to `backend/models.py` mapping option IDs to `{"name": str, "price": float}` for: `extra-shot`, `oat-milk`, `almond-milk`, `soy-milk`, `whipped-cream`
- [x] 1.2 Add `customizations: List[str]` field to the `Order` dataclass (default: empty list)

## 2. Backend Service Layer

- [x] 2.1 Update `OrderService.place_order()` to accept a `customizations` parameter, validate IDs against `CUSTOMIZATIONS`, sum surcharges into `total_price`, and append customization names to the display name
- [x] 2.2 Return `None` (or raise) when an invalid customization ID is provided

## 3. Backend API Layer

- [x] 3.1 Extend `OrderRequest` Pydantic model with `customizations: List[str] = []`
- [x] 3.2 Pass `request.customizations` through to `order_service.place_order()` in the POST route
- [x] 3.3 Add `GET /api/customizations` endpoint returning all options with `id`, `name`, and `price`

## 4. Frontend Customization Picker

- [x] 4.1 Fetch customization options from `GET /api/customizations` on page load and store them
- [x] 4.2 Render a checkbox group for customizations on each menu card (option name + surcharge price)
- [x] 4.3 Add CSS styling for the customization checkboxes (`.customization-option` class) consistent with the existing dark theme

## 5. Frontend Dynamic Price Update

- [x] 5.1 Create a shared `updatePrice(itemId)` function that calculates base size price + sum of checked customization surcharges and updates the order button price display
- [x] 5.2 Wire `updatePrice()` to fire on both size radio changes and customization checkbox changes

## 6. Frontend Order Submission

- [x] 6.1 Update `placeOrder()` to collect checked customization IDs and include them in the POST request body
- [x] 6.2 Reset customization checkboxes on the ordered card after successful order placement and revert the displayed price to base

## 7. Frontend Order Queue Display

- [x] 7.1 Update `renderOrder()` to display customizations from the order data (customization names are already embedded in `items` display string from the backend)
