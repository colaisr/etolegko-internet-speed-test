# Legko — техконтекст (OpenSpec)

Обёртка Keitaro для медиабайера: **симулятор сплита** (SQLite черновик → Push в Keitaro).

## Стек

Python 3.11, FastAPI, SQLAlchemy 2, Alembic, SQLite, Jinja2, HTMX, httpx.

## Документы

- Архитектура: `PlanDocs/15-architecture.md`
- Фичи / AC: `PlanDocs/30-mvp-features-and-acceptance.md`
- Карта реализации: `PlanDocs/31-feature-to-implementation-map.md`
- In-app docs: `PlanDocs/32-in-app-docs.md` — `ProductDocs/` рендерится на `/docs`
- In-app docs (поставка): `PlanDocs/32-product-docs-in-app.md` — `/docs` рендерит `ProductDocs/`

## Репозиторий (целевой пакет)

`legko/` — см. §2 в `15-architecture.md`.