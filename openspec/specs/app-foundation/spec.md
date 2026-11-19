# app-foundation Specification

## Purpose
TBD - created by archiving change foundation-keitaro-client. Update Purpose after archive.

## Requirements

### Requirement: Application bootstrap

The system SHALL provide a FastAPI application entrypoint loadable as `legko.main:app` and serve project static assets under `/static`.

#### Scenario: Start server

- **WHEN** the operator runs `uvicorn legko.main:app`
- **THEN** the application starts without import errors

### Requirement: Configuration from environment

The system SHALL read `DATABASE_URL`, `KEITARO_BASE_URL`, and `KEITARO_API_KEY` from environment or `.env` via settings.

#### Scenario: Missing API key

- **WHEN** `KEITARO_API_KEY` is empty
- **THEN** health reports Keitaro as not configured without exposing secrets

### Requirement: Database migrations

The system SHALL apply Alembic migrations from an empty database to create core tables for campaigns, streams, and stream offers.

#### Scenario: Fresh migrate

- **WHEN** migrations are applied on empty SQLite
- **THEN** tables exist and the app can open a DB session

### Requirement: Base web layout

The system SHALL render a corporate-styled base layout with a header link placeholder for documentation.

#### Scenario: Root page

- **WHEN** the user opens `GET /`
- **THEN** a minimal home stub is shown inside the base layout
