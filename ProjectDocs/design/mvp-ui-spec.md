# MVP — UI-спека (фаза C)

> **Статус:** актуален (2026-11-19). Бренд и компоненты: [`design-system.md`](design-system.md), [`ux-principles.md`](ux-principles.md). **Эталон UI:** [`artifacts/prototypes/legko-corporate-prototype.html`](artifacts/prototypes/legko-corporate-prototype.html). Wireframe (устарел): `mvp-wireframe.html`.

## 1. Принципы

| Принцип | Как в UI |
| --- | --- |
| **Симулятор сплита** | Жёлтый = «ещё не в Keitaro»; Push всегда через **diff** |
| **Цифры важнее красоты** | Таблица офферов — главный элемент; крупные **%** |
| **Не как Keitaro admin** | Мало колонок, один оффер-поток, служебный поток — одна серая строка |
| **Срочность** | Ошибки у Push, не всплывашки на фоне |

## 2. Карта экранов

```text
[Home] ── Create ──> [Creator]
  │                      │
  │ Open by ID / Recent  └────> [Editor]
  └──────────────────────────> [Editor]
```

**Home:** два primary CTA — «Создать кампанию», блок «Открыть» (поле Keitaro ID + список недавних).

## 3. Экран: Home

- Заголовок Legko + одна строка: «Настройте сплит до выкладки в Keitaro».
- **Создать кампанию** (primary).
- **Открыть:** input `Campaign ID (Keitaro)` + кнопка Open.
- **Недавние:** до 10 строк — имя, keitaro id, мини-бейдж статуса → клик = Editor.

## 4. Экран: Creator

| Зона | Элементы |
| --- | --- |
| Форма | Name, Geo (ISO-2 + hint), Offer (combobox поиск) |
| Превью | Карточка: «Поток 1: {geo} → Google» / «Поток 2: остальное → {offer}» |
| Инфо | Серый блок: Domain · Group · Source (read-only из конфига) |
| Действия | Create (primary) |

**Success state (тот же route или success panel):**

- Campaign URL + copy
- Keitaro ID
- CTA **Открыть редактор**

## 5. Экран: Editor

### 5.1 Шапка

```
[← Home]  Campaign name · ID · [бейдж статуса]     [Fetch Streams]
Campaign URL (copy) · Domain / Group / Source (muted)
```

**Бейджи:**

| Бейдж | Цвет | Текст |
| --- | --- | --- |
| Синхронно | зелёный outline | «В Keitaro как здесь» |
| Черновик | янтарный fill | «Есть несохранённое» |
| Проверьте Keitaro | синий outline | «Сделайте Fetch» (после подсказки/drift) |

### 5.2 Потоки

- **Служебный:** строка `🔒 Служебный поток (geo → …) — не редактируется`.
- **Оффер-поток:** card с заголовком «Ротация офферов» + pill **Белый** / **Жёлтый** (фон card border: default / amber-3px).

### 5.3 Таблица офферов

| Колонка | Примечание |
| --- | --- |
| Оффер | Имя + мелкий id |
| Вес % | Input number или readonly после pin; **жирный** |
| Pin | Toggle / lock icon |
| Статус | — / «Удалён» |
| Действия | Remove / Bring back |

- Строка **removed:** opacity 0.55, фон `#f4f4f5`.
- **Add offer:** под таблицей, combobox + «Добавить».

### 5.4 Footer actions

```
[Cancel — вторичный, слева]              [Push to Keitaro — primary, справа]
```

Push **disabled** + tooltip: «Сумма весов: 94% (нужно 100%)» или «Нет активных офферов».

### 5.5 Modal: Push (diff)

- Заголовок: «Выложить в Keitaro?»
- Три блока: **Добавить** / **Убрать** / **Изменить веса** (списки или «без изменений»).
- Footer: Отмена · **Подтвердить Push**

## 6. Бренд и токены

Корпоративный стиль [etolegko.ru](https://etolegko.ru/): тёмный **header**, лайм **CTA**, Montserrat, почти прямоугольные кнопки. Рабочая зона — **светлая** (таблица читаема). Полный каталог: [`design-system.md`](design-system.md).

| Семантика | Token |
| --- | --- |
| Черновик | `--status-draft-border` (не путать с лайм CTA) |
| Синхронно | `--status-sync` |
| Removed | `--status-removed` |

## 7. Дизайн-вердикт

- Экраны и иерархия согласованы с фазой B.
- Ценность «симулятор» читается через **жёлтый**, **disabled Push**, **diff modal**.
- Product: подтвердить при закрытии фазы C.

## 8. Следующие роли

- **product** — фаза D (разрез по фичам + acceptance).
- **developer** — фаза E после D.