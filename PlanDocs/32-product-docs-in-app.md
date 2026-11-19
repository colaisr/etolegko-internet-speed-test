# Встроенная документация (F9)

> **Статус:** актуален (2026-11-19). **Часть поставки MVP** — не опция и не «потом в Confluence».

## Зачем

Пользователь (байер, проверяющий) в **любой момент** открывает справку **в том же приложении** и читает, как работает продукт **сейчас**. Источник текста — **`ProductDocs/`** в репозитории; после каждого change страницы обновляются через гейт **docs-sync** (`ProjectDocs/roles/openspec-gates.md`).

## Что показываем / что нет

| Показываем | Не показываем |
| --- | --- |
| `ProductDocs/*.md` | `PlanDocs/` (замысел) |
| Индекс `ProductDocs/README.md` | `openspec/` (техспеки) |
| | `ProjectDocs/` (роли, процесс) |

## UX

- Ссылка **«Документация»** в `AppHeader` (рядом с логотипом Legko) на Home, Creator, Editor.
- **`GET /docs`** — список разделов (таблицы из README или автосписок `.md`).
- **`GET /docs/{slug}`** — одна страница, markdown → HTML (безопасный рендер, без raw HTML из файлов).
- Внизу страницы доки: **«Вернуться в приложение»** → `/`.

## Техническое (см. `15-architecture.md`)

- Модуль `legko/web/routes_docs.py`
- Рендер: **markdown** (stdlib `markdown` или `mistune` — в E0)
- Файлы читаются с диска из `ProductDocs/` при старте или на каждый запрос (MVP: на запрос, кэш optional).
- При отсутствии файла — 404 с ссылкой на оглавление.

## Связь с OpenSpec

1. В **tasks.md** каждого change — группа **ProductDocs** (как в Gloom/Legko).
2. **docs-sync** перед archive.
3. Перед **`git push`**: `node scripts/verify-productdocs.mjs` и хук [`.githooks/pre-push`](../.githooks/pre-push) — см. [`openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md) § push.
4. Пользователь на `/docs` видит то же, что в git — **поставка = код + ProductDocs + рендер**.

## Приёмка

**F9.1–F9.6** в [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md).

## ProductDocs при сдаче

Минимальный набор страниц (создаются по мере changes, финально полные к F9):

| Файл | Содержание |
| --- | --- |
| `00-product-overview.md` | ✅ Что такое Legko, F0, `/health` |
| `03-home-and-navigation.md` | Главная, недавние, open by id |
| `01-campaign-creator.md` | Создание кампании |
| `02-stream-offer-editor.md` | Редактор, Push, Cancel, Fetch |

Индекс `ProductDocs/README.md` — колонка «Обновлено» ведётся при archive.