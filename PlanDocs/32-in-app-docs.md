# Встроенная документация (F9)

> **Статус:** актуален (2026-11-19). **Часть поставки MVP** — не post-MVP.

## Зачем

Документация **готового работающего продукта** для пользователя (байера): как создать кампанию, что значит жёлтый поток, как Push и diff. Аналог Confluence, но **внутри Legko**, источник — `ProductDocs/`.

## Что показываем / что нет

| Показываем | Не показываем |
| --- | --- |
| `ProductDocs/*.md` | `PlanDocs/` (замысел) |
| Индекс `ProductDocs/README.md` | `openspec/` (технические спеки) |
| | `ProjectDocs/` (роли, дизайн) |

## UX

- Ссылка **«Документация»** в [`AppHeader`](../ProjectDocs/design/design-system.md) на всех экранах (Home, Creator, Editor).
- `/docs` — оглавление с краткими описаниями из индекса ProductDocs.
- `/docs/<slug>` — например `01-campaign-creator` → файл `ProductDocs/01-campaign-creator.md`.
- Оформление: layout как у приложения (header + светлая колонка контента), типографика design-system.

## Связь с процессом OpenSpec

1. Реализуем фичу → обновляем **ProductDocs** (гейт docs-sync).
2. Те же файлы **автоматически** доступны на `/docs` (читаются с диска при старте или при запросе).
3. PlanDocs: пометка «реализовано, см. ProductDocs/…» — по [`openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md).

## Реализация (фаза F)

- Модуль `legko/web/routes_docs.py` (см. [`15-architecture.md`](15-architecture.md) §7).
- Рендер: markdown → HTML (stdlib + минимальный sanitizer или `markdown` lib в pyproject).
- Allowlist: только файлы, перечисленные в `ProductDocs/README.md`, защита от path traversal.

## Приёмка

Критерии **F9.1–F9.6** в [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md).