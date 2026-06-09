from __future__ import annotations

from typing import Literal

from notification_dispatcher.application.ports.channels import ChannelAdapter
from notification_dispatcher.domain.models import ChannelAttemptResult, Notification


class EmailStubAdapter(ChannelAdapter):
    channel_name: Literal["email"] = "email"

    def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult:
        return ChannelAttemptResult(
            channel=self.channel_name,
            success=True,
            failure_category=None,
            reason="email stub delivered",
            attempt=attempt,
        )
