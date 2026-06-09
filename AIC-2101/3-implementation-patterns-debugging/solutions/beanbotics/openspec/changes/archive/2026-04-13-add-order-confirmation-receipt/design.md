## Context

BeanBotics currently sends orders to the backend immediately when the customer clicks the Order button. There is no review step. Completed orders show in the order queue with a status badge but no price breakdown — the customer sees a single total with no visibility into how it was calculated.

The proposal calls for two new UI flows: a pre-submission confirmation overlay and a post-completion receipt view. Both require itemized pricing data that the backend does not currently return.

## Goals / Non-Goals

**Goals:**
- Let customers review their order (drink, size, customizations, total) before submitting
- Show a line-item receipt for completed orders with base price, customizations, subtotal, tax, and total
- Return itemized pricing from the backend so the frontend doesn't recalculate prices

**Non-Goals:**
- Print or email receipts
- Receipt history or persistence across server restarts
- Tax configuration UI (rate is fixed at 8.5%)
- Changes to the order status lifecycle or state machine

## Decisions

### 1. Confirmation as a modal overlay, not a separate page

The confirmation step will be a modal overlay that appears on top of the menu. The customer can confirm to submit or dismiss to go back and edit.

**Why not a separate page/route?** The app is a single-page design with no router. A modal keeps the architecture consistent and lets the customer see the menu context behind the overlay. It also avoids introducing client-side routing for a single interaction.

### 2. Backend computes and returns itemized pricing

Order responses will include a pricing breakdown (base price, customization line items, subtotal, tax, total) so the frontend can render receipts without recalculating.

**Why not compute on the frontend?** The frontend already has the prices in memory, but duplicating price logic across frontend and backend creates drift risk. The backend already calculates totals — extending it to return the breakdown is straightforward.

### 3. Tax applied only at receipt display, not stored on the order model

Tax (8.5%) is a display concern for receipts. The existing `total_price` field on the Order model continues to represent the pre-tax subtotal. The backend will compute and include tax in the itemized response.

**Why not add tax to the stored total?** Changing what `total_price` means would be a breaking change to every existing consumer. Keeping it as the subtotal and adding tax as a separate field in the response is additive and non-breaking.

### 4. Receipt as an expandable section on completed orders, not a modal

Completed orders will have a "View Receipt" toggle that expands an inline receipt panel below the order. This keeps receipts glanceable without covering the rest of the UI.

**Why not a modal?** The confirmation step already uses a modal. Using a different pattern for receipts avoids stacking modals and lets the customer view multiple receipts simultaneously. An inline expand/collapse is simpler and fits the order list layout.

### 5. Confirmation overlay gets pricing data from the frontend state

The confirmation overlay displays pricing computed from the currently selected size and customizations — the same data the dynamic price display already shows. No API call is needed for the confirmation step; the order is only submitted when the customer confirms.

**Why not hit an API for a price quote?** There is no server-side state to validate until the order is placed. The frontend already has accurate prices from the menu and customizations APIs. Adding a quote endpoint would add latency and complexity with no benefit.

## Risks / Trade-offs

- **Tax rate is hardcoded** → Acceptable for current scope. If tax configuration is needed later, extract the rate to a config constant. The 8.5% value lives in one place in the backend.
- **In-memory orders lose receipts on restart** → Same limitation as all order data today. Out of scope per proposal.
- **Confirmation adds a click to every order** → Intentional trade-off: fewer mistakes at the cost of one extra interaction. The overlay is lightweight and fast to dismiss.
