"""
Agent Evaluation and Cost Management

Comprehensive framework for measuring agent quality and tracking costs.

Core features:
- Test suite execution with golden datasets
- Quality metrics (accuracy, consistency, relevance)
- Cost tracking per request/user/day
- Model comparison across tiers
- Performance dashboards

Run: python main.py
"""

import os
import json
import asyncio
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()


# Test case model
@dataclass
class TestCase:
    id: str
    question: str
    expected_keywords: List[str]
    category: str
    expected_response: Optional[str] = None


# Judge score schema
class JudgeScore(BaseModel):
    helpfulness: float = Field(
        ge=0.0,
        le=1.0,
        description="How directly the response addresses the question",
    )
    correctness: float = Field(
        ge=0.0,
        le=1.0,
        description="How factually accurate the response is",
    )
    completeness: float = Field(
        ge=0.0,
        le=1.0,
        description="How well the response covers the expected content",
    )
    rationale: str = Field(description="A short explanation of the score.")


# Test result model
@dataclass
class TestResult:
    test_id: str
    question: str
    response: str
    passed: bool
    keywords_found: List[str]
    keywords_missing: List[str]
    tokens_used: int
    latency_ms: float
    cost_usd: float
    timestamp: str
    judge_score: Optional[JudgeScore] = None


# Judge agent schema and builder
class JudgeAgent:
    def __init__(self, model: str | None = None):
        resolved = model or os.getenv("JUDGE_MODEL", "openai:gpt-4-turbo")
        if ":" not in resolved:
            resolved = f"openai:{resolved}"
        self.agent = Agent(
            resolved,
            output_type=JudgeScore,
            system_prompt=(
                "You are a fair but exacting judge of customer support quality. "
                "Evaluate the provided response against the question and expected keywords. "
                "Score helpfulness, correctness, and completeness on a 0.0-1.0 scale, "
                "and include a concise rationale explaining the score."
            ),
        )

    async def judge(self, question: str, response: str, expected: str) -> JudgeScore:
        prompt = (
            f"Question: {question}\n\n"
            f"Agent response:\n{response}\n\n"
            f"Expected keywords / guidance: {expected}\n\n"
            "Evaluate the response on helpfulness, correctness, and completeness, "
            "then return only the structured scores and rationale."
        )
        result = await self.agent.run(prompt)
        return result.output


# Agent under test
class SupportAgent:
    def __init__(self, model: str | None = None):
        # Resolve the model: explicit arg > AI_MODEL env var > openai default.
        # Accept either a bare model name ("gpt-5.4-mini") or a fully
        # provider-prefixed identifier ("openai:gpt-5.4-mini",
        # "anthropic:claude-sonnet-4-5"). Bare names get the openai prefix
        # for backwards compatibility with the COST_PER_1K_TOKENS lookup.
        resolved = model or os.getenv("AI_MODEL", "openai:gpt-5.4-mini")
        if ":" not in resolved:
            resolved = f"openai:{resolved}"
        self.agent = Agent(
            resolved,
            system_prompt="""You are a friendly customer support agent.
            Answer questions accurately and concisely.
            Provide helpful information about our policies and services.""",
        )
        # Strip the provider prefix for the cost-table lookup so existing
        # COST_PER_1K_TOKENS keys ("gpt-5.4-mini", etc.) still resolve.
        self.model = resolved.split(":", 1)[1] if ":" in resolved else resolved

    async def handle_query(self, question: str) -> tuple[str, dict]:
        """Handle query and return (response, metadata)."""
        result = await self.agent.run(question)

        metadata = {
            "tokens": result.usage().total_tokens if result.usage() else 0,
            "model": self.model,
        }

        return result.output, metadata


