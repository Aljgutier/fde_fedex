# Release Readiness and Dependency Risk Agent — Track B

## Scenario

You are joining the FedEx Shipping Platform team mid-sprint. The team runs a
release pipeline that has been in production for several months. Until now, the
deploy gate (in `pipeline/deploy.py`) only checks CI pass/fail. Two recurring
post-release incidents prompted leadership to expand the gate:

1. A deployment shipped with a HIGH-severity CVE in a transitive dependency that
   was caught only after a security scan ran post-deploy.
2. A major version bump landed in production with breaking API changes that were
   never documented in the changelog — downstream teams were not notified.

Your task: integrate a **release readiness agent** into the existing pipeline. The
agent scans dependencies for known vulnerabilities, checks for open blocking
tickets, and validates changelog coherence. It produces a structured recommendation
— **release**, **hold**, or **escalate** — with written rationale that a release
manager can act on before the deploy gate runs.

The agent's output is advisory. The deploy gate and the human release manager
remain the final decision-makers. The agent must be reliable, explainable, and
consistent.

## Acceptance Criteria

- [ ] The agent accepts a `ReleaseRequest` as input and returns a `ReleaseRecommendation`
- [ ] The recommendation is always one of `release`, `hold`, or `escalate`
- [ ] Every recommendation includes a non-empty `rationale` referencing which check(s) drove the decision
- [ ] The agent performs all four checks: dependency CVE scan, blocking ticket query, changelog coherence, CI gate
- [ ] Tool errors are caught and reflected in the output — the agent does not silently fail
- [ ] All three decision types are reachable using the provided sample requests in `mock_data/release_requests.json`
- [ ] The functional pipeline modules (runner, deploy, changelog_reader) continue to pass their tests
- [ ] A pytest test suite passes covering at minimum: release, hold (CI fail), hold (blocking ticket), and escalate (CRITICAL CVE)
- [ ] `openspec verify` passes across the complete spec suite
- [ ] `docs/rapid-peer-review.md` exists and all findings are addressed
- [ ] `docs/go-no-go-checklist.md` is completed with a written decision rationale

## Project Structure

```
release-agent/
├── agent.py              # Pydantic AI agent definition (you build this)
├── models.py             # ReleaseRequest and ReleaseRecommendation models (you build this)
├── tools/                # Agent tool functions (you build this)
├── data/
│   └── loader.py         # Mock data loader (you build this)
├── tests/                # Test suite (you build this)
├── pipeline/             # Brownfield pipeline — read carefully before modifying
│   ├── __init__.py
│   ├── runner.py         # Functional — pipeline orchestrator
│   ├── deploy.py         # Functional — deploy gate (CI pass/fail check)
│   ├── changelog_reader.py   # Functional — CHANGELOG.md parser
│   ├── dependency_scanner.py # STUB — implement this as an agent tool
│   └── ticket_client.py      # STUB — implement this as an agent tool
├── mock_data/            # Reference data — do not modify
│   ├── cve_database.json
│   ├── tickets.json
│   ├── ci_results.json
│   ├── release_requests.json
│   ├── requirements_shipping_api.txt
│   ├── requirements_label_service.txt
│   ├── requirements_notification_service.txt
│   └── CHANGELOG.md
├── openspec/             # Spec-driven development artifacts (you populate this)
│   └── pipeline-architecture.md   # Pre-authored spec of existing pipeline
├── docs/                 # RAPID compliance documents (templates provided)
│   ├── rapid-peer-review.md
│   └── go-no-go-checklist.md
└── .github/
    └── skills/
        └── rapid-peer-review.md  # RAPID peer review Agent Skill
```

## Getting Started

See the lab guide for step-by-step instructions. Complete environment setup before Session 1.

### Quick start

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Verify the existing pipeline runs
python -m pipeline.runner

# Run tests
pytest tests/ -v
```

## Data Reference

The `mock_data/` directory contains:
- **12 CVEs** across common Python packages (HIGH and CRITICAL severity entries present)
- **15 tickets** across 6 components, with blocking and non-blocking variants
- **8 CI run records** across 3 components, including passing and failing builds
- **9 sample release requests** designed to produce all three decision outcomes
- **3 component requirements files** with intentional vulnerability variation
- **1 CHANGELOG.md** with a major-version coherence gap in the v3.0.0 entry

Review `release_requests.json` carefully during Session 1 — the `expected_outcome`
and `outcome_reason` fields explain what each sample request is designed to test.

## Decision Rules

The agent must implement these rules consistently (see `copilot-instructions.md`
for the full decision table):

| Signal | Decision |
|--------|----------|
| CRITICAL CVE | escalate |
| HIGH CVE + blocking ticket | escalate |
| Major version, no breaking-change docs | escalate |
| HIGH CVE only | hold |
| Blocking ticket only | hold |
| CI test failures | hold |
| All checks pass | release |
