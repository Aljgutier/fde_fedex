## 1. Order Form UI Updates

- [ ] 1.1 Add a size selector control to the order form markup in `frontend/index.html` with label and placeholder location for size-based price display.
- [ ] 1.2 Add scoped styling in `frontend/style.css` so the size selector and price display align with the existing form layout on desktop and mobile.

## 2. Frontend State And Rendering

- [ ] 2.1 Update order form state in `frontend/script.js` to track selected item and selected size, initializing size deterministically when item selection changes.
- [ ] 2.2 Render available size options from the selected menu item `sizes` data and keep selector options synchronized with item changes.
- [ ] 2.3 Implement price rendering logic that derives and displays the currently selected size price and updates immediately when size changes.

## 3. Order Submission Integration And Validation

- [ ] 3.1 Update order submission logic in `frontend/script.js` to include selected size in the existing `POST /api/orders` payload.
- [ ] 3.2 Add client-side guards to prevent submission when selected item/size is invalid for the current menu data.

## 4. Verification

- [ ] 4.1 Manually verify the order form flow: item selection populates sizes, size changes update displayed price, and form submits successfully.
- [ ] 4.2 Validate out-of-scope constraints are preserved: no drink customizations, no menu schema changes, no new backend endpoints, and no unrelated UI changes.
