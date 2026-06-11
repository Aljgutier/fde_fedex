"""
Lab Solution: Conversation Session Management
Tracks conversation metadata, turns, and token usage
"""

from pydantic import BaseModel
from pydantic_ai.messages import ModelMessage
from datetime import datetime
from typing import List, Dict


class ConversationMetadata(BaseModel):
    """Metadata about the conversation."""

    session_id: str
    started_at: datetime
    turn_count: int = 0
    total_tokens: int = 0


class ConversationSession:
    """Manages a conversation session with metadata."""

    def __init__(self, session_id: str):
        self.metadata = ConversationMetadata(
            session_id=session_id, started_at=datetime.now()
        )
        self.history: list[ModelMessage] = []

    def add_turn(self, result):
        """Add a turn to the conversation."""
        # YOUR CODE HERE

    def get_stats(self) -> str:
        """Get conversation statistics."""
        duration = (datetime.now() - self.metadata.started_at).seconds
        avg_tokens = self.metadata.total_tokens // max(1, self.metadata.turn_count)

        return f"""Conversation Stats:
        - Session ID: {self.metadata.session_id}
        - Turns: {self.metadata.turn_count}
        - Duration: {duration}s
        - Total tokens: {self.metadata.total_tokens}
        - Avg tokens/turn: {avg_tokens}
        """


class ConversationBranch:
    """Manages conversation branches for what-if scenarios."""

    def __init__(self, parent_session: ConversationSession):
        self.parent = parent_session
        self.branches: Dict[str, Dict] = {}
        self.active_branch = "main"

    def create_branch(self, branch_name: str):
        """Create new branch from current state."""
        self.branches[branch_name] = {
            "history": list(self.parent.history),
            "created_at": datetime.now(),
        }

    def switch_branch(self, branch_name: str) -> bool:
        """Switch to a branch.

        "main" is the implicit default branch — its history lives on the
        parent ConversationSession (`self.parent.history`) rather than in
        `self.branches`. Without this special case, `switch_branch("main")`
        returned False because "main" was never registered as a branch
        name, even though `get_active_history`, `update_active_history`,
        and `list_branches` all already special-case it. The pre-fix
        runner papered over this by routing `/main` outside the method;
        the public API now matches the rest of the class.
        """
        if branch_name == "main" or branch_name in self.branches:
            self.active_branch = branch_name
            return True
        return False

    def list_branches(self) -> List[str]:
        """List all available branches."""
        return ["main"] + list(self.branches.keys())

    def get_active_history(self) -> List[ModelMessage]:
        """Get history for active branch."""
        if self.active_branch == "main":
            return self.parent.history
        return self.branches[self.active_branch]["history"]

    def update_active_history(self, history: List[ModelMessage]):
        """Update history for active branch."""
        if self.active_branch == "main":
            self.parent.history = history
        else:
            self.branches[self.active_branch]["history"] = history
