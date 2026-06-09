from __future__ import annotations

from notification_dispatcher.application.ports.repositories import NotificationRepository
from notification_dispatcher.domain.models import Notification


class InMemoryNotificationRepository(NotificationRepository):
    def __init__(self) -> None:
        self._notifications: dict[str, Notification] = {}

    def add(self, notification: Notification) -> None:
        self._notifications[notification.id] = notification

    def get(self, notification_id: str) -> Notification | None:
        return self._notifications.get(notification_id)

    def save(self, notification: Notification) -> None:
        self._notifications[notification.id] = notification

    def list_by_recipient(self, recipient: str) -> list[Notification]:
        return [n for n in self._notifications.values() if n.recipient == recipient]
