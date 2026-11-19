# Редактор потоков и офферов

> **Обновлено:** 2026-11-19 · **Change:** stream-editor-fetch-ui  
> **Замысел:** [PlanDocs/02-stream-offer-editor.md](../PlanDocs/02-stream-offer-editor.md) · **Спеки:** `stream-editor-fetch`

## 1. Что это и зачем

Редактор — **симулятор сплита**: байер видит потоки кампании и веса офферов локально, сверяясь с Keitaro через Fetch. До F4 все веса read-only.

## 2. Как это работает сейчас

- **`/campaigns/{id}/editor`** — шапка (имя, Keitaro id, geo, status pill, URL), кнопка **Fetch Streams**.
- После **create (F2)** потоки подтягиваются автоматически (`full_fetch`); если потоков нет — блок «Потоки ещё не загружены» и CTA Fetch.
- **POST `/campaigns/{id}/fetch`** — перезагрузка потоков из Keitaro; при ошибке — сообщение на странице редактора.
- **Служебный поток** — одна серая строка с lock (geo → Google), без деталей фильтра.
- **Оффер-поток** — таблица: имя, id, вес %, pin (да/—), статус active/removed; сумма активных %.
- **Push / Отменить** — кнопки есть, но **disabled** до F4/F5.
- Добавление/правка весов — следующий change **stream-editor-offer-ops (F4)**.

## 3. Кто что может

Один байер — полный доступ к экрану и Fetch при настроенном Keitaro API.

## 4. Правила и граничные случаи

- Fetch **заменяет** локальные потоки снимком Keitaro (в F3 нет черновиков и merge F7).
- Кампания без Keitaro id — Fetch невозможен (ошибка адаптера).

## 5. Отличия от замысла (PlanDocs)

Нет Add/Remove/Pin, Push, Cancel, diff-модалки — F4–F6. Drift-merge — F7.

## 6. Связанные страницы

- [Создатель](01-campaign-creator.md)
- [Главная](03-home-and-navigation.md)

## Журнал обновлений

| Дата | Change | Что изменилось |
| --- | --- | --- |
| 2026-11-19 | stream-editor-fetch-ui | Экран editor, Fetch, таблица read-only, служебный поток |