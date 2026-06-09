from __future__ import annotations

from datetime import datetime

from notification_dispatcher.application.dto import RetryJob
from notification_dispatcher.application.ports.retry_scheduler import RetryScheduler


class InProcessRetryScheduler(RetryScheduler):
    def __init__(self) -> None:
        self._jobs: list[RetryJob] = []

    def schedule(self, job: RetryJob) -> None:
        self._jobs.append(job)

    def pop_due(self, now: datetime) -> list[RetryJob]:
        due: list[RetryJob] = []
        future: list[RetryJob] = []
        for job in self._jobs:
            if job.run_at <= now:
                due.append(job)
            else:
                future.append(job)
        self._jobs = future
        return due
