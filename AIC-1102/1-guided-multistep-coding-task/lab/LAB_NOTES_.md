Supervision level is checkpoint supervision. This grants the coding agent plenty of autonomy and chances to evolve the code without interference. However the code can be reviewed at each checkpoint. 


Key Functional Requirements

You will want to review all the bullet line item features at each checkpoint



# Revised Plan

## Reviesed Plan Prompt

```
We need to revise the plan

Change the validation: instead of returning 400 for an invalid status, reject with 422 and include the list of valid statuses in the
error body Apply this to both POST and PUT.

Make sure to update all routes according to this requirement, not just the ones in your previous plan.

Make sure tu update all corrresponding tests

Please list all routes that what will change.

Please list all tests that will be updated

Please list any conflicts that you may run into

Do not code, just show me the updated plan. 
```

Checklist

Does it update only the already-written endpoints, or does it carry the
new rule into the remaining ones?
Does it mention the conflict with the original plan, or silently override
it?
Does it update the tests you already approved?


## Revised Plan
Plan update only, no code changes.

Updated Scope

Change invalid status handling from 400 to 422 for both create and update flows.
Return an error body that includes the allowed statuses list when status is invalid.
Keep all other validation behavior unchanged unless it conflicts with this new rule.
Update tests to reflect new status-specific behavior.
Shared Helpers To Adjust

In app.py, split validation outcomes into:
Generic validation errors that still return 400.
Status validation errors that return 422 with allowed statuses in body.
Standardize a status-error payload shape (proposed):
error: message string
valid_statuses: array with pending, in_progress, done
Keep the allowed statuses as a single shared constant used by both POST and PUT.
File-by-File Plan

app.py

Update the validation helper contract so it can distinguish:
invalid title or missing required fields -> 400
invalid status -> 422 + valid_statuses list
Update POST /tasks to use the new status-specific response.
Update PUT /tasks/<task_id> to use the new status-specific response.
Confirm non-status validation paths still return 400.
Confirm not-found behavior remains 404 where required.
Confirm list/filter behavior remains unchanged unless explicitly status-validation related.
test_app.py

Update status-validation tests for POST to expect 422 and valid_statuses in body.
Update status-validation tests for PUT to expect 422 and valid_statuses in body.
Keep title-related validation tests expecting 400.
Keep not-found tests expecting 404.
Keep status filter tests for GET /tasks?status=... unchanged unless any shared error-shape assertion is reused.
storage.py

No functional change expected for this requirement.
Confirm no store-level status validation was introduced that conflicts with route-level HTTP semantics.
All Routes Reviewed and Change Impact

POST /tasks

Will change.
Invalid status: 422 + valid_statuses in response body.
Other invalid input: remains 400.
PUT /tasks/<task_id>

Will change.
Invalid status: 422 + valid_statuses in response body.
Other invalid input: remains 400.
Missing task: remains 404.
GET /tasks

No change expected.
Status query filter behavior should remain: unknown status returns 200 with empty list.
GET /tasks/<task_id>

No change expected.
Still 200 when found, 404 when missing.
DELETE /tasks/<task_id>

No change expected.
Still 204 when deleted, 404 when missing.
Tests To Update

Based on current test names in test_app.py, these will be updated:

test_create_task_with_invalid_status
test_update_task_invalid_status
Potentially updated if they assert full shared error format or shared helper behavior:

Any helper-coupled validation assertion tests that currently assume status errors are plain error-only JSON
Any parametrized validation tests, if introduced, that combine status and title cases
Tests expected to remain unchanged:

Title validation tests (missing, empty, wrong type) expecting 400
Not-found tests for GET, PUT, DELETE expecting 404
Status filter tests for GET list endpoint expecting 200 and filtered/empty arrays
Conflicts / Risks To Resolve Before Coding

Spec conflict with original brief:

Original said invalid input returns 400 globally.
New requirement introduces 422 for invalid status specifically.
Resolution: treat invalid status as a special case and keep 400 for other validation failures.
Error body shape ambiguity:

New request says include valid statuses, but does not prescribe exact keys.
Proposed stable shape: error plus valid_statuses.
Needs confirmation only if strict contract already exists elsewhere.
Behavior consistency risk:

Shared validator used by both POST and PUT may accidentally change unrelated responses.
Mitigation in plan: explicitly separate status error path from generic validation path.
Ordering of valid statuses in tests:

If using a set internally, output order can be non-deterministic.
Plan should enforce deterministic order in response to keep tests stable.
GPT-5.3-Codex • 2.3 credits

# Plan 1 

