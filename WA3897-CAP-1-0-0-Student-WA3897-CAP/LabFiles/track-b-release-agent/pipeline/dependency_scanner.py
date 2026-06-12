"""
Dependency scanner — checks a requirements file against the CVE database.

This module is a STUB. The function signatures, docstrings, and return-type
contracts are defined here; the implementation is intentionally missing.

Session 2 task: implement scan_dependencies() and is_version_affected() so that
the release readiness agent can use them as tools.
"""

from __future__ import annotations


def scan_dependencies(
    requirements_path: str,
    cve_db_path: str = "mock_data/cve_database.json",
) -> list[dict[str, object]]:
    """Scan a requirements file and return all matching CVE records.

    Reads the pinned package versions from a pip-style requirements file,
    then compares each package and version against the CVE database loaded
    from ``cve_db_path``. Returns only the CVE records whose package name
    and version range match an installed package.

    Version comparison logic: a package version ``v`` is considered
    affected by a CVE record whose ``affected_below`` field is ``threshold``
    when the semantic version of ``v`` is strictly less than the semantic
    version of ``threshold``. Use the ``packaging`` library's
    ``packaging.version.Version`` class for comparison.

    Args:
        requirements_path: Path to a pip-compatible requirements file.
            Lines beginning with ``#`` are comments and must be ignored.
            Lines of the form ``package==version`` are the only format
            that needs to be supported for this lab.
        cve_db_path: Path to the JSON CVE database file. Defaults to the
            project's mock data location.

    Returns:
        A list of CVE record dicts. Each dict contains at minimum the keys
        ``cve_id``, ``package``, ``affected_below``, ``severity``,
        ``cvss_score``, and ``description`` — matching the structure in
        ``mock_data/cve_database.json``. Returns an empty list if no
        vulnerabilities are found.

    Raises:
        FileNotFoundError: If ``requirements_path`` or ``cve_db_path`` do
            not exist on disk.
        ValueError: If a requirements line cannot be parsed into a
            ``package==version`` pair.

    Examples:
        >>> hits = scan_dependencies("mock_data/requirements_shipping_api.txt")
        >>> any(h["cve_id"] == "CVE-2024-5678" for h in hits)
        True
        >>> hits[0]["severity"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
        True
    """
    raise NotImplementedError(
        "scan_dependencies() is not implemented. "
        "Complete this function during Session 2."
    )


def is_version_affected(installed_version: str, affected_below: str) -> bool:
    """Return True if ``installed_version`` is strictly below ``affected_below``.

    Uses semantic version comparison (not lexicographic string comparison).
    Both arguments must be valid PEP 440 version strings.

    Args:
        installed_version: The version string of the installed package,
            e.g. ``"41.0.5"``.
        affected_below: The patched threshold version from the CVE record,
            e.g. ``"41.0.6"``.

    Returns:
        True if the installed version is below the threshold, False otherwise.

    Examples:
        >>> is_version_affected("41.0.5", "41.0.6")
        True
        >>> is_version_affected("41.0.6", "41.0.6")
        False
        >>> is_version_affected("2.0.0", "1.99.0")
        False
    """
    raise NotImplementedError(
        "is_version_affected() is not implemented. "
        "Complete this function during Session 2."
    )
