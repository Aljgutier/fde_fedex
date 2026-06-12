"""Unit tests for the ticket client implementation."""

from __future__ import annotations

import pytest

from pipeline.ticket_client import get_blocking_tickets, get_open_tickets


# ---------------------------------------------------------------------------
# get_blocking_tickets
# ---------------------------------------------------------------------------

def test_shipping_api_241_blocked_by_ship1042() -> None:
    """SHIP-1042 blocks shipping-api 2.4.1."""
    tickets = get_blocking_tickets("shipping-api", "2.4.1")
    ids = [t["ticket_id"] for t in tickets]
    assert "SHIP-1042" in ids, f"Expected SHIP-1042 in {ids}"


def test_notification_service_123_no_blockers() -> None:
    """notification-service 1.2.3 has no blocking tickets."""
    tickets = get_blocking_tickets("notification-service", "1.2.3")
    assert tickets == []


def test_label_service_300_blocked_by_label203() -> None:
    """LABEL-203 blocks label-service 3.0.x."""
    tickets = get_blocking_tickets("label-service", "3.0.0")
    ids = [t["ticket_id"] for t in tickets]
    assert "LABEL-203" in ids


def test_component_match_is_case_insensitive() -> None:
    """Component name matching should be case-insensitive."""
    lower = get_blocking_tickets("shipping-api", "2.4.1")
    upper = get_blocking_tickets("Shipping-API", "2.4.1")
    assert [t["ticket_id"] for t in lower] == [t["ticket_id"] for t in upper]


@pytest.mark.parametrize("version,pattern,should_match", [
    ("2.4.1", "2.4.x", True),
    ("2.4.0", "2.4.x", True),
    ("2.5.0", "2.4.x", False),
    ("3.0.0", "3.0.0", True),
    ("3.0.1", "3.0.0", False),
])
def test_version_pattern_matching(
    version: str, pattern: str, should_match: bool
) -> None:
    """Wildcard and exact version patterns must match correctly."""
    from pipeline.ticket_client import _version_matches_pattern  # type: ignore[attr-defined]
    assert _version_matches_pattern(version, pattern) is should_match


def test_missing_tickets_file_raises() -> None:
    """FileNotFoundError raised when the tickets file does not exist."""
    with pytest.raises(FileNotFoundError):
        get_blocking_tickets("shipping-api", "2.4.1", tickets_path="nonexistent.json")


# ---------------------------------------------------------------------------
# get_open_tickets
# ---------------------------------------------------------------------------

def test_get_open_tickets_label_service() -> None:
    """label-service has multiple open tickets."""
    tickets = get_open_tickets("label-service")
    assert len(tickets) >= 1
    assert all(t["status"] == "open" for t in tickets)
    assert all(
        t["component"].lower() == "label-service" for t in tickets
    )


def test_get_open_tickets_unknown_component_returns_empty() -> None:
    """An unknown component name returns an empty list."""
    tickets = get_open_tickets("nonexistent-service")
    assert tickets == []
