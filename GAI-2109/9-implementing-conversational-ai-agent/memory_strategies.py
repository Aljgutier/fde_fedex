"""
Lab Starter: Memory Management Strategies
Implements sliding window, summary-based, and hybrid memory strategies
"""

from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    UserPromptPart,
)
from dotenv import load_dotenv
from typing import List, Optional
import os

load_dotenv()


# Summary agent for condensing conversation history
summary_agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""Summarize conversation history concisely.
    Focus on key facts, decisions, and preferences.
    Keep summary under 200 words.""",
)


class SlidingWindowMemory:
    """Keep only the N most recent messages."""

    def __init__(self, window_size: int = 10):
        """
        Initialize sliding window memory.

        Args:
            window_size: Number of recent messages to keep
        """
        self.window_size = window_size

    def apply(self, history: List[ModelMessage]) -> List[ModelMessage]:
        """
        Return most recent messages within window.

        Args:
            history: Full conversation history

        Returns:
            Truncated history with only recent messages
        """
        # YOUR CODE HERE


class SummaryMemory:
    """Summarize older messages, keep recent ones."""

    def __init__(self, summarize_after: int = 10, keep_recent: int = 4):
        """
        Initialize summary-based memory.

        Args:
            summarize_after: Number of messages before summarization kicks in
            keep_recent: Number of recent messages to keep verbatim
        """
        self.summarize_after = summarize_after
        self.keep_recent = keep_recent
        self.summary: Optional[str] = None

    def apply(self, history: List[ModelMessage]) -> List[ModelMessage]:
        """
        Summarize old messages, keep recent ones.

        Args:
            history: Full conversation history

        Returns:
            Summary + recent messages
        """
        if len(history) <= self.summarize_after:
            return history

        # Split into old and recent
        old_messages = history[: -self.keep_recent]
        recent_messages = history[-self.keep_recent :]

        # Generate summary if not cached
        if not self.summary:
            conversation_text = self._format_messages(old_messages)
            result = summary_agent.run_sync(
                f"Summarize this conversation:\n\n{conversation_text}"
            )
            self.summary = result.output

        # Create synthetic system message with summary
        summary_msg = ModelRequest(
            parts=[
                SystemPromptPart(
                    content=f"Previous conversation summary: {self.summary}"
                )
            ]
        )

        return [summary_msg] + recent_messages

    def _format_messages(self, messages: List[ModelMessage]) -> str:
        """
        Format messages for summarization.

        Pydantic AI's ModelMessage union (ModelRequest / ModelResponse)
        does not expose top-level `.role` or `.content` attributes — the
        text lives inside `.parts` as part-kind-specific objects. Walk
        the parts and pull text from UserPromptPart / TextPart, tagging
        each line with USER / ASSISTANT / SYSTEM so the summarizer agent
        sees a structured transcript rather than an empty string.

        Args:
            messages: List of messages to format

        Returns:
            Formatted conversation text
        """
        formatted = []
        for msg in messages:
            for part in getattr(msg, "parts", []):
                if isinstance(part, UserPromptPart):
                    formatted.append(f"USER: {part.content}")
                elif isinstance(part, TextPart):
                    formatted.append(f"ASSISTANT: {part.content}")
                elif isinstance(part, SystemPromptPart):
                    formatted.append(f"SYSTEM: {part.content}")
        return "\n\n".join(formatted)

    def reset_summary(self):
        """Clear cached summary to force regeneration."""
        self.summary = None


class HybridMemory:
    """Combine summary and sliding window strategies."""

    def __init__(
        self,
        max_messages: int = 10,
        summarize_threshold: int = 20,
        keep_recent: int = 6,
    ):
        """
        Initialize hybrid memory strategy.

        Threshold ordering: ``max_messages < summarize_threshold``. The
        previous defaults (``max_messages=20`` / ``summarize_threshold=15``)
        had Phase 1 (``<= max_messages``) subsuming Phase 2's range, so
        Phase 2 was unreachable and the sliding-window phase never fired.
        Defaults now express three distinct phases:

        * ``msg_count <= max_messages`` (≤10) → return full history.
        * ``msg_count <= summarize_threshold`` (11–20) → sliding window,
          keep last ``max_messages``.
        * ``msg_count > summarize_threshold`` (>20) → summary + last
          ``keep_recent``.

        Args:
            max_messages: Window size used in Phase 2 (and the upper
                bound below which we keep everything in Phase 1).
            summarize_threshold: Above this, switch to summary + recent
                (Phase 3) instead of sliding window.
            keep_recent: Number of recent messages to keep verbatim
                alongside the summary in Phase 3.
        """
        if max_messages >= summarize_threshold:
            raise ValueError(
                "HybridMemory requires max_messages < summarize_threshold "
                f"(got {max_messages=} >= {summarize_threshold=}); otherwise "
                "Phase 2 (sliding window) is unreachable."
            )
        self.max_messages = max_messages
        self.summarize_threshold = summarize_threshold
        self.keep_recent = keep_recent
        self.summary: Optional[str] = None

    def apply(self, history: List[ModelMessage]) -> List[ModelMessage]:
        """
        Apply hybrid memory strategy.

        Phases:
        1. No limit needed (< max_messages)
        2. Apply sliding window (< summarize_threshold)
        3. Summarize old + keep recent (> summarize_threshold)

        Args:
            history: Full conversation history

        Returns:
            Optimized conversation history
        """
        msg_count = len(history)

        # Phase 1: No limit needed
        if msg_count <= self.max_messages:
            return history

        # Phase 2: Apply sliding window
        if msg_count <= self.summarize_threshold:
            return history[-self.max_messages :]

        # Phase 3: Summarize old + keep recent
        if not self.summary:
            old = history[: -self.keep_recent]
            # Walk parts — see SummaryMemory._format_messages for the
            # rationale (ModelMessage doesn't expose top-level .content).
            lines = []
            for m in old:
                for part in getattr(m, "parts", []):
                    if isinstance(part, UserPromptPart):
                        lines.append(f"USER: {part.content}")
                    elif isinstance(part, TextPart):
                        lines.append(f"ASSISTANT: {part.content}")
                    elif isinstance(part, SystemPromptPart):
                        lines.append(f"SYSTEM: {part.content}")
            conversation_text = "\n".join(lines)

            result = summary_agent.run_sync(
                f"Summarize concisely:\n{conversation_text}"
            )
            self.summary = result.output

        # Create summary message
        summary_msg = ModelRequest(
            parts=[SystemPromptPart(content=f"Context summary: {self.summary}")]
        )
        recent = history[-self.keep_recent :]

        return [summary_msg] + recent

    def reset_summary(self):
        """Clear cached summary to force regeneration."""
        self.summary = None


class AdaptiveMemory:
    """Automatically choose strategy based on conversation length."""

    def __init__(self):
        """Initialize adaptive memory with multiple strategies."""
        self.full_history_limit = 10
        self.window_strategy = SlidingWindowMemory(window_size=15)
        self.summary_strategy = SummaryMemory(summarize_after=20, keep_recent=6)

    def apply(self, history: List[ModelMessage]) -> List[ModelMessage]:
        """
        Choose and apply appropriate strategy.

        Args:
            history: Full conversation history

        Returns:
            Optimized conversation history
        """
        msg_count = len(history)

        # Short conversations: keep everything
        if msg_count <= self.full_history_limit:
            return history

        # Medium conversations: sliding window
        if msg_count <= 20:
            return self.window_strategy.apply(history)

        # Long conversations: summarize
        return self.summary_strategy.apply(history)

    def get_current_strategy(self, history: List[ModelMessage]) -> str:
        """Get name of currently applied strategy."""
        msg_count = len(history)

        if msg_count <= self.full_history_limit:
            return "full_history"
        elif msg_count <= 20:
            return "sliding_window"
        else:
            return "summary"
