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
    try:
        args = {"order_id": order_id}
        if order_id not in ORDERS:
            analytics.record_call("get_order_status", args, False)
            return f"Order {order_id} not found."

        order = ORDERS[order_id]
        status = order["status"]
        total = order["total"]
        tracking = order["tracking"]

        result = f"Order {order_id}: Status: {status}, Total: ${total:.2f}, Tracking: {tracking}"
        analytics.record_call("get_order_status", args, True)
        return result
    except Exception as exc:
        analytics.record_call("get_order_status", {"order_id": order_id, "error": str(exc)}, False)
        raise
@agent.tool_plain
def check_inventory(product_name: str) -> str:
    """Check if a product is in stock (with analytics tracking)."""
    try:
        args = {"product_name": product_name}
        if product_name not in INVENTORY:
            analytics.record_call("check_inventory", args, False)
            return f"Product '{product_name}' not found in inventory."

        product = INVENTORY[product_name]
        available = product["available"]
        price = product["price"]

        if available > 0:
            result = f"{product_name}: In stock ({available} units available), Price: ${price:.2f}"
            analytics.record_call("check_inventory", args, True)
            return result
        else:
            result = f"{product_name}: Out of stock, Price: ${price:.2f}"
            analytics.record_call("check_inventory", args, True)
            return result
    except Exception as exc:
        analytics.record_call("check_inventory", {"product_name": product_name, "error": str(exc)}, False)
        raise
@agent.tool_plain
def calculate_shipping(destination: str, weight_kg: float) -> str:
    """Calculate shipping cost (with analytics tracking)."""
    try:
        args = {"destination": destination, "weight_kg": weight_kg}

        if weight_kg <= 0:
            analytics.record_call("calculate_shipping", args, False)
            return "Error: Weight must be positive"

        if weight_kg > 30:
            analytics.record_call("calculate_shipping", args, False)
            return "Error: Package exceeds maximum weight limit (30kg)"

        base_rates = {"US": 10.00, "CA": 12.00, "UK": 15.00, "MX": 18.00}
        base_rate = base_rates.get(destination.upper(), 20.00)

        if weight_kg > 1:
            weight_charge = (weight_kg - 1) * 2.00
        else:
            weight_charge = 0

        total_cost = base_rate + weight_charge

        delivery_days = {
            "US": "3-5 business days",
            "CA": "5-7 business days",
            "UK": "7-10 business days",
            "MX": "7-10 business days",
        }

        estimated_delivery = delivery_days.get(destination.upper(), "10-14 business days")

        result = f"Shipping to {destination.upper()}: ${total_cost:.2f}, Estimated delivery: {estimated_delivery}"
        analytics.record_call("calculate_shipping", args, True)
        return result
    except Exception as exc:
        analytics.record_call("calculate_shipping", {"destination": destination, "weight_kg": weight_kg, "error": str(exc)}, False)
        raise
if __name__ == "__main__":
    print("Order status query:")
    result = agent.run_sync("What is the status of order ORD-001?")
    print(result.output)

    print("\nInventory query:")
    result = agent.run_sync("Is Laptop in stock and what is its price?")
    print(result.output)

    print("\nShipping query:")
    result = agent.run_sync("What is the shipping cost to US for a 5kg package?")
    print(result.output)

    # Show analytics summary
    analytics.get_stats()
