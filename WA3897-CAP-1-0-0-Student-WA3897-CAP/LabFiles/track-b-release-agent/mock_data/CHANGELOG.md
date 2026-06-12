# Changelog

All notable changes to the FedEx Shipping Platform are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2024-11-20

### Added
- Multi-carrier rate shopping API endpoint (`/v3/rates/compare`)
- Real-time webhook delivery status callbacks for all notification types
- GraphQL query interface alongside existing REST endpoints

### Changed
- Improved label generation throughput by 40% via async rendering pipeline
- Updated internal logging to structured JSON format for centralized observability
- Refreshed developer portal documentation with interactive API examples

### Fixed
- Resolved edge case in address normalization for Canadian postal codes with spaces
- Corrected fuel surcharge rounding for international freight invoices

---

## [2.4.1] - 2024-11-14

### Fixed
- Corrected rate limiter threshold for authenticated API users (SHIP-1042 regression)
- Fixed ZIP+4 suffix calculation for PO Box addresses (SHIP-1055)
- Patched address validation for APO/FPO/DPO military addresses

---

## [2.4.0] - 2024-11-05

### Added
- Dimensional weight API for international freight rate calculation
- Batch label generation endpoint supporting up to 500 labels per request
- New webhook event type: `shipment.exception` for carrier-reported exceptions

### Changed
- Upgraded internal HTTP client from `httpx` 0.25 to `httpx` 0.27
- Authentication token expiry extended from 12 hours to 24 hours

### Fixed
- Tracking event deduplication for multi-leg international shipments
- SMS notification retry logic now honors provider Retry-After headers

### Deprecated
- `/v2/label/single` endpoint — use `/v2/label/batch` with a single-item array instead
- Legacy API key authentication — OAuth 2.0 required from 2025-Q1

---

## [2.3.1] - 2024-10-12

### Fixed
- Security patch: updated `requests` library to 2.31.0 (CVE-2024-1234)
- Resolved memory leak in long-running webhook delivery workers
- Corrected invoice total rounding for shipments with multiple dimensional weight segments

---

## [2.3.0] - 2024-09-28

### Added
- Carrier performance dashboard API (`/v2/analytics/carrier-performance`)
- Support for FedEx One Rate flat-rate packaging in rate calculation
- Configurable retry policy for outbound webhooks (max retries, backoff factor)

### Changed
- Notification service SMS provider updated to support A2P 10DLC compliance
- Internal service discovery migrated from Consul to Kubernetes service mesh

### Fixed
- Eliminated duplicate tracking events on scan arrivals at hub facilities
- Fixed edge case where `None` recipient email caused unhandled exception in notification worker

---

## [1.2.3] - 2024-08-15

### Fixed
- SMS delivery delays under peak load (NOTIF-055): implemented exponential backoff and queue priority
- Email template encoding fixed for UTF-8 recipient names in subject lines
- Corrected webhook signature HMAC computation for payloads exceeding 64 KB

---

## [1.2.0] - 2024-07-01

### Added
- Outbound webhook support for shipment lifecycle events
- Email notification templates with FedEx brand guidelines compliance
- Carrier tracking feed integration for six additional regional last-mile carriers

### Changed
- Notification service extracted from monolith into standalone microservice
- All public API endpoints now require Bearer token authentication

### Fixed
- Resolved race condition in tracking number sequence generator under concurrent load

### Security
- Rotated all internal service-to-service mTLS certificates
- Enforced TLS 1.2 minimum across all inter-service communication

---

## [1.1.0] - 2024-05-20

### Added
- SMS notification support via third-party provider integration
- Rate limiting on public API endpoints (configurable per client tier)
- Health check endpoints for all services (`/health`, `/ready`)

### Changed
- Logging migrated from print statements to structured `logging` module
- Deployment artifacts now include Software Bill of Materials (SBOM)

---

## [1.0.0] - 2024-03-01

### Added
- Initial release of the FedEx Shipping Platform microservices architecture
- Shipping API: label generation, rate calculation, address validation
- Label Service: PDF label rendering for domestic and international shipments
- Notification Service: email delivery for shipment confirmations and exceptions
- Tracking Service: real-time shipment status aggregation
- API Gateway: authentication, rate limiting, request routing
