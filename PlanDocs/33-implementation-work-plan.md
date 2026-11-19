# План работ — реализация по OpenSpec changes

> **Статус:** актуален (2026-11-19). **Фаза F.** Иди **сверху вниз**; не перескакивай. Команда владельца: **«начинаем следующий change»** → propose → apply → verify → **«проверь»** → archive.

**Перед стартом:** [`28-pre-implementation-process.md`](28-pre-implementation-process.md) §6 ✓ · [`30-mvp-features-and-acceptance.md`](30-mvp-features-and-acceptance.md) · [`15-architecture.md`](15-architecture.md) · [`design-system.md`](../ProjectDocs/design/design-system.md)

**Как пользоваться:** ставь `[x]` у change только после **archive**. Между шагами — только по твоей фразе «следующий».

---

## Общий ритм на каждый change

| Шаг | Действие | Ссылки |
| --- | --- | --- |
| 1 | **Propose** | Cursor: `/opsx:propose` · контекст [`openspec/config.yaml`](../openspec/config.yaml) · [`openspec/project.md`](../openspec/project.md) |
| 2 | **Product гейт 1** | Фичи из таблицы ниже · AC в [`30`](30-mvp-features-and-acceptance.md) |
| 3 | **Apply** | `/opsx:apply` · роль [`developer`](../ProjectDocs/roles/developer.md) |
| 4 | **Verify** | `/verify-change <slug>` · гейты [`openspec-gates.md`](../ProjectDocs/roles/openspec-gates.md) · `node scripts/verify-change-gates.mjs --change <slug>` |
| 5 | **Ты проверяешь** | Блок **«Проверь»** ниже для этого slug |
| 6 | **Archive** | `/opsx:archive` · хук не заблокирует только при зелёных гейтах + ProductDocs |

---

## Change 1: `foundation-keitaro-client`

- [x] **Заархивирован** (поставь `[x]` после archive)

| | |
| --- | --- |
| **Фичи** | F0 (основа) |
| **PlanDocs** | [`15`](15-architecture.md) §2–5, §9 · [`31`](31-feature-to-implementation-map.md) F0 |
| **ProductDocs** | Создать/обновить `ProductDocs/00-product-overview.md` (кратко: что такое Legko) |
| **Capabilities** | `foundation`, `keitaro-client`, `health` (уточни в propose) |

**После apply должно появиться:** пакет `legko/`, `.env.example`, Alembic, пустые модели или миграция v1, `GET /health`, `KeitaroClient.ping`, статика `legko-tokens.css` в `static/`, базовый `base.html` + header с заглушкой «Документация».

### Проверь (ручная приёмка)

1. `uvicorn legko.main:app` стартует без ошибок.
2. Открыть `/health` — JSON с признаком связи с Keitaro (ok или понятная ошибка с ключом).
3. SQLite-файл создаётся после миграции.
4. Секретов нет в git.

**Если ок →** `/verify-change foundation-keitaro-client` → **archive** → следующий change.

---

## Change 2: `home-navigation`

- [x] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F1 · [`03-home-and-navigation.md`](03-home-and-navigation.md) |
| **AC** | F1.1–F1.4 в [`30`](30-mvp-features-and-acceptance.md) |
| **UI** | [`mvp-ui-spec.md`](../ProjectDocs/design/mvp-ui-spec.md) §3 Home · прототип [`legko-corporate-prototype.html`](../ProjectDocs/design/artifacts/prototypes/legko-corporate-prototype.html) |
| **ProductDocs** | `ProductDocs/03-home-and-navigation.md` (или `03-…` по шаблону `_template.md`) |

**После apply:** `GET /` — Home, «Создать», open by Keitaro id, «Недавние».

### Проверь

1. Главная в корп. стиле, есть ссылка **«Документация»** (может вести на заглушку до change 8).
2. Open по **существующему** Keitaro campaign id → редактор или lazy import + fetch (как в `03`).
3. После create (change 3) недавние заполняются — пока можно пропустить, если id ещё нет.

**Ок → verify → archive → следующий.**

---

## Change 3: `campaign-creator`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F2 · [`01-campaign-creator.md`](01-campaign-creator.md) |
| **AC** | F2.1–F2.6 [`30`](30-mvp-features-and-acceptance.md) |
| **Keitaro** | [`15`](15-architecture.md) §5 `create_campaign_with_template` |
| **ProductDocs** | `ProductDocs/01-campaign-creator.md` |

**После apply:** форма create, превью, успех с URL, переход в editor с авто-fetch.

### Проверь

1. Create с тестовым Keitaro: в админке 2 потока, geo→Google, 1 оффер 100%.
2. Domain/group/source совпадают с env и видны в UI.
3. Запись в SQLite; редирект в редактор.
4. Сломать offer id — ошибка, без «половины» кампании в Keitaro.

**Ок → verify → archive → следующий.**

---

