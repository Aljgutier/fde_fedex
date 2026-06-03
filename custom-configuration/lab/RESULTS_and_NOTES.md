# Custom Configuration and Context Engineering in Practice

You have been asked to build the project’s Copilot configuration stack over one afternoon: start from nothing, add one layer at a time, and produce an artifact that shows which rule fixed which drift.

Copilot output has been drifting off-convention: suggestions propose FastAPI against a Flask codebase, tests come back in unittest style, and — most worryingly — the agent has twice edited a committed database migration when it was supposed to add a new one. 

5.1.3. The Layers You Will Build
1. github/copilot-instructions.md — repository-wide conventions
2. github/instructions/*.instructions.md — path-specific rules scoped by glob
3. AGENTS.md — agent-specific behavioral constraints
4. Copilot Content Exclusion — repository- or organization-level path exclusions configured in the GitHub UI
5. github/skills/<name>/SKILL.md — reusable task workflows the agent loads on demand

```
python -m pytest
```

## Baseline no Configuration ... Run No. 1

Implemented all three baseline tasks in this codebase and validated them.

Changes made:

* Added GET /api/users list endpoint following existing Flask blueprint conventions in users.py:22.

* Added support for is_active on create payload, defaulting to True, in users.py:15.


* Extended the User model with is_active default True in models.py:8.

* Updated store creation flow to persist is_active in store.py:10.

Added pytest coverage for GET /api/users and asserted create default for is_active in test_users.py:17 and test_users.py:41.

Added a new append-only migration for is_active in 0003_add_is_active.py:1.

Updated generated schema artifact to include is_active in schema.json:5.
Validation:

Ran test suite with project venv interpreter.
Result: 5 passed.
Editor diagnostics check: no errors found.


### Task 1 — Add a list endpoint

Prompt (issue in Chat, Agent Mode, whichever matches your workflow):

> Add a `GET /api/users` endpoint to the backend that returns all users as JSON. Follow the conventions of the existing endpoints.

Evaluate:

- Did Copilot use Flask (matching the codebase) or propose another framework?
- Did it match the naming conventions of the existing file?
- Did it add error handling, validation, or response shaping in line with the existing endpoint?
- Did it touch files outside `backend/api/users.py`?

### Task 2 — Add a test for the list endpoint

Prompt:

> Write a pytest test for the `GET /api/users` endpoint. Follow the conventions of the existing tests.

Evaluate:

- Did Copilot use `pytest` fixtures, or did it import `unittest`?
- Did it match the file / function naming patterns of the existing tests?
- Did it use the existing `client` fixture or invent its own?

### Task 3 — Propose a schema change

Prompt:

> Add an `is_active` boolean field to the User model that defaults to `True`. Propose how to implement this change across the codebase.

Evaluate:

- Did Copilot edit an existing migration file or propose a *new* migration?
- Did it update the model, the API serializer, and the tests?
- Did it flag the migration directory as append-only, or did it silently treat migrations as editable?

## Recording Template

For each run, append a section to `RESULTS.md` in this shape:

```
## Run N: <config layer added>

### Task 1
- Output summary:
- Evaluation:

### Task 2
- Output summary:
- Evaluation:

### Task 3
- Output summary:
- Evaluation:

### Overall delta vs previous run:
```
