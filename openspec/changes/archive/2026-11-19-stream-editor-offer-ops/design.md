# Design: stream-editor-offer-ops

| Область | Решение |
| --- | --- |
| Домен | `domain/weights.py` — largest remainder; pin-ограничения в `offer_editor` |
| API | `POST .../offers`, `.../remove`, `.../restore`, `.../pin`, `.../unpin` → redirect editor + `op_error` |
| Состояние | `Stream.has_draft`, `Campaign.sync_status` → DRAFT после любой локальной правки |
| Keitaro | Только чтение (`list_offers`, `get_offer`) при add; запись в трекер — F5 |
| UI | `editor.html`, `card--editor-lab`, иконки строк, pin «Закрепить» + %; Push/Cancel disabled |