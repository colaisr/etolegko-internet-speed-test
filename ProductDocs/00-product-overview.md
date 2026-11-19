# Обзор Legko

> **Обновлено:** 2026-11-19 · **Change:** stream-editor-fetch-ui · **PlanDocs (F0–F3):** реализовано  
> **Замысел:** [PlanDocs/00-product-overview.md](../PlanDocs/00-product-overview.md) · **Технические спеки:** openspec/specs (после archive)

## 1. Что это и зачем

Legko — рабочее место медиабайера поверх Keitaro: быстро заводить типовые кампании и менять сплит офферов в потоке ротации **в черновике**, с просмотром diff и только потом Push в трекер.

## 2. Как это работает сейчас

На этапе **foundation** (F0) доступны:

- веб-приложение со стартовой страницей и корпоративным оформлением;
- проверка готовности по адресу **`/health`** (база данных и подключение к Keitaro);
- техническая OpenAPI-схема на **`/api/docs`** (путь `/docs` зарезервирован под ProductDocs, F9);
- ссылка «Документация» в шапке ведёт на **`/docs`** — рендер ProductDocs появится в change `project-readme-delivery`.

**Главная (F1):** поиск и open кампании Keitaro, таблица недавних, модалки — [03-home-and-navigation.md](03-home-and-navigation.md).

**Создатель (F2):** [01-campaign-creator.md](01-campaign-creator.md). **Редактор / Fetch (F3):** [02-stream-offer-editor.md](02-stream-offer-editor.md) — таблица офферов read-only, Push в F5.

## 3. Кто что может

Один пользователь (байер) без разграничения ролей — доступ ко всем экранам приложения.

## 4. Правила и граничные случаи

- API-ключ Keitaro задаётся только в окружении сервера, не хранится в интерфейсе.
- Без ключа Keitaro `/health` сообщит, что ключ не задан.

## 5. Отличия от замысла (PlanDocs)

Редактор (таблица весов, Push) и in-app ProductDocs — в следующих changes.

## 6. Связанные страницы и спеки

- Замысел: [PlanDocs/00-product-overview.md](../PlanDocs/00-product-overview.md)
- Спеки: `app-foundation`, `keitaro-client`, `health`, `home-navigation`, `campaign-creator`, `stream-editor-fetch`

## Журнал обновлений

| Дата | Change | Что изменилось |
| --- | --- | --- |
| 2026-11-19 | foundation-keitaro-client | Первая страница ProductDocs: каркас приложения, /health, /api/docs |
| 2026-11-19 | docs-sync-followup | Уточнения F0, OpenAPI; синхронизация с планом и хуком push |
| 2026-11-19 | home-navigation | Ссылка на F1; детализация главной в 03-home |
| 2026-11-19 | campaign-creator | F2 создатель; обзор и ссылки на 01/03 |
| 2026-11-19 | stream-editor-fetch-ui | F3 редактор и Fetch; ссылка на 02 |