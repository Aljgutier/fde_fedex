import os
from pydantic_ai import Agent
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
import logging
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Import mock API and models
from mock_api import USERS, get_user
from tools.models import ToolResponse


class UpdateRequest(BaseModel):
    """User update request."""

    user_id: str
    email: Optional[str] = None
    tier: Optional[str] = None
    idempotency_key: str  # Prevents duplicate operations


# Track processed requests for idempotency
processed_requests = {}

agent = Agent(
    os.getenv("AI_MODEL", "openai:gpt-5.4-mini"),
    system_prompt="""You are a customer service assistant with the ability
    to update user account information. Always use unique idempotency keys
    for update operations to prevent duplicate processing.""",
)


@agent.tool_plain
def update_user(
    user_id: str,
    email: Optional[str] = None,
    tier: Optional[str] = None,
    idempotency_key: str = None,
) -> str:
    """
    Update user information idempotently.

    Args:
        user_id: User to update
        email: New email (optional)
        tier: New tier (optional)
        idempotency_key: Unique request identifier

    Returns:
        Update result with idempotency protection
    """
    # YOUR CODE HERE
    pass
if __name__ == "__main__":
    # YOUR CODE HERE
    pass
