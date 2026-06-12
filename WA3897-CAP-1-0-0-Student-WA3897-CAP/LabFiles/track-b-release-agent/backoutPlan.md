# Backout Plan — Release Readiness Agent

**Control**: ITC.013 — Backout Plan
**Component**: Release Readiness and Dependency Risk Agent (Track B Capstone)
**Repository**: [GitLab repository URL]
**Last Updated**: [fill in before Session 4 peer review]
**Prepared By**: [team name]

---

## 1. Stable Baseline

Fill this section in during Session 4 after the peer review is complete
and the test suite is passing.

| Field | Value |
|-------|-------|
| Last stable commit hash | [run: `git log --oneline -1`] |
| Last stable tag / version | [fill in if tagged; otherwise use commit hash] |
| Date of last stable state | |
| Verified by | |

---

## 2. Scope of This Component

The Release Readiness Agent is an advisory layer that sits alongside the existing
pipeline. Removing it restores the pipeline to its pre-integration state.
The three functional pipeline modules (`runner.py`, `deploy.py`, `changelog_reader.py`)
are not modified by this component and do not need to be reverted.

**Files added by this component (removed on rollback):**

- `agent.py`
- `models.py`
- `data/loader.py`
- `tools/release_tools.py`
- `pipeline/dependency_scanner.py` (stub implementation)
- `pipeline/ticket_client.py` (stub implementation)
- `tests/test_agent.py`
- `tests/test_dependency_scanner.py`
- `tests/test_ticket_client.py`
- `openspec/` (integration specs authored during the capstone)
- `docs/rapid-peer-review.md`
- `docs/test-results.xml`
- `docs/go-no-go-checklist.md`
- `backoutPlan.md` (this file)

**Files that are NOT reverted (pre-existing brownfield components):**

- `pipeline/runner.py`
- `pipeline/deploy.py`
- `pipeline/changelog_reader.py`
- `pipeline/__init__.py`
- `mock_data/` — reference fixtures; never modified
- `openspec/pipeline-architecture.md` — pre-authored spec; pre-existing

---

## 3. Revert Procedure

### Step 1 — Confirm a revert is needed

Before reverting, verify:

- [ ] The issue is reproducible against the current commit (run `pytest tests/ -v`)
- [ ] The three pre-existing pipeline modules still pass: `python -m pipeline.runner`
- [ ] The issue is not caused by an external factor (expired API key, network outage, Python version mismatch)
- [ ] At least one group member has reviewed the failing output

### Step 2 — Identify the target commit

```bash
git log --oneline -10
# Identify the last commit where all tests passed and pipeline.runner ran cleanly
```

### Step 3 — Revert

**Option A — Revert a specific bad commit (preferred; preserves history):**

```bash
git revert <bad-commit-hash>
# Git opens an editor for the commit message; save and close
git push origin <branch-name>
```

**Option B — Reset to a known-good commit (use only if Option A is not feasible):**

```bash
git reset --hard <known-good-commit-hash>
git push origin <branch-name> --force-with-lease
# Note: force-with-lease aborts if the remote has commits you haven't seen,
# preventing accidental data loss
```

**Option C — Remove the agent layer entirely (return to pre-integration state):**

If the agent needs to be fully removed rather than rolled back to a previous
version, delete the files listed in Section 2 and restore the stubs to their
original `NotImplementedError` state:

```bash
# Remove agent-authored files
git rm agent.py models.py
git rm -r data/ tools/
git rm tests/test_agent.py tests/test_dependency_scanner.py tests/test_ticket_client.py

# Restore stubs to their original NotImplementedError state
git checkout <pre-integration-commit-hash> -- pipeline/dependency_scanner.py
git checkout <pre-integration-commit-hash> -- pipeline/ticket_client.py

git commit -m "[US-005] Revert: remove release readiness agent layer"
git push origin <branch-name>
```

### Step 4 — Verify the revert

```bash
# Activate the virtual environment
source .venv/Scripts/activate

# Verify pre-existing pipeline still works
python -m pipeline.runner

# Run the remaining test suite and capture results
pytest tests/ -v --tb=short --junitxml=docs/test-results.xml
```

### Step 5 — Document the incident

Update this section after completing the revert:

| Field | Value |
|-------|-------|
| Date of incident | |
| Reverted from commit | |
| Reverted to commit | |
| Root cause | |
| Follow-up actions | |

---

## 4. Cross-Impact Statement

The agent is advisory and integrates with the pipeline as a read-only layer.
Removing it does not alter the behavior of the deploy gate (`pipeline/deploy.py`),
the CI runner, or any downstream deployment systems.

**Downstream consumers**: None in capstone context.
[Add here if the agent's recommendation is consumed by other systems in production.]

---

## 5. Contacts

| Role | Name | Contact |
|------|------|---------|
| Release Manager / Decision Maker | | |
| Technical Lead | | |
| Instructor / Supervisor | | |

---

*This document satisfies FedEx RAPID Framework control ITC.013 (Backout Plan).*
*Update this file before the Session 4 peer review and any time the deployment*
*or revert procedure changes.*
