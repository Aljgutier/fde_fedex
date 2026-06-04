# Core Issue: Add PATCH /tickets/<id>/status

Copy the content below (starting at `## Summary`) into a new GitHub issue on your fork. Assign the issue to `@copilot` to trigger the cloud agent.

---

## Summary

Allow clients to change the status of an existing ticket by sending a PATCH request to the ticket resource. This enables the typical triage workflow: a ticket starts as `open`, moves to `in_progress` when someone picks it up, and finishes as `resolved` or `closed`.

## Acceptance Criteria

- [ ] Endpoint `PATCH /tickets/<id>/status` is added to the Flask app.
- [ ] Accepts a JSON body of the form `{"status": "<value>"}`.
- [ ] On success, returns `200` with the updated ticket as JSON (same shape as `GET /tickets/<id>`).
- [ ] Returns `404` with `{"error": "ticket not found"}` if the ticket does not exist.
- [ ] Returns `400` with `{"error": "..."}` if the body is missing, the `status` field is missing, or the value is not one of `open`, `in_progress`, `resolved`, `closed`.
- [ ] Valid status transitions from any status to any other status are allowed (no workflow restrictions).
- [ ] Updating a ticket's status also updates a new `updated_at` field on the ticket with the current UTC timestamp in ISO 8601 format (same format as `created_at`).
- [ ] All existing tests continue to pass.
- [ ] At least one new test covers each acceptance criterion above.

## In Scope

- `tickets/app.py` (new route)
- `tickets/store.py` (add an `update_status` method that sets both `status` and `updated_at`)
- `tickets/models.py` (add `updated_at` field to the `Ticket` dataclass; default to the same value as `created_at` on new tickets)
- `tests/test_tickets.py` (new tests for the new endpoint)

## Out of Scope

- Do not modify existing endpoints beyond what is required to add `updated_at` to their responses.
- Do not add authentication, authorization, or rate limiting.
- Do not introduce new dependencies (no ORM, no validation libraries).
- Do not rewrite the in-memory store as a database.
- Do not change the module layout or move files.
- Do not modify existing tests except to update assertions that need to know about `updated_at`.

## Definition of Done

`pytest` passes with no warnings. The updated ticket includes a valid `updated_at` value in its JSON response. A freshly-started server accepts `PATCH /tickets/1/status` with a valid body and returns the updated ticket.