## Plan 1 Prompt

```
#file:FEATURE_BRIEF.md 
Read FEATURE_BRIEF.md. Produce a step-by-step implementation
plan for the feature. Do not make any code changes yet. Group steps
by file and call out any shared helpers you intend to add.
```


## Plan 1

No code changes were made. I reviewed the brief and current implementation, and this is the implementation plan grouped by file.

Shared Helpers To Add

Add a single source of truth for allowed statuses:
pending, in_progress, done
Add request validation helper(s) used by both create and update flows:
Validate title rules:
Required and non-empty string on create
Optional on update, but if provided must be non-empty string
Validate status rules:
Optional on both create and update
If provided, must be in allowed statuses
Add a small error response helper to standardize JSON errors:
Shape: { "error": "<message>" }
Used for 400 and 404 responses
Planned location: app.py, unless you prefer a separate module.

Plan By File

1. storage.py

Extend TaskStore with read/update/delete operations:
get(task_id) returning task or None
update(task_id, fields) returning updated task or None
delete(task_id) returning True or False
Extend list_all to support optional filtering:
list_all(status=None)
If status is provided, return only matching tasks
Unknown status naturally returns empty list
Keep in-memory behavior unchanged otherwise.
2. app.py

Add validation and error helper functions near route definitions.
Update POST /tasks:
Parse JSON safely
Validate payload with shared validator
Return 400 with error JSON on invalid input
On success, create task and return 201
Update GET /tasks:
Read optional status query parameter
Call store.list_all with status filter when present
Return filtered or full list with 200
Add GET /tasks/<task_id>:
Return task with 200 when found
Return 404 with { "error": "task not found" } when missing
Add PUT /tasks/<task_id>:
Return 404 if task does not exist
Parse and validate update payload
Apply partial updates only for provided fields
Return updated task with 200
Add DELETE /tasks/<task_id>:
Delete and return 204 with empty body if found
Return 404 with task not found error if missing
3. test_app.py

Keep existing baseline tests.
Add tests for GET /tasks/<id>:
Success path
Not found path (404 + correct error body)
Add tests for PUT /tasks/<id>:
Update title only
Update status only
Update both fields
Not found path
Invalid title path(s)
Invalid status path
Add tests for DELETE /tasks/<id>:
Success path (204 and task removed)
Not found path
Add tests for GET /tasks with status filter:
Returns only matching status
Returns all tasks when query omitted
Unknown status returns empty list with 200
Add tests for POST validation:
Missing title
Empty title
Non-string title
Invalid status
Ensure fixture reset remains reliable between tests (including ID behavior if needed for deterministic assertions).
Execution Order

Implement store capabilities in storage.py.
Implement route and validation logic in app.py.
Add and run tests in test_app.py.
Run full test suite and adjust messages/assertions for exact expected API behavior.



Below are the goals and Features 

## Goal

Extend the existing Task Manager API with the missing CRUD operations, a status filter on the list endpoint, and input validation. Add tests covering the new behavior.

## Functional Requirements

### 1. Retrieve a single task

- Route: `GET /tasks/<task_id>`
- Returns the task as JSON with status `200` when it exists.
- Returns status `404` with a JSON body `{"error": "task not found"}` when it does not.

### 2. Update a task

- Route: `PUT /tasks/<task_id>`
- Accepts a JSON body that may contain `title` and/or `status`.
- Updates only the fields provided. Omitted fields stay the same.
- Returns the updated task as JSON with status `200`.
- Returns status `404` when the task does not exist.
- Returns status `400` for invalid input (see Validation below).

### 3. Delete a task

- Route: `DELETE /tasks/<task_id>`
- Returns status `204` with no body when the task is deleted.
- Returns status `404` when the task does not exist.

### 4. Filter the list by status

- Route: `GET /tasks?status=<status>`
- When the `status` query parameter is present, return only tasks with that status.
- When omitted, return all tasks (existing behavior).
- An unknown status value returns an empty list with status `200`.

## Validation Rules

- `title` is required on `POST /tasks` and must be a non-empty string.
- `status` must be one of: `pending`, `in_progress`, `done`.
- Invalid input returns status `400` with a JSON body `{"error": "<message>"}`.
- These rules apply to both `POST /tasks` and `PUT /tasks/<task_id>`.

## Test Coverage

Add tests in `tests/test_app.py` that cover each new endpoint, the status filter, and both the success and failure paths for validation and not-found cases.

## Out of Scope

- Persistence to disk or a database. The in-memory store is sufficient.
- Authentication or authorization.
- Pagination or sorting on the list endpoint.