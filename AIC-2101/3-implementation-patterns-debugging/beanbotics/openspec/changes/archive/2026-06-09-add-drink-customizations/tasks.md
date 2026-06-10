## 1. Backend order model and API updates

- [x] 1.1 Extend order request handling in `backend/app.py` to accept optional `customizations` with defaults for missing fields.
- [x] 1.2 Update `backend/models.py` to represent customization fields and include computed total in order serialization.
- [x] 1.3 Update `backend/services/orders.py` to validate customization values, compute authoritative totals, and persist customizations on created orders.
- [x] 1.4 Add or update backend tests for customization validation, default behavior, and total calculation combinations.

## 2. Frontend customization selection and dynamic totals

- [x] 2.1 Update menu card rendering in `frontend/script.js` to include controls for extra shot, milk alternative, and whipped cream on every card.
- [x] 2.2 Implement client-side pricing helpers in `frontend/script.js` so button totals update as size/customization selections change.
- [x] 2.3 Update order submission payload in `frontend/script.js` to send selected customizations with `item_id` and `size`.
- [x] 2.4 Add or refine styles in `frontend/style.css` for compact, readable customization controls across desktop and mobile layouts.

## 3. Order queue and status board customization display

- [x] 3.1 Update order rendering logic in `frontend/script.js` to show human-readable customization summaries on order cards.
- [x] 3.2 Ensure grouped status-board sections continue to render correctly while including customization summaries for active and completed orders.
- [x] 3.3 Verify no-customization orders omit customization badges/text while preserving existing order details.

## 4. Integration verification and readiness

- [x] 4.1 Run end-to-end manual checks: place orders with none, single, and multiple customizations; confirm totals and displayed details match expected values.
- [x] 4.2 Confirm backward-compatible behavior for requests omitting `customizations` defaults all extras off.
- [x] 4.3 Update any relevant docs or notes describing the new order payload and customization behavior.
