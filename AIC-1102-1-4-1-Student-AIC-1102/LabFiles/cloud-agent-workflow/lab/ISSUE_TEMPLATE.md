# Cloud Agent Issue Template

Use this shape when writing any issue you intend to assign to the Copilot cloud agent. The cloud agent reads the issue body as its primary context; sections the issue omits become sections the agent guesses.

---

## Title

One line. Imperative. Describes the outcome, not the mechanism.

- Good: `Add PATCH /tickets/<id>/status endpoint with validation`
- Poor: `Fix tickets` or `Let users change things`

## Summary

2-3 sentences stating what the change does and the user-facing outcome. No implementation details.

## Acceptance Criteria

A checklist of testable conditions. Each item should be something a reviewer can verify in the diff or by running the tests. Aim for 4-8 items.

Example:

- [ ] Endpoint `PATCH /tickets/<id>/status` exists and is reachable
- [ ] Accepts JSON body `{ "status": "<value>" }`
- [ ] Returns `200` with the updated ticket on success
- [ ] Returns `400` with `{"error": "..."}` if `status` is missing or not one of the valid values
- [ ] Returns `404` if the ticket does not exist
- [ ] At least one test per acceptance criterion above

## In Scope

Bulleted list of files or areas the change is expected to touch. Helps the agent bound its exploration.

## Out of Scope

Bulleted list of things the agent must *not* do. This is the most underused section and the one that most often saves time on review. Common items:

- Do not modify existing tests unless a test was objectively wrong.
- Do not add new dependencies.
- Do not change the response shape of existing endpoints.
- Do not add authentication or authorization.

## Definition of Done

One line stating the quality bar. For example: "`pytest` passes with no warnings, and the new endpoint is reachable from a freshly-started server."

---

## Why This Shape

The cloud agent optimizes for the issue it was given. An issue without acceptance criteria becomes code without testable outcomes. An issue without an Out of Scope section becomes a PR that touches more than you wanted. Write the issue you want the agent to close, not the issue you have time to type.
