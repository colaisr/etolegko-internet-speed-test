# Фичи → реализация (фаза E)

> **Статус:** актуален (2026-11-19). Архитектура: [`15-architecture.md`](15-architecture.md).

Краткая матрица для OpenSpec tasks и для проверки «ничего не забыли».

| Фича | Ключевые файлы (создать) | Критерий smoke |
| --- | --- | --- |
| F0 | `settings.py`, `db/session.py`, `integrations/keitaro/client.py`, `/health` | curl `/health` → keitaro ok |
| F1 | `templates/home.html`, `campaign_nav.open_by_keitaro_id` | open id + recent list |
| F2 | `campaign_creator.py`, `templates/creator.html` | кампания в Keitaro + redirect editor |
| F3 | `stream_fetch.py`, `partials/offer_table.html` | auto fetch после create |
| F4 | `offer_editor.py`, `domain/weights.py` | add/remove/pin, сумма 100 |
| F5 | `publish.py`, snapshots model | push в Keitaro; cancel restore |
| F6 | `domain/diff.py`, push preview partial | disabled push + modal diff |
| F7 | merge в `stream_fetch` | removed после manual keitaro delete |
| F8 | `README.md` | новый клон → create → push |
| F9 | `routes_docs.py`, link в header, ProductDocs pages | `/docs` открывается, разделы после changes |
| F9 | `routes_docs.py`, `templates/docs/*`, header link | `/docs` открывается, страницы ProductDocs рендерятся |

## UI compliance

Любой новый template — layout `base.html` + классы из [`components.css`](../ProjectDocs/design/artifacts/prototypes/) (создать при E0 из design-system).

## ProductDocs (после F)

| Страница | Когда |
| --- | --- |
| `ProductDocs/00-product-overview.md` | после foundation |
| `ProductDocs/01-…`, `02-…`, `03-…` | после соответствующих changes |