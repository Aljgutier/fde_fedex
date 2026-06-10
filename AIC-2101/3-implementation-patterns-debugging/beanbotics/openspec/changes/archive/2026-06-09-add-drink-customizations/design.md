## Context

BeanBotics currently supports size selection and order status tracking, but orders do not capture add-on choices. Pricing logic for the order button is presently driven by selected size only, and order rendering in the queue/status board focuses on size, drink name, and status controls. Because orders are in-memory and API-driven, customization support must remain lightweight, deterministic, and synchronized between frontend calculation and backend validation.

Stakeholders are customers (who need transparent totals while selecting options) and operators (who need customization visibility while preparing drinks).

## Goals / Non-Goals

**Goals:**
- Add optional extras to every drink order: extra espresso shot, milk alternative, and whipped cream.
- Reflect selected extras in menu card pricing before submission.
- Persist customization selections and computed totals with each order.
- Display selected customizations in order queue and status-oriented order displays.
- Keep implementation consistent with existing FastAPI + vanilla JS architecture.

**Non-Goals:**
- Per-drink customization eligibility rules.
- Inventory or availability tracking for customization options.
- Saved or recurring customer preference profiles.
- Tax, discounts, or broader pricing-engine changes beyond fixed add-on amounts.

## Decisions

1. Represent customizations as a structured object in the order payload and model.
- Decision: Extend order create input and stored order structure with:
  - `customizations.extra_shot: bool`
  - `customizations.milk_alternative: "none" | "oat" | "almond" | "soy"`
  - `customizations.whipped_cream: bool`
- Rationale: A typed object avoids fragile string parsing, keeps API explicit, and supports future extensions.
- Alternatives considered:
  - Free-form array of strings: simpler at first but harder to validate and evolve.
  - Flattened top-level fields: workable but less cohesive than a nested customization group.

2. Compute total on backend as source of truth; mirror same formula on frontend for live UX.
- Decision: Frontend computes dynamic button total for immediate feedback, while backend recalculates final total from base size price plus fixed surcharges.
- Rationale: Prevents mismatches or tampering and preserves responsive UI.
- Alternatives considered:
  - Frontend-only total: rejected due to trust and consistency risk.
  - Backend-only total with no live preview: rejected due to poor UX.

3. Keep customization price constants centralized in backend and frontend modules.
- Decision: Define explicit constants for add-on prices in each layer (`0.75`, `0.60`, `0.50`) and use them in calculation helpers.
- Rationale: Reduces magic numbers and makes updates localized.
- Alternatives considered:
  - Embed in menu JSON: adds schema complexity for globally fixed options.
  - Hardcode inline at call sites: increases drift risk.

4. Render customization summary as compact chips/text rows in order cards.
- Decision: Show only selected options; omit unselected defaults except milk alternative when chosen.
- Rationale: Keeps cards scannable while surfacing preparation-critical details.
- Alternatives considered:
  - Always show full option list with true/false states: too noisy.
  - Tooltip-only details: lower visibility for operators.

5. Backward-compatible request handling for missing customization object.
- Decision: Treat omitted `customizations` as all defaults (no extra shot, no milk alt, no whipped cream).
- Rationale: Prevents immediate breakage of older clients and supports incremental rollout.
- Alternatives considered:
  - Require new fields immediately: simpler validation but breaking for old clients.

## Risks / Trade-offs

- [Pricing mismatch between frontend preview and backend stored total] -> Mitigation: Implement shared formula semantics with explicit constants and add tests for representative combinations.
- [UI complexity on menu cards] -> Mitigation: Use compact control layout and scoped styles to avoid clutter.
- [Data shape drift across API, model, and rendering] -> Mitigation: Add validation defaults in backend and small serialization helpers in frontend.
- [Operators miss customization details if styling is subtle] -> Mitigation: Use clear labels/chips with contrast and consistent card placement.

## Migration Plan

- Deploy backend and frontend changes together in one release cycle.
- Preserve backward compatibility by defaulting missing customization input values on the backend.
- Verify smoke flow:
  - Place orders with zero, one, and multiple customizations.
  - Confirm queue/status board display includes selected extras.
  - Confirm order totals align with expected surcharge math.
- Rollback strategy:
  - Revert frontend customization controls and display logic.
  - Revert backend payload/model extensions while preserving existing size-based ordering behavior.

## Open Questions

- Should milk alternative selection be mutually exclusive with an explicit "none" UI state (default), or represented by unselected radio options plus implicit none? (Design assumes explicit none/default value.)
- Should customization labels in the queue/status board be abbreviated (for compactness) or fully human-readable? (Design favors readable labels.)
