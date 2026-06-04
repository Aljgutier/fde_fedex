from __future__ import annotations

from typing import Protocol

from notification_dispatcher.domain.models import AuditEntry, Notification


class NotificationRepository(Protocol):
    """Port for notification persistence.

    Promise:
    - Store and retrieve Notification aggregates by identity and recipient.

    Out of scope:
    - Applying business rules, retries, or transport-level concerns.
    """

    def add(self, notification: Notification) -> None:
        """Persist a newly created notification.

        Promise:
        - Make the notification retrievable by its id.

        Out of scope:
        - Generating ids, validating domain invariants, or audit logging.
        """
        ...

    def get(self, notification_id: str) -> Notification | None:
        """Retrieve one notification by id if present.

        Promise:
        - Return Notification when found, else None.

        Out of scope:
        - Raising HTTP-friendly errors or transforming to DTOs.
        """
        ...

    def save(self, notification: Notification) -> None:
        """Persist updates for an existing notification.

        Promise:
        - Store the latest state of the aggregate.

        Out of scope:
        - Conflict resolution policy and business transition validation.
        """
        ...

    def list_by_recipient(self, recipient: str) -> list[Notification]:
        """List notifications associated with a recipient.

        Promise:
        - Return zero or more notifications for the given recipient id.

        Out of scope:
        - Pagination, sorting policy, or authorization checks.
        """
        ...


class AuditRepository(Protocol):
    """Port for audit trail persistence.

    Promise:
    - Store and retrieve immutable audit events for notifications.

    Out of scope:
    - Deciding when events are emitted or deriving business status.
    """

    def append(self, entry: AuditEntry) -> None:
        """Persist a single audit event entry.

        Promise:
        - Add the event to the notification's audit history.

        Out of scope:
        - Event schema enrichment or lifecycle orchestration.
        """
        ...

    def list_for_notification(self, notification_id: str) -> list[AuditEntry]:
        """Return audit events for one notification.

        Promise:
        - Return all persisted entries for that notification id.

        Out of scope:
        - Filtering by event type or time-window interpretation.
        """
        ...
