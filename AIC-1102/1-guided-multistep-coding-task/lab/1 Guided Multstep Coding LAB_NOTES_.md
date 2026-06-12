Supervision level is checkpoint supervision. This grants the coding agent plenty of autonomy and chances to evolve the code without interference. However the code can be reviewed at each checkpoint. 

# Setup directory structure
```text
guided-multi-step-coding-task/
├── app.py              # Flask routes (partial)
├── storage.py          # In-memory task store (partial)
├── requirements.txt
├── tests/
│   └── test_app.py     # Starter tests
├── FEATURE_BRIEF.md    # The feature you will implement
└── README.md
```

* create venv with uv
* install packages pip install
* pytest

# Plan, approve and execute
* Read Feature Brief 
   * Extend the existing Task Manager API with the missing CRUD operations, a status filter on the list endpoint, and input validation. Add tests covering the new behavior.... instead of returning 400 for an invalid status,

* plan ... mode ... Add FeatureBrief.md to the context
prompt
```text
Read FEATURE_BRIEF.md. Produce a step-by-step implementation plan
for the feature. Do not make any code changes yet. Group steps by
file and call out any shared helpers you intend to add.
```
* Review the plan against the brief
    * Does this step correspond to a requirement in FEATURE_BRIEF.md?
    * Does it touch any files outside app.py, storage.py, or tests/?
    * Does it add dependencies, frameworks, or abstractions the brief did not request?

* Refine if needed... you can tell copilot to refine
* make sure there are tests
* Approve the plan and execute ... agent mode
Once the plan matches the brief, tell Copilot to proceed. Keep the plan visible as your reference during execution.
* run pytest


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
