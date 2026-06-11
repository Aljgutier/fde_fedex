"""
Interactive Streaming Conversation Loop

Demonstrates multi-turn streaming conversations with:
- Message history persistence across turns
- Real-time streaming display
- Interactive commands (quit, history, clear)
- Conversation context management

Run:
    python interactive_loop.py
"""

import os
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()

# Create creative writing assistant
agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a creative writing assistant.
    Help develop story elements through collaborative conversation.
    Remember previous context and build upon it naturally.
    Be encouraging and offer creative suggestions.""",
)


async def interactive_session():
    """
    Run interactive streaming conversation.

    Features:
    - Multi-turn conversations with history
    - Real-time streaming responses
    - Special commands: quit, history, clear, save
    - Automatic history management
    """
    print("=" * 60)
    print("  Creative Writing Assistant - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  quit    - Exit the session")
    print("  history - Show conversation history")
    print("  clear   - Clear conversation history")
    print("  save    - Save conversation to file")
    print()

    # Track conversation history
    history: list[ModelMessage] = []
    session_start = datetime.now()
    turn_count = 0

    while True:
        # Get user input
        try:
            user_input = input("\n\033[1;34mYou: \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! Happy writing!")
            break

        # YOUR CODE HERE

        if not user_input:
            continue

        # YOUR CODE HERE


def show_history(history: list[ModelMessage]):
    """Display conversation history with formatting."""
    print(f"\n{'='*60}")
    print(f"  Conversation History ({len(history)} messages)")
    print(f"{'='*60}\n")

    if not history:
        print("  (No messages yet)")
        print()
        return

    for i, msg in enumerate(history, 1):
        # Determine message type and format accordingly
        if isinstance(msg, ModelRequest):
            role = "USER"
            color = "\033[1;34m"  # Blue

            # Extract content from parts
            if hasattr(msg, "parts") and msg.parts:
                content = ""
                for part in msg.parts:
                    if hasattr(part, "content"):
                        content += str(part.content)
                    elif isinstance(part, str):
                        content += part
            else:
                content = str(msg)

        elif isinstance(msg, ModelResponse):
            role = "ASSISTANT"
            color = "\033[1;32m"  # Green

            # Extract content from parts
            if hasattr(msg, "parts") and msg.parts:
                content = ""
                for part in msg.parts:
                    if hasattr(part, "content"):
                        content += str(part.content)
                    elif isinstance(part, str):
                        content += part
            else:
                content = str(msg)
        else:
            role = "SYSTEM"
            color = "\033[1;33m"  # Yellow
            content = str(msg)

        # Truncate long messages
        max_length = 100
        if len(content) > max_length:
            content = content[:max_length] + "..."

        print(f"{color}[{i}] {role}\033[0m: {content}")

    print()


def save_conversation(history: list[ModelMessage], session_start: datetime):
    """Save conversation to a file."""
    # YOUR CODE HERE
    pass


async def guided_story_development():
    """
    Guided multi-turn story development session.

    Demonstrates structured conversation flow with streaming.
    """
    print("=" * 60)
    print("  Guided Story Development")
    print("=" * 60)
    print("\nLet's develop a story together!\n")

    # YOUR CODE HERE
    pass


async def main():
    """Main entry point with mode selection."""
    print("\n\033[1;35mSelect mode:\033[0m")
    print("  1 - Interactive conversation (free-form)")
    print("  2 - Guided story development (structured)")
    print()

    choice = input("Choice (1 or 2): ").strip()

    if choice == "2":
        await guided_story_development()
    else:
        await interactive_session()


if __name__ == "__main__":
    asyncio.run(main())
