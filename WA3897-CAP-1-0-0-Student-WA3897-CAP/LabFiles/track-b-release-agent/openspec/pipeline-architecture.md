# OpenSpec — Pipeline Architecture (Existing System)

**Status**: `stable` — describes the brownfield pipeline as delivered.
**Scope**: Documents existing, functional components only. Components marked
`[STUB]` have defined interfaces but unimplemented bodies. The release
readiness decision module is NOT described here — that is the component
students specify and implement.

---

## Module: `pipeline.changelog_reader`

### Purpose

Parses a [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) formatted
`CHANGELOG.md` file and returns structured version entries. Used by the agent
to detect coherence gaps in major version releases.

### Classes

#### `ChangelogEntry`

A dataclass representing a single versioned entry.

| Field | Type | Description |
|-------|------|-------------|
| `version` | `str` | Version string as it appears in the header, e.g. `"3.0.0"` |
| `date` | `str \| None` | ISO 8601 date string from the header, or None if absent |
| `sections` | `dict[str, list[str]]` | Maps section name (e.g. `"Added"`) to bullet items |

**Properties**:
- `has_breaking_changes: bool` — True if any section key matches the set
  `{"Breaking Changes", "Breaking", "Removed", "Incompatible"}` (case-insensitive)
- `is_major_version: bool` — True if the major version component is non-zero
- `section_items(name: str) -> list[str]` — Returns bullet items for a named section

#### `ChangelogReader`

Parses the changelog file. Instantiated with the path to `CHANGELOG.md`.

| Method | Signature | Returns |
|--------|-----------|---------|
| `read_all` | `() -> list[ChangelogEntry]` | All entries, newest-first |
| `find_version` | `(version: str) -> ChangelogEntry \| None` | Entry for exact version, or None |
| `versions` | `() -> list[str]` | All version strings in parse order |
| `detect_major_version_gap` | `(version: str) -> dict \| None` | Gap descriptor if major bump has no breaking-change docs |

**Gap descriptor keys**: `previous_version`, `current_version`, `description`

### Invariants

- Reads the file on each call to `read_all()`; no caching between calls
- Raises `FileNotFoundError` if the path does not exist at construction time
- Section headers are case-preserved; comparisons in `has_breaking_changes` are case-insensitive

---

## Module: `pipeline.deploy`

### Purpose

Provides the existing deploy gate. Evaluates a CI result record and returns an
approval decision. This gate runs AFTER the release readiness agent produces its
recommendation — it is a separate, independent check.

### Classes

#### `GateDecision`

A frozen dataclass representing the gate output.

| Field | Type | Description |
|-------|------|-------------|
| `approved` | `bool` | True if the build may proceed to deployment |
| `reason` | `str` | Human-readable explanation |
| `ci_run_id` | `str \| None` | The CI run ID that was evaluated |

#### `DeployGate`

Evaluates CI result dicts against configurable thresholds.

| Method | Signature | Returns |
|--------|-----------|---------|
| `__init__` | `(min_coverage_percent: float = 80.0)` | — |
| `evaluate` | `(ci_result: dict) -> GateDecision` | Approval decision |

**Decision rules** (checked in order):
1. CI `status` must equal `"passed"` → deny otherwise
2. `test_summary.failed` must be 0 → deny otherwise
3. `test_summary.errors` must be 0 → deny otherwise
4. `coverage_percent` must be ≥ `min_coverage_percent` → deny otherwise
5. All checks pass → approve

### Invariants

- `GateDecision` is immutable (frozen dataclass)
- `reason` is always a non-empty string
- Does not call external services or read files directly

---

## Module: `pipeline.runner`

### Purpose

Orchestrates a pipeline run. Loads CI results, looks up the relevant record by
`ci_run_id`, and passes it to `DeployGate`. Produces a `PipelineRun` summary.

### Classes

#### `PipelineRun`

A dataclass holding the run outcome.

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | `str` | The release request ID |
| `component` | `str` | The component being released |
| `version` | `str` | The version string |
| `ci_run_id` | `str \| None` | The CI run that was evaluated |
| `gate_decision` | `GateDecision` | The deploy gate output |
| `warnings` | `list[str]` | Non-fatal issues (e.g. mismatched component in CI run) |

**Properties**:
- `passed: bool` — True if `gate_decision.approved` is True
- `summary() -> str` — Multi-line human-readable summary

#### `PipelineRunner`

| Method | Signature | Returns |
|--------|-----------|---------|
| `__init__` | `(ci_results_path: str, min_coverage_percent: float)` | — |
| `run` | `(release_request: dict) -> PipelineRun` | Single run result |
| `run_all` | `(release_requests: list[dict]) -> list[PipelineRun]` | Batch results |

**CLI**: `python -m pipeline.runner` runs all requests from `mock_data/release_requests.json`.

### Invariants

- Returns a denied `GateDecision` (not an exception) when the CI result file is
  missing or the `ci_run_id` is not found
- Appends a warning (not an error) when the CI run's `component` field does not
  match the release request `component`

---

## Module: `pipeline.dependency_scanner` [STUB]

### Purpose

Scans a pip-format requirements file against the CVE database and returns
matching vulnerability records.

### Functions

#### `scan_dependencies(requirements_path, cve_db_path) -> list[dict]`

- Reads pinned packages from `requirements_path` (lines of the form `package==version`)
- Loads CVE records from `cve_db_path` (JSON array)
- Returns CVE records where the installed version is strictly below `affected_below`
- Returns an empty list if no vulnerabilities are found
- Raises `FileNotFoundError` if either file is missing
- Raises `ValueError` on unparseable requirements lines

#### `is_version_affected(installed_version, affected_below) -> bool`

- Returns True if `installed_version < affected_below` using PEP 440 version comparison
- Both arguments must be valid PEP 440 version strings

### **Implementation Status**: NOT IMPLEMENTED — raises `NotImplementedError`

---

## Module: `pipeline.ticket_client` [STUB]

### Purpose

Queries open tickets for a component and version from the mock ticket database.

### Functions

#### `get_blocking_tickets(component, version, tickets_path) -> list[dict]`

- Returns tickets where `status == "open"`, `blocking_release == True`,
  `component` matches (case-insensitive), and `version` matches `affected_versions`
- Version matching: exact string OR wildcard pattern ending in `x`
  (e.g. `"2.4.x"` matches `"2.4.0"`, `"2.4.1"`)
- Returns an empty list if no blocking tickets found
- Raises `FileNotFoundError` if the tickets file is missing

#### `get_open_tickets(component, tickets_path) -> list[dict]`

- Returns all tickets where `status == "open"` and `component` matches
- Returns an empty list if none found

### **Implementation Status**: NOT IMPLEMENTED — raises `NotImplementedError`

---

## What Is Not Described Here

The following components do not yet exist and are NOT part of this specification.
Students must specify them using OpenSpec before implementing:

- `agent.py` — the Pydantic AI release readiness agent
- `models.py` — `ReleaseRequest` and `ReleaseRecommendation` Pydantic models
- `tools/` — agent tool wrappers around the pipeline modules
- `data/loader.py` — the mock data loader

Use `openspec propose` to draft specifications for these components, then
`openspec specify` to finalize them before writing any implementation code.
