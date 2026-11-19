# Legko (Python app)

Запуск из этой папки:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
# в корне репозитория: cp .env.example .env → KEITARO_API_KEY (см. корневой README.md)
alembic upgrade head
uvicorn legko.main:app --reload
```

`GET /health` — проверка БД и Keitaro.