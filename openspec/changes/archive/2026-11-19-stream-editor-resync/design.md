# Design: stream-editor-resync

| Область | Решение |
| --- | --- |
| Триггер | `offer_stream.has_draft` → merge вместо delete/rebuild |
| Drift | active в снимке, нет в Keitaro API → `removed` + пересчёт |
| Local add | id не в снимке → не трогаем, даже если нет в Keitaro |
| Снимок | merge-fetch **не** перезаписывает snapshot (Cancel остаётся к push/fetch sync) |
| Служебные потоки | Пересоздаются из Keitaro, оффер-поток и строки сохраняются |