## Change 4: `stream-editor-fetch-ui`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F3 · [`02-stream-offer-editor.md`](02-stream-offer-editor.md) |
| **AC** | F3.1–F3.5 [`30`](30-mvp-features-and-acceptance.md) |
| **Модель** | [`15`](15-architecture.md) §4 snapshots (база stream_offers) |
| **ProductDocs** | `ProductDocs/02-stream-offer-editor.md` (часть: открытие, Fetch) |

**После apply:** экран редактора, Fetch, таблица офферов, служебный поток одной строкой, бейдж статуса.

### Проверь

1. После create — таблица с одним оффером 100% без ручного Fetch (авто).
2. Кнопка Fetch обновляет данные из Keitaro.
3. Служебный поток без деталей фильтров.
4. Жёлтый/белый/бейдж кампании отображаются логично.

**Ок → verify → archive → следующий.**

---

## Change 5: `stream-editor-offer-ops`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F4 · [`02`](02-stream-offer-editor.md) §5 |
| **AC** | F4.1–F4.6 · unit-тесты `domain/weights.py` |
| **Видео-эталон** | [`video-notes`](../PlanDocs/interview/sources/2026-11-19-keitaro-wrapper-video-notes.md) |
| **ProductDocs** | дополнить `02` (Add/Remove/Pin/Bring back) |

**После apply:** Add, Remove, Bring back, Pin, пересчёт %, Keitaro без изменений до Push.

### Проверь

1. Add → пересчёт (например 2×50%, 3×34/33/33).
2. Remove → 0%, серый; Bring back восстанавливает.
3. Pin 25% — остальные делят остаток; сумма 100%.
4. **Keitaro admin:** веса **не** менялись, пока не Push (change 6).
5. `pytest` на веса — зелёные.

**Ок → verify → archive → следующий.**

---

## Change 6: `stream-editor-publish`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F5 + F6 · [`02`](02-stream-offer-editor.md) · [`32`](32-product-docs-in-app.md) (если только UI push) |
| **AC** | F5.*, F6.* [`30`](30-mvp-features-and-acceptance.md) |
| **ProductDocs** | `02` — Push, Cancel, diff, валидация |

**После apply:** Cancel, Push disabled при ≠100%, modal diff, Push в Keitaro, snapshot, белый поток.

### Проверь

1. Сумма ≠ 100% → Push недоступен, текст причины.
2. Diff совпадает с тем, что уйдёт в Keitaro.
3. После Push — веса в Keitaro = таблице.
4. Cancel сбрасывает черновик; Keitaro не трогался.
5. Ошибка Push — черновик остаётся.

**Ок → verify → archive → следующий.**

---

## Change 7: `stream-editor-resync`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F7 · [`02`](02-stream-offer-editor.md) §6 |
| **AC** | F7.1–F7.3 [`30`](30-mvp-features-and-acceptance.md) |

**После apply:** Fetch после ручного удаления оффера в Keitaro → removed + bring back.

### Проверь

1. Удалить оффер в Keitaro admin → Fetch → строка removed (серая).
2. Bring back + Push → оффер снова в Keitaro.
3. Локальный черновик (жёлтый) не теряется безумно при Fetch (см. `15` merge).

**Ок → verify → archive → следующий.**

---

## Change 8: `project-readme-delivery`

- [ ] **Заархивирован**

| | |
| --- | --- |
| **Фичи** | F8 + F9 · [`32-product-docs-in-app.md`](32-product-docs-in-app.md) |
| **AC** | F8.*, F9.* [`30`](30-mvp-features-and-acceptance.md) |
| **ProductDocs** | Все страницы индекса заполнены; README в корне |

**После apply:** README, `/docs` + `/docs/{page}`, ссылка в header, полный сценарий сдачи.

### Проверь

1. README: clone, env, migrate, run — с нуля на чистой машине (по возможности).
2. `/docs` — оглавление; страницы 00, 01, 02, 03 читаются.
3. Сквозной сценарий: Home → Create → Editor → Add/Pin → diff → Push (как в [`26`](26-key-flows.md) Flow 5).
4. GitHub push (когда решишь) — ссылка в README.

**Ок → verify → archive → **MVP сдан**.**

---

## Сводка прогресса

| # | Change | Фичи | Готово |
| --- | --- | --- | --- |
| 1 | `foundation-keitaro-client` | F0 | [x] |
| 2 | `home-navigation` | F1 | [x] |
| 3 | `campaign-creator` | F2 | [ ] |
| 4 | `stream-editor-fetch-ui` | F3 | [ ] |
| 5 | `stream-editor-offer-ops` | F4 | [ ] |
| 6 | `stream-editor-publish` | F5,F6 | [ ] |
| 7 | `stream-editor-resync` | F7 | [ ] |
| 8 | `project-readme-delivery` | F8,F9 | [ ] |

---

## Что говорить агенту

| Ты | Агент |
| --- | --- |
| «Начинаем change N» / «следующий» | propose для slug из таблицы, product go, apply |
| «Проверь» после apply | вывести блок **Проверь** этого change + запустить verify |
| «Всё ок, архивируем» | archive + отметить `[x]` в этом файле |

Пока change не archive — **не** начинай следующий.