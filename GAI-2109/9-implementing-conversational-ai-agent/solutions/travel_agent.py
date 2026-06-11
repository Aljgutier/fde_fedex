"""
Lab Solution: Implementing Conversational Memory in an AI Agent
Demonstrates multi-turn conversation with various memory strategies
"""

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic import BaseModel
from dotenv import load_dotenv
from conversation import ConversationSession, ConversationBranch
from memory_strategies import (
    SlidingWindowMemory,
    SummaryMemory,
    HybridMemory,
    AdaptiveMemory,
)
import uuid
import os
from typing import Optional

load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. "
        "Make sure .env file exists in the same directory as this script."
    )

# Get model from environment variable
model = os.getenv("AI_MODEL", "openai:gpt-5.4-mini")
print(f"Using model: {model}")

# Main travel planning agent
agent = Agent(
    model,
    system_prompt="""You are a helpful travel planning assistant.
    Help users plan trips by asking about their preferences,
    making recommendations, and answering questions.
    Remember details from the conversation.""",
)


class ClarificationCheck(BaseModel):
    """Result of checking if clarification is needed."""

    needs_clarification: bool
    question: Optional[str] = None
    confidence: float


# Agent for detecting ambiguity and suggesting clarifications
clarification_agent = Agent(
    model,
    output_type=ClarificationCheck,
    system_prompt="""Analyze if the user's request is clear enough to act on.
    If ambiguous, suggest a clarifying question.
    Be helpful but don't over-clarify obvious requests.""",
)


def run_basic_conversation():
    """
    Run basic interactive conversation with memory.
    Demonstrates fundamental conversation history management.
    """
    print("=" * 60)
    print("Basic Conversation with Memory")
    print("=" * 60)
    print("Travel Assistant: Hello! I'm here to help plan your trip.")
    print("Type 'quit' to exit.\n")

    # Store conversation history
    history: list[ModelMessage] = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Travel Assistant: Goodbye! Have a great trip!")
            break

        if not user_input:
            continue

        # Run agent with conversation history
        result = agent.run_sync(user_input, message_history=history)

        print(f"Travel Assistant: {result.output}\n")

        # Update history with this exchange
        history = result.all_messages()


