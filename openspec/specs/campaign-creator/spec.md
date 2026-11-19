# campaign-creator Specification

## Purpose

Шаблонный создатель 2-поточной кампании в Keitaro: geo → Google, остальной трафик → один оффер 100%, запись в SQLite и post-create fetch.

## Requirements

### Requirement: Creator modal on Home

The system SHALL open the creator as a modal panel on Home via `GET /campaigns/new/panel` (HTMX), primary CTA on the workspace card, nav link `/?create=1`, and redirect `GET /campaigns/new` → `/?create=1`.

#### Scenario: Open create modal

- **WHEN** the user clicks «Создать кампанию» on Home
- **THEN** the modal shows the creator form without leaving Home

### Requirement: Creator form

The system SHALL render a creator form with fields campaign name, geo (ISO-2 with quick picks and search), offer combobox, read-only template preview, and read-only domain/group/source from configuration.

#### Scenario: Form loads in modal

- **WHEN** the user opens the create panel
- **THEN** the form shows corporate styling, template preview placeholders, and env read-only ids

### Requirement: Offer search combobox

The system SHALL provide HTMX typeahead for Keitaro offers by id or name fragment, including suggestions on field focus.

#### Scenario: Offer suggestions

- **WHEN** the user types or focuses the offer field
- **THEN** matching offers appear in a dropdown

### Requirement: Client validation before submit

The system SHALL validate required name, geo ISO-2, and offer id in the browser before POST; errors SHALL appear as inline messages in reserved slots without resizing the modal abruptly.

#### Scenario: Missing offer

- **WHEN** the user submits without a selected offer id
- **THEN** the offer field is highlighted and a single inline error is shown; Keitaro create is not called

### Requirement: Create campaign template

The system SHALL on valid submit create in Keitaro a campaign with two streams: geo traffic redirects to Google; remaining traffic goes to one selected offer at 100% share; domain, group, and traffic source from env defaults.

#### Scenario: Successful create

- **WHEN** the user submits valid name, geo, and offer id
- **THEN** Keitaro receives campaign and both streams, SQLite stores the campaign, streams are fetched, and the user sees a success panel with Keitaro id and campaign URL

#### Scenario: API failure with rollback

- **WHEN** stream creation fails after the campaign was created
- **THEN** the remote campaign is deleted and the user sees an error without a local record

### Requirement: Validation before API

The system SHALL reject invalid geo format or missing/invalid offer on the server without calling Keitaro create.

#### Scenario: Invalid geo

- **WHEN** geo is not two-letter ISO-2
- **THEN** the form redisplays in the modal with an error

### Requirement: Post-create fetch and editor

The system SHALL run a full stream fetch into SQLite after create and provide navigation to the campaign editor from the success panel.

#### Scenario: Open editor from success

- **WHEN** the user clicks through to the editor from success
- **THEN** the editor opens for the local campaign id