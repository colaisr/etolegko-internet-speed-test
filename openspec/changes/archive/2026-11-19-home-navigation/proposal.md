# Proposal: home-navigation

## Why

После F0 байеру нужна **точка входа**: создать кампанию или открыть известную по Keitaro ID / из недавних — без обхода Keitaro admin.

## Бизнес-обоснование

F1 в [`PlanDocs/03-home-and-navigation.md`](../../../PlanDocs/03-home-and-navigation.md) и AC F1.1–F1.4 в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- Экран Home (hero, CTA «Создать», open by ID, недавние).
- `campaign_nav`: недавние из SQLite, lazy import по Keitaro id.
- Заглушки маршрутов Creator и минимальный Editor (полный UI — changes 3–4).
- Keitaro `get_campaign(id)`.

## Вне scope

- Полный Creator (F2), Fetch/таблица офферов (F3).
- `/docs` рендер ProductDocs (F9) — заглушка или 404.

## Capabilities

### New Capabilities

- `home-navigation`: Home UI, recent list, open by Keitaro id, переход в editor.

### Modified Capabilities

_(нет)_

## Impact

- **PlanDocs:** [`03-home-and-navigation.md`](../../../PlanDocs/03-home-and-navigation.md)
- **ProductDocs:** создать `ProductDocs/03-home-and-navigation.md`