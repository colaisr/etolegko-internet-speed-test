# Tasks: foundation-keitaro-client

## Implementation

- [x] 1.1 `legko/pyproject.toml`, структура пакета по `15-architecture.md`
- [x] 1.2 `settings.py`, `.env` loading; `data/` в `.gitignore`
- [x] 1.3 SQLAlchemy models + Alembic initial revision
- [x] 1.4 `KeitaroClient.ping`, errors
- [x] 1.5 `GET /health`, `services/health.py`
- [x] 1.6 `main.py`: static, Jinja2, `/` stub, base template + tokens CSS
- [x] 1.7 Smoke: import app, optional pytest health unit

## ProductDocs

- [x] 2.1 Создать `ProductDocs/00-product-overview.md`, индекс в `ProductDocs/README.md`

## Гейты ролей

- [ ] 3.1 spec-verify
- [ ] 3.2 code-reviewer
- [ ] 3.3 security-reviewer
- [ ] 3.4 qa
- [ ] 3.5 docs-sync

## Валидация (qa)

- [x] 4.1 `alembic upgrade head` с нуля
- [x] 4.2 `curl /health` (локально)
- [x] 4.3 ruff / pytest при наличии