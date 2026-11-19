# ProductDocs — бизнес-база знаний Legko

> **Единая точка входа в `ProductDocs/`.** Описание того, **как продукт работает сейчас**. В приложении: **`GET /docs`** (оглавление) и **`/docs/{slug}`** — тот же markdown ([`PlanDocs/32-product-docs-in-app.md`](../PlanDocs/32-product-docs-in-app.md)). Шаблон новой страницы — [`_template.md`](_template.md). Перед **`git push`**: `node scripts/verify-productdocs.mjs` (хук `.githooks/pre-push`). **Change:** project-readme-delivery (F9).

## 1. Как пользоваться

1. Номера и имена файлов совпадают с разделами PlanDocs, когда те появятся.
2. **Пустая страница** — раздела ещё нет в продукте.
3. Колонка «Обновлено» — дата и slug change, который последним менял страницу.

## 2. Как слои связаны

| Слой | Где | Отвечает на |
| --- | --- | --- |
| Замысел | [`PlanDocs/`](../PlanDocs/README.md) | зачем и что задумано |
| Технические спеки | [`openspec/`](../openspec/README.md) | как система работает |
| **Бизнес-база** | **`ProductDocs/`** | **как есть сейчас** |

Если ProductDocs и спеки расходятся, побеждает спека.

## 3. Индекс страниц

| Файл | Что описывает | Замысел (PlanDocs) | Спеки (OpenSpec) | Обновлено |
| --- | --- | --- | --- | --- |
| [`00-product-overview.md`](00-product-overview.md) | Обзор MVP, `/docs`, health | [`00-product-overview`](../PlanDocs/00-product-overview.md) | app-foundation, health, project-readme-delivery | 2026-11-19 · project-readme-delivery |
| [`03-home-and-navigation.md`](03-home-and-navigation.md) | Главная, Open, недавние (F1) | [`03-home-and-navigation`](../PlanDocs/03-home-and-navigation.md) | home-navigation | 2026-11-19 · home-navigation |
| [`01-campaign-creator.md`](01-campaign-creator.md) | Создатель кампании (F2) | [`01-campaign-creator`](../PlanDocs/01-campaign-creator.md) | campaign-creator | 2026-11-19 · campaign-creator |
| [`02-stream-offer-editor.md`](02-stream-offer-editor.md) | Редактор, Fetch, симулятор, Push, merge Fetch (F3–F7) | [`02-stream-offer-editor`](../PlanDocs/02-stream-offer-editor.md) | stream-editor-fetch, stream-editor-offer-ops, stream-editor-publish, stream-editor-resync | 2026-11-19 · stream-editor-resync |

## 4. Как добавить страницу

Скопируй [`_template.md`](_template.md), дай то же имя, что у раздела в PlanDocs, добавь строку в таблицу выше.