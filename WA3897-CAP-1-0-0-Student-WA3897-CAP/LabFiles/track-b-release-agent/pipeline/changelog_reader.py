"""Reads and parses CHANGELOG.md entries for a given version."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ChangelogEntry:
    """A single versioned entry parsed from CHANGELOG.md."""

    version: str
    date: str | None
    sections: dict[str, list[str]] = field(default_factory=dict)

    @property
    def has_breaking_changes(self) -> bool:
        """Return True if the entry documents any breaking changes."""
        breaking_keys = {"breaking changes", "breaking", "removed", "incompatible"}
        return any(k.lower() in breaking_keys for k in self.sections)

    @property
    def is_major_version(self) -> bool:
        """Return True if the version string has a non-zero major component."""
        parts = self.version.lstrip("v").split(".")
        return len(parts) >= 1 and parts[0] != "0"

    def section_items(self, section_name: str) -> list[str]:
        """Return bullet items for a named section, case-insensitively."""
        for key, items in self.sections.items():
            if key.lower() == section_name.lower():
                return items
        return []


class ChangelogReader:
    """Parses a Keep-a-Changelog formatted CHANGELOG.md file."""

    # Matches: ## [1.2.3] - 2024-11-14  or  ## [Unreleased]
    _VERSION_HEADER = re.compile(
        r"^##\s+\[(?P<version>[^\]]+)\](?:\s+-\s+(?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
    )
    # Matches: ### Added / ### Changed / etc.
    _SECTION_HEADER = re.compile(r"^###\s+(?P<name>.+)\s*$")
    # Matches: - bullet item text
    _BULLET = re.compile(r"^[-*]\s+(?P<text>.+)$")

    def __init__(self, changelog_path: str | Path) -> None:
        """Initialize the reader with the path to CHANGELOG.md.

        Args:
            changelog_path: Absolute or relative path to the changelog file.

        Raises:
            FileNotFoundError: If the file does not exist at the given path.
        """
        self.path = Path(changelog_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Changelog not found: {self.path}")

    def read_all(self) -> list[ChangelogEntry]:
        """Parse all versioned entries in the changelog.

        Returns:
            A list of ChangelogEntry objects in the order they appear in the file
            (typically newest-first for Keep-a-Changelog format).
        """
        entries: list[ChangelogEntry] = []
        current_entry: ChangelogEntry | None = None
        current_section: str | None = None

        for raw_line in self.path.read_text(encoding="utf-8").splitlines():
            line = raw_line.rstrip()

            version_match = self._VERSION_HEADER.match(line)
            if version_match:
                current_entry = ChangelogEntry(
                    version=version_match.group("version"),
                    date=version_match.group("date"),
                )
                current_section = None
                entries.append(current_entry)
                continue

            section_match = self._SECTION_HEADER.match(line)
            if section_match and current_entry is not None:
                current_section = section_match.group("name").strip()
                current_entry.sections.setdefault(current_section, [])
                continue

            bullet_match = self._BULLET.match(line)
            if bullet_match and current_entry is not None and current_section is not None:
                current_entry.sections[current_section].append(
                    bullet_match.group("text").strip()
                )

        return entries

    def find_version(self, version: str) -> ChangelogEntry | None:
        """Return the changelog entry for an exact version string, or None.

        Args:
            version: The version string to look up, e.g. ``"1.2.3"`` or ``"3.0.0"``.
                Leading ``v`` prefix is stripped before comparison.

        Returns:
            The matching ChangelogEntry, or None if the version is not present.
        """
        normalized = version.lstrip("v")
        for entry in self.read_all():
            if entry.version.lstrip("v") == normalized:
                return entry
        return None

    def versions(self) -> list[str]:
        """Return a list of all version strings found in the changelog."""
        return [e.version for e in self.read_all()]

    def detect_major_version_gap(self, version: str) -> dict[str, object] | None:
        """Check whether a major version bump lacks breaking-change documentation.

        Compares the given version against the previous version in the changelog.
        If the major version number increased and the entry contains no
        "Breaking Changes" section, returns a dict describing the gap.

        Args:
            version: The version string to check, e.g. ``"3.0.0"``.

        Returns:
            A dict with keys ``previous_version``, ``current_version``, and
            ``description`` if a gap is detected, or None if the version is clean.
        """
        entry = self.find_version(version)
        if entry is None:
            return None

        all_versions = self.read_all()
        try:
            idx = next(i for i, e in enumerate(all_versions) if e.version == entry.version)
        except StopIteration:
            return None

        if idx + 1 >= len(all_versions):
            # No previous version to compare against
            return None

        prev_entry = all_versions[idx + 1]

        def major(v: str) -> int:
            try:
                return int(v.lstrip("v").split(".")[0])
            except (ValueError, IndexError):
                return 0

        if major(entry.version) > major(prev_entry.version):
            if not entry.has_breaking_changes:
                return {
                    "previous_version": prev_entry.version,
                    "current_version": entry.version,
                    "description": (
                        f"Major version bump from {prev_entry.version} to {entry.version} "
                        f"with no 'Breaking Changes' section in the changelog entry. "
                        f"Semantic Versioning requires breaking changes to be explicitly documented."
                    ),
                }

        return None
