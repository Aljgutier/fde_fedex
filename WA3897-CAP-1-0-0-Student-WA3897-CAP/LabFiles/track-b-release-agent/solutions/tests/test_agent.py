"""Integration tests for the Release Readiness Agent.

Requires a valid ANTHROPIC_API_KEY in .env (or environment).
"""

from __future__ import annotations

import pytest

from agent import agent
from models import ReleaseRecommendation, ReleaseRequest


def _req(**kwargs) -> ReleaseRequest:
    return ReleaseRequest(**kwargs)


# ---------------------------------------------------------------------------
# Core four required test cases
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_release_rel001() -> None:
    """REL-001: notification-service 1.2.3, clean requirements, CI passes → release."""
    req = _req(
        request_id="REL-001",
        component="notification-service",
        version="1.2.3",
        requirements_file="mock_data/requirements_notification_service.txt",
        changelog_version="1.2.3",
        ci_run_id="CI-2024-001",
        requested_by="r.chen@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "release", f"Expected release, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()
    assert rec.request_id == "REL-001"


@pytest.mark.asyncio
async def test_hold_ci_failures_rel003() -> None:
    """REL-003: notification-service 1.1.0, CI-2024-005 has 13 test failures → hold."""
    req = _req(
        request_id="REL-003",
        component="notification-service",
        version="1.1.0",
        requirements_file="mock_data/requirements_notification_service.txt",
        changelog_version="1.1.0",
        ci_run_id="CI-2024-005",
        requested_by="r.chen@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "hold", f"Expected hold, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()


@pytest.mark.asyncio
async def test_hold_blocking_ticket_rel004() -> None:
    """REL-004: tracking-service 5.2.1, TRACK-088 blocking → hold."""
    req = _req(
        request_id="REL-004",
        component="tracking-service",
        version="5.2.1",
        requirements_file="mock_data/requirements_notification_service.txt",
        changelog_version="2.4.1",
        ci_run_id="CI-2024-001",
        requested_by="s.kim@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "hold", f"Expected hold, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()


@pytest.mark.asyncio
async def test_escalate_critical_cve_rel006() -> None:
    """REL-006: shipping-api 2.4.1, cryptography CRITICAL CVE → escalate."""
    req = _req(
        request_id="REL-006",
        component="shipping-api",
        version="2.4.1",
        requirements_file="mock_data/requirements_shipping_api.txt",
        changelog_version="2.4.1",
        ci_run_id="CI-2024-004",
        requested_by="t.walsh@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "escalate", f"Expected escalate, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()
    # Rationale should mention the CVE or severity
    assert any(
        kw in rec.rationale for kw in ["CVE-2024-5678", "CRITICAL", "cryptography"]
    ), f"Rationale should reference the critical CVE: {rec.rationale}"


# ---------------------------------------------------------------------------
# Additional coverage
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_escalate_changelog_gap_rel009() -> None:
    """REL-009: notification-service 3.0.0, changelog major-version gap → escalate."""
    req = _req(
        request_id="REL-009",
        component="notification-service",
        version="3.0.0",
        requirements_file="mock_data/requirements_notification_service.txt",
        changelog_version="3.0.0",
        ci_run_id="CI-2024-007",
        requested_by="l.garcia@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "escalate", f"Expected escalate, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()


@pytest.mark.asyncio
async def test_release_rel002() -> None:
    """REL-002: notification-service 1.3.0, clean requirements, CI passes → release."""
    req = _req(
        request_id="REL-002",
        component="notification-service",
        version="1.3.0",
        requirements_file="mock_data/requirements_notification_service.txt",
        changelog_version="1.3.0",
        ci_run_id="CI-2024-002",
        requested_by="l.garcia@fedex.com",
        target_environment="production",
    )
    result = await agent.run(str(req))
    rec: ReleaseRecommendation = result.data
    assert rec.decision == "release", f"Expected release, got {rec.decision}: {rec.rationale}"
    assert rec.rationale.strip()
