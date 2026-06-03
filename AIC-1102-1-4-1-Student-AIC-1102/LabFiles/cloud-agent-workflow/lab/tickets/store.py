from datetime import datetime, timezone
from itertools import count

from tickets.models import Ticket


class TicketStore:
    def __init__(self):
        self._tickets = {}
        self._ids = count(1)

    def create(self, title, description):
        ticket_id = next(self._ids)
        ticket = Ticket(
            id=ticket_id,
            title=title,
            description=description,
            status="open",
            created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        self._tickets[ticket_id] = ticket
        return ticket

    def get(self, ticket_id):
        return self._tickets.get(ticket_id)

    def list_all(self):
        return list(self._tickets.values())


store = TicketStore()
