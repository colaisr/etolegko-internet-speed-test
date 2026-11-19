# Обзор Legko

> **Обновлено:** 2026-11-19 · **Change:** project-readme-delivery (F8/F9)  
> **Замысел:** [PlanDocs/00-product-overview.md](../PlanDocs/00-product-overview.md)

## 1. Что это и зачем

Legko — рабочее место медиабайера поверх Keitaro: быстро заводить типовые кампании и менять сплит офферов в потоке ротации **в черновике**, с просмотром diff и только потом Push в трекер.

## 2. Как это работает сейчас

| Область | Где | Документация |
| --- | --- | --- |
| Проверка сервиса | `GET /health` | ниже |
| API-схема | `GET /api/docs` (OpenAPI) | — |
| Справка в UI | `GET /docs`, шапка «Документация» | этот раздел + 01–03 |
| Главная | `/` | [03-home-and-navigation.md](03-home-and-navigation.md) |
| Создатель | модалка «Создать» | [01-campaign-creator.md](01-campaign-creator.md) |
| Редактор | `/campaigns/{id}/editor` | [02-stream-offer-editor.md](02-stream-offer-editor.md) |

MVP редактора (F3–F7): Fetch, локальный симулятор, Push/Cancel/diff, merge-Fetch при черновике.

## 3. Кто что может

Один пользователь (байер) без разграничения ролей — доступ ко всем экранам приложения.

## 4. Правила и граничные случаи

- API-ключ Keitaro задаётся только в окружении сервера, не хранится в интерфейсе.
- Без ключа Keitaro `/health` сообщит, что ключ не задан.
- Текст на `/docs` читается с диска из `ProductDocs/` при запросе (без отдельного деплоя доков).

## 5. Отличия от замысла (PlanDocs)

Нет.

## 6. Связанные страницы

- [Главная и навигация](03-home-and-navigation.md)
- [Создатель кампании](01-campaign-creator.md)
- [Редактор офферов](02-stream-offer-editor.md)

## Журнал обновлений

| Дата | Change | Что изменилось |
| --- | --- | --- |
| 2026-11-19 | foundation-keitaro-client | Первая страница ProductDocs: каркас, /health |
| 2026-11-19 | stream-editor-resync | Ссылки на полный редактор F3–F7 |
| 2026-11-19 | project-readme-delivery | Актуальный обзор MVP; in-app `/docs` |