# home-navigation Specification

## Purpose

Точка входа Legko: главная, поиск и открытие кампании Keitaro, список недавних, модальные сценарии create/open.

## Requirements

### Requirement: Home screen

The system SHALL render Home at `GET /` with a dark hero strip (copy only), a workspace card with search/open, a centered create CTA above recent campaigns, and a recent campaigns table (max 10).

#### Scenario: Home loads

- **WHEN** the user opens `GET /`
- **THEN** the page shows corporate styling, workspace search, create CTA, and recent table

### Requirement: Campaign search combobox

The system SHALL provide a typeahead combobox on Home that queries Keitaro campaigns by partial ID or name and lets the user pick from a dropdown.

#### Scenario: Suggestions while typing

- **WHEN** the user types in the open field
- **THEN** matching campaigns from Keitaro appear in a dropdown

### Requirement: Open campaign by Keitaro ID

The system SHALL accept a numeric Keitaro campaign ID via preview modal or POST and navigate to the campaign editor when confirmed.

#### Scenario: Local campaign exists

- **WHEN** the user opens a Keitaro ID that exists in SQLite
- **THEN** the user can navigate to `/campaigns/{local_id}/editor`

#### Scenario: Lazy import from Keitaro

- **WHEN** the user opens a Keitaro ID that exists in Keitaro but not locally
- **THEN** the system creates a local shell campaign and allows navigation to the editor

#### Scenario: Campaign not found

- **WHEN** the ID is invalid or missing in Keitaro
- **THEN** Home or the modal shows error «Кампания не найдена»

### Requirement: Recent campaigns

The system SHALL list up to 10 recent campaigns from SQLite ordered by `updated_at` descending, each with name, Keitaro id, geo, short traffic url label, updated time, and sync status as a non-button status pill.

#### Scenario: Open from recent

- **WHEN** the user clicks a recent table row
- **THEN** a preview modal opens with navigation to the editor