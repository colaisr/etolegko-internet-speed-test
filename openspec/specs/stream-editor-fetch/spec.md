# stream-editor-fetch Specification

## Purpose

Экран редактора кампании: загрузка потоков из Keitaro (Fetch), отображение служебного потока и таблицы офферов.

## Requirements

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
- **THEN** local streams mirror Keitaro and sync status becomes synced when there is no draft

#### Scenario: Fetch fails

- **WHEN** Keitaro returns an error
- **THEN** the editor redisplays with an error message and does not delete the campaign record

### Requirement: Post-create auto fetch

The system SHALL run full_fetch automatically after successful campaign create when Keitaro API succeeds.

#### Scenario: Create then open editor

- **WHEN** the user opens the editor after create
- **THEN** offer and service streams are usually already present without manual Fetch

### Requirement: Draft-preserving fetch (F7)

When the offer stream has `has_draft`, the system SHALL merge Keitaro stream data instead of replacing local offer rows: service streams may refresh; local unpushed adds remain; offers that were active in the published snapshot but are missing from Keitaro become **removed**.

#### Scenario: Drift marks removed

- **WHEN** the user runs Fetch with a draft and Keitaro no longer lists an offer that was active in the published snapshot
- **THEN** that local row becomes removed and active weights are recalculated

#### Scenario: Local add survives fetch

- **WHEN** the user added an offer only locally (not in the published snapshot) and runs Fetch
- **THEN** that row stays active even if Keitaro does not list it yet

#### Scenario: No draft replaces

- **WHEN** `has_draft` is false
- **THEN** Fetch replaces local streams from Keitaro and updates the published snapshot