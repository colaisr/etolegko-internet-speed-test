# ProductDocs — бизнес-база знаний Legko

> **Единая точка входа в `ProductDocs/`.** Описание того, **как продукт работает сейчас**, для владельцев и исполнителей. **Часть поставки:** те же файлы рендерятся в приложении на **`/docs`** ([`PlanDocs/32-product-docs-in-app.md`](../PlanDocs/32-product-docs-in-app.md)). Разделы появляются по мере changes; шаблон новой страницы — [`_template.md`](_template.md). Перед **`git push`**: `node scripts/verify-productdocs.mjs` (хук `.githooks/pre-push`).

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
| [`00-product-overview.md`](00-product-overview.md) | Что такое Legko сейчас (F0) | [`00-product-overview`](../PlanDocs/00-product-overview.md) | app-foundation, health, keitaro-client | 2026-11-19 · foundation-keitaro-client |
| [`03-home-and-navigation.md`](03-home-and-navigation.md) | Главная, Open, недавние (F1) | [`03-home-and-navigation`](../PlanDocs/03-home-and-navigation.md) | home-navigation | 2026-11-19 · home-navigation |

## 4. Как добавить страницу

Скопируй [`_template.md`](_template.md), дай то же имя, что у раздела в PlanDocs, добавь строку в таблицу выше.