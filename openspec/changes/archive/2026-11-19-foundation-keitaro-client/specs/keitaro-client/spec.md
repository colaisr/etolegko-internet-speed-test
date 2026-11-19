## ADDED Requirements

### Requirement: Keitaro API client

The system SHALL provide an httpx-based client that sends the Keitaro `Api-Key` header on admin API requests.

#### Scenario: Authenticated request

- **WHEN** settings include base URL and API key
- **THEN** outbound requests include header `Api-Key` with the configured key

### Requirement: Keitaro connectivity check

The system SHALL expose `ping()` that performs a lightweight GET to the campaigns list endpoint.

#### Scenario: Successful ping

- **WHEN** Keitaro accepts the API key
- **THEN** `ping()` returns success

#### Scenario: Auth failure

- **WHEN** Keitaro returns 401 or 403
- **THEN** `ping()` fails with a user-safe error message