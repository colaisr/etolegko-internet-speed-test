# Legko (Python app)

Запуск из этой папки:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp ../.env.example ../.env   # заполнить KEITARO_API_KEY
alembic upgrade head
uvicorn legko.main:app --reload
```

`GET /health` — проверка БД и Keitaro.