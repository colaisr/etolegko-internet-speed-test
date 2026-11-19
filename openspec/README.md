# openspec — технические спеки и активные changes

> **Статус:** активных changes нет. Следующий: `project-readme-delivery` (F8/F9). Замысел — [`PlanDocs/README.md`](../PlanDocs/README.md). Бизнес-описание — [`ProductDocs/README.md`](../ProductDocs/README.md).

## Активные changes

_(нет)_

## Живые спеки `specs/<capability>/spec.md`

| Capability | Что описывает | ProductDocs |
| --- | --- | --- |
| `app-foundation` | Каркас FastAPI, шаблоны, статика | `00-product-overview` |
| `health` | `/health` | `00-product-overview` |
| `keitaro-client` | HTTP-адаптер Keitaro | `00-product-overview` |
| `home-navigation` | Главная, open, недавние | `03-home-and-navigation` |
| `campaign-creator` | Создатель шаблона, модалка | `01-campaign-creator` |
| `stream-editor-fetch` | Редактор, Fetch, merge F7 | `02-stream-offer-editor` |
| `stream-editor-offer-ops` | Add/remove/pin, пересчёт %, черновик | `02-stream-offer-editor` |
| `stream-editor-publish` | Push, Cancel, diff, snapshot | `02-stream-offer-editor` |

## Archive

Завершённые changes — `changes/archive/`.

| Archived | Дата |
| --- | --- |
| `foundation-keitaro-client` | 2026-11-19 |
| `home-navigation` | 2026-11-19 |
| `campaign-creator` | 2026-11-19 |
| `stream-editor-fetch-ui` | 2026-11-19 |
| `stream-editor-offer-ops` | 2026-11-19 |
| `stream-editor-publish` | 2026-11-19 |
| `stream-editor-resync` | 2026-11-19 |

## Связка с процессом

- Гейты: [`ProjectDocs/roles/openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md)
- Verify: `node scripts/verify-change-gates.mjs --change <slug>`

## Техконтекст

Стек: [`project.md`](project.md), архитектура: [`PlanDocs/15-architecture.md`](../PlanDocs/15-architecture.md).