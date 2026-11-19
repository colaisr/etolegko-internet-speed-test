# Legko

Обёртка над [Keitaro](https://keitaro.io) для тестового задания: создание типовых кампаний и **симулятор сплита офферов** с Push в трекер.

**Репозиторий:** https://github.com/colaisr/etolegko-internet-speed-test

## Быстрый старт

```bash
git clone https://github.com/colaisr/etolegko-internet-speed-test.git
cd etolegko-internet-speed-test/legko
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn legko.main:app --reload
```

Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/) — главная Legko.  
Справка по продукту в приложении: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** (рендер `ProductDocs/`).  
OpenAPI: `/api/docs`.

### Переменные окружения

Файл **`.env` в корне репозитория** (рядом с `ProductDocs/`, не внутри `legko/`):

```bash
cp .env.example .env
```

Минимум для работы с Keitaro:

```bash
KEITARO_API_KEY=ваш_ключ
KEITARO_BASE_URL=https://tlgk.host/admin_api/v1
KEITARO_DEFAULT_DOMAIN_ID=...
KEITARO_DEFAULT_GROUP_ID=...
KEITARO_DEFAULT_SOURCE_ID=...
```

Без ключа `/health` сообщит об ошибке; без `KEITARO_DEFAULT_*` недоступен создатель кампании. `.env` не коммитится.

### Память проекта

| Папка | Назначение |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Процесс и правила |
| [`PlanDocs/`](PlanDocs/README.md) | Замысел продукта |
| [`ProductDocs/`](ProductDocs/README.md) | Как продукт работает **сейчас** (тот же текст на `/docs`) |
| [`openspec/`](openspec/README.md) | Технические спеки |
| [`ProjectDocs/`](ProjectDocs/roles/README.md) | Роли, дизайн |

## Сценарий приёмки (проверяющему)

1. **Главная** — открыть кампанию по Keitaro ID или создать новую.
2. **Создатель** — имя, geo, оффер → двухпотоковая кампания в Keitaro → переход в редактор.
3. **Редактор** — при необходимости «Обновить из Keitaro»; Add / Remove / Pin; сумма active **100%**.
4. **Push** — diff-модалка → подтверждение → веса в Keitaro = таблице.
5. **Документация** — шапка «Документация» → `/docs` (разделы 00–03).

Подробнее: [`PlanDocs/26-key-flows.md`](PlanDocs/26-key-flows.md), ProductDocs в приложении.

## Разработка

```bash
cd legko
source .venv/bin/activate
pytest -q
ruff check .
```

Перед push:

```bash
git config core.hooksPath .githooks   # один раз
node scripts/verify-productdocs.mjs
node scripts/verify-change-gates.mjs --change <slug>
```

План этапов: [`PlanDocs/33-implementation-work-plan.md`](PlanDocs/33-implementation-work-plan.md).