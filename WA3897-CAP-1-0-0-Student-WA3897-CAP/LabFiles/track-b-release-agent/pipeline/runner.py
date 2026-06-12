"""Pipeline runner — orchestrates the existing pre-agent release pipeline.

This module was the primary release verification entrypoint before the
release readiness agent was introduced. It runs the deploy gate against a
CI result and reports the outcome. The runner does NOT call the dependency
scanner or ticket client because those modules are stubs pending implementation.

After students implement the stubs in Sessions 2–3, the agent (agent.py at
the project root) will coordinate all four checks. The runner remains in the
pipeline as the final deploy gate step.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pipeline.deploy import DeployGate, GateDecision


@dataclass
class PipelineRun:
    """The result of a single pipeline execution."""

    request_id: str
    component: str
    version: str
    ci_run_id: str | None
    gate_decision: GateDecision
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Return True if the deploy gate approved the build."""
        return self.gate_decision.approved

    def summary(self) -> str:
        """Return a single-line human-readable summary of the run."""
        status = "APPROVED" if self.passed else "DENIED"
        parts = [
            f"[{self.request_id}] {self.component} v{self.version} — {status}",
            f"  Gate: {self.gate_decision.reason}",
        ]
        for w in self.warnings:
            parts.append(f"  Warning: {w}")
        return "\n".join(parts)


class PipelineRunner:
    """Runs the pre-agent release pipeline for a given release request.

    The runner loads CI result data and passes it to the DeployGate. It also
    performs lightweight sanity checks (missing CI run, unknown component) and
    records those as warnings in the PipelineRun output.
    """

    def __init__(
        self,
        ci_results_path: str = "mock_data/ci_results.json",
        min_coverage_percent: float = DeployGate.DEFAULT_MIN_COVERAGE,
    ) -> None:
        """Initialize the runner.

        Args:
            ci_results_path: Path to the CI results JSON file.
            min_coverage_percent: Minimum test coverage threshold passed to
                the deploy gate.
        """
        self.ci_results_path = Path(ci_results_path)
        self.gate = DeployGate(min_coverage_percent=min_coverage_percent)
        self._ci_index: dict[str, dict[str, object]] | None = None

    def _load_ci_results(self) -> dict[str, dict[str, object]]:
        """Load and index CI results by run_id (cached after first load)."""
        if self._ci_index is None:
            if not self.ci_results_path.exists():
                raise FileNotFoundError(
                    f"CI results not found: {self.ci_results_path}"
                )
            raw: list[dict[str, object]] = json.loads(
                self.ci_results_path.read_text(encoding="utf-8")
            )
            self._ci_index = {r["run_id"]: r for r in raw}  # type: ignore[index]
        return self._ci_index

    def run(self, release_request: dict[str, object]) -> PipelineRun:
        """Execute the pipeline for one release request.

        Args:
            release_request: A dict matching the schema in
                ``mock_data/release_requests.json``. The ``ci_run_id`` field
                is used to look up CI results; if not found, the gate is
                automatically denied.

        Returns:
            A PipelineRun describing the gate decision and any warnings.
        """
        request_id = str(release_request.get("request_id", "UNKNOWN"))
        component = str(release_request.get("component", ""))
        version = str(release_request.get("version", ""))
        ci_run_id = release_request.get("ci_run_id")
        warnings: list[str] = []

        try:
            ci_index = self._load_ci_results()
        except FileNotFoundError as exc:
            return PipelineRun(
                request_id=request_id,
                component=component,
                version=version,
                ci_run_id=str(ci_run_id) if ci_run_id else None,
                gate_decision=GateDecision(
                    approved=False,
                    reason=str(exc),
                ),
                warnings=["CI results file could not be loaded — gate denied automatically."],
            )

        if not ci_run_id:
            warnings.append("No ci_run_id provided in the release request.")
            gate = GateDecision(
                approved=False,
                reason="Cannot evaluate deploy gate without a CI run ID.",
            )
            return PipelineRun(
                request_id=request_id,
                component=component,
                version=version,
                ci_run_id=None,
                gate_decision=gate,
                warnings=warnings,
            )

        ci_result = ci_index.get(str(ci_run_id))
        if ci_result is None:
            warnings.append(f"CI run '{ci_run_id}' not found in results database.")
            gate = GateDecision(
                approved=False,
                reason=f"CI run '{ci_run_id}' does not exist.",
                ci_run_id=str(ci_run_id),
            )
            return PipelineRun(
                request_id=request_id,
                component=component,
                version=version,
                ci_run_id=str(ci_run_id),
                gate_decision=gate,
                warnings=warnings,
            )

        # Warn if the CI result is for a different component
        ci_component = ci_result.get("component", "")
        if ci_component and ci_component != component:
            warnings.append(
                f"CI run '{ci_run_id}' is for component '{ci_component}', "
                f"but this request targets '{component}'."
            )

        gate = self.gate.evaluate(ci_result)

        return PipelineRun(
            request_id=request_id,
            component=component,
            version=version,
            ci_run_id=str(ci_run_id),
            gate_decision=gate,
            warnings=warnings,
        )

    def run_all(
        self,
        release_requests: list[dict[str, object]],
    ) -> list[PipelineRun]:
        """Run the pipeline for every request in a list.

        Args:
            release_requests: A list of release request dicts.

        Returns:
            A list of PipelineRun results, one per request, in the same order.
        """
        return [self.run(req) for req in release_requests]


def main() -> None:
    """CLI entry point — runs all sample release requests and prints a summary."""
    requests_path = Path("mock_data/release_requests.json")
    if not requests_path.exists():
        print(f"Error: {requests_path} not found", file=sys.stderr)
        sys.exit(1)

    requests: list[dict[str, object]] = json.loads(
        requests_path.read_text(encoding="utf-8")
    )
    runner = PipelineRunner()
    results = runner.run_all(requests)

    approved = sum(1 for r in results if r.passed)
    print(f"\nPipeline Results — {approved}/{len(results)} approved\n" + "=" * 50)
    for result in results:
        print(result.summary())
        print()


if __name__ == "__main__":
    main()
