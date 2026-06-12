"""Unit tests for the agent tool wrappers in tools/release_tools.py.

These tests exercise the four tool functions directly against mock data —
no Anthropic API key is required. Each function wraps a pipeline module;
tests verify the wrapper's output contract rather than the pipeline internals
(which are covered by test_dependency_scanner.py and test_ticket_client.py).
"""

from __future__ import annotations

import pytest

from tools.release_tools import (
    check_changelog_coherence,
    evaluate_ci_gate,
    get_release_blocking_tickets,
    scan_release_dependencies,
)


# ---------------------------------------------------------------------------
# scan_release_dependencies
# ---------------------------------------------------------------------------

def test_scan_critical_cve_shipping_api() -> None:
    """shipping-api requirements contain cryptography 41.0.5 → CRITICAL CVE."""
    result = scan_release_dependencies("mock_data/requirements_shipping_api.txt")
    assert result["highest_severity"] == "CRITICAL"
    assert result["hit_count"] >= 1
    cve_ids = [h.get("cve_id") for h in result["cve_hits"]]
    assert "CVE-2024-5678" in cve_ids
    assert "error" not in result


def test_scan_high_cve_label_service() -> None:
    """label-service requirements contain requests 2.30.0 → HIGH CVE."""
    result = scan_release_dependencies("mock_data/requirements_label_service.txt")
    assert result["highest_severity"] in ("HIGH", "CRITICAL")
    assert result["hit_count"] >= 1
    assert "error" not in result


def test_scan_clean_notification_service() -> None:
    """notification-service requirements have no CVE matches → NONE."""
    result = scan_release_dependencies("mock_data/requirements_notification_service.txt")
    assert result["highest_severity"] == "NONE"
    assert result["hit_count"] == 0
    assert result["cve_hits"] == []
    assert "error" not in result


def test_scan_missing_file_returns_error() -> None:
    """A nonexistent requirements file returns an error key, not an exception."""
    result = scan_release_dependencies("mock_data/does_not_exist.txt")
    assert "error" in result
    assert result["hit_count"] == 0
    assert result["highest_severity"] == "NONE"


def test_scan_result_contains_required_keys() -> None:
    """Every result must contain cve_hits, hit_count, and highest_severity."""
    result = scan_release_dependencies("mock_data/requirements_notification_service.txt")
    for key in ("cve_hits", "hit_count", "highest_severity"):
        assert key in result, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# get_release_blocking_tickets
# ---------------------------------------------------------------------------

def test_blocking_ticket_tracking_service() -> None:
    """tracking-service 5.2.1 has TRACK-088 as a blocking ticket."""
    result = get_release_blocking_tickets("tracking-service", "5.2.1")
    assert result["blocking_count"] >= 1
    ticket_ids = [t.get("ticket_id") for t in result["blocking_tickets"]]
    assert "TRACK-088" in ticket_ids
    assert "error" not in result


def test_no_blocking_tickets_notification_service() -> None:
    """notification-service 1.2.3 has no blocking tickets."""
    result = get_release_blocking_tickets("notification-service", "1.2.3")
    assert result["blocking_count"] == 0
    assert result["blocking_tickets"] == []
    assert "error" not in result


def test_unknown_component_returns_empty_not_error() -> None:
    """A component with no tickets at all returns zero blocking tickets."""
    result = get_release_blocking_tickets("unknown-service", "9.9.9")
    assert result["blocking_count"] == 0
    assert "error" not in result


def test_blocking_tickets_result_contains_required_keys() -> None:
    """Every result must contain blocking_tickets and blocking_count."""
    result = get_release_blocking_tickets("notification-service", "1.2.3")
    assert "blocking_tickets" in result
    assert "blocking_count" in result


# ---------------------------------------------------------------------------
# check_changelog_coherence
# ---------------------------------------------------------------------------

def test_major_version_gap_detected_v3() -> None:
    """v3.0.0 has a major-version coherence gap in CHANGELOG.md → gap_detected=True."""
    result = check_changelog_coherence("3.0.0")
    assert result["version_found"] is True
    assert result["gap_detected"] is True
    assert result["gap_details"] is not None
    assert "error" not in result


def test_no_gap_patch_version() -> None:
    """v2.4.1 is a regular patch release with no major-version gap."""
    result = check_changelog_coherence("2.4.1")
    assert result["version_found"] is True
    assert result["gap_detected"] is False
    assert result["gap_details"] is None
    assert "error" not in result


def test_version_not_in_changelog() -> None:
    """A version not present in CHANGELOG.md returns version_found=False."""
    result = check_changelog_coherence("99.0.0")
    assert result["version_found"] is False
    assert result["gap_detected"] is False


def test_changelog_result_contains_required_keys() -> None:
    """Every result must contain version_found, gap_detected, and gap_details."""
    result = check_changelog_coherence("1.2.3")
    for key in ("version_found", "gap_detected", "gap_details"):
        assert key in result, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# evaluate_ci_gate
# ---------------------------------------------------------------------------

def test_ci_gate_approves_passing_run() -> None:
    """CI-2024-001 is a passing run → approved=True."""
    result = evaluate_ci_gate("CI-2024-001")
    assert result["approved"] is True
    assert result["ci_run_id"] == "CI-2024-001"
    assert result["reason"]
    assert "error" not in result


def test_ci_gate_rejects_failing_run() -> None:
    """CI-2024-005 has 13 test failures → approved=False."""
    result = evaluate_ci_gate("CI-2024-005")
    assert result["approved"] is False
    assert result["ci_run_id"] == "CI-2024-005"
    assert result["reason"]
    assert "error" not in result


def test_ci_gate_unknown_run_id_returns_error() -> None:
    """An unrecognised CI run ID returns an error key and approved=False."""
    result = evaluate_ci_gate("CI-9999-999")
    assert "error" in result
    assert result["approved"] is False
    assert result["ci_run_id"] == "CI-9999-999"


def test_ci_gate_result_contains_required_keys() -> None:
    """Every result must contain approved, reason, and ci_run_id."""
    result = evaluate_ci_gate("CI-2024-001")
    for key in ("approved", "reason", "ci_run_id"):
        assert key in result, f"Missing key: {key}"
