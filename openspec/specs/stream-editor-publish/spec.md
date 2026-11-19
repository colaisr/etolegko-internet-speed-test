# stream-editor-publish Specification

## Purpose

Публикация локального сплита в Keitaro (F5) с обязательным diff и валидацией (F6).

## Requirements

### Requirement: Publish snapshot baseline

The system SHALL persist a JSON snapshot of offer-stream rows after each successful Fetch and after each successful Push, used for Cancel and diff.

#### Scenario: Fetch establishes baseline

- **WHEN** `full_fetch` completes for a campaign with an offer stream
- **THEN** a `stream_published_snapshots` row exists for that stream with the current offer rows

### Requirement: Push validation (F6)

The system SHALL enable Push only when the offer stream has `has_draft`, at least one active offer, and active weights sum to 100%.

#### Scenario: Invalid sum blocks Push

- **WHEN** active weights sum is not 100%
- **THEN** the Push control is disabled with a reason mentioning the sum

### Requirement: Push diff modal (F6)

The system SHALL serve `GET /campaigns/{local_id}/push/preview` returning add/remove/weight changes vs the published snapshot before POST push.

#### Scenario: Preview lists delta

- **WHEN** the user opens Push with a valid draft
- **THEN** the modal lists additions, removals, and weight changes compared to the snapshot

### Requirement: Push to Keitaro (F5)

The system SHALL apply active offers and weights via Keitaro stream update on confirmed POST push; on success clear `has_draft`, set campaign `sync_status` to synced, and refresh the snapshot.

#### Scenario: Successful push

- **WHEN** POST push succeeds
- **THEN** Keitaro receives active `offer_id` and `share` pairs matching the table and the stream is no longer draft

#### Scenario: Failed push keeps draft

- **WHEN** Keitaro returns an error on push
- **THEN** the local draft remains and the user sees an error message

### Requirement: Cancel draft (F5)

The system SHALL restore offer-stream rows from the published snapshot on `POST /campaigns/{local_id}/cancel` without calling Keitaro.

#### Scenario: Cancel restores

- **WHEN** Cancel is submitted with an active draft and a snapshot exists
- **THEN** local rows match the snapshot and `has_draft` is false