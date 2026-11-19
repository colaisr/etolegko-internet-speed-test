# Proposal: stream-editor-publish

## Why

F5/F6 — осознанный Push в Keitaro с diff-модалкой, валидацией Σ=100% и Cancel к последнему синхронизированному снимку.

## Бизнес-обоснование

[`PlanDocs/02-stream-offer-editor.md`](../../../PlanDocs/02-stream-offer-editor.md) §5 Push/Cancel, AC F5.* и F6.* в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- `domain/validation.py`, `domain/diff.py`, `services/publish.py`, `services/stream_snapshot.py`
- ORM `stream_published_snapshots`, Alembic migration
- `KeitaroClient.update_stream_offers`, маршруты push preview/push/cancel
- Editor dock + PushConfirm modal, `ProductDocs/02`

## Вне scope

- Drift-merge при Fetch (F7), in-app `/docs` (F9)

## Capabilities

### New Capabilities

- `stream-editor-publish`: Cancel, Push, diff modal, snapshot baseline

### Modified Capabilities

- `stream-editor-fetch`: после Fetch сохраняется опорный snapshot
- `stream-editor-offer-ops`: dock Push/Cancel активируется при черновике

## Impact

- **ProductDocs:** `02-stream-offer-editor.md`
- **Design:** PushConfirmModal, editor publish dock