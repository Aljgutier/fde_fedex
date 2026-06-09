from __future__ import annotations

from datetime import datetime
from typing import Protocol

from notification_dispatcher.application.dto import RetryJob


class RetryScheduler(Protocol):
    """Port for scheduling retry jobs.

    Promise:
    - Accept retry jobs and return due jobs at caller-provided time boundaries.

    Out of scope:
    - Executing jobs, mutating notification state, or status computation.
    """

    def schedule(self, job: RetryJob) -> None:
        """Register a retry job for later processing.

        Promise:
        - Make the job available to pop_due once due.

        Out of scope:
        - Running the retry action itself.
        """
        ...

    def pop_due(self, now: datetime) -> list[RetryJob]:
        """Return and remove all jobs due at or before now.

        Promise:
        - Yield currently due jobs and prevent duplicate return on next pop.

        Out of scope:
        - Error handling policy for execution failures.
        """
        ...
