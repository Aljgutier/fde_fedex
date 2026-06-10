import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from typing import Optional
import logging
import contextvars
import uuid

# Configure logging with custom format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# Import tools
from tools.api_tools import lookup_user as lookup_user_impl
from tools.api_tools import search_user_orders as search_orders_impl

# Thread-local correlation ID storage
correlation_id_var = contextvars.ContextVar("correlation_id", default=None)


def get_correlation_id() -> str:
    """Get or create correlation ID for current request."""
    current_id = correlation_id_var.get()
    if current_id is None:
        current_id = str(uuid.uuid4())
        correlation_id_var.set(current_id)
    return current_id
def log_with_correlation(message: str, level: str = "INFO"):
    """Log message with correlation ID."""
    correlation_id = get_correlation_id()
    formatted_message = f"[correlation_id={correlation_id}] {message}"
    log_level = getattr(logging, level)
    logger.log(log_level, formatted_message)
agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a customer service assistant with comprehensive
    access to user and order information. Use your tools to provide accurate
    information.""",
)


@agent.tool_plain
def lookup_user(user_id: str) -> str:
    """Look up user with correlation tracking."""
    log_with_correlation(f"Starting lookup_user for user_id={user_id}")
    try:
        result = lookup_user_impl(user_id)
        log_with_correlation(f"Completed lookup_user for user_id={user_id}")
        return result
    except Exception as e:
        log_with_correlation(f"Error in lookup_user for user_id={user_id}: {e}", "ERROR")
        raise
@agent.tool_plain
def search_user_orders(
    user_id: Optional[str] = None, status: Optional[str] = None
) -> str:
    """Search orders with correlation tracking."""
    log_with_correlation(f"Starting search_user_orders for user_id={user_id}, status={status}")
    try:
        result = search_orders_impl(user_id, status)
        log_with_correlation(f"Completed search_user_orders for user_id={user_id}, status={status}")
        return result
    except Exception as e:
        log_with_correlation(f"Error in search_user_orders for user_id={user_id}, status={status}: {e}", "ERROR")
        raise
if __name__ == "__main__":
    # Test 1: Single-tool lookup request
    print("\n" + "="*80)
    print("REQUEST 1: Single-tool lookup")
    print("="*80)
    correlation_id_var.set(str(uuid.uuid4()))
    log_with_correlation("Request started - lookup user")
    response1 = agent.run_sync("Look up user user-123")
    log_with_correlation("Request completed - lookup user")
    print(f"\nAgent Response:\n{response1.output}\n")
    
    # Test 2: Multi-tool request that forces both tools to fire
    print("\n" + "="*80)
    print("REQUEST 2: Multi-tool query (lookup + search orders)")
    print("="*80)
    correlation_id_var.set(str(uuid.uuid4()))
    log_with_correlation("Request started - lookup and search orders")
    response2 = agent.run_sync("Can you look up user user-456 and find all their pending orders?")
    log_with_correlation("Request completed - lookup and search orders")
    print(f"\nAgent Response:\n{response2.output}\n")
    
    # Test 3: Search-only query
    print("\n" + "="*80)
    print("REQUEST 3: Search-only query")
    print("="*80)
    correlation_id_var.set(str(uuid.uuid4()))
    log_with_correlation("Request started - search orders")
    response3 = agent.run_sync("Find all completed orders in the system")
    log_with_correlation("Request completed - search orders")
    print(f"\nAgent Response:\n{response3.output}\n")
