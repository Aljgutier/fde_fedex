"""Unit tests for the dependency scanner implementation."""

from __future__ import annotations

import pytest

from pipeline.dependency_scanner import is_version_affected, scan_dependencies


# ---------------------------------------------------------------------------
# is_version_affected
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("installed,threshold,expected", [
    ("41.0.5", "41.0.6", True),    # below threshold
    ("41.0.6", "41.0.6", False),   # at threshold (not affected)
    ("41.0.7", "41.0.6", False),   # above threshold
    ("2.30.0", "2.31.0", True),    # requests CVE
    ("2.31.0", "2.31.0", False),   # patched version
    ("2.32.0", "2.31.0", False),   # newer than patch
    ("1.0.0",  "2.0.0",  True),    # major version below
    ("3.0.0",  "2.0.0",  False),   # major version above
])
def test_is_version_affected(installed: str, threshold: str, expected: bool) -> None:
    assert is_version_affected(installed, threshold) is expected


# ---------------------------------------------------------------------------
# scan_dependencies
# ---------------------------------------------------------------------------

def test_scan_shipping_api_finds_critical_cve() -> None:
    """requirements_shipping_api.txt has cryptography 41.0.5 → CVE-2024-5678 (CRITICAL)."""
    hits = scan_dependencies("mock_data/requirements_shipping_api.txt")
    cve_ids = [h["cve_id"] for h in hits]
    assert "CVE-2024-5678" in cve_ids, f"Expected CVE-2024-5678 in {cve_ids}"
    critical = [h for h in hits if h["severity"] == "CRITICAL"]
    assert len(critical) >= 1


def test_scan_label_service_finds_high_cve() -> None:
    """requirements_label_service.txt has requests 2.30.0 → CVE-2024-1234 (HIGH)."""
    hits = scan_dependencies("mock_data/requirements_label_service.txt")
    cve_ids = [h["cve_id"] for h in hits]
    assert "CVE-2024-1234" in cve_ids, f"Expected CVE-2024-1234 in {cve_ids}"


def test_scan_notification_service_is_clean() -> None:
    """requirements_notification_service.txt has all safe versions → empty list."""
    hits = scan_dependencies("mock_data/requirements_notification_service.txt")
    assert hits == [], f"Expected no CVEs for clean requirements, got: {hits}"


def test_scan_missing_file_raises() -> None:
    """FileNotFoundError raised for a non-existent requirements file."""
    with pytest.raises(FileNotFoundError):
        scan_dependencies("mock_data/requirements_nonexistent.txt")


def test_scan_returns_severity_field() -> None:
    """Every hit must contain cve_id, severity, and cvss_score."""
    hits = scan_dependencies("mock_data/requirements_shipping_api.txt")
    for hit in hits:
        assert "cve_id" in hit
        assert "severity" in hit
        assert "cvss_score" in hit
