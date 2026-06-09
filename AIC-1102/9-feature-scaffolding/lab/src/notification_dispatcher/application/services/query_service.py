from __future__ import annotations

from notification_dispatcher.application.dto import NotificationView
from notification_dispatcher.application.ports.repositories import NotificationRepository


class QueryService:
    def __init__(self, notification_repository: NotificationRepository) -> None:
        self._notification_repository = notification_repository

    def get_notification(self, notification_id: str) -> NotificationView | None:
        notification = self._notification_repository.get(notification_id)
        if notification is None:
            return None
        return NotificationView(
            id=notification.id,
            recipient=notification.recipient,
            channels=list(notification.channels),
            subject=notification.subject,
            body=notification.body,
            status=notification.status,
            created_at=notification.created_at,
            updated_at=notification.updated_at,
        )

    def list_for_recipient(self, recipient: str) -> list[NotificationView]:
        notifications = self._notification_repository.list_by_recipient(recipient)
        return [
            NotificationView(
                id=notification.id,
                recipient=notification.recipient,
                channels=list(notification.channels),
                subject=notification.subject,
                body=notification.body,
                status=notification.status,
                created_at=notification.created_at,
                updated_at=notification.updated_at,
            )
            for notification in notifications
        ]
