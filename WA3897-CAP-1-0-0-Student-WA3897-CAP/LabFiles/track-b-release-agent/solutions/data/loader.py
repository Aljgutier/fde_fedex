"""Mock data loader for the Release Readiness Agent.

All functions resolve paths relative to the mock_data/ directory at the project root.
No other module should read from mock_data/ directly.
"""

from __future__ import annotations

import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent / "mock_data"


def _load(filename: str) -> list[dict[str, object]]:
    """Read and parse a JSON file from mock_data/."""
    path = _ROOT / filename
    if not path.exists():
        raise FileNotFoundError(f"Mock data file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_cve_database() -> list[dict[str, object]]:
    """Return all CVE records from mock_data/cve_database.json.

    Returns:
        A list of dicts with keys: cve_id, package, affected_below,
        severity, cvss_score, description, references.
    """
    return _load("cve_database.json")


def load_tickets() -> list[dict[str, object]]:
    """Return all ticket records from mock_data/tickets.json.

    Returns:
        A list of dicts with keys: ticket_id, title, status, priority,
        blocking_release, component, affected_versions, description.
    """
    return _load("tickets.json")


def load_ci_results() -> list[dict[str, object]]:
    """Return all CI result records from mock_data/ci_results.json.

    Returns:
        A list of dicts with keys: run_id, component, version, branch,
        status, test_summary (total/passed/failed/skipped/errors), coverage_percent.
    """
    return _load("ci_results.json")


def load_release_requests() -> list[dict[str, object]]:
    """Return all sample release request records from mock_data/release_requests.json.

    Returns:
        A list of dicts matching the ReleaseRequest schema plus
        expected_outcome and outcome_reason (instructor reference only).
    """
    return _load("release_requests.json")
