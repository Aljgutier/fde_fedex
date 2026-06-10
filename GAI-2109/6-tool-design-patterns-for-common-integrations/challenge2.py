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
    # YOUR CODE HERE
    pass
def log_with_correlation(message: str, level: str = "INFO"):
    """Log message with correlation ID."""
    # YOUR CODE HERE
    pass
agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a customer service assistant with comprehensive
    access to user and order information. Use your tools to provide accurate
    information.""",
)


@agent.tool_plain
def lookup_user(user_id: str) -> str:
    """Look up user with correlation tracking."""
    # YOUR CODE HERE
    pass
@agent.tool_plain
def search_user_orders(
    user_id: Optional[str] = None, status: Optional[str] = None
) -> str:
    """Search orders with correlation tracking."""
    # YOUR CODE HERE
    pass
if __name__ == "__main__":
    # YOUR CODE HERE
    pass
