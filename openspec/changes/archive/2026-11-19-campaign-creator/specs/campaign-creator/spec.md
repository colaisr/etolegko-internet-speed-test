## ADDED Requirements

### Requirement: Creator form

The system SHALL render a creator form at `GET /campaigns/new` with fields campaign name, geo (ISO-2), offer search combobox, read-only template preview, and read-only domain/group/source from configuration.

#### Scenario: Form loads

- **WHEN** the user opens `GET /campaigns/new`
- **THEN** the page shows corporate styling and template preview placeholders

### Requirement: Offer search combobox

The system SHALL provide HTMX typeahead for Keitaro offers by id or name fragment.

#### Scenario: Offer suggestions

- **WHEN** the user types in the offer field
- **THEN** matching offers appear in a dropdown

### Requirement: Create campaign template

The system SHALL on valid submit create in Keitaro a campaign with two streams: geo traffic redirects to Google; remaining traffic goes to one selected offer at 100% share; domain, group, and traffic source from env defaults.

#### Scenario: Successful create

- **WHEN** the user submits valid name, geo, and offer id
- **THEN** Keitaro receives campaign and both streams, SQLite stores the campaign, and the user sees a success screen with Keitaro id and campaign URL

#### Scenario: API failure with rollback

- **WHEN** stream creation fails after the campaign was created
- **THEN** the remote campaign is deleted and the user sees an error without a local record

### Requirement: Validation before API

The system SHALL reject invalid geo format or missing/invalid offer without calling Keitaro create.

#### Scenario: Invalid geo

- **WHEN** geo is not two-letter ISO-2
- **THEN** the form redisplays with an error

### Requirement: Post-create fetch and editor

The system SHALL run a full stream fetch into SQLite after create and provide navigation to the campaign editor from the success screen.

#### Scenario: Open editor from success

- **WHEN** the user clicks through to the editor from success
- **THEN** the editor opens for the local campaign id