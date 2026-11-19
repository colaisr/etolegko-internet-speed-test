# Proposal: stream-editor-resync

## Why

F7 — повторный Fetch при **черновике** не затирает локальный микс; офферы, пропавшие в Keitaro (относительно снимка), → **removed**.

## Бизнес-обоснование

[`PlanDocs/02-stream-offer-editor.md`](../../../PlanDocs/02-stream-offer-editor.md), AC F7.1–F7.3 в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- `stream_fetch.full_fetch` — ветка `merge` при `has_draft`
- Сравнение с `stream_published_snapshots` для drift
- Unit-тесты merge

## Capabilities

### Modified Capabilities

- `stream-editor-fetch`: merge Fetch при черновике (F7)

## Impact

- **ProductDocs:** `02-stream-offer-editor.md`