# Proposal: foundation-keitaro-client

## Why

Без запускаемого приложения, БД и проверки Keitaro невозможно строить Home, создатель и редактор (F1–F7). Это первый change фазы F по [`PlanDocs/33-implementation-work-plan.md`](../../../PlanDocs/33-implementation-work-plan.md).

## Бизнес-обоснование

Проверяющий должен убедиться, что Legko **реально подключён** к тестовому Keitaro (F0 в [`PlanDocs/30-mvp-features-and-acceptance.md`](../../../PlanDocs/30-mvp-features-and-acceptance.md)).

## What Changes

- Каркас Python-пакета `legko/` (FastAPI, settings, SQLite, Alembic).
- HTTP-клиент Keitaro с `ping()` и обработкой ошибок без утечки ключа.
- `GET /health` — статус БД и Keitaro.
- Корневой UI-каркас: `base.html`, статика design tokens, заглушка ссылки «Документация».
- Начальная миграция ORM под кампании/потоки/офферы (схема из [`PlanDocs/15-architecture.md`](../../../PlanDocs/15-architecture.md) §4).

## Вне scope

- Home, create, editor (change 2–4).
- Реальные вызовы create/push Keitaro (кроме ping).
- F9 `/docs` (change 8).

## Capabilities

### New Capabilities

- `app-foundation`: конфигурация, FastAPI app, SQLite, миграции, статика и базовый layout.
- `keitaro-client`: httpx-адаптер, аутентификация Api-Key, `ping`.
- `health`: readiness endpoint.

### Modified Capabilities

_(нет — `openspec/specs/` пуст)_

## Impact

- Новый каталог `legko/` в репозитории, зависимости в `pyproject.toml`.
- **ProductDocs:** создать `ProductDocs/00-product-overview.md`.
- **PlanDocs:** F0 AC — без изменений замысла.