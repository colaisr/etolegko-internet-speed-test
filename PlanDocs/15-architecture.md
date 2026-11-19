# Архитектура Legko (MVP)

> **Статус:** актуален (2026-11-19, **фаза E**). Фичи: [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md). UI: [`../ProjectDocs/design/design-system.md`](../ProjectDocs/design/design-system.md).

## 1. Стек (решение)

| Слой | Технология | Почему |
| --- | --- | --- |
| Язык | **Python 3.11+** | ТЗ / вакансия; тестовое |
| HTTP API + страницы | **FastAPI** | ТЗ; async **httpx** к Keitaro; один процесс с UI |
| ORM | **SQLAlchemy 2.x** | Зрелая модель, миграции |
| Миграции | **Alembic** | F0.2 |
| БД | **SQLite** | Решение product |
| Шаблоны | **Jinja2** | Корп. HTML из [`legko-corporate-prototype.html`](../ProjectDocs/design/artifacts/prototypes/legko-corporate-prototype.html) |
| Интерактив без SPA | **HTMX 2** | Частичные обновления таблицы, modal push |
| Стили | **legko-tokens.css** + **components.css** | Единый design-system |
| Запуск | **uvicorn** | `uvicorn legko.main:app` |
| Тесты | **pytest** | Unit: веса, diff; integration: SQLite in-memory |
| Lint | **ruff** | Минимально |

**Не в MVP:** Celery, Redis, отдельный фронт-сборщик (Vite/React), Postgres.

## 2. Структура репозитория (целевая)

```text
legko/
  pyproject.toml
  alembic.ini
  .env.example
  README.md
  alembic/versions/
  legko/
    main.py                 # FastAPI app, static, templates
    settings.py             # pydantic-settings
    db/
      session.py
      base.py
    models/                 # SQLAlchemy ORM
      campaign.py
      stream.py
      stream_offer.py
    domain/                 # Чистая логика без HTTP/ORM
      weights.py            # largest remainder, pin rules
      diff.py               # F6: delta для modal
      validation.py         # sum 100%, min 1 active
    services/
      health.py             # F0.3
      campaign_creator.py   # F2
      campaign_nav.py       # F1, lazy import
      stream_fetch.py       # F3, F7
      offer_editor.py       # F4
      publish.py            # F5, F6 push/cancel
    integrations/
      keitaro/
        client.py           # httpx, timeouts, errors
        mappers.py          # API DTO ↔ domain
        types.py
    web/
      routes_pages.py       # HTML: home, create, editor
      routes_actions.py     # HTMX POST endpoints
      routes_docs.py        # F9: /docs, рендер ProductDocs/*.md
      routes_docs.py        # F9: ProductDocs → HTML
      doc_renderer.py       # markdown, safe
      deps.py               # DB session, settings
    templates/
      base.html
      home.html
      creator.html
      editor.html
      partials/             # offer_table, push_modal, badges
    static/
      css/legko-tokens.css
      css/components.css
  tests/
    unit/test_weights.py
    unit/test_diff.py
    integration/...
```

Один пакет **`legko`**: домен не зависит от Keitaro; интеграция — за adapter.

## 3. Слои и зависимости

```text
┌─────────────────────────────────────────┐
│  web (Jinja + HTMX)                     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  services (use-cases: F1–F7)            │
└─────┬───────────────────────┬───────────┘
      │                       │
┌─────▼─────┐           ┌─────▼──────────┐
│  domain   │           │ integrations/  │
│  weights  │           │ keitaro/client │
│  diff     │           └────────────────┘
└───────────┘
      │
┌─────▼─────┐
│ models +  │
│ SQLite    │
└───────────┘
```

## 4. Модель данных (ORM)

### `campaigns`

| Поле | Тип | Примечание |
| --- | --- | --- |
| `id` | UUID PK | Локальный id для URL редактора |
| `keitaro_campaign_id` | int, unique nullable | После create |
| `name` | str | |
| `campaign_url` | str nullable | После create |
| `geo_code` | str nullable | Из create, справочно |
| `sync_status` | enum | `synced` / `draft` / `needs_fetch` |
| `created_at`, `updated_at` | datetime | Недавние F1 |

### `streams`

| Поле | Тип | Примечание |
| --- | --- | --- |
| `id` | UUID PK | |
| `campaign_id` | FK | |
| `keitaro_stream_id` | int | |
| `stream_type` | enum | `offer` \| `service` |
| `has_draft` | bool | Жёлтый UI |

### `stream_offers`

| Поле | Тип | Примечание |
| --- | --- | --- |
| `id` | UUID PK | |
| `stream_id` | FK | Только `offer` stream |
| `keitaro_offer_id` | int | |
| `offer_name` | str nullable | Кэш для таблицы |
| `weight_percent` | int 0–100 | |
| `is_pinned` | bool | |
| `pinned_percent` | int nullable | Если pinned |
| `status` | enum | `active` \| `removed` |

### `stream_published_snapshots`

JSON-снимок строк `stream_offers` **после последнего успешного Push** — для **Cancel** (F5.1).

### Настройки создателя (F2)

Из **env** (не БД в MVP): `KEITARO_DEFAULT_DOMAIN_ID`, `KEITARO_DEFAULT_GROUP_ID`, `KEITARO_DEFAULT_SOURCE_ID` (+ опционально человекочитаемые label для UI).

## 5. Keitaro adapter

Класс `KeitaroClient` (httpx):

