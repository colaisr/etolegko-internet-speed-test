# Legko

Обёртка над Keitaro (тестовое задание). Репозиторий на этапе **скелета**: продуктовая память, агенты и OpenSpec (по образцу проекта Gloom), **код приложения пока не добавлен**.

## Память проекта

| Папка | Назначение |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Конституция и процесс |
| [`PlanDocs/`](PlanDocs/README.md) | Замысел продукта (сейчас пустой каталог) |
| [`ProductDocs/`](ProductDocs/README.md) | Как продукт работает сейчас (пусто) |
| [`openspec/`](openspec/README.md) | Технические спеки и changes |
| [`ProjectDocs/`](ProjectDocs/roles/README.md) | Роли агентов, PM, дизайн-артефакты |

## Агенты и OpenSpec

- Команды Cursor: `.cursor/commands/` (`/opsx:propose`, `/opsx:apply`, …)
- Роли: `ProjectDocs/roles/`, субагенты Claude: `.claude/agents/`
- Гейты и verify: `scripts/verify-change-gates.mjs`, `ProjectDocs/roles/openspec-gates.md`

## Запуск кода

Появится после выбора стека в PlanDocs и первого change «фундамент».