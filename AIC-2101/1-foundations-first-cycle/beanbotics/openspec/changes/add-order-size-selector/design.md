## Context

BeanBotics currently renders menu items and allows order placement via existing frontend controls and backend order APIs. The backend already supports validating `size` on order submission, but the frontend flow does not explicitly expose size selection as part of the order decision point, creating ambiguity in price and submitted order details.

Constraints for this change are to keep implementation within the existing architecture (vanilla JS frontend, existing FastAPI endpoints) and to avoid introducing drink customizations, menu schema changes, or unrelated UI redesign.

## Goals / Non-Goals

**Goals:**
- Add an explicit size selector (`small`, `medium`, `large`) to the order form flow.
- Ensure displayed price updates based on the selected size before order submission.
- Submit the selected size in the existing order payload without changing backend API contracts.
- Keep behavior consistent across desktop and mobile layouts.

**Non-Goals:**
- Adding customization options (milk, flavor, extra shots).
- Modifying menu data structure or item catalog content.
- Creating new backend endpoints or changing response schemas.
- Broader visual redesign beyond controls needed for size selection and size-based price display.

## Decisions

1. Use a `<select>` control for size selection in the existing order form UI.
- Rationale: Native select is accessible, lightweight, mobile-friendly, and aligns with current no-framework frontend.
- Alternative considered: size buttons/radio group. Rejected to avoid additional layout complexity and larger style changes out of scope.

2. Derive current price client-side from menu item `sizes` map and selected size state.
- Rationale: Menu data already includes per-size pricing; client-side derivation provides immediate feedback without extra API calls.
- Alternative considered: recomputing only on submit. Rejected because user would not see accurate price before placing order.

3. Keep backend integration unchanged and send `{ item_id, size }` using existing `POST /api/orders` contract.
- Rationale: Existing endpoint already supports size and validation; no API evolution required.
- Alternative considered: introducing a dedicated size-pricing endpoint. Rejected as unnecessary and out of scope.

4. Initialize default selection deterministically when an item is chosen.
- Rationale: Ensures there is always a valid size and price shown, preventing null/invalid submits.
- Alternative considered: requiring explicit manual selection with empty default. Rejected due to extra friction and possible validation edge cases.

## Risks / Trade-offs

- [Risk] Frontend state can become inconsistent if selected item changes but size/price UI does not refresh. → Mitigation: centralize form state update in one render/update function triggered on item and size changes.
- [Risk] Some menu items could have missing or unexpected size keys in data. → Mitigation: derive available options from actual item `sizes` keys and validate selection before submit.
- [Trade-off] Native select styling flexibility is limited compared to custom UI controls. → Mitigation: accept native behavior to keep scope minimal and accessibility strong.

## Migration Plan

- Implement and test frontend-only updates in `frontend/index.html`, `frontend/script.js`, and `frontend/style.css`.
- Validate order creation against existing backend endpoint and ensure no API contract changes.
- Rollback strategy: revert frontend changes only; backend remains untouched.

## Open Questions

- Should default size always be `medium` when available, or first available size from menu data order? For now, select first available size to avoid assumptions beyond data.
