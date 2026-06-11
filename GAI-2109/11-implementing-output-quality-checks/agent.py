"""
Guardrail-Protected Agent

Complete integration of input validation, output validation, and PII detection.

Features:
- Pre-processing input validation
- Post-processing output validation
- Automatic PII redaction
- Retry logic with correction prompts
- Comprehensive logging

Run: python agent.py
"""

import os
import time
import asyncio
from typing import Dict, Optional, List
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from dotenv import load_dotenv

from input_guards import InputGuardrails
from output_guards import OutputGuardrails
from pii_detector import PIIDetector

load_dotenv()


# Create financial services support agent
support_agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a professional financial services support agent.

Guidelines:
- Provide accurate information about our services
- Be professional and courteous  
- Never discuss competitors or provide financial/legal/tax advice
- Do not express personal opinions
- Keep responses concise and helpful
- Never use inappropriate language
""",
)

HEDGING_PHRASES = [
    "i'm not sure",
    "im not sure",
    "i don't know",
    "i can't predict",
    "cannot predict",
    "not certain",
    "uncertain",
    "possibly",
    "might be",
    "could be",
    "perhaps",
    "it's possible",
    "there is a chance",
    "with certainty",
    "i can't say",
]


def compute_confidence(response: str) -> float:
    """Estimate a simple confidence score from hedging phrases."""
    response_lower = response.lower().replace("’", "'").replace("‘", "'")
    hedging_count = sum(1 for phrase in HEDGING_PHRASES if phrase in response_lower)
    if hedging_count == 0:
        return 1.0
    return max(0.0, 1.0 - 0.5 * hedging_count)


async def handle_query_with_guardrails(query: str) -> Dict:
    """
    Process query with complete guardrail protection.

    Pipeline:
    1. Input validation
    2. Agent execution
    3. Output validation
    4. PII detection and redaction
    5. Return results with metadata

    Returns:
        {
            'success': bool,
            'response': str,
            'error': str (if failed),
            'guardrails_triggered': List[str],
            'pii_redacted': Dict[str, int]
        }
    """
    triggered: List[str] = []

    input_result = InputGuardrails.validate_input(query)
    if not input_result.is_valid:
        triggered.append("input_validation")
        return {
            "success": False,
            "response": None,
            "error": input_result.error_message,
            "guardrails_triggered": triggered,
            "pii_redacted": {},
        }

    try:
        result = await support_agent.run(query)
        response = result.output
    except Exception as e:
        return {
            "success": False,
            "response": None,
            "error": f"Agent error: {str(e)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
        }

    output_result = OutputGuardrails.validate_output(response)
    if output_result.policy_violations:
        triggered.append("policy_compliance")
        return {
            "success": False,
            "response": response,
            "error": f"Policy violations: {'; '.join(output_result.policy_violations)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
            "validation_details": {
                "errors": output_result.errors,
                "warnings": output_result.warnings,
                "policy_violations": output_result.policy_violations,
            },
        }

    if not output_result.is_valid:
        triggered.append("output_validation")
        return {
            "success": False,
            "response": response,
            "error": f"Output validation failed: {'; '.join(output_result.errors)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
            "validation_details": {
                "errors": output_result.errors,
                "warnings": output_result.warnings,
                "policy_violations": output_result.policy_violations,
            },
        }

    confidence_score = compute_confidence(response)
    if confidence_score < 0.6:
        triggered.append("low_confidence")
        return {
            "success": False,
            "response": response,
            "error": "Low confidence response; route for human review.",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
            "validation_details": {
                "errors": output_result.errors,
                "warnings": output_result.warnings,
                "policy_violations": output_result.policy_violations,
                "confidence_score": confidence_score,
            },
        }

    redacted_response, pii_found = PIIDetector.redact_pii(response)
    if pii_found:
        triggered.append("pii_redaction")
        response = redacted_response

    return {
        "success": True,
        "response": response,
        "error": None,
        "guardrails_triggered": triggered,
        "pii_redacted": pii_found,
        "quality_score": output_result.quality_score,
    }


async def handle_query_skipping_input_validation(query: str) -> Dict:
    """Run agent + output validation + PII redaction, *without* input validation.

    Pre-built for the retry path. Only call this for framework-generated
    text such as the correction prompts produced by
    ``handle_query_with_retry`` — skipping input validation on actual
    user input would defeat the input guard.
    """
    triggered: List[str] = []

    try:
        result = await support_agent.run(query)
        response = result.output
    except Exception as e:
        return {
            "success": False,
            "response": None,
            "error": f"Agent error: {str(e)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
        }

    output_result = OutputGuardrails.validate_output(response)

    if output_result.policy_violations:
        triggered.append("policy_compliance")
        return {
            "success": False,
            "response": response,
            "error": f"Policy violations: {'; '.join(output_result.policy_violations)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
            "validation_details": {
                "errors": output_result.errors,
                "warnings": output_result.warnings,
                "policy_violations": output_result.policy_violations,
            },
        }

    if not output_result.is_valid:
        triggered.append("output_validation")
        return {
            "success": False,
            "response": response,
            "error": f"Output validation failed: {'; '.join(output_result.errors)}",
            "guardrails_triggered": triggered,
            "pii_redacted": {},
            "validation_details": {
                "errors": output_result.errors,
                "warnings": output_result.warnings,
                "policy_violations": output_result.policy_violations,
            },
        }

    redacted_response, pii_found = PIIDetector.redact_pii(response)
    if pii_found:
        triggered.append("pii_redaction")
        response = redacted_response

    return {
        "success": True,
        "response": response,
        "error": None,
        "guardrails_triggered": triggered,
        "pii_redacted": pii_found,
        "quality_score": output_result.quality_score,
    }


async def handle_query_with_retry(
    query: str,
    max_retries: int = 2,
    message_history: Optional[List[ModelMessage]] = None,
) -> Dict:
    """
    Handle query with automatic retry on guardrail failures.

    If output validation or policy compliance fails, retry with a
    correction prompt. Input validation failures are not retried — the
    user's original query was rejected on its own merits.

    The correction prompt is treated as framework-generated text:
    ``handle_query_skipping_input_validation`` runs the post-input-
    validation flow on it directly. The original user question is
    anchored in ``original_query`` so retries do not nest correction
    prompts inside each other.

    Args:
        query: User's query
        max_retries: Maximum retry attempts
        message_history: Conversation history

    Returns:
        Result dictionary
    """
    # Anchored — never reassign across retries.
    original_query = query
    latency_budget_seconds = 10.0
    start_time = time.monotonic()
    total_attempts = 1

    result = await handle_query_with_guardrails(query)

    for attempt in range(max_retries):
        if result["success"]:
            result["attempts"] = total_attempts
            return result

        # Don't retry input validation failures — the user's actual
        # query was rejected, not a framework-generated correction.
        if "input_validation" in result["guardrails_triggered"]:
            result["attempts"] = total_attempts
            return result

        # Only retry output validation or policy failures.
        if not any(
            g in result["guardrails_triggered"]
            for g in ("output_validation", "policy_compliance")
        ):
            result["attempts"] = total_attempts
            return result

        elapsed = time.monotonic() - start_time
        if elapsed >= latency_budget_seconds:
            result["attempts"] = total_attempts
            result["error"] = (
                f"Retry aborted: exceeded latency budget of {latency_budget_seconds:.1f}s"
            )
            return result

        failure_category = (
            "policy_compliance"
            if "policy_compliance" in result["guardrails_triggered"]
            else "output_validation"
        )

        validation_details = result.get("validation_details", {})
        policy_violations = validation_details.get("policy_violations", [])
        errors = validation_details.get("errors", [])
        warnings = validation_details.get("warnings", [])

        if failure_category == "policy_compliance":
            correction_prompt = f"""
