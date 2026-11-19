# Design: home-navigation

## Решения

| Тема | Решение |
| --- | --- |
| Маршруты | `legko/web/routes_pages.py`, подключение в `main.py` |
| Open by ID | Combobox + `POST /campaigns/open`; `GET /campaigns/search` (HTMX) |
| Lazy import | Нет локальной записи → `GET campaigns/{id}` в Keitaro → shell в SQLite → redirect editor |
| Недавние | `SELECT` campaigns `ORDER BY updated_at DESC LIMIT 10` |
| Бейджи | `synced` → «Синхронно», `draft` → «Черновик», `needs_fetch` → «Проверьте Keitaro» |
| Creator CTA | `GET /campaigns/new` — заглушка до change 3 |
| Editor | `GET /campaigns/{uuid}/editor` — заглушка до F3 |

## Keitaro

`KeitaroClient.get_campaign(campaign_id)` → `GET {base}/campaigns/{id}`, 404 = не найдена.