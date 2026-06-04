# Baseline Sketch

Fill this in **before** you prompt Copilot. Once you start a scaffolding run, the run will shape your judgment about what "looks right" — the point of the baseline is to capture your expectation uncontaminated by the agent's output.

Copy this template to `BASELINE.md` at the repository root and edit there. Leave this template file unchanged so later runs can reuse it.

---

## Expected Directory Layout

Sketch the tree you would produce if you were scaffolding this microservice by hand. Include every module you expect and the intended purpose of each.

```
notifications/
├── ...
tests/
├── ...
```

## Expected Public Interfaces

For each major module in the sketch, write the function or class signatures you would expect, with type hints. Interface, not implementation.

### `notifications/<module>.py`

```python
def example(arg: str) -> None: ...
```

### `notifications/<other>.py`

```python
...
```

## Dependency Direction

Draw (in text) which modules depend on which. This is what you will audit most carefully in the generated scaffolding.

```
api -> service -> repository
                \-> channels
```

## Architectural Pattern

One or two sentences naming the pattern you are defaulting to (layered, hexagonal, event-driven, CQRS, pipes-and-filters) and why.

## Decisions You Are Leaving to Copilot

List the structural choices you deliberately did *not* make, so you can observe how the agent resolves them.

- (for example) Whether retry scheduling lives inside the service or as a separate module
- (for example) Whether channel adapters implement a shared protocol or extend a base class
- (for example) Whether the audit log is a sibling module or a sub-module of the repository layer


Here is your **baseline scaffolding in raw Markdown/text form** (fully copyable, no rendering tricks):

```
# BASELINE.md

## Expected Directory Layout

notifications/
├── __init__.py
├── api/
│   ├── __init__.py
│   └── routes.py              # Flask routes (thin layer)
│
├── domain/
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
├── repository/
│   ├── __init__.py
│   ├── notification_repo.py   # Interface + in-memory impl
│   └── audit_repo.py          # Interface + in-memory impl
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
└── test_repository.py


## Expected Public Interfaces

### notifications/domain/models.py

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
from notifications.domain.models import Notification


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
    def send(self, recipient: str, subject: str, body: str):
        ...


### notifications/repository/notification_repo.py

from typing import List, Optional
from notifications.domain.models import Notification


class NotificationRepository:
    def save(self, notification: Notification) -> None: ...
    def get(self, notification_id: str) -> Optional[Notification]: ...
    def list_by_recipient(self, recipient: str) -> List[Notification]: ...


### notifications/repository/audit_repo.py

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


class AuditRepository:
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


## Dependency Direction

api/routes
    ↓
service/notification_service
    ↓
domain/models

service → repository (notification + audit)
service → channels (via base interface)
service → retry (policy + scheduler)

channels → (no dependency on service)

repository → domain

retry → (no dependency on service logic)

app → api


## Architectural Pattern

Hexagonal (Ports and Adapters)

The service layer defines the core workflow, while repositories, channels, and retry scheduling are adapters plugged in via interfaces.


## Decisions You Are Leaving to Copilot

- Whether channel adapters return structured result objects vs tuples
- Whether retry scheduling is synchronous or queue-based
- Whether audit logging is triggered inline or via events
- How dependency injection / wiring is handled
- ABC vs Protocol usage for interfaces
- Whether dispatch is synchronous or async-triggered
```
