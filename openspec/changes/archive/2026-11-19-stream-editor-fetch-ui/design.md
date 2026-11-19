# Design: stream-editor-fetch-ui

| Область | Решение |
| --- | --- |
| Маршруты | `GET/POST /campaigns/{id}/editor`, `POST /campaigns/{id}/fetch` → redirect editor |
| Данные | `selectinload` streams + offers; `full_fetch` переиспользуется |
| UI | `editor.html`, status-pill, `card--draft` если `has_draft`, footer disabled (F4/F5) |
| Ошибка Fetch | redirect `?fetch_error=` + alert на странице |