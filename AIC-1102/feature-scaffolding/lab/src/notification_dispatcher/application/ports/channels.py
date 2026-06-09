from __future__ import annotations

from typing import Protocol

from notification_dispatcher.domain.enums import ChannelName
from notification_dispatcher.domain.models import ChannelAttemptResult, Notification


class ChannelAdapter(Protocol):
    """Port for channel delivery adapters.

    Promise:
    - Attempt delivery for a single channel and return a normalized result.

    Out of scope:
    - Deciding retries, status transitions, auditing, or persistence.
    """

    channel_name: ChannelName

    def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult:
        """Attempt one delivery and return success/failure details.

        Promise:
        - Return a ChannelAttemptResult for the provided attempt number.

        Out of scope:
        - Updating notification state or scheduling retry jobs.
        """
        ...
