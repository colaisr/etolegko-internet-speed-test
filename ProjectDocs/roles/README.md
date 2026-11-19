# Роли агентов Legko

> **Статус:** инфраструктура скопирована из Gloom (2026-11-19). Суть роли — в `ProjectDocs/roles/<role>.md`, адаптеры (`.claude/agents/<role>.md`) только маршрутизируют и задают tools.

## Слои

| Слой | Путь | Назначение |
| --- | --- | --- |
| Конституция | `AGENTS.md` | Продукт, метрики, процесс |
| Индекс памяти | `PlanDocs/README.md` | Замысел продукта, по нему делается реализация |
| Технические спеки | `openspec/README.md` | Как система работает: `specs/` и активные `changes/` |
| Бизнес-база | `ProductDocs/README.md` | Как продукт работает сейчас, для владельцев и сотрудников |
| Роль | `ProjectDocs/roles/<role>.md` | Миссия, гейты, «не делать», чтение по задаче |
| Субагент Claude Code | `.claude/agents/<role>.md` | `name`, `description`, `tools` + короткое тело |

Правило: меняешь поведение роли — правишь файл роли; меняешь только маршрутизацию или tools — правишь адаптер.

## Иерархия правды

1. `AGENTS.md` (конституция) → 2. `PlanDocs/` (замысел) → 3. `openspec/specs/` (норма поведения после archive) → 4. `ProjectDocs/roles/<role>.md` → 5. адаптеры. При конфликте выше побеждает. `ProductDocs/` — производное описание для бизнеса: расходится со спекой — исправляют страницу.

## Чтение контекста

T0 — `AGENTS.md`; T1 — файл роли; T2 — файлы из «Обязательного чтения» роли для этой задачи; T3 — справочники по триггеру. Не читать весь `PlanDocs` целиком.

## Роли

| Роль | Когда вызывать |
| --- | --- |
| product | Приоритеты, scope, экономика, гейты 1/4, Outcome Check |
| **project-manager** | Задачи и статусы в task-системе, ежедневный статус, недельный отчёт владельцу с часами |
| designer | UX/UI, дизайн-система, ревью интерфейса |
| content-manager | Тексты интерфейса, помощь, правила, промо-копирайт |
| developer | Реализация по спеке |
| spec-verifier | Сверка кода со спекой |
| code-reviewer | Ревью diff по scope_files |
| security-reviewer | change-гейт и audit (платежи, коины, выплаты, видео, PII) |
| qa | Проверка по acceptance criteria, пост-деплой |
| seo | SEO + AEO, срез трафика |
| marketing | Привлечение зрителей и креаторов, фестивали и сейлы |

## Поток разработки

```text
product (гейт 1) → project-manager заводит задачи → developer
  → /verify-change: spec-verifier → code-reviewer ∥ security-reviewer → qa → spec-verifier (docs-sync)
  → seo (публичные страницы) → product (гейт 4) → релиз → qa пост-деплой → /opsx:archive → Outcome Check
project-manager: статусы на каждом шаге, ежедневный статус, недельный отчёт
```

Различие с AgentPoint: добавлен **project-manager**; в verify добавлен гейт **docs-sync** (ProductDocs). OpenSpec подключён 2026-11-04 (рецепт — [`openspec-gates.md`](openspec-gates.md)); скрипты проверок `verify:*` и замок на push появятся с кодом.
