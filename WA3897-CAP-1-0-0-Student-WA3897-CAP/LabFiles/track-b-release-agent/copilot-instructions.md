# GitHub Copilot Instructions — Release Readiness Agent (Track B)

These instructions apply to all Copilot suggestions and Agent Mode sessions
in this repository. Follow them exactly; do not invent conventions not listed here.

## Language and Runtime

- Python 3.11+ only
- Type hints are required on every function parameter and return value
- Use `from __future__ import annotations` at the top of every module

## Frameworks and Libraries

- **Agent framework**: `pydantic-ai` — use `pydantic_ai.Agent` for all agent definitions
- **Structured outputs**: Pydantic v2 models only — use `model_config = ConfigDict(...)` not class-based `Config`
- **Version comparison**: `packaging.version.Version` from the `packaging` library — never string comparison
- **Environment variables**: `python-dotenv` — load with `load_dotenv()` at module level

## Project Architecture

- `agent.py` — the Pydantic AI agent definition; tools are registered here
- `models.py` — `ReleaseRequest` and `ReleaseRecommendation` Pydantic models
- `pipeline/` — brownfield pipeline components (read before modifying)
  - `runner.py`, `deploy.py`, `changelog_reader.py` — functional; do not break these
  - `dependency_scanner.py`, `ticket_client.py` — stubs; implement these
- `data/loader.py` — all mock data access goes through this module; no direct file reads in agent or tools
- `tools/` — agent tool functions; one file per logical capability
- `tests/` — all tests go here; do not modify `mock_data/`
- `mock_data/` — reference fixtures; never modify these files

## Naming and Style

- PEP 8 style; 100-character line length limit
- Tool functions must have complete docstrings — the agent selects tools by docstring content
- One Pydantic model per concept; do not embed raw dicts in tool return values
- Use snake_case for all function and variable names
- Class names in PascalCase

## Agent Output Contract

- `ReleaseRecommendation.decision` must always be exactly one of: `release`, `hold`, `escalate`
- `ReleaseRecommendation.rationale` must be a non-empty string referencing which check(s) drove the decision
- Tool errors must be caught and reflected in the rationale — the agent must not silently fail
- The agent is advisory; it never directly calls deploy.py or triggers a deployment

## Pydantic AI — Structured Output Pattern

The agent **must** be constructed with `output_type=ReleaseRecommendation`.
This tells Pydantic AI to constrain the LLM's response to that model's schema.
Do not return raw strings or dicts from the agent — always use the typed output contract.

> **Note:** The older `result_type=` parameter is deprecated in Pydantic AI v1.x and will
> emit a warning. Always use `output_type=` in new code.

```python
from pydantic_ai import Agent
from models import ReleaseRequest, ReleaseRecommendation

agent = Agent(
    "anthropic:claude-3-5-haiku-latest",
    output_type=ReleaseRecommendation,  # structured output contract
    system_prompt="...",
)

result = agent.run_sync(user_prompt)
recommendation = result.data  # ReleaseRecommendation — never a raw string
```

Reference: <https://ai.pydantic.dev/results/#structured-results>

## Decision Rules (implement these in the system prompt and/or tool logic)

| Condition | Decision |
|-----------|----------|
| Any CVE with severity CRITICAL | escalate |
| HIGH severity CVE + blocking ticket | escalate |
| Major version bump with no breaking-change docs in changelog | escalate |
| CI failures AND CVEs present | escalate |
| HIGH severity CVE only (no blocking ticket) | hold |
| Blocking ticket only (no CVE) | hold |
| CI test failures only | hold |
| All checks pass | release |

## Data Access

- Load `mock_data/release_requests.json` through `data/loader.py`
- Do not hardcode file paths outside `data/loader.py`
- Do not make real network calls; all data comes from mock files

## RAPID DevSecOps Conventions

### ITC.014 — Requirements Traceability
Every commit message must reference the applicable user story from `user-stories.md`.

Format: `[US-XXX] Short description of change`
Example: `[US-001] Implement scan_dependencies with CVSS score return`

A commit that touches multiple stories may reference both: `[US-001][US-005] Return CVE severity in escalate rationale`

### ITC.003 — Test Execution Records
Run the test suite with results capture before every code review and Go/No-Go:

```
pytest tests/ -v --tb=short --junitxml=docs/test-results.xml
```

Commit `docs/test-results.xml` alongside the code under review. This file is the
ITC.003-compliant test execution record.

### ITC.013 — Backout Plan
`backoutPlan.md` at the repository root is a living document. Update it:
- Before the Session 4 peer review (fill in stable baseline commit hash and contacts)
- Whenever the revert procedure or pipeline integration approach changes
