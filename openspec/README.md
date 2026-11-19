# openspec — технические спеки и активные changes

> **Статус:** инфраструктура готова, активных changes нет. Замысел — [`PlanDocs/README.md`](../PlanDocs/README.md). Бизнес-описание — [`ProductDocs/README.md`](../ProductDocs/README.md).

## Активные changes

| Change | Назначение |
| --- | --- |
| — | Пока нет. |

`npx @fission-ai/openspec@latest list` — актуальный список.

## Живые спеки `specs/<capability>/spec.md`

| Capability | Что описывает | ProductDocs |
| --- | --- | --- |
| — | Появятся после первого archive | — |

## Archive

Завершённые changes — `changes/archive/`. Не использовать как норму для новых решений.

## Связка с процессом

- Гейты: [`ProjectDocs/roles/openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md)
- Правила артефактов: [`config.yaml`](config.yaml)
- Verify: `/verify-change <slug>`; `node scripts/verify-change-gates.mjs --change <slug>`

## Техконтекст

Стек: [`project.md`](project.md), архитектура: [`PlanDocs/15-architecture.md`](../PlanDocs/15-architecture.md).