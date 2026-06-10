## Context

BeanBotics currently supports size selection, customization surcharges, and lifecycle-driven order status updates. Pricing authority already lives on the backend for persisted order totals, while frontend cards display dynamic estimated totals for user feedback.

This change introduces two connected experiences:
1. A pre-submit review step that prevents accidental order submissions and shows a final line-item summary before creating the order.
2. A completed-order receipt view that explains how the final amount was derived, including base price, customization surcharges, subtotal, tax, and tax-inclusive total.

Constraints:
- No database; order data remains in-memory.
- Existing endpoints should be preserved where possible.
- Existing customization surcharge constants and semantics must remain consistent with current specs.
- Tax is required for receipt totals, but tax configuration UI is out of scope.
- Tax for this change is fixed at 8.25% (0.0825) and must be applied to subtotal only.

## Goals / Non-Goals

**Goals:**
- Add an explicit review/confirm UX step between selection and POST /api/orders.
- Ensure confirmation and receipt both use the same line-item pricing model.
- Persist receipt-ready pricing breakdown with orders so completed orders can be rendered without recomputation drift.
- Display receipts only when order status is completed.

**Non-Goals:**
- Printing, emailing, or exporting receipts.
- Receipt history/index pages beyond current order list grouping.
- Runtime tax configuration UI or per-order custom tax overrides.
- Introducing authentication, payments, or database persistence.

## Decisions

1. Decision: Add backend-generated receipt breakdown fields to order payloads.
- Rationale: Backend is authoritative for pricing and already computes totals. Returning a structured breakdown avoids frontend duplication and prevents mismatches.
- Alternatives considered:
  - Frontend-only computation from base/customization inputs: rejected due to risk of drift and duplicated business logic.
  - Separate receipt endpoint: rejected to avoid extra API complexity for in-memory single-page flow.

2. Decision: Represent receipt line items as explicit structured fields (base line + customization lines + subtotal + tax + total_with_tax).
- Rationale: Structured data is easier to test and render than parsing formatted strings.
- Alternatives considered:
  - Single human-readable receipt text blob: rejected as brittle and not reusable for UI updates.
  - Only return final taxed total: rejected because requirement needs itemized breakdown.

3. Decision: Use a fixed server-side tax constant of 8.25% for this change.
- Rationale: Scope requires tax-inclusive total but excludes tax configuration UI; a constant keeps behavior deterministic and testable.
- Calculation: `subtotal = base_price + sum(selected_customization_surcharges)`; `tax_amount = round(subtotal * 0.0825, 2)`; `total_with_tax = round(subtotal + tax_amount, 2)`.
- Accuracy rule: tax MUST be computed from subtotal (not from any rounded total_with_tax back-calculation), and subtotal MUST remain the pre-tax amount.
- Alternatives considered:
  - Zero tax placeholder: rejected because requirement explicitly needs total including tax.
  - Environment-driven tax config: deferred for a future change to avoid configuration overhead.

4. Decision: Implement confirmation as an in-page state transition (card -> review -> confirm/back), not a multi-page route.
- Rationale: Current frontend is a single static page with vanilla JS; stateful panel/modal flow fits architecture and minimizes disruption.
- Alternatives considered:
  - Separate HTML page: rejected due to extra navigation/state complexity.
  - Immediate submit with lightweight browser confirm(): rejected because it cannot present required line-item detail cleanly.

5. Decision: Show receipt UI only for orders in completed status within the existing Completed group.
- Rationale: Aligns with order-status lifecycle and current grouped order board.
- Alternatives considered:
  - Show provisional receipts for active orders: rejected because ask explicitly targets completed orders.

## Risks / Trade-offs

- [Risk] Frontend state complexity increases due to per-card review mode and back navigation.
  - Mitigation: Keep isolated per-item state object and reset review state after confirm/cancel/back.

- [Risk] Rounding inconsistencies between subtotal, tax, and total could cause visible mismatches.
  - Mitigation: Compute monetary values server-side in one function and round to two decimals at each externally visible value.

- [Risk] Extending order response shape may impact existing UI/tests expecting older fields.
  - Mitigation: Add backward-compatible fields (do not remove existing total/customization fields) and update tests accordingly.

- [Risk] Tax constant assumption may become incorrect for future requirements.
  - Mitigation: Encapsulate tax constant and calculation helper so future tax-config change can swap implementation with minimal API churn.

## Migration Plan

1. Add backend receipt breakdown model fields and calculation helper while preserving existing order payload fields.
2. Update order creation/list responses to include receipt data for all orders.
3. Implement frontend review step wired to selected drink/size/customizations before submission.
4. Implement completed-order receipt rendering using backend receipt data.
5. Update/add tests for pricing breakdown, tax totals, review flow, and completed receipt display.
6. Rollback strategy: disable new frontend review/receipt rendering and ignore new payload fields while retaining old order creation flow.

## Open Questions

- Should subtotal in receipt equal pre-tax total exactly as currently persisted total, or should existing total field be redefined as tax-inclusive?
- Should completed order cards show receipt collapsed by default with a toggle, or always expanded?
