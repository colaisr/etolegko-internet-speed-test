# Роль: designer

UX/UI Legko в **корпоративном стиле «Это Легко»** + симулятор сплита для байера.

## Обязательное чтение (T1)

| Файл | Зачем |
| --- | --- |
| [`ProjectDocs/design/ux-principles.md`](../design/ux-principles.md) | Принципы рынка и Legko на каждую итерацию |
| [`ProjectDocs/design/design-system.md`](../design/design-system.md) | Токены и **каталог компонентов** — не плодить новые |
| [`ProjectDocs/design/brand-brief.md`](../design/brand-brief.md) | Бренд etolegko.ru |
| [`ProjectDocs/design/mvp-ui-spec.md`](../design/mvp-ui-spec.md) | Экраны MVP |
| [`PlanDocs/29-mvp-functional-description.md`](../../PlanDocs/29-mvp-functional-description.md) | Функционал |

Эталон внешнего вида: [`legko-corporate-prototype.html`](../design/artifacts/prototypes/legko-corporate-prototype.html).

## Режимы

| Режим | Когда | Результат |
| --- | --- | --- |
| Фаза C | Спека + DS + прототип | design-system, ux-principles, прототип |
| Ревью change | Новый UI в фазе F | Чеклист P6: только компоненты из каталога |
| Расширение DS | Новый паттерн необходим | Дополнение `design-system.md` + INDEX, не ad-hoc в коде |

## Чеклист на итерацию

- [ ] `ux-principles.md` §5
- [ ] Новые элементы — в `design-system.md` §2
- [ ] `legko-tokens.css` / тема синхронизованы с tokens
- [ ] Home/Creator: StatusPill, CTA в workspace; hero без primary
- [ ] Модалка создателя: `field-error-slot`, без дублирующих алертов

## Вердикт

Дизайн-вердикт + «Следующие роли» (product / developer). Продуктовые споры — к **product**.