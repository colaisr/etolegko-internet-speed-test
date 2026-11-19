# project-readme-delivery Specification

## Purpose

Сдача MVP: README и встроенная документация ProductDocs (F8, F9).

## Requirements

### Requirement: Root README (F8)

The repository SHALL provide a root README with install, env, migrations, run, acceptance scenario, repository URL, and mention of in-app `/docs`.

#### Scenario: New clone runbook

- **WHEN** a reviewer follows the README
- **THEN** they can start uvicorn and open the UI and `/docs`

### Requirement: In-app docs index (F9)

The system SHALL serve `GET /docs` with a list of ProductDocs numbered pages and rendered README index content.

#### Scenario: Docs index

- **WHEN** the user opens `/docs`
- **THEN** they see links to pages 00, 01, 02, 03

### Requirement: In-app doc page (F9)

The system SHALL serve `GET /docs/{slug}` for slugs matching `ProductDocs/{slug}.md` numbered pages only; unknown slugs return 404 with link to index.

#### Scenario: Page render

- **WHEN** the user opens `/docs/02-stream-offer-editor`
- **THEN** markdown is rendered as readable HTML with a link back to the app

### Requirement: Header link (F9)

The application header SHALL link to `/docs` on main screens.