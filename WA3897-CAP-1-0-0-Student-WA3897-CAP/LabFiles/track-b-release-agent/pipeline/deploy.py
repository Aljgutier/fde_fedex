"""Deploy gate — authoritative pre-deployment safety check.

This is the existing deploy gate used by the pipeline before the release
readiness agent was introduced. It performs a basic pass/fail check on CI
results and is intentionally narrow in scope: it only looks at test counts.

The agent you build in Session 2 does NOT replace this gate. Instead, the
agent produces a recommendation that feeds into the human review step that
precedes this gate. Both exist independently in the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    """The output of a deploy gate evaluation."""

    approved: bool
    reason: str
    ci_run_id: str | None = None


class DeployGate:
    """Evaluates a CI result record and decides whether deployment may proceed.

    Decision rules (in priority order):
    1. If the CI status is not ``"passed"``, deny.
    2. If the number of failed tests is greater than zero, deny.
    3. If the number of errors is greater than zero, deny.
    4. If test coverage is below the ``min_coverage_percent`` threshold, deny.
    5. Otherwise, approve.
    """

    DEFAULT_MIN_COVERAGE: float = 80.0

    def __init__(self, min_coverage_percent: float = DEFAULT_MIN_COVERAGE) -> None:
        """Initialize the gate with a minimum coverage threshold.

        Args:
            min_coverage_percent: Minimum acceptable test coverage percentage.
                Defaults to 80.0. Builds below this threshold are denied.
        """
        self.min_coverage_percent = min_coverage_percent

    def evaluate(self, ci_result: dict[str, object]) -> GateDecision:
        """Evaluate a CI result record and return a gate decision.

        Args:
            ci_result: A CI result dict matching the schema in
                ``mock_data/ci_results.json``.  Must contain at minimum
                ``status``, ``run_id``, ``test_summary`` (with ``failed``
                and ``errors`` keys), and ``coverage_percent``.

        Returns:
            A GateDecision with ``approved=True`` if all checks pass,
            or ``approved=False`` with a human-readable ``reason`` describing
            the first failing check.
        """
        run_id: str | None = ci_result.get("run_id")  # type: ignore[assignment]

        status = ci_result.get("status", "unknown")
        if status != "passed":
            return GateDecision(
                approved=False,
                reason=f"CI run status is '{status}', not 'passed'.",
                ci_run_id=run_id,
            )

        summary = ci_result.get("test_summary", {})
        if not isinstance(summary, dict):
            return GateDecision(
                approved=False,
                reason="CI result is missing a valid 'test_summary' field.",
                ci_run_id=run_id,
            )

        failed = int(summary.get("failed", 0))
        if failed > 0:
            total = int(summary.get("total", 0))
            return GateDecision(
                approved=False,
                reason=f"{failed} of {total} tests failed.",
                ci_run_id=run_id,
            )

        errors = int(summary.get("errors", 0))
        if errors > 0:
            return GateDecision(
                approved=False,
                reason=f"{errors} test runner error(s) reported.",
                ci_run_id=run_id,
            )

        coverage = float(ci_result.get("coverage_percent", 0.0))
        if coverage < self.min_coverage_percent:
            return GateDecision(
                approved=False,
                reason=(
                    f"Test coverage {coverage:.1f}% is below the required "
                    f"{self.min_coverage_percent:.1f}% threshold."
                ),
                ci_run_id=run_id,
            )

        return GateDecision(
            approved=True,
            reason=(
                f"All checks passed: CI status 'passed', "
                f"0 failures, 0 errors, coverage {coverage:.1f}%."
            ),
            ci_run_id=run_id,
        )
