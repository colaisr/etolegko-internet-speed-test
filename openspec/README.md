# openspec — технические спеки и активные changes

> **Статус:** активных changes нет (после archive `stream-editor-fetch-ui`). Замысел — [`PlanDocs/README.md`](../PlanDocs/README.md). Бизнес-описание — [`ProductDocs/README.md`](../ProductDocs/README.md).

## Активные changes

| Change | Назначение |
| --- | --- |
| — | Пока нет. |

## Живые спеки `specs/<capability>/spec.md`

| Capability | Что описывает | ProductDocs |
| --- | --- | --- |
| `app-foundation` | Каркас FastAPI, шаблоны, статика | `00-product-overview` |
| `health` | `/health` | `00-product-overview` |
| `keitaro-client` | HTTP-адаптер Keitaro | `00-product-overview` |
| `home-navigation` | Главная, open, недавние | `03-home-and-navigation` |
| `campaign-creator` | Создатель шаблона, модалка | `01-campaign-creator` |
| `stream-editor-fetch` | Редактор, Fetch, таблица read-only | `02-stream-offer-editor` |

## Archive

Завершённые changes — `changes/archive/`.

| Archived | Дата |
| --- | --- |
| `foundation-keitaro-client` | 2026-11-19 |
| `home-navigation` | 2026-11-19 |
| `campaign-creator` | 2026-11-19 |
| `stream-editor-fetch-ui` | 2026-11-19 |

## Связка с процессом

- Гейты: [`ProjectDocs/roles/openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md)
- Verify: `node scripts/verify-change-gates.mjs --change <slug>`

## Техконтекст

Стек: [`project.md`](project.md), архитектура: [`PlanDocs/15-architecture.md`](../PlanDocs/15-architecture.md).