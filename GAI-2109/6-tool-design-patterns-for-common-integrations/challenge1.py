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
    try:
        # Check for duplicate request
        if idempotency_key and idempotency_key in processed_requests:
            logger.info(
                "Duplicate request detected for idempotency_key: %s",
                idempotency_key,
            )
            return processed_requests[idempotency_key]

        # Validate user exists
        result = get_user(user_id)
        if not result["success"]:
            response = ToolResponse(
                success=False,
                error_type="UserNotFound",
                error_message=f"User {user_id} not found",
            )
            return response.model_dump_json()

        # Get current user data
        current_user = USERS[user_id]
        changed_fields = {}

        # Mutate only supplied fields that differ
        if email is not None and email != current_user.get("email"):
            changed_fields["email"] = {
                "old": current_user.get("email"),
                "new": email,
            }
            current_user["email"] = email

        if tier is not None and tier != current_user.get("tier"):
            changed_fields["tier"] = {"old": current_user.get("tier"), "new": tier}
            current_user["tier"] = tier

        # Build success response
        response = ToolResponse(
            success=True,
            data={
                "user": current_user,
                "changed_fields": changed_fields,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Cache the response if idempotency_key supplied
        response_json = response.model_dump_json()
        if idempotency_key:
            processed_requests[idempotency_key] = response_json
            logger.info("Cached response for idempotency_key: %s", idempotency_key)

        return response_json

    except Exception as e:
        logger.error("Update error: %s", e)
        response = ToolResponse(
            success=False, error_type="UpdateError", error_message=str(e)
        )
        return response.model_dump_json()
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TEST CASE 1: Initial update with idempotency key")
    print("=" * 80)
    result1 = agent.run_sync(
        "Update user-001's email to alice.new@example.com using idempotency key idem-001"
    )
    print(f"\n{result1.output}\n")

    print("=" * 80)
    print("TEST CASE 2: Duplicate request with same idempotency key")
    print("(Should return cached result from TEST CASE 1, not apply new email)")
    print("=" * 80)
    result2 = agent.run_sync(
        "Update user-001's email to different.email@example.com using the same idempotency key idem-001"
    )
    print(f"\n{result2.output}\n")
    print("(Note: The email should still be alice.new@example.com from the first request)\n")

    print("=" * 80)
    print("TEST CASE 3: Different user with new idempotency key")
    print("=" * 80)
    result3 = agent.run_sync(
        "Update user-002's tier to premium using idempotency key idem-002"
    )
    print(f"\n{result3.output}\n")
