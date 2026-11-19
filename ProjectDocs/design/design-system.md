# Design system — Legko (MVP)

> **Статус:** актуален (2026-11-19). Источник бренда: [`brand-brief.md`](brand-brief.md). UX: [`ux-principles.md`](ux-principles.md).

**Правило:** в коде и прототипах **не изобретать** новые кнопки/бейджи — расширять этот каталог через PR в design-system.

## 1. Design tokens

### Цвета

| Token | Значение | Использование |
| --- | --- | --- |
| `--color-bg-app` | `#f4f4f5` | Фон рабочей зоны |
| `--color-surface` | `#ffffff` | Карточки, таблица |
| `--color-header` | `#0d1117` | Верхняя панель (как hero сайта) |
| `--color-accent` | `#c8f542` | Primary CTA (лайм «Это Легко») |
| `--color-accent-hover` | `#b8e636` | Hover primary |
| `--color-on-accent` | `#0a0a0a` | Текст на лайме |
| `--color-text` | `#18181b` | Основной текст |
| `--color-text-muted` | `#71717a` | Подписи |
| `--color-text-on-dark` | `#fafafa` | Текст в header |
| `--color-border` | `#e4e4e7` | Рамки на светлом |
| `--color-border-dark` | `#27272a` | Header border |
| `--status-sync` | `#16a34a` | Синхронно |
| `--status-draft` | `#ca8a04` | Черновик (янтарь, не путать с лайм CTA) |
| `--status-draft-border` | `#eab308` | Рамка оффер-потока |
| `--status-removed` | `#f4f4f5` | Строка removed |
| `--color-danger` | `#dc2626` | Ошибки |

### Типографика

| Token | Значение |
| --- | --- |
| `--font-sans` | `"Montserrat", system-ui, sans-serif` (Google Fonts) |
| `--text-xs` | 0.75rem |
| `--text-sm` | 0.875rem |
| `--text-base` | 1rem |
| `--text-lg` | 1.125rem |
| `--text-xl` | 1.25rem |
| `--text-2xl` | 1.5rem |
| `--weight-medium` | 500 |
| `--weight-semibold` | 600 |
| `--weight-bold` | 700 |
| `--tracking-nav` | 0.06em (uppercase nav) |

Заголовки экранов: `text-2xl` / bold. Навигация и primary кнопки: **uppercase**, `tracking-nav`, semibold.

### Радиусы и тени

| Token | Значение |
| --- | --- |
| `--radius-none` | 0 |
| `--radius-sm` | 2px |
| `--shadow-card` | `0 1px 3px rgba(0,0,0,.08)` |
| `--shadow-modal` | `0 16px 48px rgba(0,0,0,.2)` |

Кнопки и поля ввода: **`radius-sm`** (почти прямоугольник, как сайт).

### Отступы

Шкала 4px: 4, 8, 12, 16, 24, 32, 48. Контент max-width **1120px**, centered.

## 2. Компоненты (каталог)

### `AppHeader`

- Фон `--color-header`, высота 56px.
- Слева: логотип (куб-пиксель + «LEGKO»), подпись «Keitaro» muted.
- Справа: ссылка **«Документация»** → `/docs` (обязательно, F9).

### `NavTab` (внутри приложения, не маркетинг)

- Uppercase, `text-sm`.
- Active: outline 1px `--color-accent` + лёгкий фон `rgba(200,245,66,.12)`.

### `Button`

| Вариант | Стиль |
| --- | --- |
| **primary** | bg accent, color on-accent, uppercase, padding 12px 24px |
| **secondary** | border border, bg surface |
| **ghost** | текст only, на тёмном — on-dark |
| **danger** | border danger, текст danger |

States: hover, disabled (opacity .45), loading (spinner).

### `IconButton` (`btn-icon`)

- Квадрат 34×34 для действий в таблице редактора; stroke-SVG 16px, `title` + `aria-label`.
- Варианты: `btn-icon--ghost`, `btn-icon--accent` (pin), `btn-icon--danger` (remove).

### `Input` / `Select`

