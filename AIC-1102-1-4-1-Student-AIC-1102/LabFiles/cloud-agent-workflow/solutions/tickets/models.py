from dataclasses import dataclass

VALID_STATUSES = ("open", "in_progress", "resolved", "closed")


@dataclass
class Ticket:
    id: int
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str
