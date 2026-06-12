"""
Ticket client — queries open and blocking tickets for a component and version.

This module is a STUB. The function signatures, docstrings, and return-type
contracts are defined here; the implementation is intentionally missing.

Session 2 task: implement get_blocking_tickets() and get_open_tickets() so that
the release readiness agent can use them as tools.
"""

from __future__ import annotations


def get_blocking_tickets(
    component: str,
    version: str,
    tickets_path: str = "mock_data/tickets.json",
) -> list[dict[str, object]]:
    """Return all open tickets that are marked as blocking for a component release.

    Loads ticket records from ``tickets_path`` and filters for tickets where:
    - ``status`` is ``"open"``
    - ``blocking_release`` is ``True``
    - ``component`` matches the requested component (case-insensitive)
    - The requested ``version`` matches at least one pattern in
      ``affected_versions``. Matching rules:
        - An exact version string (e.g. ``"2.4.1"``) matches only that version.
        - A wildcard pattern ending in ``x`` (e.g. ``"2.4.x"``) matches any
          version whose major.minor prefix equals the pattern prefix.
          Example: ``"2.4.x"`` matches ``"2.4.0"``, ``"2.4.1"``, ``"2.4.99"``.

    Args:
        component: The component name to filter on, e.g. ``"shipping-api"`` or
            ``"label-service"``. Comparison is case-insensitive.
        version: The release version being evaluated, e.g. ``"2.4.1"``.
        tickets_path: Path to the JSON tickets file. Defaults to the project's
            mock data location.

    Returns:
        A list of ticket record dicts. Each dict contains at minimum the keys
        ``ticket_id``, ``title``, ``status``, ``priority``,
        ``blocking_release``, ``component``, and ``affected_versions`` —
        matching the structure in ``mock_data/tickets.json``. Returns an
        empty list if no blocking tickets are found.

    Raises:
        FileNotFoundError: If ``tickets_path`` does not exist on disk.

    Examples:
        >>> tickets = get_blocking_tickets("shipping-api", "2.4.1")
        >>> any(t["ticket_id"] == "SHIP-1042" for t in tickets)
        True
        >>> tickets = get_blocking_tickets("notification-service", "1.2.3")
        >>> tickets
        []
    """
    raise NotImplementedError(
        "get_blocking_tickets() is not implemented. "
        "Complete this function during Session 2."
    )


def get_open_tickets(
    component: str,
    tickets_path: str = "mock_data/tickets.json",
) -> list[dict[str, object]]:
    """Return all open tickets for a component, regardless of blocking status.

    Loads ticket records from ``tickets_path`` and filters for tickets where:
    - ``status`` is ``"open"``
    - ``component`` matches the requested component (case-insensitive)

    Args:
        component: The component name to filter on, e.g. ``"label-service"``.
        tickets_path: Path to the JSON tickets file.

    Returns:
        A list of all open ticket record dicts for the component.
        Returns an empty list if no open tickets are found.

    Raises:
        FileNotFoundError: If ``tickets_path`` does not exist on disk.

    Examples:
        >>> tickets = get_open_tickets("label-service")
        >>> any(t["ticket_id"] == "LABEL-203" for t in tickets)
        True
        >>> blocking = [t for t in tickets if t["blocking_release"]]
        >>> len(blocking) >= 1
        True
    """
    raise NotImplementedError(
        "get_open_tickets() is not implemented. "
        "Complete this function during Session 2."
    )