| Метод | Фича | Примечание |
| --- | --- | --- |
| `ping()` | F0.3 | Лёгкий endpoint |
| `search_offers(q)` | F2, F4 | Для combobox |
| `create_campaign_with_template(...)` | F2 | Атомарная последовательность API; rollback-компенсация при сбое |
| `get_campaign_streams(campaign_id)` | F3, F7 | |
| `get_stream_offers(stream_id)` | F3 | |
| `update_stream_offers(stream_id, offers[])` | F5 | Push |

Точные пути API — **spike в E0** (`foundation-keitaro-client`); adapter изолирует расхождения документации.

Ошибки: `KeitaroError` с `user_message` → flash/HTMX alert.

## 6. Доменная логика (тестируемая без БД)

### `domain/weights.py` — F4.5

- `recalculate(offers, pinned_policy) -> list[int]` — largest remainder, сумма 100.
- Учёт: только `status=active`; remove = 0, не в пуле.

### `domain/validation.py` — F6

- `can_push(offers) -> (bool, reason)`.

### `domain/diff.py` — F6.3

- `build_push_diff(current, published_snapshot) -> PushDiff` (add/remove/weight changes).

### `services/stream_fetch.py` — F3, F7

- С merge-правилом: если **есть локальный draft** (`has_draft`), Fetch обновляет только «пропавшие в Keitaro» → `removed`, не затирает незапушенные add без явной product-политики → **если has_draft: merge по id; исчезнувшие → removed**.

### `services/publish.py` — F5

1. `validate` → `diff` → Keitaro `update` → snapshot → `sync_status=synced`, `has_draft=false`.

### `services/campaign_nav.py` — F1 lazy import

- `open_by_keitaro_id`: нет локальной записи → create shell campaign → `stream_fetch.full_fetch`.

## 7. Web / маршруты

| Метод | Путь | Фича |
| --- | --- | --- |
| GET | `/` | F1 Home |
| GET | `/health` | F0 JSON |
| GET | `/docs` | F9 индекс ProductDocs |
| GET | `/docs/{page_slug}` | F9 страница ProductDocs |
| GET | `/docs` | F9 index ProductDocs |
| GET | `/docs/{page}` | F9 render ProductDocs/*.md |
| POST | `/campaigns/open` | F1.2 open by keitaro id |
| GET/POST | `/campaigns/new` | F2 create form |
| GET | `/campaigns/{id}/editor` | F3 editor (+ auto fetch if never) |
| POST | `/campaigns/{id}/fetch` | F3, F7 HTMX |
| POST | `/campaigns/{id}/offers` | F4 add |
| POST | `/campaigns/{id}/offers/{oid}/remove` | F4 |
| POST | `/campaigns/{id}/offers/{oid}/restore` | F4 bring back |
| POST | `/campaigns/{id}/offers/{oid}/pin` | F4 |
| POST | `/campaigns/{id}/cancel` | F5 |
| GET | `/campaigns/{id}/push/preview` | F6 modal |
| POST | `/campaigns/{id}/push` | F5 |

HTMX: partial `partials/offer_table.html`, `partials/campaign_header.html`.

## 8. Картирование F0–F8 → модули

| Фича | Модули |
| --- | --- |
| F0 | `settings`, `db`, `alembic`, `health`, `KeitaroClient.ping` |
| F1 | `routes_pages`, `campaign_nav`, templates `home.html` |
| F2 | `campaign_creator`, `KeitaroClient.create_*` |
| F3 | `stream_fetch`, `editor` template |
| F4 | `offer_editor`, `domain/weights` |
| F5 | `publish`, snapshots |
| F6 | `validation`, `diff`, push preview template |
| F7 | `stream_fetch.merge_removed` |
| F8 | README, `.env.example`, `pyproject.toml` scripts |
| F9 | `routes_docs.py`, link в `base.html`, markdown render |
| F9 | `routes_docs`, `doc_renderer`, header link, ProductDocs pages |

## 9. Конфигурация (`.env.example`)

```bash
DATABASE_URL=sqlite:///./data/legko.db
KEITARO_BASE_URL=https://tlgk.host/admin_api/v1
KEITARO_API_KEY=
KEITARO_DEFAULT_DOMAIN_ID=
KEITARO_DEFAULT_GROUP_ID=
KEITARO_DEFAULT_SOURCE_ID=
KEITARO_GOOGLE_REDIRECT_URL=https://www.google.com
```

`KEITARO_GOOGLE_REDIRECT_URL` — поток 1 (F2), по умолчанию Google.

## 10. Безопасность (MVP)

- API key только env, не логировать.
- Нет auth: один байер, один инстанс (scope product).
- CSRF: для HTMX POST — SameSite cookies + token при необходимости (E0 decision minimal).

## 11. Тесты (минимум для сдачи)

| Область | Тип |
| --- | --- |
| `domain/weights` | unit, таблица примеров F4 |
| `domain/diff` | unit |
| `domain/validation` | unit |
| `publish` + fake Keitaro | integration с mock httpx |

## 12. Точка готовности §28

После этого документа и [`31-feature-to-implementation-map.md`](31-feature-to-implementation-map.md):

- Product: фичи покрыты модулями ✓  
- Design: tokens → `static/css` ✓  
- Architecture: стек и границы ✓  

→ **фаза F** (OpenSpec + код).

## 13. OpenSpec: порядок changes (рекомендация developer)

1. ~~`foundation-keitaro-client`~~ — **готово** (F0); ProductDocs: `00-product-overview.md`  
2. `home-navigation` — F1  
3. `campaign-creator` — F2  
4. `stream-editor-fetch-ui` — F3  
5. `stream-editor-offer-ops` — F4  
6. `stream-editor-publish` — F5+F6  
7. `stream-editor-resync` — F7  
8. `project-readme-delivery` — F8  