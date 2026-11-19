# Design: stream-editor-publish

| Область | Решение |
| --- | --- |
| Baseline | `stream_published_snapshots.payload` — JSON строк офферов; пишется после Fetch и успешного Push |
| Diff | `domain/diff.py` — active-only: add / remove / weight Δ vs snapshot |
| Валидация | `push_readiness`: ≥1 active, Σ=100%; Push только при `has_draft` |
| Keitaro | GET `streams/{id}` → PUT с обновлённым `offers[]` (`share`, `state: active`) |
| UI | GET preview HTML → modal; POST push; POST cancel без модалки |
| Ошибки | Push fail — черновик и snapshot не трогаем; flash `push_error` |