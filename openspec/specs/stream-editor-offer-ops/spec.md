# stream-editor-offer-ops Specification

## Purpose

Локальные операции с оффер-ротацией в редакторе: добавление, удаление, возврат, pin/unpin и пересчёт весов без записи в Keitaro до Push.

## Requirements

### Requirement: Add offer to rotation

The system SHALL add an offer to the local offer stream via `POST /campaigns/{local_id}/offers` with Keitaro offer id, recalculate active weights to sum 100%, and mark the offer stream draft.

#### Scenario: Add succeeds

- **WHEN** the user submits a valid offer id from search or manual entry
- **THEN** a new active row appears, weights redistribute, and `has_draft` is true

#### Scenario: Add invalid offer

- **WHEN** the offer id is missing or not found in Keitaro
- **THEN** the user sees `op_error` on the editor and no partial row is left inconsistent

### Requirement: Remove and restore offers

The system SHALL set an active offer to removed with weight 0%, recalculate remaining active weights, and allow restore to active with recalculation.

#### Scenario: Remove row

- **WHEN** the user removes an active offer
- **THEN** the row shows removed styling, weight is 0%, and active weights sum to 100%

#### Scenario: Restore row

- **WHEN** the user restores a removed offer
- **THEN** the row becomes active and weights recalculate to 100%

### Requirement: Pin and unpin weights

The system SHALL pin an active offer to a given percent (1–99), redistribute unpinned active offers, and unpin to return the offer to the unpinned pool.

#### Scenario: Pin fixed percent

- **WHEN** the user pins an offer with a valid percent
- **THEN** pinned percent is stored, unpinned rows split the remainder, and total active weight is 100%

#### Scenario: Unpin

- **WHEN** the user unpins a pinned offer
- **THEN** all active offers become unpinned and weights recalculate to 100%

### Requirement: Weight distribution algorithm

The system SHALL distribute integer percents using largest remainder so active weights sum to exactly 100.

#### Scenario: Three equal unpinned offers

- **WHEN** three active unpinned offers share the pool
- **THEN** weights are 34/33/33 or equivalent per largest remainder

### Requirement: No Keitaro push in F4

The system SHALL NOT update Keitaro campaign stream weights via API during add/remove/pin operations in this capability.

#### Scenario: Local-only mutation

- **WHEN** the user performs add/remove/pin/unpin
- **THEN** only SQLite rows change until F5 Push is implemented