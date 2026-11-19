# openspec — технические спеки и активные changes

> **Статус:** активных changes нет (после archive `campaign-creator`). Замысел — [`PlanDocs/README.md`](../PlanDocs/README.md). Бизнес-описание — [`ProductDocs/README.md`](../ProductDocs/README.md).

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

## Archive

Завершённые changes — `changes/archive/`. Не использовать как норму для новых решений.

| Archived | Дата |
| --- | --- |
| `foundation-keitaro-client` | 2026-11-19 |
| `home-navigation` | 2026-11-19 |
| `campaign-creator` | 2026-11-19 |

## Связка с процессом

- Гейты: [`ProjectDocs/roles/openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md)
- Правила артефактов: [`config.yaml`](config.yaml)
- Verify: `/verify-change <slug>`; `node scripts/verify-change-gates.mjs --change <slug>`

## Техконтекст

Стек: [`project.md`](project.md), архитектура: [`PlanDocs/15-architecture.md`](../PlanDocs/15-architecture.md).