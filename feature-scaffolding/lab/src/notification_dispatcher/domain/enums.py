from __future__ import annotations

from typing import Literal, TypeAlias

ChannelName: TypeAlias = Literal["email", "sms", "push"]
DeliveryStatus: TypeAlias = Literal[
    "pending", "sending", "sent", "partial", "failed", "retrying"
]
FailureCategory: TypeAlias = Literal["transient", "permanent"]
AuditEventType: TypeAlias = Literal["status_change", "channel_attempt"]
