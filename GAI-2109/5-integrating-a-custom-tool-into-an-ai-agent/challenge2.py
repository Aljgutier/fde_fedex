import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime
from mock_database import ORDERS, INVENTORY

load_dotenv()


class ToolAnalytics:
    """Track tool usage statistics for monitoring and optimization."""

    def __init__(self):
        self.call_counts = defaultdict(int)
        self.call_history = []

    def record_call(self, tool_name: str, args: dict, success: bool):
        """Record a tool invocation with timestamp."""
        self.call_counts[tool_name] += 1
        self.call_history.append(
            {
                "timestamp": datetime.now(),
                "tool": tool_name,
                "args": args,
                "success": success,
            }
        )

    def get_stats(self):
        """Display usage statistics."""
        total = sum(self.call_counts.values())
        print(f"\nTool Usage Statistics ({total} total calls):")
        print("=" * 50)
        for tool, count in sorted(
            self.call_counts.items(), key=lambda x: x[1], reverse=True
        ):
            pct = (count / total) * 100 if total > 0 else 0
            print(f"  {tool}: {count} calls ({pct:.1f}%)")

        print(f"\nMost recent calls:")
        for call in self.call_history[-5:]:  # Show last 5 calls
            timestamp = call["timestamp"].strftime("%H:%M:%S")
            status = "✓" if call["success"] else "✗"
            print(f"  {status} [{timestamp}] {call['tool']} - {call['args']}")


# Initialize analytics tracker
analytics = ToolAnalytics()

agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a customer service assistant with tool analytics.
    Use your tools to provide accurate information about orders, inventory, and shipping.""",
)


@agent.tool_plain
def get_order_status(order_id: str) -> str:
    """Look up the current status of an order (with analytics tracking)."""
    # YOUR CODE HERE
    # Hint: Wrap the tool logic with analytics.record_call()
    pass
@agent.tool_plain
def check_inventory(product_name: str) -> str:
    """Check if a product is in stock (with analytics tracking)."""
    # YOUR CODE HERE
    # Hint: Record analytics for both success and failure cases
    pass
@agent.tool_plain
def calculate_shipping(destination: str, weight_kg: float) -> str:
    """Calculate shipping cost (with analytics tracking)."""
    # YOUR CODE HERE
    # Hint: Track analytics at multiple exit points (validation failures and success)
    pass
if __name__ == "__main__":
    # YOUR CODE HERE
    pass
