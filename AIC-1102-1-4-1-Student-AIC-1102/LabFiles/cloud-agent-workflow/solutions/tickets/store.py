from datetime import datetime, timezone
from itertools import count

from tickets.models import Ticket


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class TicketStore:
    def __init__(self):
        self._tickets = {}
        self._ids = count(1)

    def create(self, title, description):
        ticket_id = next(self._ids)
        now = _now()
        ticket = Ticket(
            id=ticket_id,
            title=title,
            description=description,
            status="open",
            created_at=now,
            updated_at=now,
        )
        self._tickets[ticket_id] = ticket
        return ticket

    def get(self, ticket_id):
        return self._tickets.get(ticket_id)

    def list_all(self):
        return list(self._tickets.values())

    def update_status(self, ticket_id, status):
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            return None
        ticket.status = status
        ticket.updated_at = _now()
        return ticket


store = TicketStore()
