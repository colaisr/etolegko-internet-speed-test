## ADDED Requirements

### Requirement: Health endpoint

The system SHALL expose `GET /health` returning JSON with subsystem status for application, database, and Keitaro.

#### Scenario: All healthy

- **WHEN** database is reachable and Keitaro ping succeeds
- **THEN** response indicates overall OK and Keitaro OK

#### Scenario: Keitaro unavailable

- **WHEN** Keitaro ping fails
- **THEN** response includes a clear error message without API keys or stack traces