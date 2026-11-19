# Design: foundation-keitaro-client

## Решения

| Тема | Решение |
| --- | --- |
| Расположение кода | `legko/pyproject.toml`, пакет `legko/legko/` — по [`15-architecture.md`](../../../PlanDocs/15-architecture.md) §2 |
| Settings | `pydantic-settings`, чтение `.env`, секреты только из env |
| DB | SQLAlchemy 2 declarative, `DATABASE_URL`, каталог `data/` для SQLite (в `.gitignore`) |
| Миграции | Alembic autogenerate от моделей; первая ревизия — campaigns, streams, stream_offers |
| Keitaro ping | `GET {KEITARO_BASE_URL}/campaigns?limit=1`, заголовок `Api-Key` |
| Health | JSON: `app`, `database`, `keitaro` с `ok` / сообщением ошибки (без ключа в ответе) |
| UI | Скопировать `legko-tokens.css` в `static/css/`; `base.html` с header по design-system |

## Keitaro adapter

Класс `KeitaroClient` в `integrations/keitaro/client.py`:

- Таймаут httpx 15s.
- `KeitaroError` с `user_message` для UI позже.
- `ping()` → bool + опциональная причина.

Security-reviewer: ключ не логировать; при отсутствии ключа — понятная ошибка health.

## Зависимости (pyproject)

fastapi, uvicorn[standard], sqlalchemy, alembic, pydantic-settings, httpx, jinja2, python-multipart.

Dev: pytest, ruff.