# Evaluator
class AgentEvaluator:
    """Evaluate agent performance."""

    # Cost per 1K tokens (example rates - adjust for actual provider)
    COST_PER_1K_TOKENS = {
        "gpt-5.4-mini": 0.00015,
        "gpt-4o": 0.0050,
        "gpt-4-turbo": 0.0030,
    }

    def __init__(self, test_cases: List[TestCase]):
        self.test_cases = test_cases
        self.judge_agent = JudgeAgent()

    async def evaluate(self, model: str = "gpt-5.4-mini") -> List[TestResult]:
        """Run evaluation suite."""
        agent = SupportAgent(model)
        results = []

        for case in self.test_cases:
            result = await self._evaluate_case(agent, case)
            results.append(result)

        return results

    async def _evaluate_case(self, agent: SupportAgent, case: TestCase) -> TestResult:
        """Evaluate single test case.

        Wraps the agent call in try/except so a per-case failure (rate
        limit, transient network error, unexpected response shape) is
        captured as a failed TestResult with zeroed metrics rather than
        propagating out and crashing the rest of the evaluation suite.
        """
        # YOUR CODE HERE
        start = datetime.now()

        try:
            response, metadata = await agent.handle_query(case.question)

            # latency in milliseconds
            latency_ms = (datetime.now() - start).total_seconds() * 1000.0

            # tokens from metadata (SupportAgent.populate ensures this)
            tokens = int(metadata.get("tokens", 0))

            # Keyword matching (case-insensitive substring match)
            resp_lower = (response or "").lower()
            keywords_found = [k for k in case.expected_keywords if k.lower() in resp_lower]
            keywords_missing = [k for k in case.expected_keywords if k.lower() not in resp_lower]

            passed = len(keywords_missing) == 0

            # Cost calculation: per-1k-token rate lookup with small fallback
            model_key = metadata.get("model", getattr(agent, "model", None))
            rate_per_1k = self.COST_PER_1K_TOKENS.get(model_key, 0.0001)
            cost_usd = (tokens / 1000.0) * rate_per_1k

            expected = (
                ", ".join(case.expected_keywords)
                if case.expected_keywords
                else "(none specified)"
            )
            judge_score = None
            try:
                judge_score = await self.judge_agent.judge(
                    case.question, response, expected
                )
            except Exception:
                judge_score = None

            return TestResult(
                test_id=case.id,
                question=case.question,
                response=response,
                passed=passed,
                keywords_found=keywords_found,
                keywords_missing=keywords_missing,
                tokens_used=tokens,
                latency_ms=latency_ms,
                cost_usd=cost_usd,
                timestamp=datetime.now().isoformat(),
                judge_score=judge_score,
            )

        except Exception as e:
            # On error, return a failed TestResult with zeroed numeric metrics
            return TestResult(
                test_id=case.id,
                question=case.question,
                response=f"ERROR: {e}",
                passed=False,
                keywords_found=[],
                keywords_missing=list(case.expected_keywords),
                tokens_used=0,
                latency_ms=0.0,
                cost_usd=0.0,
                timestamp=datetime.now().isoformat(),
            )

    async def compare_models(self, models: List[str]) -> Dict[str, Dict]:
        """Compare performance across models."""
        comparison = {}

        for model in models:
            print(f"\nEvaluating {model}...")
            results = await self.evaluate(model)

            comparison[model] = {
                "pass_rate": sum(1 for r in results if r.passed) / len(results),
                "avg_cost_usd": sum(r.cost_usd for r in results) / len(results),
                "total_cost_usd": sum(r.cost_usd for r in results),
                "avg_latency_ms": sum(r.latency_ms for r in results) / len(results),
                "total_tokens": sum(r.tokens_used for r in results),
                "passed_tests": sum(1 for r in results if r.passed),
                "total_tests": len(results),
            }

        return comparison

    def generate_report(self, results: List[TestResult]) -> str:
        """Generate formatted evaluation report."""
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        total_cost = sum(r.cost_usd for r in results)
        avg_latency = sum(r.latency_ms for r in results) / total
        total_tokens = sum(r.tokens_used for r in results)
        judge_scores = [r.judge_score for r in results if r.judge_score is not None]
        avg_helpfulness = (
            sum(s.helpfulness for s in judge_scores) / len(judge_scores)
            if judge_scores
            else 0.0
        )
        avg_correctness = (
            sum(s.correctness for s in judge_scores) / len(judge_scores)
            if judge_scores
            else 0.0
        )
        avg_completeness = (
            sum(s.completeness for s in judge_scores) / len(judge_scores)
            if judge_scores
            else 0.0
        )

        report = []
        report.append("=" * 60)
        report.append("  AGENT EVALUATION REPORT")
        report.append("=" * 60)
        report.append(f"\nTimestamp: {datetime.now().isoformat()}")
        report.append(f"\nSUMMARY:")
        report.append(f"  Keyword Pass Rate: {passed}/{total} ({100*passed/total:.1f}%)")
        report.append(f"  Total Cost: ${total_cost:.4f}")
        report.append(f"  Total Tokens: {total_tokens:,}")
        report.append(f"  Avg Latency: {avg_latency:.0f}ms")
        if judge_scores:
            report.append(f"  Avg Judge Helpfulness: {avg_helpfulness:.2f}")
            report.append(f"  Avg Judge Correctness: {avg_correctness:.2f}")
            report.append(f"  Avg Judge Completeness: {avg_completeness:.2f}")
        report.append(f"\nDETAILED RESULTS:")

        for r in results:
            status = "PASS" if r.passed else "FAIL"
            report.append(f"\n{status} | {r.test_id}")
            report.append(f"  Question: {r.question}")
            report.append(f"  Response: {r.response[:100]}...")
            report.append(
                f"  Tokens: {r.tokens_used} | Cost: ${r.cost_usd:.5f} | Latency: {r.latency_ms:.0f}ms"
            )

            if not r.passed:
                report.append(f"  Missing keywords: {', '.join(r.keywords_missing)}")

            if r.judge_score is not None:
                judge_avg = (
                    r.judge_score.helpfulness
                    + r.judge_score.correctness
                    + r.judge_score.completeness
                ) / 3
                report.append(
                    f"  Judge avg: {judge_avg:.2f} "
                    f"(help={r.judge_score.helpfulness:.2f}, "
                    f"corr={r.judge_score.correctness:.2f}, "
                    f"comp={r.judge_score.completeness:.2f})"
                )
                report.append(f"  Judge rationale: {r.judge_score.rationale}")
                if r.passed and judge_avg < 0.5:
                    report.append("  NOTE: Keywords passed but judge is unhappy.")
                elif not r.passed and judge_avg >= 0.6:
                    report.append("  NOTE: Keywords failed but judge sees the response as reasonable.")

        report.append("\n" + "=" * 60)

        return "\n".join(report)


