# План MVP (тестовое задание)

> **Статус:** актуален (2026-11-19). Фичи и AC: [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md).

## 1. Цель MVP

Симулятор сплита + создатель по шаблону; guardrails обязательны; SQLite. См. [`00-product-overview.md`](00-product-overview.md).

## 2. Реестр фич (фаза D)

| ID | Название | Эпик |
| --- | --- | --- |
| F0 | Основа | E0 |
| F1 | Главная / навигация | E0–E1 |
| F2 | Создатель | E1 |
| F3 | Fetch | E2 |
| F4 | Операции офферов | E3 |
| F5 | Push / Cancel | E4 |
| F6 | Валидация + diff | E4, E6 |
| F7 | Resync | E5 |
| F8 | README / сдача | E7 |
| F9 | Встроенная `/docs` (ProductDocs) | E7 |
| F9 | Встроенная `/docs` (ProductDocs) | E7 |

## 3. Порядок реализации (эпики)

```text
E0 Фундамент      F0, F1 (shell)
E1 Создаватель    F2
E2 Editor fetch   F3
E3 Editor ops     F4
E4 Publish        F5 + F6 (вместе)
E5 Resync         F7
E6 UI polish      вшито в E0–E4 (design-system)
E7 Сдача          F8, F9 + F9 (README + in-app docs)
```

## 4. OpenSpec changes (target)

| Change slug | Фичи |
| --- | --- |
| `foundation-keitaro-client` | F0, F1 |
| `home-navigation` | F1 (если не в foundation) |
| `campaign-creator` | F2 |
| `stream-editor-fetch-ui` | F3 |
| `stream-editor-offer-ops` | F4 |
| `stream-editor-publish` | F5, F6 |
| `stream-editor-resync` | F7 |
| `project-readme-delivery` | F8, F9 |

## 5. Карта PlanDocs ↔ ProductDocs

| PlanDocs | ProductDocs (после F) |
| --- | --- |
| `00` | `00` |
| `03` | `03-home` (создать при первом change) |
| `01` | `01` |
| `02` | `02` |
| `15` | `15` |

## 6. Решения (зафиксированы)

- Guardrails, SQLite, pin/bring back, один оффер при Create, product-решения nav/Fetch — см. `29` §10, `30`.

## 7. План работ (фаза F)

Пошагово с чекбоксами: [`33-implementation-work-plan.md`](33-implementation-work-plan.md). Команда: **«следующий change»** → propose → apply → **«проверь»** → archive.