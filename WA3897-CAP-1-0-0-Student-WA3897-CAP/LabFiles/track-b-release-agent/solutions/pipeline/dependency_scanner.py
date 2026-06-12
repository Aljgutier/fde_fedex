"""Dependency scanner — implemented solution for pipeline/dependency_scanner.py."""

from __future__ import annotations

import json
from pathlib import Path

from packaging.version import Version


def scan_dependencies(
    requirements_path: str,
    cve_db_path: str = "mock_data/cve_database.json",
) -> list[dict[str, object]]:
    """Scan a requirements file and return all matching CVE records.

    Reads pinned package versions from a pip-style requirements file, then
    compares each package and version against the CVE database. Returns only
    CVE records whose package name and version range match an installed package.

    Args:
        requirements_path: Path to a pip-compatible requirements file.
        cve_db_path: Path to the JSON CVE database file.

    Returns:
        A list of matching CVE record dicts. Empty list if no vulnerabilities found.

    Raises:
        FileNotFoundError: If either file does not exist.
        ValueError: If a requirements line cannot be parsed.
    """
    req_path = Path(requirements_path)
    if not req_path.exists():
        raise FileNotFoundError(f"Requirements file not found: {req_path}")

    cve_path = Path(cve_db_path)
    if not cve_path.exists():
        raise FileNotFoundError(f"CVE database not found: {cve_path}")

    cve_db: list[dict[str, object]] = json.loads(
        cve_path.read_text(encoding="utf-8")
    )

    # Parse requirements — only "package==version" lines; skip comments and blanks
    installed: dict[str, str] = {}
    for line in req_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            continue  # extras, options, etc. — skip
        parts = line.split("==", 1)
        if len(parts) != 2:
            raise ValueError(f"Cannot parse requirements line: {line!r}")
        pkg_name = parts[0].strip().lower()
        pkg_version = parts[1].strip().split()[0]  # strip inline comments
        installed[pkg_name] = pkg_version

    # Match against CVE database
    hits: list[dict[str, object]] = []
    for cve in cve_db:
        pkg = str(cve["package"]).lower()
        affected_below = str(cve["affected_below"])
        installed_version = installed.get(pkg)
        if installed_version and is_version_affected(installed_version, affected_below):
            hits.append(cve)

    return hits


def is_version_affected(installed_version: str, affected_below: str) -> bool:
    """Return True if ``installed_version`` is strictly below ``affected_below``.

    Uses PEP 440 semantic version comparison via the ``packaging`` library.

    Args:
        installed_version: The version string of the installed package.
        affected_below: The patched threshold version from the CVE record.

    Returns:
        True if installed_version < affected_below, False otherwise.
    """
    return Version(installed_version) < Version(affected_below)
