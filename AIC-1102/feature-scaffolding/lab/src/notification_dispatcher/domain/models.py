from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from notification_dispatcher.domain.enums import (
    AuditEventType,
    ChannelName,
    DeliveryStatus,
    FailureCategory,
)


@dataclass(slots=True)
class ChannelAttemptResult:
    channel: ChannelName
    success: bool
    failure_category: FailureCategory | None
    reason: str
    attempt: int


@dataclass(slots=True)
class Notification:
    id: str
    recipient: str
    channels: list[ChannelName]
    subject: str
    body: str
    status: DeliveryStatus
    created_at: datetime
    updated_at: datetime
    attempts_by_channel: dict[ChannelName, int] = field(default_factory=dict)
    delivered_channels: set[ChannelName] = field(default_factory=set)
    failed_channels: set[ChannelName] = field(default_factory=set)
    retrying_channels: set[ChannelName] = field(default_factory=set)


@dataclass(slots=True)
class AuditEntry:
    id: str
    notification_id: str
    timestamp: datetime
    event_type: AuditEventType
    previous_status: DeliveryStatus | None
    new_status: DeliveryStatus | None
    channel: ChannelName | None
    attempt: int | None
    reason: str
