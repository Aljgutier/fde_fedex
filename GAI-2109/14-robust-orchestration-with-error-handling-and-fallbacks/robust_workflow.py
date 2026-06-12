"""
Robust Workflow Orchestration with Error Handling and Fallbacks

Advanced orchestration with:
- Compensation actions for rollback
- Fallback strategies
- Circuit breakers
- Timeout management
- Comprehensive error recovery

Run: python robust_workflow.py
"""

import asyncio
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from types import SimpleNamespace
from abc import ABC, abstractmethod
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class CircuitBreaker:
    """Circuit breaker to prevent cascading failures."""

    failure_threshold: int = 3
    timeout_seconds: float = 60.0

    failures: int = 0
    last_failure: Optional[datetime] = None
    is_open: bool = False

    def record_success(self):
        """Record successful execution."""
        self.failures = 0
        self.is_open = False

    def record_failure(self):
        """Record failure."""
        self.failures += 1
        self.last_failure = datetime.now()

        if self.failures >= self.failure_threshold:
            self.is_open = True

    def can_execute(self) -> bool:
        """Check if execution is allowed."""
        if not self.is_open:
            return True

        # Check if timeout has passed
        if self.last_failure:
            elapsed = (datetime.now() - self.last_failure).total_seconds()
            if elapsed >= self.timeout_seconds:
                # Half-open state - allow one attempt
                self.is_open = False
                self.failures = self.failure_threshold - 1
                return True

        return False


class SagaStep(ABC):
    """Abstract base class for saga steps with mandatory compensation.
    
    Every saga step must implement both execute() and compensate().
    This ensures every transactional stage declares its rollback behavior up front.
    """

    def __init__(self, name: str):
        self.name = name
        self.circuit_breaker = CircuitBreaker()

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> str:
        """Execute the forward action of this saga step."""
        pass

    @abstractmethod
    async def compensate(self, context: Dict[str, Any]):
        """Execute the compensating action (rollback) for this saga step."""
        pass


class RobustWorkflowStep(SagaStep):
    """Workflow step with error handling."""

    def __init__(
        self,
        name: str,
        agent: Agent,
        prompt_template: str,
        fallback_agent: Optional[Agent] = None,
        compensation_action: Optional[Callable] = None,
        timeout_seconds: float = 30.0,
        max_retries: int = 2,
    ):
        super().__init__(name)
        self.agent = agent
        self.prompt_template = prompt_template
        self.fallback_agent = fallback_agent
        self.compensation_action = compensation_action
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    async def execute(self, context: Dict[str, Any]) -> str:
        """Execute step with error handling."""
        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            raise RuntimeError(f"Circuit breaker open for {self.name}")

        # Format prompt
        prompt = self.prompt_template.format(**context)

        # Try main agent with retries
        for attempt in range(self.max_retries + 1):
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    self.agent.run(prompt), timeout=self.timeout_seconds
                )

                self.circuit_breaker.record_success()
                return result.output

            except asyncio.TimeoutError:
                if attempt < self.max_retries:
                    print(f"  ⏱ Timeout on attempt {attempt + 1}, retrying...")
                    continue
                else:
                    print(f"  ⏱ Timeout after {self.max_retries + 1} attempts")
                    break

            except Exception as e:
                if attempt < self.max_retries:
                    print(f"  ⚠ Error on attempt {attempt + 1}: {e}")
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                    continue
                else:
                    print(f"  ✗ Failed after {self.max_retries + 1} attempts")
                    break

        # Record failure
        self.circuit_breaker.record_failure()

        # Try fallback agent
        if self.fallback_agent:
            print(f"  🔄 Using fallback agent...")
            try:
                result = await asyncio.wait_for(
                    self.fallback_agent.run(prompt), timeout=self.timeout_seconds
                )
                return result.output

            except Exception as e:
                print(f"  ✗ Fallback also failed: {e}")

        raise RuntimeError(f"Step {self.name} failed completely")

    async def compensate(self, context: Dict[str, Any]):
        """Execute compensation action."""
        if self.compensation_action:
            print(f"  ↶ Running compensation for {self.name}")
            await self.compensation_action(context)
        else:
            print(f"  ⚠ No compensation action defined for {self.name}")


