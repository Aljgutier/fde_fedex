from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timedelta
from uuid import uuid4

from notification_dispatcher.application.dto import (
    CreateNotificationCommand,
    NotificationView,
    RetryJob,
)
from notification_dispatcher.application.ports.channels import ChannelAdapter
from notification_dispatcher.application.ports.repositories import (
    AuditRepository,
    NotificationRepository,
)
from notification_dispatcher.application.ports.retry_scheduler import RetryScheduler
from notification_dispatcher.domain.enums import AuditEventType, ChannelName, DeliveryStatus
from notification_dispatcher.domain.models import AuditEntry, ChannelAttemptResult, Notification
from notification_dispatcher.domain.status_rules import (
    backoff_seconds,
    next_status_after_attempts,
    should_retry,
)


MAX_RETRY_ATTEMPTS = 3


class DispatchService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        audit_repository: AuditRepository,
        retry_scheduler: RetryScheduler,
        channel_adapters: Mapping[ChannelName, ChannelAdapter],
    ) -> None:
        self._notification_repository = notification_repository
        self._audit_repository = audit_repository
        self._retry_scheduler = retry_scheduler
        self._channel_adapters = channel_adapters

    def create_and_dispatch(
        self, cmd: CreateNotificationCommand, now: datetime | None = None
    ) -> NotificationView:
        timestamp = now or datetime.utcnow()
        if not cmd.recipient.strip():
            raise ValueError("recipient is required")
        if not cmd.channels:
            raise ValueError("at least one channel is required")
        for channel in cmd.channels:
            if channel not in self._channel_adapters:
                raise ValueError(f"unsupported channel: {channel}")

        notification = Notification(
            id=str(uuid4()),
            recipient=cmd.recipient,
            channels=cmd.channels,
            subject=cmd.subject,
            body=cmd.body,
            status="pending",
            created_at=timestamp,
            updated_at=timestamp,
        )
        self._notification_repository.add(notification)
        self._append_audit_entry(
            notification_id=notification.id,
            timestamp=timestamp,
            event_type="status_change",
            previous_status=None,
            new_status="pending",
            channel=None,
            attempt=None,
            reason="notification created",
        )
        return self.dispatch_existing(notification.id, now=timestamp)

    def dispatch_existing(
        self, notification_id: str, now: datetime | None = None
    ) -> NotificationView:
        timestamp = now or datetime.utcnow()
        notification = self._require_notification(notification_id)
        self._set_status(
            notification=notification,
            new_status="sending",
            reason="dispatch started",
            timestamp=timestamp,
        )

        for channel in notification.channels:
            if channel in notification.delivered_channels:
                continue
            if channel in notification.retrying_channels:
                continue

            attempt = notification.attempts_by_channel.get(channel, 0) + 1
            result = self._channel_adapters[channel].send(notification=notification, attempt=attempt)
            self._record_attempt(notification=notification, result=result, timestamp=timestamp)

        new_status = next_status_after_attempts(notification)
        self._set_status(
            notification=notification,
            new_status=new_status,
            reason="dispatch cycle completed",
            timestamp=timestamp,
        )
        self._notification_repository.save(notification)
        return self._to_view(notification)

    def process_due_retries(self, now: datetime | None = None) -> int:
        timestamp = now or datetime.utcnow()
        jobs = self._retry_scheduler.pop_due(timestamp)
        processed = 0
        for job in jobs:
            self.retry_channel(
                notification_id=job.notification_id,
                channel=job.channel,
                attempt=job.attempt,
                now=timestamp,
            )
            processed += 1
        return processed

    def retry_channel(
        self,
        notification_id: str,
        channel: ChannelName,
        attempt: int,
        now: datetime | None = None,
    ) -> NotificationView:
        timestamp = now or datetime.utcnow()
        notification = self._require_notification(notification_id)

        self._set_status(
            notification=notification,
            new_status="sending",
            reason=f"retry dispatch started for {channel}",
            timestamp=timestamp,
        )

        notification.retrying_channels.discard(channel)
        result = self._channel_adapters[channel].send(notification=notification, attempt=attempt)
        self._record_attempt(notification=notification, result=result, timestamp=timestamp)

        new_status = next_status_after_attempts(notification)
        self._set_status(
            notification=notification,
            new_status=new_status,
            reason=f"retry dispatch completed for {channel}",
            timestamp=timestamp,
        )
        self._notification_repository.save(notification)
        return self._to_view(notification)

    def _require_notification(self, notification_id: str) -> Notification:
        notification = self._notification_repository.get(notification_id)
        if notification is None:
            raise KeyError(f"notification not found: {notification_id}")
        return notification

    def _set_status(
        self,
        notification: Notification,
        new_status: DeliveryStatus,
        reason: str,
        timestamp: datetime,
    ) -> None:
        previous_status = notification.status
        if previous_status == new_status:
            return
        notification.status = new_status
        notification.updated_at = timestamp
        self._append_audit_entry(
            notification_id=notification.id,
            timestamp=timestamp,
            event_type="status_change",
            previous_status=previous_status,
            new_status=new_status,
            channel=None,
            attempt=None,
            reason=reason,
        )

    def _record_attempt(
        self, notification: Notification, result: ChannelAttemptResult, timestamp: datetime
    ) -> None:
        channel = result.channel
        notification.attempts_by_channel[channel] = result.attempt

        if result.success:
            notification.delivered_channels.add(channel)
            notification.failed_channels.discard(channel)
            notification.retrying_channels.discard(channel)
        elif should_retry(result=result, max_attempts=MAX_RETRY_ATTEMPTS):
            notification.retrying_channels.add(channel)
            delay = backoff_seconds(result.attempt)
            self._retry_scheduler.schedule(
                RetryJob(
                    notification_id=notification.id,
                    channel=channel,
                    attempt=result.attempt + 1,
                    run_at=timestamp + timedelta(seconds=delay),
                )
            )
        else:
            notification.failed_channels.add(channel)
            notification.retrying_channels.discard(channel)

        self._append_audit_entry(
            notification_id=notification.id,
            timestamp=timestamp,
            event_type="channel_attempt",
            previous_status=None,
            new_status=None,
            channel=channel,
            attempt=result.attempt,
            reason=result.reason,
        )

    def _append_audit_entry(
        self,
        notification_id: str,
        timestamp: datetime,
        event_type: AuditEventType,
        previous_status: DeliveryStatus | None,
        new_status: DeliveryStatus | None,
        channel: ChannelName | None,
        attempt: int | None,
        reason: str,
    ) -> None:
        self._audit_repository.append(
            AuditEntry(
                id=str(uuid4()),
                notification_id=notification_id,
                timestamp=timestamp,
                event_type=event_type,
                previous_status=previous_status,
                new_status=new_status,
                channel=channel,
                attempt=attempt,
                reason=reason,
            )
        )

    def _to_view(self, notification: Notification) -> NotificationView:
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
