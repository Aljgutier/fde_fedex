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

## Baseline no Configuration ... Run No. 1 No Configuration

Implemented all three baseline tasks in this codebase and validated them.

Changes made:

1. Added GET /api/users list endpoint following existing Flask blueprint conventions in users.py:22.
2. Added support for is_active on create payload, defaulting to True, in users.py:15.
3.  Extended the User model with is_active default True in models.py:8.
4. Updated store creation flow to persist is_active in store.py:10.
5. dded pytest coverage for GET /api/users and asserted create default for is_active in test_users.py:17 and test_users.py:41.
6. Added a new append-only migration for is_active in 0003_add_is_active.py:1.
7. Updated generated schema artifact to include is_active in schema.json:5.

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

### Task 2 Evaluation — Add a test for the list endpoint

Prompt:

> Write a pytest test for the `GET /api/users` endpoint. Follow the conventions of the existing tests.

Evaluate:

- Did Copilot use `pytest` fixtures, or did it import `unittest`?
- Did it match the file / function naming patterns of the existing tests?
- Did it use the existing `client` fixture or invent its own?

### Task 3 Evaluation — Propose a schema change

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


### Run 1 No Config 
***Evaluatiom Task 1 Evaluation : Add a list endpoint***
Prompt:
> Write a pytest test for the `GET /api/users` endpoint. Follow the conventions of the existing tests.
* Implemented a new GET endpoint at /api/users in users.py:22.
* Endpoint returns all users as JSON by calling store.list_all() and serializing each user with asdict.
* Kept routing and response style consistent with existing endpoints in users.py.

Evaluate:

- Did Copilot use `pytest` fixtures, or did it import `unittest`? ... used pytest
- Did it match the file / function naming patterns of the existing tests? ... used proper naming conventions
- Did it use the existing `client` fixture or invent its own? ... used client

***Run 1 No Config Task 2 Evaluation : Add a test for the list endpoint***
Prompt:
> Write a pytest test for the `GET /api/users` endpoint. Follow the conventions of the existing tests.
* Added a pytest test named **test_list_users_returns_all_users** using the existing * client fixture in test_users.py:41.
* Test creates two users, calls GET /api/users, and asserts 200 plus expected returned usernames.
* Also added a small assertion in the create test to verify the new default is_active behavior in test_users.py:17.

Evaluate:

- Did Copilot use `pytest` fixtures, or did it import `unittest`? ... pytest
- Did it match the file / function naming patterns of the existing tests? yes file function naming conventions
- Did it use the existing `client` fixture or invent its own? used client 

***Run 1 No Config Task 3 Evaluation: Propose and implement is_active schema change***
Prompt:
> Add an `is_active` boolean field to the User model that defaults to `True`. Propose how to implement this change across the codebase.

* Updated the User model to include is_active: bool = True in models.py:8.
Updated store creation to accept/persist is_active with default True in store.py:10.
* Updated create API to accept optional is_active and default to True in users.py:15.
* Added a new append-only migration (did not edit old migrations) in 0003_add_is_active.py:1.
* Updated schema artifact to include is_active in schema.json:5.
Validation

Evaluate
- Did Copilot use `pytest` fixtures, or did it import `unittest`? ... used pytest
- Did it match the file / function naming patterns of the existing tests? .. yes file function 
- Did it use the existing `client` fixture or invent its own? ... client


***Run 1 No Config Pytests***


Ran pytest: 5 passed.


## Run No. 2 Repository Wide Conventions
* copilot-instructions.md
* this would typically be at the top level directory  of the project
* A rule like "Flask, not FastAPI" belongs here because it is universal; 


## Path Specific Rules
* A rule that makes sense inside backend/ is distracting inside tests/ and probably wrong inside frontend/

* For example .instructions.md
```sh
---
applyTo: "backend/**/*.py"
---

# Backend Instructions
...

```

* Use Copilot Chat on a backend file and a test file separately. Ask something that should trigger each instruction file. Confirm that the backend rules do not fire in test files and vice versa.
* Run the baseline tasks again. Append ## Run 3: after path-specific instructions to RESULTS.md.

## 5.3.4 Agent Behavioral Guidance

AGENTS.md is the layer that most often gets miscategorized. It is not where you put style preferences or naming conventions — those belong in copilot-instructions.md. AGENTS.md is for constraints on what the agent is allowed to do autonomously: which directories are off-limits, which actions require confirmation, which pre-action checks are mandatory. 

The distinction matters because Chat reads copilot-instructions.md and Agents read both — a rule in the wrong file fires at the wrong time.

The test for whether a rule belongs here: does this rule prevent harm from something the agent could do without a human noticing? If yes, it belongs in AGENTS.md. 