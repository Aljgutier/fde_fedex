# User Stories — Release Readiness Agent

These user stories define the scope of the capstone implementation.
Reference the applicable story ID in every commit message using the format:

```
[US-XXX] Short description of change
```

Example: `[US-001] Implement scan_dependencies with CVSS score return`

---

| ID | Role | Need | Acceptance Signal |
|----|------|------|-------------------|
| US-001 | Release Manager | Scan the component's requirements file for packages matching known CVEs before a release is approved | `scan_dependencies` returns CVE ID, severity, CVSS score, and affected package for every match; CRITICAL severity drives an escalate decision |
| US-002 | Release Manager | Identify open release-blocking tickets for the component and version before proceeding | `get_blocking_tickets` filters by component (case-insensitive), applies version-pattern matching (`2.4.x`), and returns only tickets with `blocking: true` |
| US-003 | Release Manager | Detect major version bumps that lack breaking-change documentation in the changelog | `check_changelog_coherence` returns `gap_detected: true` when a major version entry has no "Breaking Changes" section; rationale names the version |
| US-004 | Release Manager | Evaluate CI run results before a release recommendation is issued | `evaluate_ci_gate` wraps `DeployGate.evaluate()` and returns `approved`, `denial_reason`, and counts for test failures and skipped tests |
| US-005 | Release Manager | Receive a structured recommendation — release, hold, or escalate — with written rationale naming specific findings | `ReleaseRecommendation.rationale` references CVE IDs, ticket IDs, CI run IDs, and changelog versions; `decision` is always one of the three allowed values |

---

## Story-to-Session Mapping

| Session | Primary Stories |
|---------|----------------|
| Session 1 | All (analysis phase — all stories are scoped in the integration spec) |
| Session 2 | US-005 (models, agent shell, data loader) |
| Session 3 | US-001 (dependency scanner), US-002 (ticket client), US-003 (changelog), US-004 (CI gate) |
| Session 4 | US-005 (test coverage and peer review) |
| Session 5 | US-005 (Go/No-Go, final verify, showcase) |

---

*These stories map to the acceptance criteria in `README.md`.*
*A single commit may reference multiple story IDs if the change spans more than one:*
*`[US-001][US-005] Return CVE severity in escalate rationale`*
