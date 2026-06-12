"""
FedEx Shipping Platform — Release Pipeline

This package provides the brownfield pipeline components that were in place before
the release readiness agent was introduced. The package is organized as follows:

- runner.py        Orchestrates a full pipeline run across all stages
- deploy.py        Deploy gate logic — decides whether a build may be deployed
- changelog_reader.py  Reads and parses CHANGELOG.md entries
- dependency_scanner.py  (stub) Scans requirements files against a CVE database
- ticket_client.py       (stub) Queries open and blocking tickets for a component

Students implement the two stub modules and wire them into the Pydantic AI agent
defined in agent.py at the project root.
"""
