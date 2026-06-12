"""Agent tool wrappers that connect the release readiness agent to pipeline modules.

Each function is registered as a tool on the agent. The agent selects tools based
on their docstrings — keep them precise and informative.
"""

from __future__ import annotations

from data.loader import load_ci_results
from pipeline.changelog_reader import ChangelogReader
from pipeline.dependency_scanner import scan_dependencies
from pipeline.deploy import DeployGate
from pipeline.ticket_client import get_blocking_tickets

_CHANGELOG_PATH = "mock_data/CHANGELOG.md"


def scan_release_dependencies(requirements_file: str) -> dict[str, object]:
    """Scan a requirements file for known CVE vulnerabilities.

    Call this tool to check whether any packages in the release's dependency
    set have known security vulnerabilities. Returns a list of matching CVE records
    with severity and CVSS score. Use the results to determine hold or escalate.

    Args:
        requirements_file: Path to the pip requirements file for this component
            (e.g. "mock_data/requirements_shipping_api.txt").

    Returns:
        A dict with:
        - ``cve_hits`` (list): CVE records matching installed packages.
        - ``hit_count`` (int): Number of CVEs found.
        - ``highest_severity`` (str): "CRITICAL", "HIGH", "MEDIUM", "LOW", or "NONE".
        - ``error`` (str, optional): Present if scanning failed.
    """
    try:
        hits = scan_dependencies(requirements_file)
    except FileNotFoundError as exc:
        return {
            "error": str(exc),
            "cve_hits": [],
            "hit_count": 0,
            "highest_severity": "NONE",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "error": f"Unexpected error during CVE scan: {exc}",
            "cve_hits": [],
            "hit_count": 0,
            "highest_severity": "NONE",
        }

    _order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0}
    highest = "NONE"
    for h in hits:
        sev = str(h.get("severity", "NONE")).upper()
        if _order.get(sev, 0) > _order.get(highest, 0):
            highest = sev

    return {
        "cve_hits": hits,
        "hit_count": len(hits),
        "highest_severity": highest,
    }


def get_release_blocking_tickets(
    component: str, version: str
) -> dict[str, object]:
    """Query open tickets that are blocking a release for a given component and version.

    Call this tool to check whether any open defects are marked as release blockers
    for the component and version being deployed. A blocking ticket prevents release
    regardless of CVE or CI status.

    Args:
        component: The component name (e.g. "shipping-api", "label-service").
        version: The release version string (e.g. "2.4.1").

    Returns:
        A dict with:
        - ``blocking_tickets`` (list): Ticket records that are open and blocking.
        - ``blocking_count`` (int): Number of blocking tickets.
        - ``error`` (str, optional): Present if the ticket query failed.
    """
    try:
        tickets = get_blocking_tickets(component, version)
    except FileNotFoundError as exc:
        return {
            "error": str(exc),
            "blocking_tickets": [],
            "blocking_count": 0,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "error": f"Unexpected error querying tickets: {exc}",
            "blocking_tickets": [],
            "blocking_count": 0,
        }

    return {
        "blocking_tickets": tickets,
        "blocking_count": len(tickets),
    }


def check_changelog_coherence(version: str) -> dict[str, object]:
    """Check the CHANGELOG.md entry for a version and detect major-version gaps.

    Call this tool to verify that a major version bump has proper breaking-change
    documentation. A major version increment (e.g. 2.x → 3.0.0) with no
    "Breaking Changes" section in the changelog is a coherence gap that warrants
    escalation for architectural review.

    Args:
        version: The version string to look up (e.g. "3.0.0").

    Returns:
        A dict with:
        - ``version_found`` (bool): True if the version entry exists in CHANGELOG.md.
        - ``gap_detected`` (bool): True if a major-version coherence gap is found.
        - ``gap_details`` (dict | None): Description of the gap if detected.
        - ``error`` (str, optional): Present if the changelog could not be read.
    """
    try:
        reader = ChangelogReader(_CHANGELOG_PATH)
        entry = reader.find_version(version)
        gap = reader.detect_major_version_gap(version)
    except FileNotFoundError as exc:
        return {
            "error": str(exc),
            "version_found": False,
            "gap_detected": False,
            "gap_details": None,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "error": f"Unexpected error reading changelog: {exc}",
            "version_found": False,
            "gap_detected": False,
            "gap_details": None,
        }

    return {
        "version_found": entry is not None,
        "gap_detected": gap is not None,
        "gap_details": gap,
    }


def evaluate_ci_gate(ci_run_id: str) -> dict[str, object]:
    """Evaluate the CI gate for a specific run ID using the existing DeployGate.

    Call this tool to check whether the CI run for this release passed all
    quality gates (test pass rate, coverage threshold). A failed CI gate
    is a hold signal — the agent does not approve releases with failing tests.

    Note: This tool is advisory. The actual deploy gate runs independently;
    the agent must not trigger deployments.

    Args:
        ci_run_id: The CI run identifier (e.g. "CI-2024-001").

    Returns:
        A dict with:
        - ``approved`` (bool): True if the CI gate approves the build.
        - ``reason`` (str): Human-readable gate decision reason.
        - ``ci_run_id`` (str): The run that was evaluated.
        - ``error`` (str, optional): Present if the CI result could not be found.
    """
    try:
        ci_results = load_ci_results()
    except FileNotFoundError as exc:
        return {
            "error": str(exc),
            "approved": False,
            "reason": "CI results data unavailable.",
            "ci_run_id": ci_run_id,
        }

    ci_index = {r["run_id"]: r for r in ci_results}
    ci_result = ci_index.get(ci_run_id)
    if ci_result is None:
        return {
            "error": f"CI run '{ci_run_id}' not found in results database.",
            "approved": False,
            "reason": f"CI run '{ci_run_id}' does not exist.",
            "ci_run_id": ci_run_id,
        }

    gate = DeployGate().evaluate(ci_result)
    return {
        "approved": gate.approved,
        "reason": gate.reason,
        "ci_run_id": ci_run_id,
    }
