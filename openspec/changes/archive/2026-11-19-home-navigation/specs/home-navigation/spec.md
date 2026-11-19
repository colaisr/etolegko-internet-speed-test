## ADDED Requirements

### Requirement: Home screen

The system SHALL render Home at `GET /` with hero copy, primary CTA to create a campaign, open-by-Keitaro-id form, and a recent campaigns list (max 10).

#### Scenario: Home loads

- **WHEN** the user opens `GET /`
- **THEN** the page shows corporate styling, create CTA, open form, and recent section

### Requirement: Campaign search combobox

The system SHALL provide a typeahead combobox on Home that queries Keitaro campaigns by partial ID or name and lets the user pick from a dropdown.

#### Scenario: Suggestions while typing

- **WHEN** the user types in the open field
- **THEN** matching campaigns from Keitaro appear in a dropdown

### Requirement: Open campaign by Keitaro ID

The system SHALL accept a numeric Keitaro campaign ID and navigate to the campaign editor.

#### Scenario: Local campaign exists

- **WHEN** the user submits a Keitaro ID that exists in SQLite
- **THEN** the user is redirected to `/campaigns/{local_id}/editor`

#### Scenario: Lazy import from Keitaro

- **WHEN** the user submits a Keitaro ID that exists in Keitaro but not locally
- **THEN** the system creates a local shell campaign and redirects to the editor

#### Scenario: Campaign not found

- **WHEN** the ID is invalid or missing in Keitaro
- **THEN** Home shows error «Кампания не найдена»

### Requirement: Recent campaigns

The system SHALL list up to 10 recent campaigns from SQLite ordered by `updated_at` descending, each with name, Keitaro id, and sync status badge.

#### Scenario: Open from recent

- **WHEN** the user clicks a recent campaign row
- **THEN** the editor opens without re-entering the Keitaro ID