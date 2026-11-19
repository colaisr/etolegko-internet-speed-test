# Сквозные сценарии (ключевые flows)

> **Статус:** актуален (2026-11-19, фаза B закрыта). Детали: [`29-mvp-functional-description.md`](29-mvp-functional-description.md) §7.

## Flow 1 — Новая кампания под ленд

**Ценность:** шаблон → сразу симулятор.

1. Создаватель: имя + geo + оффер, превью шаблона.
2. Create → URL + domain/group/source.
3. Редактор → Fetch → оффер 100%.
4. (Дальше Flow 2.)

## Flow 2 — Подкрутить ротацию (симулятор)

**Ценность:** играть со сплитом без Keitaro.

1. Add / Remove / Pin → жёлтый поток, новые %.
2. Push disabled, если ≠100%.
3. Diff → подтверждение → Push → синхронно.

## Flow 3 — Отмена эксперимента

**Ценность:** нулевой риск.

1. Изменения без Push.
2. Cancel → белый, Keitaro как было.

## Flow 4 — Keitaro правили без меня

**Ценность:** честный Fetch.

1. В Keitaro удалили офферы.
2. Fetch → removed.
3. Bring back + Push **или** оставить и Push.

## Flow 5 — День от Create до Push

Create → редактор → Fetch → Add×2 → Pin → diff → Push → (опционально) drift + Fetch → решение.

См. [`29`](29-mvp-functional-description.md) §7.