- Высота 40px, border `--color-border`, focus ring 2px accent.
- Label uppercase xs muted.

### `Card`

- bg surface, border 1px, shadow-card, padding 24px.
- **Card--draft:** border 2px `--status-draft-border`.

### `Badge`

| Variant | Вид |
| --- | --- |
| `sync` | зелёный outline |
| `draft` | янтарный fill light |
| `warning` | синий outline «Проверьте Keitaro» |

### `StatusPill`

- Для статуса кампании в таблицах и модалках (не CTA): скруглённый pill, точка + текст sentence case.
- Варианты: `status-pill--sync`, `--draft`, `--attention`.
- Не использовать uppercase/outline «как у кнопки».

### `DataTable`

- Header row muted xs uppercase.
- Колонка **Weight**: `font-size: text-lg`, `font-weight: bold`, `font-variant-numeric: tabular-nums`.
- Row removed: bg `--status-removed`, opacity .85.
- Footer: «Сумма: **100%**» или ошибка красным.
- **Home recent:** `data-table--recent`, строка-кнопка `recent-row`, hover bg app.

### `OfferCombobox`

- Input + dropdown; debounce поиска; empty state.

### `StreamMutedRow`

- Внутри editor workspace: lock, название служебного потока, подпись «не редактируется»; фон app, левая граница.

### `HeroStrip` (Home)

- `hero-strip--brand`: тёмный фон header, нижняя граница 3px accent, только copy (без primary CTA).
- Kicker «Legko × Keitaro» accent uppercase.

### `WorkspaceCreateStrip`

- Внутри `card--home-workspace`: центрированный `btn-primary--workspace` + muted meta про шаблон.
- Лёгкий лаймовый градиент фона, border card.

### `CreatorForm` (modal)

- `field-label--required` — метка «· обязательно».
- `field-error-slot` — зарезервированная высота под ошибку (модалка не скачет).
- `field--invalid` — красная рамка; одна строка ошибки, без дублирующего summary-блока.

### `Modal` / `PushConfirmModal`

- Overlay; заголовок; секции diff (Add/Remove/Weights); footer Cancel + primary «Подтвердить Push».
- Create/open/recent на Home — `modal-panel` в `#app-modal-body`.

### `Toast` / `InlineAlert`

- success / error; для API Keitaro.

### `CopyField`

- URL кампании + кнопка copy (accent icon).

### `EditorWorkspace` (`card--editor-lab`)

- Как **workspace-create-strip** на Home: верхняя граница 3px accent, лёгкий лаймовый градиент фона, тень с зелёным оттенком.
- Таблица в рамке; hover строки — лайм 7%; **добавление оффера** — ghost-строка (`offer-row--add`) в `tfoot` таблицы (не отдельная градиентная полоса).
- Dock Push: верх 3px accent (связь с header hero).

### `EditorCommandBar`

- Верх редактора: kicker **лайм** (как hero-kicker), **имя + StatusPill**, Keitaro id · geo (muted).
- Справа: `CopyField` (если есть URL) + **Fetch Streams** (secondary).
- Не дублировать hero Home — светлая зона, разделитель снизу.

### `EditorPublishDock`

- Sticky footer: слева подсказка (веса / готовность Push), справа **Отменить** + **Push** (primary).
- Push disabled с понятным title/hint при Σ ≠ 100%.

## 3. Макет страниц

| Страница | Структура |
| --- | --- |
| Home | Header dark + hero copy; card: search/Open, create strip по центру, таблица недавних |
| Creator | Модалка на Home: форма + preview + env read-only |
| Editor | `EditorCommandBar` (статус, Σ, Fetch, Copy URL) + `editor-workspace` (таблица) + `EditorPublishDock` |

## 4. Реализация (фаза E)

- Один источник токенов: `tokens.css` или theme в выбранном UI-фреймворке.
- Компоненты — папка `ui/`; **запрещено** inline-стили кнопок вне каталога.

## 5. Референс-прототип

[`artifacts/prototypes/legko-corporate-prototype.html`](artifacts/prototypes/legko-corporate-prototype.html) — эталон внешнего вида MVP.