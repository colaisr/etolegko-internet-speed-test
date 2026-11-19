# Proposal: stream-editor-fetch-ui

## Why

F3 даёт байеру **реальный экран редактора** после create/open: сверка с Keitaro (Fetch), таблица офферов и служебный поток — база для симулятора сплита (F4+).

## Бизнес-обоснование

[`PlanDocs/02-stream-offer-editor.md`](../../../PlanDocs/02-stream-offer-editor.md), AC F3.1–F3.5 в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- `GET /campaigns/{id}/editor` — шапка, status pill, Fetch Streams.
- `POST /campaigns/{id}/fetch` — `full_fetch` из Keitaro.
- Таблица офферов (read-only в F3), строка служебного потока.
- ProductDocs `02-stream-offer-editor.md`.

## Вне scope

- Add/Remove/Pin, Push/Cancel (F4–F6), merge при drift (F7).

## Capabilities

### New Capabilities

- `stream-editor-fetch`: editor UI, manual fetch, отображение потоков.

### Modified Capabilities

_(нет)_

## Impact

- **PlanDocs:** `02-stream-offer-editor.md`
- **ProductDocs:** `ProductDocs/02-stream-offer-editor.md`