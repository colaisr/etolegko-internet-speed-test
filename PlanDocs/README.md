# PlanDocs — индекс продуктовой памяти Legko

> **Единая точка входа в `PlanDocs/`.** Статус: **идёт проработка** (2026-11-19). Тестовое Keitaro wrapper; карта разделов для MVP заведена.
>
> **PlanDocs — замысел продукта**, не код. PlanDocs отвечает на «зачем и что». Как система работает после реализации — [`openspec/`](../openspec/README.md) (технически) и [`ProductDocs/`](../ProductDocs/README.md) (для бизнеса).

## 1. Как пользоваться

1. Перед задачей открой этот индекс, найди нормативный документ, читай только его.
2. **Статусы:** `Заглушка` / `Черновик` / `Актуален` / `Историческая справка` — см. будущие строки таблицы.
3. Новый раздел получает следующий свободный номер (`00`, `01`, …); шаблон содержания — обсудим при первом propose.
4. **Прогресс (когда появятся файлы):** `node scripts/plandocs-progress.mjs`.

## 2. Конституция и обзор

| Файл | Статус | Что внутри |
| --- | --- | --- |
| [`00-product-overview.md`](00-product-overview.md) | Актуален | Зачем обёртка, симулятор сплита, scope |
| [`26-key-flows.md`](26-key-flows.md) | Актуален | Сквозные сценарии |
| [`29-mvp-functional-description.md`](29-mvp-functional-description.md) | Актуален | Сводное функциональное описание MVP |

## 3. Фичи тестового задания

| Файл | Статус | Для MVP | Что внутри |
| --- | --- | --- | --- |
| [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md) | Актуален | обязательно | **F0–F8**, acceptance, OpenSpec map |
| [`03-home-and-navigation.md`](03-home-and-navigation.md) | Актуален | обязательно | F1 — главная, недавние, open by id |
| [`01-campaign-creator.md`](01-campaign-creator.md) | Актуален | обязательно | F2 — создатель |
| [`02-stream-offer-editor.md`](02-stream-offer-editor.md) | Актуален | обязательно | F3–F7 — редактор |

## 4. План

| Файл | Статус | Для MVP | Что внутри |
| --- | --- | --- | --- |
| [`25-mvp-plan.md`](25-mvp-plan.md) | Актуален | обязательно | Эпики E0–E7 ↔ F0–F8 |
| [`27-product-gate-1-mvp.md`](27-product-gate-1-mvp.md) | Актуален | — | Гейт 1 product: **go**, решения 2026-11-19 |
| [`28-pre-implementation-process.md`](28-pre-implementation-process.md) | Актуален | — | Фазы A–F, без project-manager |
| [`33-implementation-work-plan.md`](33-implementation-work-plan.md) | **Рабочий** | — | **Чеклист changes 1–8**, проверки, archive |
| [`15-architecture.md`](15-architecture.md) | Актуален | обязательно | Стек, ORM, Keitaro adapter, маршруты |
| [`31-feature-to-implementation-map.md`](31-feature-to-implementation-map.md) | Актуален | обязательно | F0–F9 → файлы и smoke |
| [`32-product-docs-in-app.md`](32-product-docs-in-app.md) | Актуален | обязательно | F9 — `/docs`, ProductDocs в UI |
| [`17-design-guidelines.md`](17-design-guidelines.md) | Актуален | обязательно | Ссылка на UI-спеку и wireframe |

## 5. Рабочие планы

Этапы реализации — в `25-mvp-plan.md` после фаз B–E (`28` §6). Jira / PM не используем.

## 6. Интервью и источники

| Путь | Назначение |
| --- | --- |
| [`interview/sources/`](interview/sources/README.md) | Транскрипты, PDF ТЗ, скриншоты от заказчика |