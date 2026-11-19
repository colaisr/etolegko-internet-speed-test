# Design: campaign-creator

## Решения

| Тема | Решение |
| --- | --- |
| Маршруты | Модалки на Home: `GET /campaigns/new/panel`, `POST /campaigns/new` (HTMX), `GET …/created/panel`, `GET /campaigns/open/panel`; редиректы `/campaigns/new` → `/?create=1` |
| UX | Creator и success — **Modal** (design-system); редактор остаётся отдельной страницей |
| Home layout | Hero — copy only; workspace card: search + Open, centered CTA над таблицей недавних; status-pill в таблице |
| Defaults | `KEITARO_DEFAULT_*_ID` из env; без них — блокировка create с понятным текстом |
| Шаблон Keitaro | POST `campaigns` → POST `streams` (geo redirect → Google) → POST `streams` (default landings, 1 offer 100%) |
| Rollback | При ошибке после создания кампании — `DELETE campaigns/{id}` |
| URL трафика | `{domain.rstrip('/')}/{alias}` из ответа Keitaro после create |
| Оффер-поиск | Список offers (limit ~200) + клиентский filter как у кампаний; HTMX partial |
| После create | SQLite Campaign + `full_fetch` потоков → success → редактор |
| Google URL | `KEITARO_GOOGLE_REDIRECT_URL` (default google.com) |

## Keitaro

Проверено на tlgk.host admin API v1: `POST campaigns`, `POST streams`, `GET campaigns/{id}/streams`, `GET offers`.