from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from notification_dispatcher.domain.enums import ChannelName, DeliveryStatus


@dataclass(slots=True)
class CreateNotificationCommand:
    recipient: str
    channels: list[ChannelName]
    subject: str
    body: str


@dataclass(slots=True)
class NotificationView:
    id: str
    recipient: str
    channels: list[ChannelName]
    subject: str
    body: str
    status: DeliveryStatus
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class RetryJob:
    notification_id: str
    channel: ChannelName
    attempt: int
    run_at: datetime
