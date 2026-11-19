# Роли агентов Legko

> **Статус:** актуален (2026-11-19). Процесс до кода — [`PlanDocs/28-pre-implementation-process.md`](../../PlanDocs/28-pre-implementation-process.md). **Project-manager в Legko не используется.**

## Слои

| Слой | Путь | Назначение |
| --- | --- | --- |
| Конституция | `AGENTS.md` | Продукт, память, процесс |
| Процесс до реализации | `PlanDocs/28-pre-implementation-process.md` | Фазы A–F, точка готовности |
| Индекс памяти | `PlanDocs/README.md` | Замысел продукта |
| Технические спеки | `openspec/README.md` | После начала реализации |
| Бизнес-база | `ProductDocs/README.md` | «Как есть» после changes |
| Роль | `ProjectDocs/roles/<role>.md` | Миссия, гейты, чтение |
| Субагент | `.claude/agents/<role>.md` | Маршрутизация и tools |

## Иерархия правды

`AGENTS.md` → `PlanDocs/` → `openspec/specs/` → роли → адаптеры. `ProductDocs/` — производное для бизнеса.

## Поток Legko (без PM)

```text
До реализации (фазы A–E):
  product (ценность, функционал, фичи)
    → designer (облик)
    → product (детальный разрез)
    → developer (стек + архитектура)
  → точка готовности §6 в PlanDocs/28

Реализация (фаза F):
  product (гейт 1 на change) → developer → /verify-change → релиз → /opsx:archive
```

Планирование этапов: **владелец + product** в `PlanDocs/25-mvp-plan.md` и OpenSpec, без отдельной task-системы.

## Активные роли (предача и MVP)

| Роль | Когда |
| --- | --- |
| **product** | Фазы A, B, D; гейт 1; Outcome Check |
| **designer** | Фаза C |
| **developer** | Фаза E; реализация |

## Роли после старта кода

| Роль | Когда |
| --- | --- |
| developer | Реализация по спеке |
| spec-verifier | Сверка со спекой |
| code-reviewer | Ревью diff |
| security-reviewer | Keitaro API, секреты, auth (когда появится) |
| qa | Acceptance criteria |

## Не используем в Legko

| Роль / путь | Причина |
| --- | --- |
| **project-manager** | Решение владельца; план в PlanDocs |
| marketing, seo, content-manager | Не нужны для тестового |
| `ProjectDocs/pm/` | Не ведём статусы в Jira |

## Поток OpenSpec (фаза F)

Порядок гейтов: [`openspec-gates.md`](openspec-gates.md).