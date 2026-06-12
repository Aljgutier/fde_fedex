"""Pydantic v2 data models for the Release Readiness Agent."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReleaseRequest(BaseModel):
    """A release request submitted to the release readiness agent for evaluation.

    Fields match the records in mock_data/release_requests.json.
    The ``expected_outcome`` and ``outcome_reason`` fields present in the JSON
    are excluded — the agent must derive its own decision.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    request_id: str = Field(description="Unique identifier for the release request")
    component: str = Field(description="Name of the component being released (e.g. shipping-api)")
    version: str = Field(description="Version string being deployed (e.g. 2.4.1)")
    requirements_file: str = Field(description="Path to the requirements file for CVE scanning")
    changelog_version: str = Field(description="Version string to look up in CHANGELOG.md")
    ci_run_id: str = Field(description="CI run ID to evaluate via the deploy gate")
    requested_by: str = Field(description="Email of the release requestor")
    target_environment: str = Field(description="Target deployment environment (e.g. production)")


class ReleaseRecommendation(BaseModel):
    """The agent's structured recommendation for a release request.

    The ``decision`` field is always one of the three allowed literals.
    The ``rationale`` must be non-empty and reference the specific checks
    that drove the decision.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    request_id: str = Field(description="The request_id from the originating ReleaseRequest")
    decision: Literal["release", "hold", "escalate"] = Field(
        description="The agent's recommendation: release, hold, or escalate"
    )
    rationale: str = Field(
        description=(
            "Non-empty explanation of the decision. Must name the specific check(s) "
            "that drove the outcome (e.g. CVE ID, ticket ID, CI run status)."
        )
    )

    @field_validator("rationale")
    @classmethod
    def rationale_non_empty(cls, v: str) -> str:
        """Ensure the rationale is not blank after whitespace stripping."""
        if not v.strip():
            raise ValueError("rationale must be a non-empty string")
        return v
