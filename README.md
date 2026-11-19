# Legko

Обёртка над Keitaro (тестовое задание): Legko — симулятор сплита офферов с Push в Keitaro.

## Память проекта

| Папка | Назначение |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Конституция и процесс |
| [`PlanDocs/`](PlanDocs/README.md) | Замысел продукта (сейчас пустой каталог) |
| [`ProductDocs/`](ProductDocs/README.md) | Как продукт работает сейчас (пусто) |
| [`openspec/`](openspec/README.md) | Технические спеки и changes |
| [`ProjectDocs/`](ProjectDocs/roles/README.md) | Роли агентов, дизайн-артефакты |
| [`PlanDocs/28-pre-implementation-process.md`](PlanDocs/28-pre-implementation-process.md) | Фазы до реализации (без PM) |
| [`PlanDocs/33-implementation-work-plan.md`](PlanDocs/33-implementation-work-plan.md) | **Реализация: 8 changes, чеклисты** |

## Запуск приложения

```bash
cd legko
python3.12 -m venv .venv && source .venv/bin/activate
uv pip install -e ".[dev]"   # или pip install -e ".[dev]"
alembic upgrade head
uvicorn legko.main:app --reload
```

### Ключ Keitaro (обязательно)

1. В трекере: **Account → API keys** — создайте ключ.
2. В **корне репозитория** (рядом с `PlanDocs/`, не внутри `legko/`):

```bash
cp .env.example .env
```

3. В `.env` пропишите:

```bash
KEITARO_API_KEY=ваш_ключ_без_кавычек
KEITARO_BASE_URL=https://tlgk.host/admin_api/v1   # если другой хост — замените
KEITARO_DEFAULT_DOMAIN_ID=...
KEITARO_DEFAULT_GROUP_ID=...
KEITARO_DEFAULT_SOURCE_ID=...
```

Файл `.env` в git **не коммитится**. Без ключа `/health` и поиск кампаний на главной не работают. Для **создателя кампании** (`/campaigns/new`) нужны три `KEITARO_DEFAULT_*_ID` (ID из Keitaro admin).

### Git hooks (ProductDocs перед push)

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
node scripts/verify-productdocs.mjs   # ручная проверка
```

## Агенты и OpenSpec

- Команды Cursor: `.cursor/commands/` (`/opsx:propose`, `/opsx:apply`, …)
- Роли: `ProjectDocs/roles/`, субагенты Claude: `.claude/agents/`
- Гейты и verify: `scripts/verify-change-gates.mjs`, `ProjectDocs/roles/openspec-gates.md`

## Запуск кода

Появится после выбора стека в PlanDocs и первого change «фундамент».