class RobustWorkflowOrchestrator:
    """Orchestrator with comprehensive error handling."""

    def __init__(self, name: str):
        self.name = name
        self.steps: list[RobustWorkflowStep] = []
        self.executed_steps: list[RobustWorkflowStep] = []

    def add_step(self, step: RobustWorkflowStep):
        """Add step to workflow."""
        self.steps.append(step)
        return self

    async def execute(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with error handling."""
        # YOUR CODE HERE
        # Make a local copy of the incoming context so callers are not mutated
        context: Dict[str, Any] = dict(initial_context or {})

        # Seed metadata
        context.setdefault("_metadata", {})
        context["_metadata"]["start_time"] = datetime.now()
        context["_metadata"]["steps_completed"] = []
        context["_metadata"]["steps_failed"] = []

        # Banner for operator visibility
        print(f"\n=== Running workflow: {self.name} ===\n")

        total = len(self.steps)

        try:
            for idx, step in enumerate(self.steps, 1):
                print(f"Step {idx}/{total}: {step.name}")

                try:
                    result_value = await step.execute(context)
                    # store under <step.name>_result for downstream templates
                    context[f"{step.name}_result"] = result_value

                    # book-keeping for rollback and metadata
                    context["_metadata"]["steps_completed"].append(step.name)
                    self.executed_steps.append(step)

                except Exception as err:  # narrow to the single step
                    print(f"  ✗ Step failed: {step.name} -> {err}")
                    context["_metadata"]["steps_failed"].append(step.name)
                    # Run rollback and finalize metadata
                    await self._rollback(context)
                    context["_metadata"]["end_time"] = datetime.now()
                    context["_metadata"]["status"] = "failed"
                    return context

        except Exception:
            # Unexpected error around the loop - ensure rollback then re-raise
            await self._rollback(context)
            raise

        # Completed all steps successfully
        context["_metadata"]["end_time"] = datetime.now()
        context["_metadata"]["status"] = "completed"

        # Print duration summary
        start = context["_metadata"]["start_time"]
        end = context["_metadata"]["end_time"]
        duration = end - start
        print(f"\nWorkflow completed in {duration.total_seconds():.2f} seconds\n")

        return context

    async def _rollback(self, context: Dict[str, Any]):
        """Rollback executed steps.

        Return early if there are no executed steps. Otherwise print a banner
        and run each step's compensation in reverse order, then clear the
        executed_steps list.
        """
        if not self.executed_steps:
            print("  (rollback) no executed steps to compensate")
            return

        print(f"\n{'='*60}")
        print(f"  Rolling Back {len(self.executed_steps)} Steps")
        print(f"{'='*60}\n")

        # Compensate in reverse order
        for step in reversed(self.executed_steps):
            try:
                await step.compensate(context)
            except Exception as e:
                print(f"  ⚠ Compensation for {step.name} raised: {e}")

        # Clear executed steps after attempting compensation
        self.executed_steps.clear()


# Example workflow
async def example():
    """Demonstrate robust workflow."""
    # Simulated side-effect store and undo directory
    SIDE_EFFECT_STORE: Dict[str, Any] = {"count": 0, "actions": []}
    undo_dir = Path("undo_records")
    undo_dir.mkdir(exist_ok=True)

    # Simple fake agents for deterministic behavior in the example
    class FakeAgent:
        def __init__(self, name: str):
            self.name = name

        async def run(self, prompt: str):
            # Simulate a side-effect when the agent runs
            entry = {"agent": self.name, "prompt": prompt, "time": datetime.now().isoformat()}
            SIDE_EFFECT_STORE["count"] += 1
            SIDE_EFFECT_STORE["actions"].append(entry)
            return SimpleNamespace(output=f"{self.name}_output")

    class FailAgent(FakeAgent):
        async def run(self, prompt: str):
            # Force failure for testing rollback
            raise RuntimeError("forced failure in FailAgent")

    primary_agent = FakeAgent("primary")
    fallback_agent = FakeAgent("fallback")

    # Compensation actions that write observable undo records and update the store
    async def compensate_step1(ctx):
        print("    Undoing step 1 (writing undo record)...")
        record = {"step": "extract", "action": "undo", "time": datetime.now().isoformat()}
        p = undo_dir / "undo_extract.json"
        p.write_text(json.dumps(record))
        # reverse a side-effect if present
        if SIDE_EFFECT_STORE["actions"]:
            SIDE_EFFECT_STORE["actions"].pop()
            SIDE_EFFECT_STORE["count"] = max(0, SIDE_EFFECT_STORE["count"] - 1)
        await asyncio.sleep(0.1)

    async def compensate_step2(ctx):
        print("    Undoing step 2 (writing undo record)...")
        record = {"step": "transform", "action": "undo", "time": datetime.now().isoformat()}
        p = undo_dir / "undo_transform.json"
        p.write_text(json.dumps(record))
        # reverse a side-effect if present
        if SIDE_EFFECT_STORE["actions"]:
            SIDE_EFFECT_STORE["actions"].pop()
            SIDE_EFFECT_STORE["count"] = max(0, SIDE_EFFECT_STORE["count"] - 1)
        await asyncio.sleep(0.1)

    # Build workflow
    workflow = RobustWorkflowOrchestrator("Data Processing Pipeline")

    workflow.add_step(
        RobustWorkflowStep(
            name="extract",
            agent=primary_agent,
            prompt_template="Extract key information from: {input_data}",
            fallback_agent=fallback_agent,
            compensation_action=compensate_step1,
            timeout_seconds=10.0,
            max_retries=2,
        )
    )

    workflow.add_step(
        RobustWorkflowStep(
            name="transform",
            agent=primary_agent,
            prompt_template="Transform this data: {extract_result}",
            fallback_agent=fallback_agent,
            compensation_action=compensate_step2,
            timeout_seconds=10.0,
            max_retries=2,
        )
    )

    # Force the third step to fail by using FailAgent
    workflow.add_step(
        RobustWorkflowStep(
            name="summarize",
            agent=FailAgent("summarize_fail"),
            prompt_template="Summarize: {transform_result}",
            fallback_agent=None,  # no fallback so failure triggers rollback
            timeout_seconds=10.0,
            max_retries=2,
        )
    )

    # Execute
    result = await workflow.execute({"input_data": "Sample customer feedback data..."})

    print("\nFinal Result:")
    print(f"Status: {result['_metadata']['status']}")
    print(f"Steps completed: {result['_metadata']['steps_completed']}")
    print(f"SIDE_EFFECT_STORE after run: {SIDE_EFFECT_STORE}")
    print(f"Undo files: {[p.name for p in undo_dir.iterdir()]}")

if __name__ == "__main__":
    asyncio.run(example())
