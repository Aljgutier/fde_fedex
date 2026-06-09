from __future__ import annotations

from flask import Flask

from notification_dispatcher.adapters.channels.email_stub import EmailStubAdapter
from notification_dispatcher.adapters.channels.push_stub import PushStubAdapter
from notification_dispatcher.adapters.channels.sms_stub import SmsStubAdapter
from notification_dispatcher.adapters.repositories.in_memory_audit_repository import (
    InMemoryAuditRepository,
)
from notification_dispatcher.adapters.repositories.in_memory_notification_repository import (
    InMemoryNotificationRepository,
)
from notification_dispatcher.adapters.retry.in_process_retry_scheduler import (
    InProcessRetryScheduler,
)
from notification_dispatcher.api.flask_app import create_flask_app
from notification_dispatcher.application.services.dispatch_service import DispatchService
from notification_dispatcher.application.services.query_service import QueryService


def build_dispatch_service(
    notification_repo: InMemoryNotificationRepository | None = None,
    audit_repo: InMemoryAuditRepository | None = None,
    retry_scheduler: InProcessRetryScheduler | None = None,
) -> DispatchService:
    notification_repo = notification_repo or InMemoryNotificationRepository()
    audit_repo = audit_repo or InMemoryAuditRepository()
    retry_scheduler = retry_scheduler or InProcessRetryScheduler()
    channels = {
        "email": EmailStubAdapter(),
        "sms": SmsStubAdapter(),
        "push": PushStubAdapter(),
    }
    return DispatchService(
        notification_repository=notification_repo,
        audit_repository=audit_repo,
        retry_scheduler=retry_scheduler,
        channel_adapters=channels,
    )


def build_query_service(
    notification_repo: InMemoryNotificationRepository | None = None,
) -> QueryService:
    notification_repo = notification_repo or InMemoryNotificationRepository()
    return QueryService(notification_repository=notification_repo)


def build_app() -> Flask:
    notification_repo = InMemoryNotificationRepository()
    dispatch_service = build_dispatch_service(
        notification_repo=notification_repo,
        audit_repo=InMemoryAuditRepository(),
        retry_scheduler=InProcessRetryScheduler(),
    )
    query_service = build_query_service(notification_repo=notification_repo)
    return create_flask_app(dispatch_service=dispatch_service, query_service=query_service)
