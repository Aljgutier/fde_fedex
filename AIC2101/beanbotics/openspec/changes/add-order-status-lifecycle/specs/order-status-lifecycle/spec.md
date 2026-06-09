## ADDED Requirements

### Requirement: Order lifecycle statuses are defined and enforced
The system SHALL define the order lifecycle statuses as `pending`, `preparing`, `ready`, `completed`, and `cancelled`. The system MUST reject any status value outside this set when processing status updates.

#### Scenario: New order starts as pending
- **WHEN** a valid order is created
- **THEN** the order status is set to `pending`

#### Scenario: Unknown status value is rejected
- **WHEN** a client requests a status update with a value outside the defined lifecycle statuses
- **THEN** the system rejects the request with a validation error

### Requirement: System validates status transitions with a transition map
The system SHALL expose a single status transition operation that validates requested moves against the lifecycle map. The system MUST allow only `pending -> preparing`, `pending -> cancelled`, `preparing -> ready`, and `ready -> completed`.

#### Scenario: Valid transition succeeds
- **WHEN** a client requests `preparing` for an order currently in `pending`
- **THEN** the system updates the order status to `preparing`

#### Scenario: Invalid transition is rejected
- **WHEN** a client requests `completed` for an order currently in `pending`
- **THEN** the system rejects the request as an invalid transition

#### Scenario: Unknown order cannot transition
- **WHEN** a client requests a status transition for an order id that does not exist
- **THEN** the system returns a not-found error

### Requirement: Cancellation is restricted to pending orders
The system SHALL permit cancellation only while an order is in `pending` status.

#### Scenario: Pending order can be cancelled
- **WHEN** a client requests `cancelled` for an order currently in `pending`
- **THEN** the system updates the order status to `cancelled`

#### Scenario: Non-pending order cannot be cancelled
- **WHEN** a client requests `cancelled` for an order currently in `preparing`, `ready`, or `completed`
- **THEN** the system rejects the request as an invalid transition

### Requirement: Queue board shows active and completed groups
The queue board SHALL display active orders and completed orders in separate groups, where active includes `pending`, `preparing`, and `ready`, and completed includes `completed`.

#### Scenario: Completed orders remain visible in dedicated group
- **WHEN** one or more orders reach `completed`
- **THEN** the queue board displays those orders under a Completed group

#### Scenario: Active orders exclude completed orders
- **WHEN** the queue board renders active orders
- **THEN** orders with `completed` status are not shown in the active group

### Requirement: Queue board provides inline status action controls
The queue board SHALL provide inline action buttons per order based on current status, and each action MUST call the single status transition endpoint.

#### Scenario: Pending order shows prepare and cancel actions
- **WHEN** an order is in `pending`
- **THEN** the queue board shows actions to advance to `preparing` and to cancel

#### Scenario: Preparing order shows ready action
- **WHEN** an order is in `preparing`
- **THEN** the queue board shows an action to advance to `ready`

#### Scenario: Ready order shows complete action
- **WHEN** an order is in `ready`
- **THEN** the queue board shows an action to advance to `completed`

#### Scenario: Completed order has no advance actions
- **WHEN** an order is in `completed`
- **THEN** the queue board does not show status-advancement actions for that order
