## ADDED Requirements

### Requirement: OrderStatus enum

The system SHALL define an `OrderStatus` enum with values: `pending`, `preparing`, `ready`, `completed`, `cancelled`. The Order model SHALL use this enum for its `status` field. New orders SHALL be created with status `pending`.

#### Scenario: Order created with pending status
- **WHEN** a new order is placed via `POST /api/orders`
- **THEN** the order SHALL have status `pending`

#### Scenario: Invalid status rejected at creation
- **WHEN** an Order is constructed with a status value not in the enum
- **THEN** the system SHALL raise a validation error

### Requirement: Valid transition map

The system SHALL enforce the following transition rules:
- `pending` → `preparing` or `cancelled`
- `preparing` → `ready`
- `ready` → `completed`
- `completed` → *(terminal, no transitions)*
- `cancelled` → *(terminal, no transitions)*

The transition map SHALL be the single source of truth for lifecycle rules.

#### Scenario: Valid transition from pending to preparing
- **WHEN** an order has status `pending` and a transition to `preparing` is requested
- **THEN** the system SHALL update the order status to `preparing`

#### Scenario: Valid transition from preparing to ready
- **WHEN** an order has status `preparing` and a transition to `ready` is requested
- **THEN** the system SHALL update the order status to `ready`

#### Scenario: Valid transition from ready to completed
- **WHEN** an order has status `ready` and a transition to `completed` is requested
- **THEN** the system SHALL update the order status to `completed`

#### Scenario: Valid cancellation from pending
- **WHEN** an order has status `pending` and a transition to `cancelled` is requested
- **THEN** the system SHALL update the order status to `cancelled`

#### Scenario: Invalid transition rejected
- **WHEN** a transition is requested that is not in the valid transition map (e.g., `preparing` → `cancelled`, `completed` → `pending`)
- **THEN** the system SHALL reject the transition and return an error

### Requirement: PATCH endpoint for status updates

The system SHALL expose `PATCH /api/orders/{id}` accepting a JSON body `{ "status": "<next_status>" }`. The endpoint SHALL validate the requested transition against the transition map.

#### Scenario: Successful status advance
- **WHEN** a PATCH request is sent with a valid next status for the order's current status
- **THEN** the system SHALL return the updated order with HTTP 200

#### Scenario: Invalid transition returns 400
- **WHEN** a PATCH request is sent with a status that is not a valid transition from the order's current status
- **THEN** the system SHALL return HTTP 400 with an error message describing the invalid transition

#### Scenario: Order not found returns 404
- **WHEN** a PATCH request is sent for an order ID that does not exist
- **THEN** the system SHALL return HTTP 404

### Requirement: OrderService update method

The `OrderService` SHALL provide an `update_order_status(order_id, new_status)` method that looks up the order, validates the transition against the map, and updates the status. The existing `cancel_order()` method SHALL delegate to this method.

#### Scenario: Service method validates and updates
- **WHEN** `update_order_status()` is called with a valid order ID and valid next status
- **THEN** the order status SHALL be updated and the updated order SHALL be returned

#### Scenario: Service method rejects invalid transition
- **WHEN** `update_order_status()` is called with an invalid transition
- **THEN** the method SHALL raise an appropriate error without modifying the order
