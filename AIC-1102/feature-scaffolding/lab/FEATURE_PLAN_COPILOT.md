    # Implementation Plan: Notification Dispatcher
    
    ## 1) Architectural pattern and rationale
    
    **Pattern:** Hexagonal Architecture (Ports and Adapters)
    
    **Rationale (one sentence):** This pattern cleanly separates business workflow from external concerns so channels stay pluggable, persistence stays swappable, and Flask remains a thin HTTP translation layer.
    
    ## 2) Proposed complete directory tree
    
    .
    ├── BASELINE.md
    ├── BASELINE_TEMPLATE.md
    ├── FEATURE_BRIEF.md
    ├── README.md
    ├── pyproject.toml
    ├── src
    │   └── notification_dispatcher
    │       ├── __init__.py
    │       ├── bootstrap
    │       │   ├── __init__.py
    │       │   └── container.py
    │       ├── domain
    │       │   ├── __init__.py
    │       │   ├── enums.py
    │       │   ├── models.py
    │       │   └── status_rules.py
    │       ├── application
    │       │   ├── __init__.py
    │       │   ├── dto.py
    │       │   ├── ports
    │       │   │   ├── __init__.py
    │       │   │   ├── channels.py
    │       │   │   ├── repositories.py
    │       │   │   └── retry_scheduler.py
    │       │   └── services
    │       │       ├── __init__.py
    │       │       ├── dispatch_service.py
    │       │       └── query_service.py
    │       ├── adapters
    │       │   ├── __init__.py
    │       │   ├── channels
    │       │   │   ├── __init__.py
    │       │   │   ├── email_stub.py
    │       │   │   ├── sms_stub.py
    │       │   │   └── push_stub.py
    │       │   ├── repositories
    │       │   │   ├── __init__.py
    │       │   │   ├── in_memory_notification_repository.py
    │       │   │   └── in_memory_audit_repository.py
    │       │   └── retry
    │       │       ├── __init__.py
    │       │       └── in_process_retry_scheduler.py
    │       └── api
    │           ├── __init__.py
    │           └── flask_app.py
    └── tests
        ├── __init__.py
        ├── unit
        │   ├── __init__.py
        │   ├── test_dispatch_service.py
        │   ├── test_status_rules.py
        │   └── test_retry_policy.py
        └── integration
            ├── __init__.py
            └── test_notifications_api.py
    
    ## 3) Public interfaces per module (typed stubs)
    
    ### src/notification_dispatcher/bootstrap/container.py
    
    - def build_app() -> Flask: ...
    - def build_dispatch_service() -> DispatchService: ...
    - def build_query_service() -> QueryService: ...
    
    ### src/notification_dispatcher/domain/enums.py
    
    - ChannelName = Literal["email", "sms", "push"]
    - DeliveryStatus = Literal["pending", "sending", "sent", "partial", "failed", "retrying"]
    - FailureCategory = Literal["transient", "permanent"]
    
    ### src/notification_dispatcher/domain/models.py
    
    - @dataclass(slots=True)
      class ChannelAttemptResult:
      - channel: ChannelName
      - success: bool
      - failure_category: FailureCategory | None
      - reason: str
      - attempt: int
    
    - @dataclass(slots=True)
      class Notification:
      - id: str
      - recipient: str
      - channels: list[ChannelName]
      - subject: str
      - body: str
      - status: DeliveryStatus
      - created_at: datetime
      - updated_at: datetime
      - attempts_by_channel: dict[ChannelName, int] = field(default_factory=dict)
      - delivered_channels: set[ChannelName] = field(default_factory=set)
      - failed_channels: set[ChannelName] = field(default_factory=set)
    
    - @dataclass(slots=True)
      class AuditEntry:
      - id: str
      - notification_id: str
      - timestamp: datetime
      - event_type: Literal["status_change", "channel_attempt"]
      - previous_status: DeliveryStatus | None
      - new_status: DeliveryStatus | None
      - channel: ChannelName | None
      - attempt: int | None
      - reason: str
    
    ### src/notification_dispatcher/domain/status_rules.py
    
    - def next_status_after_attempts(notification: Notification) -> DeliveryStatus: ...
    - def should_retry(result: ChannelAttemptResult, max_attempts: int) -> bool: ...
    - def backoff_seconds(attempt: int) -> int: ...
    
    ### src/notification_dispatcher/application/dto.py
    
    - @dataclass(slots=True)
      class CreateNotificationCommand:
      - recipient: str
      - channels: list[ChannelName]
      - subject: str
      - body: str
    
    - @dataclass(slots=True)
      class NotificationView:
      - id: str
      - recipient: str
      - channels: list[ChannelName]
      - subject: strs
      - body: str
      - status: DeliveryStatus
      - created_at: datetime
      - updated_at: datetime
    
    - @dataclass(slots=True)
      class RetryJob:
      - notification_id: str
      - channel: ChannelName
      - attempt: int
      - run_at: datetime
    
    ### src/notification_dispatcher/application/ports/channels.py
    
    - class ChannelAdapter(Protocol):
      - channel_name: ChannelName
      - def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult: ...
    
    ### src/notification_dispatcher/application/ports/repositories.py
    
    - class NotificationRepository(Protocol):
      - def add(self, notification: Notification) -> None: ...
      - def get(self, notification_id: str) -> Notification | None: ...
      - def save(self, notification: Notification) -> None: ...
      - def list_by_recipient(self, recipient: str) -> list[Notification]: ...
    
    - class AuditRepository(Protocol):
      - def append(self, entry: AuditEntry) -> None: ...
      - def list_for_notification(self, notification_id: str) -> list[AuditEntry]: ...
    
    ### src/notification_dispatcher/application/ports/retry_scheduler.py
    
    - class RetryScheduler(Protocol):
      - def schedule(self, job: RetryJob) -> None: ...
      - def pop_due(self, now: datetime) -> list[RetryJob]: ...
    
    ### src/notification_dispatcher/application/services/dispatch_service.py
    
    - class DispatchService:
      - def create_and_dispatch(self, cmd: CreateNotificationCommand, now: datetime | None = None) -> NotificationView: ...
      - def dispatch_existing(self, notification_id: str, now: datetime | None = None) -> NotificationView: ...
      - def process_due_retries(self, now: datetime | None = None) -> int: ...
      - def retry_channel(self, notification_id: str, channel: ChannelName, attempt: int, now: datetime | None = None) -> NotificationView: ...
    
    ### src/notification_dispatcher/application/services/query_service.py
    
    - class QueryService:
      - def get_notification(self, notification_id: str) -> NotificationView | None: ...
      - def list_for_recipient(self, recipient: str) -> list[NotificationView]: ...
    
    ### src/notification_dispatcher/adapters/channels/email_stub.py
    
    - class EmailStubAdapter(ChannelAdapter):
      - channel_name: Literal["email"]
      - def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult: ...
    
    ### src/notification_dispatcher/adapters/channels/sms_stub.py
    
    - class SmsStubAdapter(ChannelAdapter):
      - channel_name: Literal["sms"]
      - def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult: ...
    
    ### src/notification_dispatcher/adapters/channels/push_stub.py
    
    - class PushStubAdapter(ChannelAdapter):
      - channel_name: Literal["push"]
      - def send(self, notification: Notification, attempt: int) -> ChannelAttemptResult: ...
    
    ### src/notification_dispatcher/adapters/repositories/in_memory_notification_repository.py
    
    - class InMemoryNotificationRepository(NotificationRepository):
      - def add(self, notification: Notification) -> None: ...
      - def get(self, notification_id: str) -> Notification | None: ...
      - def save(self, notification: Notification) -> None: ...
      - def list_by_recipient(self, recipient: str) -> list[Notification]: ...
    
    ### src/notification_dispatcher/adapters/repositories/in_memory_audit_repository.py
    
    - class InMemoryAuditRepository(AuditRepository):
      - def append(self, entry: AuditEntry) -> None: ...
      - def list_for_notification(self, notification_id: str) -> list[AuditEntry]: ...
    
    ### src/notification_dispatcher/adapters/retry/in_process_retry_scheduler.py
    
    - class InProcessRetryScheduler(RetryScheduler):
      - def schedule(self, job: RetryJob) -> None: ...
      - def pop_due(self, now: datetime) -> list[RetryJob]: ...
    
    ### src/notification_dispatcher/api/flask_app.py
    
    - def create_flask_app() -> Flask: ...
    - def register_routes(app: Flask) -> None: ...
    - def post_notifications() -> tuple[dict, int]: ...
    - def get_notification(notification_id: str) -> tuple[dict, int]: ...
    - def get_notifications() -> tuple[dict, int]: ...
    
    ## 4) Dependency direction and import rules
    
    - api may import from application and bootstrap; api must not import adapter implementations directly.
    - bootstrap may import from application, adapters, and api; no other layer imports bootstrap.
    - application.services may import from application.dto, application.ports, and domain; never from api or adapters.
    - application.ports may import domain and application.dto types only; never from adapters or api.
    - domain may import only standard library and other domain modules; never from application, adapters, api, or bootstrap.
    - adapters may import from application.ports and domain; never from api.
    - tests may import from any src module.
    - Direction summary: api and adapters point inward to application; application points inward to domain.
    
    ## 5) Open decisions resolved autonomously and why
    
    - Decision: Use Hexagonal Architecture rather than plain layered modules.
      - Reason: it enforces substitution points for channels, repositories, and retry scheduling.
    
    - Decision: Perform initial dispatch during POST request handling through application service orchestration.
      - Reason: keeps behavior simple and visible in the lab while preserving strict layering.
    
    - Decision: Implement retry scheduler as in-process queue with schedule and pop_due.
      - Reason: deterministic, testable, and swappable for real schedulers later.
    
    - Decision: Keep retry constants in domain policy (max 3 attempts, delays 1s/2s/4s).
      - Reason: business policy belongs in domain logic, not adapters or transport.
    
    - Decision: Standardize adapter result contract as structured ChannelAttemptResult with transient/permanent categories.
      - Reason: avoids leaking adapter-specific exception details into workflow logic.
    
    - Decision: Separate audit store interface from notification store interface.
      - Reason: directly meets requirement for separate persistence concerns and clear boundaries.
    
    - Decision: Keep Flask layer to request/response mapping only.
      - Reason: prevents business rules from drifting into endpoint code.
    
    - Decision: Include unit and integration test directories with placeholder files.
      - Reason: satisfies required test layout immediately and supports incremental implementation.