# Cost tracker
class CostTracker:
    """Track agent usage costs."""

    def __init__(
        self,
        log_file: str = "cost_log.json",
        daily_threshold: Optional[float] = None,
        per_user_threshold: Optional[float] = None,
    ):
        self.log_file = log_file
        self.daily_threshold = daily_threshold
        self.per_user_threshold = per_user_threshold
        # Hydrate from disk so `self.costs` reflects the full history
        # rather than just the current process's writes. Without this,
        # `get_total_cost()` returns only the current session's spend
        # while the JSONL file accumulates unbounded — a silent drift
        # that contradicts the lab's cost-accounting teaching.
        self.costs = self._load_existing()

    def _load_existing(self) -> list:
        """Read prior cost entries from log_file (one JSON object per line).

        Returns an empty list if the file doesn't exist yet, or skips any
        malformed lines so a partial write from a crashed prior run can't
        corrupt this session's totals.
        """
        path = os.fspath(self.log_file)
        if not os.path.exists(path):
            return []
        entries = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip malformed lines; don't crash on partial writes.
                    continue
        return entries

    def log_request(
        self, user_id: str, tokens: int, cost: float, metadata: dict = None
    ):
        """Log a request's cost."""
        # YOUR CODE HERE
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "tokens": tokens,
            "cost_usd": cost,
            "metadata": metadata or {},
        }

        self.costs.append(entry)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_total_cost(self, user_id: Optional[str] = None) -> float:
        """Get total cost, optionally filtered by user."""
        if user_id:
            return sum(c["cost_usd"] for c in self.costs if c["user_id"] == user_id)
        return sum(c["cost_usd"] for c in self.costs)

    def get_daily_costs(self) -> Dict[str, float]:
        """Get costs grouped by day."""
        daily = {}

        for cost in self.costs:
            date = cost["timestamp"][:10]  # YYYY-MM-DD
            daily[date] = daily.get(date, 0) + cost["cost_usd"]

        return daily

    def _alert_state(self, current: float, threshold: Optional[float]) -> str:
        if threshold is None:
            return "ok"
        if current >= threshold:
            return "over_budget"
        if current >= threshold * 0.8:
            return "warning"
        return "ok"

    def get_daily_alert_state(self) -> str:
        """Check current day's spend against the daily threshold."""
        current_day = datetime.now().date().isoformat()
        daily_costs = self.get_daily_costs()
        return self._alert_state(daily_costs.get(current_day, 0.0), self.daily_threshold)

    def get_user_alert_state(self, user_id: str) -> str:
        """Check a user's total spend against the per-user threshold."""
        return self._alert_state(self.get_total_cost(user_id), self.per_user_threshold)