The previous response violated policy compliance: {result['error']}

Please provide a response that:
- Is professional and helpful
- Stays within regulated-advice compliance and the company's content policy
- Avoids inappropriate language
- Does not express personal opinions
- Is factual and accurate
- Does not provide financial, legal, or tax advice

Original user question: {original_query}
"""
        else:
            correction_prompt = f"""
The previous response failed output validation: {result['error']}

Please provide a response that:
- Is complete, professional, and helpful
- Avoids generic or inappropriate phrasing
- Meets quality expectations and internal content policy
- Does not express personal opinions
- Is factual and accurate

Original user question: {original_query}
"""

        prompt_preview = " ".join(correction_prompt.strip().split())
        prompt_preview = prompt_preview[:200] + (
            "..." if len(prompt_preview) > 200 else ""
        )

        print(
            f"[Attempt {total_attempts + 1}/{max_retries + 1}] "
            f"Failure category: {failure_category}. "
            f"Sending correction prompt preview: {prompt_preview}"
        )

        total_attempts += 1
        result = await handle_query_skipping_input_validation(correction_prompt)

    result["attempts"] = total_attempts
    return result


async def interactive_session():
    """Run interactive guardrail-protected session."""
    print("=" * 60)
    print("  Financial Services Support Agent")
    print("  (With Comprehensive Guardrails)")
    print("=" * 60)
    print("\nCommands:")
    print("  quit - Exit")
    print("  stats - Show guardrail statistics")
    print()

    # `guardrails` uses defaultdict(int) so Challenge 2 can introduce new
    # guardrail identifiers (e.g. "low_confidence") without students
    # having to remember to pre-register every key. The pre-fix dict
    # raised KeyError as soon as a new guardrail name appeared.
    from collections import defaultdict
    stats = {
        "total_queries": 0,
        "successful": 0,
        "blocked": 0,
        "guardrails": defaultdict(int, {
            "input_validation": 0,
            "output_validation": 0,
            "policy_compliance": 0,
            "pii_redaction": 0,
        }),
    }

    while True:
        query = input("\n\033[1;34mYou: \033[0m").strip()

        if query.lower() == "quit":
            print("\nThank you for using our support service!")
            break

        if query.lower() == "stats":
            print("\n" + "=" * 60)
            print("  Guardrail Statistics")
            print("=" * 60)
            print(f"Total queries: {stats['total_queries']}")
            print(f"Successful: {stats['successful']}")
            print(f"Blocked: {stats['blocked']}")
            print(f"\nGuardrails triggered:")
            for guard, count in stats["guardrails"].items():
                print(f"  {guard}: {count}")
            print("=" * 60)
            continue

        if not query:
            continue

        stats["total_queries"] += 1

        # Process with guardrails and retry
        print("\n\033[1;32mAssistant: \033[0m", end="", flush=True)

        result = await handle_query_with_retry(query, max_retries=2)

        if result["success"]:
            stats["successful"] += 1
            print(result["response"])

            # Show triggered guardrails
            if result["guardrails_triggered"]:
                for guard in result["guardrails_triggered"]:
                    stats["guardrails"][guard] += 1

                print(
                    f"\n\033[1;33m[Note: {', '.join(result['guardrails_triggered'])} applied]\033[0m"
                )

            if result.get("pii_redacted"):
                print(f"\033[1;33m[PII redacted: {result['pii_redacted']}]\033[0m")

        else:
            stats["blocked"] += 1
            print(f"\033[1;31m[Error: {result['error']}]\033[0m")

            for guard in result["guardrails_triggered"]:
                stats["guardrails"][guard] += 1


async def demo():
    """Demonstrate guardrails."""
    print("=" * 60)
    print("  Guardrail Demonstration")
    print("=" * 60)

    test_queries = [
        "What are your business hours?",
        "Tell me about competitor products",
        # Phrased to deterministically match an InputGuardrails
        # RESTRICTED_TOPICS substring ("investment advice"). The
        # original "Should I invest in Bitcoin?" never tripped any guard
        # because none of its words appeared in the substring list, so
        # the headline validation passed silently with the wrong outcome.
        "I need investment advice on which stocks to pick this quarter.",
        "How do I reset my password?",
        "Do you think mortgage rates will fall next year?",
        "My SSN is 123-45-6789, can you help?",
    ]

    for query in test_queries:
        print(f"\n{'─'*60}")
        print(f"Query: {query}")
        print(f"{'─'*60}")

        result = await handle_query_with_retry(query)

        print(f"Success: {result['success']}")
        if result["success"]:
            print(f"Response: {result['response']}")
            if result.get("attempts", 1) > 1:
                print(f"(Required {result['attempts']} attempts)")
        else:
            print(f"Error: {result['error']}")

        if result["guardrails_triggered"]:
            print(f"Guardrails: {', '.join(result['guardrails_triggered'])}")


async def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        await demo()
    else:
        await interactive_session()


if __name__ == "__main__":
    asyncio.run(main())
