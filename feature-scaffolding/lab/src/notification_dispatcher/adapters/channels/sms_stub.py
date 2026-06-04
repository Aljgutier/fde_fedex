from __future__ import annotations

from typing import Literal

from notification_dispatcher.application.ports.channels import ChannelAdapter
from notification_dispatcher.domain.models import ChannelAttemptResult, Notification


class SmsStubAdapter(ChannelAdapter):
    channel_name: Literal["sms"] = "sms"

    def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult:
        return ChannelAttemptResult(
            channel=self.channel_name,
            success=False,
            failure_category="transient",
            reason="sms stub transient failure",
            attempt=attempt,
        )
