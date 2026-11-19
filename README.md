# Legko

Обёртка над Keitaro (тестовое задание). Репозиторий на этапе **скелета**: продуктовая память, агенты и OpenSpec (по образцу проекта Gloom), **код приложения пока не добавлен**.

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

## Запуск приложения (change foundation)

```bash
cd legko
python3.12 -m venv .venv && source .venv/bin/activate
uv pip install -e ".[dev]"   # или pip install -e ".[dev]"
cp ../.env.example ../.env    # заполнить KEITARO_API_KEY
alembic upgrade head
uvicorn legko.main:app --reload
```

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