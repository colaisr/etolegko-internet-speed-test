# Proposal: campaign-creator

## Why

F2 даёт байеру **шаблонную 2-поточную кампанию** в Keitaro за один шаг (geo → Google, остальное → один оффер 100%) без ручной сборки в админке.

## Бизнес-обоснование

[`PlanDocs/01-campaign-creator.md`](../../../PlanDocs/01-campaign-creator.md), AC F2.1–F2.6 в [`30`](../../../PlanDocs/30-mvp-features-and-acceptance.md).

## What Changes

- Экран создателя: имя, geo ISO-2, поиск оффера, превью шаблона.
- `KeitaroClient`: `search_offers`, `create_campaign_with_template`, чтение потоков.
- `campaign_creator` + SQLite; rollback при сбое потоков.
- Экран успеха: Keitaro id, campaign URL, domain/group/source из env.
- Минимальный `stream_fetch.full_fetch` после create; переход в редактор.

## Вне scope

- Редактор таблицы офферов (F3/F4), иной URL кроме Google, >2 потоков.

## Capabilities

### New Capabilities

- `campaign-creator`: форма create, Keitaro template, success, локальная запись.

### Modified Capabilities

- `home-navigation`: CTA «Создать» ведёт на реальный creator (не заглушка).

## Impact

- **PlanDocs:** [`01-campaign-creator.md`](../../../PlanDocs/01-campaign-creator.md)
- **ProductDocs:** `ProductDocs/01-campaign-creator.md`