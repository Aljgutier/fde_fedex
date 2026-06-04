# BASELINE.md

## Expected Directory Layout

notifications/
├── __init__.py
├── api/
│   ├── __init__.py
│   └── routes.py              # Flask routes (thin layer)
│
├── business_concepts/
│   ├── __init__.py
│   ├── models.py              # Notification, Status, Channel enums
│   └── events.py              # Audit event definitions
│
├── service/
│   ├── __init__.py
│   └── notification_service.py  # Core orchestration logic
│
├── channels/
│   ├── __init__.py
│   ├── base.py                # Channel interface / protocol
│   ├── email.py               # Email adapter (stub)
│   ├── sms.py                 # SMS adapter (stub)
│   └── push.py                # Push adapter (stub)
│
├── storage_abstractions/
│   ├── __init__.py
│   ├── notification_store.py  # Interface + in-memory impl
│   └── audit_store.py         # Interface + in-memory impl
│
├── retry/
│   ├── __init__.py
│   ├── policy.py              # Retry policy definition
│   └── scheduler.py           # Abstract scheduler
│
├── app.py                     # Flask app factory / entrypoint
└── config.py                  # Configuration


tests/
├── __init__.py
├── test_api.py
├── test_service.py
├── test_channels.py
└── test_storage.py


## Expected Public Interfaces

### notifications/business_concepts/models.py

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    PARTIAL = "partial"
    FAILED = "failed"
    RETRYING = "retrying"


class ChannelType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


@dataclass
class Notification:
    id: str
    recipient: str
    channels: List[ChannelType]
    subject: Optional[str]
    body: str
    status: NotificationStatus
    created_at: datetime


### notifications/service/notification_service.py

from typing import List
from notifications.business_concepts.models import Notification


class NotificationService:
    def create_notification(
        self,
        recipient: str,
        channels: List[str],
        subject: str,
        body: str
    ) -> Notification: ...

    def get_notification(self, notification_id: str) -> Notification: ...

    def list_notifications(self, recipient: str) -> List[Notification]: ...

    def dispatch(self, notification_id: str) -> None: ...


### notifications/channels/base.py

from abc import ABC, abstractmethod
from typing import Tuple


class ChannelAdapter(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> Tuple[bool, str]:
        """
        Returns:
            success: bool
            failure_type: "transient" | "permanent" | None
        """
        ...


### notifications/channels/email.py

from notifications.channels.base import ChannelAdapter


class EmailChannel(ChannelAdapter):
    def send(self, recipient: str, subject: str, body: str): ...


### notifications/storage_abstractions/notification_store.py

from typing import List, Optional
from notifications.business_concepts.models import Notification


class NotificationStore:
    def save(self, notification: Notification) -> None: ...
    def get(self, notification_id: str) -> Optional[Notification]: ...
    def list_by_recipient(self, recipient: str) -> List[Notification]: ...


### notifications/storage_abstractions/audit_store.py

from typing import List
from datetime import datetime


class AuditEntry:
    def __init__(
        self,
        notification_id: str,
        timestamp: datetime,
        from_status: str,
        to_status: str,
        reason: str
    ): ...


class AuditStore:
    def record(self, entry: AuditEntry) -> None: ...
    def list_for_notification(self, notification_id: str) -> List[AuditEntry]: ...


### notifications/retry/policy.py

class RetryPolicy:
    def should_retry(self, attempt: int, failure_type: str) -> bool: ...
    def next_delay(self, attempt: int) -> float: ...


### notifications/retry/scheduler.py

from typing import Callable


class RetryScheduler:
    def schedule(self, delay_seconds: float, task: Callable[[], None]) -> None: ...


### notifications/api/routes.py

from flask import Blueprint, request, jsonify

bp = Blueprint("notifications", __name__)


@bp.route("/notifications", methods=["POST"])
def create_notification(): ...


@bp.route("/notifications/<notification_id>", methods=["GET"])
def get_notification(notification_id: str): ...


@bp.route("/notifications", methods=["GET"])
def list_notifications(): ...


### notifications/app.py

from flask import Flask


def create_app() -> Flask: ...


## DEPENDENCY DIRECTION

api/routes
    ↓
service/notification_service
    ↓
business_concepts/models

service → storage_abstractions (notifications + audit)
service → channels (via base interface)
service → retry (policy + scheduler)

channels → (no dependency on service)

storage_abstractions → business_concepts

retry → (no dependency on service logic)

app → api


## ARCHITECTURAL PATTERN

Hexagonal (Ports and Adapters)

The service layer contains the core workflow, while storage, channels, and retry behavior are external plug-in components. This allows extending functionality (new channels, new storage backends) without modifying core logic.


## DECISIONS LEFT TO COPILOT

- Whether channel adapters return tuples vs structured result objects
- Whether retry scheduling is synchronous, threaded, or queue-based
- Whether audit logging is triggered inline or via events
- How dependency injection and wiring are handled
- Whether interfaces use ABCs or typing.Protocol
- Whether dispatch is synchronous during POST or asynchronously triggered afterward