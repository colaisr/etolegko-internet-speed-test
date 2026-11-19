## ADDED Requirements

### Requirement: Campaign editor page

The system SHALL render the campaign editor at `GET /campaigns/{local_id}/editor` with campaign header (name, Keitaro id, URL), sync status pill, and a Fetch Streams action.

#### Scenario: Editor loads with streams

- **WHEN** the campaign has fetched streams in SQLite
- **THEN** the page shows a service stream lock row and an offer stream table with id, name, weight %, pin flag, and status

#### Scenario: No streams yet

- **WHEN** the campaign has no local streams
- **THEN** the page prompts the user to run Fetch Streams

### Requirement: Manual stream fetch

The system SHALL reload streams and offer rows from Keitaro via `POST /campaigns/{local_id}/fetch` using full_fetch.

#### Scenario: Fetch succeeds

- **WHEN** the user submits Fetch and Keitaro responds
- **THEN** local streams mirror Keitaro and sync status becomes synced

#### Scenario: Fetch fails

- **WHEN** Keitaro returns an error
- **THEN** the editor redisplays with an error message and does not delete the campaign record