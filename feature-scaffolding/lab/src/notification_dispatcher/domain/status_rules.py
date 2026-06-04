from __future__ import annotations

from notification_dispatcher.domain.enums import DeliveryStatus
from notification_dispatcher.domain.models import ChannelAttemptResult, Notification


def next_status_after_attempts(notification: Notification) -> DeliveryStatus:
    if notification.retrying_channels:
        return "retrying"
    if not notification.delivered_channels and not notification.failed_channels:
        return "pending"
    if notification.delivered_channels and notification.failed_channels:
        return "partial"
    if notification.delivered_channels:
        return "sent"
    if notification.failed_channels:
        return "failed"
    return "pending"


def should_retry(result: ChannelAttemptResult, max_attempts: int) -> bool:
    return (
        not result.success
        and result.failure_category == "transient"
        and result.attempt < max_attempts
    )


def backoff_seconds(attempt: int) -> int:
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    return 2 ** (attempt - 1)