# Main demonstrations
async def main():
    # Sample test cases
    test_cases = [
        TestCase(
            id="return-policy",
            question="What is your return policy?",
            expected_keywords=["30 days", "receipt", "refund"],
            category="policy",
        ),
        TestCase(
            id="shipping-time",
            question="How long does shipping take?",
            expected_keywords=["3-5 business days", "tracking"],
            category="logistics",
        ),
        TestCase(
            id="payment-methods",
            question="What payment methods do you accept?",
            expected_keywords=["credit card", "PayPal"],
            category="payment",
        ),
        TestCase(
            id="order-status",
            question="Can you tell me the status of my order and if it has shipped?",
            expected_keywords=["order status", "tracking", "shipped"],
            category="order status",
        ),
    ]

    evaluator = AgentEvaluator(test_cases)

    print("=" * 60)
    print("  AGENT EVALUATION & COST MANAGEMENT")
    print("=" * 60)

    # Run evaluation
    print("\n1. Running evaluation suite...")
    results = await evaluator.evaluate(model="gpt-5.4-mini")

    # Generate report
    report = evaluator.generate_report(results)
    print(report)

    # Save report
    with open("evaluation_report.txt", "w") as f:
        f.write(report)
    print("\nReport saved to evaluation_report.txt")

    # Compare models
    print("\n2. Comparing model tiers...")
    comparison = await evaluator.compare_models(["gpt-5.4-mini", "gpt-4o", "gpt-4-turbo"])

    print("\n" + "=" * 60)
    print("  MODEL COMPARISON")
    print("=" * 60)

    for model, metrics in comparison.items():
        print(f"\n{model.upper()}:")
        print(f"  Pass Rate: {metrics['pass_rate']*100:.1f}%")
        print(f"  Avg Cost: ${metrics['avg_cost_usd']:.5f}/request")
        print(f"  Total Cost: ${metrics['total_cost_usd']:.4f}")
        print(f"  Avg Latency: {metrics['avg_latency_ms']:.0f}ms")
        print(f"  Total Tokens: {metrics['total_tokens']:,}")

    # Cost tracking demo with alert thresholds
    print("\n3. Cost tracking demo...")
    tracker = CostTracker(daily_threshold=0.00005, per_user_threshold=0.00002)

    for i, result in enumerate(results):
        tracker.log_request(
            user_id=f"user_{i % 3}",  # Simulate 3 users
            tokens=result.tokens_used,
            cost=result.cost_usd,
            metadata={"test_id": result.test_id},
        )

    print(f"\nTotal tracked cost: ${tracker.get_total_cost():.4f}")
    print(f"User 0 cost: ${tracker.get_total_cost('user_0'):.4f}")
    print(f"Daily budget alert state: {tracker.get_daily_alert_state()}")
    print(f"User 0 budget alert state: {tracker.get_user_alert_state('user_0')}")

    # Demonstrate higher thresholds with no alerts
    tracker_loose = CostTracker(
        log_file="cost_log.json",
        daily_threshold=0.01,
        per_user_threshold=0.01,
    )
    # Carry existing cost history into loose tracker for demo purposes.
    tracker_loose.costs = tracker.costs.copy()
    print(f"\nWith higher thresholds:")
    print(f"  Daily budget alert state: {tracker_loose.get_daily_alert_state()}")
    print(f"  User 0 budget alert state: {tracker_loose.get_user_alert_state('user_0')}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
