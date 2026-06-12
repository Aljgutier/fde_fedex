"""Ticket client — implemented solution for pipeline/ticket_client.py."""

from __future__ import annotations

import json
from pathlib import Path


def _version_matches_pattern(version: str, pattern: str) -> bool:
    """Return True if ``version`` matches a version pattern.

    Matching rules:
    - Exact: "3.0.0" matches only "3.0.0"
    - Minor wildcard: "2.4.x" matches "2.4.0", "2.4.1", "2.4.99"
    - Major wildcard: "3.x" matches "3.0.0", "3.1.2", "3.99.0"
    """
    if pattern == version:
        return True
    if pattern.endswith(".x"):
        prefix = pattern[:-1]  # e.g. "2.4." or "3."
        return version.startswith(prefix)
    return False


def get_blocking_tickets(
    component: str,
    version: str,
    tickets_path: str = "mock_data/tickets.json",
) -> list[dict[str, object]]:
    """Return all open tickets that are marked as blocking for a component release.

    Args:
        component: Component name to filter on (case-insensitive).
        version: Release version being evaluated (e.g. "2.4.1").
        tickets_path: Path to the JSON tickets file.

    Returns:
        List of matching blocking ticket dicts. Empty list if none found.

    Raises:
        FileNotFoundError: If the tickets file does not exist.
    """
    path = Path(tickets_path)
    if not path.exists():
        raise FileNotFoundError(f"Tickets file not found: {path}")

    tickets: list[dict[str, object]] = json.loads(
        path.read_text(encoding="utf-8")
    )

    results = []
    for ticket in tickets:
        if ticket.get("status") != "open":
            continue
        if not ticket.get("blocking_release", False):
            continue
        if str(ticket.get("component", "")).lower() != component.lower():
            continue
        affected: list[str] = ticket.get("affected_versions", [])  # type: ignore[assignment]
        if any(_version_matches_pattern(version, p) for p in affected):
            results.append(ticket)

    return results


def get_open_tickets(
    component: str,
    tickets_path: str = "mock_data/tickets.json",
) -> list[dict[str, object]]:
    """Return all open tickets for a component, regardless of blocking status.

    Args:
        component: Component name to filter on (case-insensitive).
        tickets_path: Path to the JSON tickets file.

    Returns:
        List of open ticket dicts for the component. Empty list if none found.

    Raises:
        FileNotFoundError: If the tickets file does not exist.
    """
    path = Path(tickets_path)
    if not path.exists():
        raise FileNotFoundError(f"Tickets file not found: {path}")

    tickets: list[dict[str, object]] = json.loads(
        path.read_text(encoding="utf-8")
    )

    return [
        t for t in tickets
        if t.get("status") == "open"
        and str(t.get("component", "")).lower() == component.lower()
    ]
