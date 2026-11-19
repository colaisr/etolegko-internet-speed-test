# Proposal: stream-editor-offer-ops

## Why

F4 — локальный симулятор: add/remove/bring back/pin с пересчётом % без изменений Keitaro до Push.

## Бизнес-обоснование

[`PlanDocs/02-stream-offer-editor.md`](../../../PlanDocs/02-stream-offer-editor.md), AC F4.1–F4.6 в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- `domain/weights.py`, `services/offer_editor.py`
- Editor routes + UI actions, draft stream (`has_draft`, yellow card)
- Unit tests weights + offer_editor

## Вне scope

- Push, Cancel, diff modal (F5/F6), drift merge (F7)

## Capabilities

### New Capabilities

- `stream-editor-offer-ops`: add/remove/restore/pin, largest remainder, local draft.

### Modified Capabilities

- `stream-editor-fetch`: editor UI расширен действиями и промежуточным dock (read-only push disabled).

## Impact

- **ProductDocs:** `02-stream-offer-editor.md`
- **Design:** `ProjectDocs/design` (EditorWorkspace, IconButton)