def run_conversation_with_stats():
    """
    Run conversation with session tracking and statistics.
    Type 'stats' to see conversation metrics.
    """
    print("=" * 60)
    print("Conversation with Statistics Tracking")
    print("=" * 60)
    print("Commands: 'stats' (view metrics), 'quit' (exit)")
    print("=" * 60)

    session = ConversationSession(session_id=str(uuid.uuid4()))

    print("Travel Assistant: Hello! I'm here to help plan your trip.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "stats":
            print(session.get_stats())
            continue

        if user_input.lower() in ["quit", "exit"]:
            print("\n" + session.get_stats())
            print("Travel Assistant: Goodbye! Have a great trip!")
            break

        if not user_input:
            continue

        result = agent.run_sync(user_input, message_history=session.history)

        print(f"Travel Assistant: {result.output}\n")
        session.add_turn(result)


def run_conversation_with_sliding_window():
    """
    Conversation with sliding window memory.
    Keeps only recent messages to limit context.
    """
    print("=" * 60)
    print("Conversation with Sliding Window Memory (6 messages)")
    print("=" * 60)
    print("Try a long conversation (10+ turns) to see older messages drop out")
    print("=" * 60)

    # YOUR CODE HERE
    # [SOLUTION]
    session = ConversationSession(session_id=str(uuid.uuid4()))
    memory = SlidingWindowMemory(window_size=6)
    # [/SOLUTION]

    print("Travel Assistant: Hello!\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(session.get_stats())
            break

        if not user_input:
            continue

        # YOUR CODE HERE
        # [SOLUTION]
        # Apply sliding window to history
        windowed_history = memory.apply(session.history)

        result = agent.run_sync(user_input, message_history=windowed_history)

        print(f"Travel Assistant: {result.output}\n")
        session.add_turn(result)

        # Show memory status
        total = len(session.history)
        windowed = len(windowed_history)
        print(f"[Memory: {windowed}/{total} messages in context]\n")
        # [/SOLUTION]


def run_conversation_with_summary():
    """
    Conversation with summary-based memory.
    Summarizes older exchanges, keeps recent ones verbatim.
    """
    print("=" * 60)
    print("Conversation with Summary-Based Memory")
    print("=" * 60)
    print("After 8 turns, older context will be summarized")
    print("=" * 60)

    session = ConversationSession(session_id=str(uuid.uuid4()))
    memory = SummaryMemory(summarize_after=8, keep_recent=4)

    print("Travel Assistant: Hello!\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(session.get_stats())
            break

        if not user_input:
            continue

        # Apply summary-based memory
        processed_history = memory.apply(session.history)

        result = agent.run_sync(user_input, message_history=processed_history)

        print(f"Travel Assistant: {result.output}\n")
        session.add_turn(result)

        # Show memory status
        total = len(session.history)
        if len(session.history) > memory.summarize_after:
            print(f"[Using summary + {memory.keep_recent} recent messages]\n")
        else:
            print(f"[Full history: {total} messages]\n")


def run_conversation_with_hybrid():
    """
    Conversation with hybrid memory strategy.
    Automatically adapts based on conversation length.
    """
    print("=" * 60)
    print("Conversation with Hybrid Memory Strategy")
    print("=" * 60)
    print("Memory strategy adapts automatically as conversation grows")
    print("=" * 60)

    session = ConversationSession(session_id=str(uuid.uuid4()))
    memory = HybridMemory(max_messages=20, summarize_threshold=15, keep_recent=6)

    print("Travel Assistant: Hello!\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(session.get_stats())
            break

        if not user_input:
            continue

        # Apply hybrid memory strategy
        optimized_history = memory.apply(session.history)

        result = agent.run_sync(user_input, message_history=optimized_history)

        print(f"Travel Assistant: {result.output}\n")
        session.add_turn(result)

        # Show current strategy
        total = len(session.history)
        if total <= memory.max_messages:
            strategy = "full history"
        elif total <= memory.summarize_threshold:
            strategy = "sliding window"
        else:
            strategy = "summary + recent"

        print(f"[Strategy: {strategy}, Messages: {total}]\n")


def run_conversation_with_clarification():
    """
    Conversation with proactive clarification.
    Agent asks for clarification when input is ambiguous.
    """
    print("=" * 60)
    print("Conversation with Human-in-the-Loop Clarification")
    print("=" * 60)
    print("Try ambiguous requests like 'I want to go somewhere warm'")
    print("=" * 60)

    session = ConversationSession(session_id=str(uuid.uuid4()))

    print("Travel Assistant: Hello! How can I help you plan your trip?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print(session.get_stats())
            break

        if not user_input:
            continue

        # Check if clarification needed
        check_result = clarification_agent.run_sync(
            f"Is this travel request clear enough to act on: '{user_input}'?",
            message_history=session.history,
        )

        check = check_result.output

        # Ask for clarification if needed and confident
        if check.needs_clarification and check.confidence > 0.7:
            print(f"Travel Assistant: {check.question}\n")

            # Get clarification
            clarification = input("You: ").strip()
            if clarification:
                user_input = f"{user_input}. Specifically: {clarification}"

        # Process with full context
        result = agent.run_sync(user_input, message_history=session.history)

        print(f"Travel Assistant: {result.output}\n")
        session.add_turn(result)


def run_conversation_with_branches():
    """
    Conversation with branch support.
    Explore what-if scenarios without losing main thread.
    """
    print("=" * 60)
    print("Conversation with Branching Support")
    print("=" * 60)
    print("Commands:")
    print("  /branch <name>  - Create new branch from current state")
    print("  /switch <name>  - Switch to a branch")
    print("  /branches       - List all branches")
    print("  /main           - Switch to main thread")
    print("=" * 60)

    session = ConversationSession(session_id=str(uuid.uuid4()))
    branches = ConversationBranch(session)

    print("\nTravel Assistant: Hello! Let's plan your trip.\n")

    while True:
        user_input = input(f"[{branches.active_branch}] You: ").strip()

        # Handle branch commands
        if user_input.startswith("/branch "):
            name = user_input.split(maxsplit=1)[1]
            branches.create_branch(name)
            print(f"✓ Created branch: {name}\n")
            continue

        if user_input.startswith("/switch "):
            name = user_input.split(maxsplit=1)[1]
            if branches.switch_branch(name):
                print(f"✓ Switched to: {name}\n")
            else:
                print(f"✗ Branch '{name}' not found\n")
            continue

        if user_input == "/branches":
            branches_list = branches.list_branches()
            print(f"Available branches: {', '.join(branches_list)}\n")
            continue

        if user_input == "/main":
            branches.active_branch = "main"
            print("✓ Switched to main thread\n")
            continue

        if user_input.lower() in ["quit", "exit"]:
            print(session.get_stats())
            break

        if not user_input:
            continue

        # Get history for active branch
        history = branches.get_active_history()

        # Run agent
        result = agent.run_sync(user_input, message_history=history)
        print(f"Travel Assistant: {result.output}\n")

        # Update active branch history
        updated_history = result.all_messages()
        branches.update_active_history(updated_history)

        # Update session if on main branch
        if branches.active_branch == "main":
            session.add_turn(result)


def main():
    """Main entry point - run different conversation modes."""
    print("\n" + "=" * 60)
    print("Conversational Memory Lab - Solution Demonstrator")
    print("=" * 60)
    print("\nSelect a conversation mode:")
    print("1. Basic conversation with memory")
    print("2. Conversation with statistics tracking")
    print("3. Sliding window memory (limits context)")
    print("4. Summary-based memory (condenses old context)")
    print("5. Hybrid memory (auto-adapts strategy)")
    print("6. Human-in-the-loop clarification")
    print("7. Conversation branching (what-if scenarios)")
    print("\n0. Exit")
    print("=" * 60)

    choice = input("\nEnter choice (1-7): ").strip()

    modes = {
        "1": run_basic_conversation,
        "2": run_conversation_with_stats,
        "3": run_conversation_with_sliding_window,
        "4": run_conversation_with_summary,
        "5": run_conversation_with_hybrid,
        "6": run_conversation_with_clarification,
        "7": run_conversation_with_branches,
    }

    if choice in modes:
        print()
        modes[choice]()
    elif choice == "0":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again and select 1-7.")


if __name__ == "__main__":
    main()
