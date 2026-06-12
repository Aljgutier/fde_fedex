# Agent Behavioral Guidelines — Release Readiness Agent Project

These instructions apply to autonomous agent sessions working in this repository.

## Scope Constraints

- Do not modify files in `mock_data/` — these are reference data fixtures, not editable configuration
- Do not modify the functional pipeline modules (`pipeline/runner.py`, `pipeline/deploy.py`,
  `pipeline/changelog_reader.py`) unless explicitly instructed — they represent the existing
  brownfield system that the agent integrates with
- Do not modify `pyproject.toml` unless explicitly instructed to add or remove a dependency
- Do not create files outside the established project structure without confirming first

## Specification Discipline

- Before implementing any new model, tool, or agent component, verify a spec exists for it in `openspec/`
- The pre-authored spec in `openspec/pipeline-architecture.md` describes the existing pipeline;
  new components must be specified separately before implementation
- If no spec exists for a new component, stop and ask before proceeding
- After implementation, run `openspec verify` and report whether the implementation matches the spec

## Code Quality Gates

- All new code must include type hints (`from __future__ import annotations` at module top)
- All new tool functions must have a docstring — the agent relies on docstrings to select tools correctly
- All implementations of stub functions must pass the examples in their docstrings
- Do not leave `# TODO` comments in submitted code — complete the implementation or raise the gap explicitly

## Pipeline Integration Rules

- The agent (agent.py) must NOT call `pipeline/deploy.py` directly — the deploy gate remains a
  separate step in the release workflow; the agent produces a recommendation only
- The agent's decision must always be one of `release`, `hold`, or `escalate`
- Tool implementations must read data through `data/loader.py`, not directly from `mock_data/`

## Testing

- Do not mark a task complete if tests are failing
- Do not delete existing tests to make a suite pass
- The functional pipeline modules (`runner.py`, `deploy.py`, `changelog_reader.py`) must continue
  to pass their tests after any changes

## RAPID DevSecOps Constraints

- Every commit message must begin with a user story ID from `user-stories.md`
  in the format `[US-XXX]`. Do not commit without one.
- When running tests before a code review or Go/No-Go, use:
  `pytest tests/ -v --tb=short --junitxml=docs/test-results.xml`
  and include `docs/test-results.xml` in the commit.
- Do not modify `backoutPlan.md` to remove steps or contacts — only append or update.
  Keep the stable baseline commit hash current after each session that ends with
  a passing test suite.
