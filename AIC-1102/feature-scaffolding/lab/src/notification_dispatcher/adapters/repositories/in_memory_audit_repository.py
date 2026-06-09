from __future__ import annotations

from notification_dispatcher.application.ports.repositories import AuditRepository
from notification_dispatcher.domain.models import AuditEntry


class InMemoryAuditRepository(AuditRepository):
    def __init__(self) -> None:
        self._entries_by_notification_id: dict[str, list[AuditEntry]] = {}

    def append(self, entry: AuditEntry) -> None:
        bucket = self._entries_by_notification_id.setdefault(entry.notification_id, [])
        bucket.append(entry)

    def list_for_notification(self, notification_id: str) -> list[AuditEntry]:
        return list(self._entries_by_notification_id.get(notification_id, []))
