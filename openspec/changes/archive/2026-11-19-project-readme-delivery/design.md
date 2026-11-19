# Design: project-readme-delivery

| Область | Решение |
| --- | --- |
| Путь к файлам | `repo/ProductDocs/` от `legko.services.product_docs` |
| Рендер | `markdown` 3.x, tables; slug только `[0-9][0-9a-z-]*` |
| OpenAPI | остаётся на `/api/docs` |
| Ссылки | `.md` в ProductDocs → `/docs/{slug}` в HTML |