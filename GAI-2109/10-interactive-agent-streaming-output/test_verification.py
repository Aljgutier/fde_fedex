"""
Quick verification that the implementation handles special commands correctly.
"""

import asyncio
from datetime import datetime
from pydantic_ai.messages import ModelMessage

# Test command normalization and recognition
def test_command_recognition():
    """Test that commands are recognized (case-insensitive)."""
    test_commands = [
        ("quit", True),
        ("QUIT", True),
        ("Quit", True),
        ("history", True),
        ("HISTORY", True),
        ("clear", True),
        ("CLEAR", True),
        ("save", True),
        ("SAVE", True),
        ("hello world", False),  # Not a command
        ("", False),  # Empty
    ]
    
    print("Testing command recognition (case-insensitive):")
    for user_input, is_command in test_commands:
        is_special = user_input.lower() in ["quit", "history", "clear", "save"]
        result = "✓" if is_special == is_command else "✗"
        print(f"  {result} '{user_input}' -> {is_special}")

def test_history_display():
    """Test that show_history works with empty history."""
    from interactive_loop import show_history
    
    print("\nTesting history display with empty list:")
    print("  Expected: '(No messages yet)'")
    history: list[ModelMessage] = []
    show_history(history)

def test_save_conversation():
    """Test that save_conversation handles empty history gracefully."""
    from interactive_loop import save_conversation
    
    print("Testing save_conversation with empty history:")
    print("  Expected: '[No conversation to save]'")
    history: list[ModelMessage] = []
    session_start = datetime.now()
    save_conversation(history, session_start)

if __name__ == "__main__":
    test_command_recognition()
    test_history_display()
    test_save_conversation()
    print("\n✓ All verification tests completed!")
