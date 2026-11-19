# OpenSpec и гейты ролей

> **Статус:** черновик (2026-11-04). Как change в `openspec/` стыкуется с агентами `ProjectDocs/roles/` и с бизнес-базой `ProductDocs/`. Образец — AgentPoint, упрощённый: нет гейтов трафика и SEO, добавлен гейт **docs-sync**. Замок на archive работает уже сейчас (скрипт и хук без зависимостей); замка на push нет, пока нет деплоя.

## Три слоя памяти

| Слой | Где | Отвечает на | Кто читает |
| --- | --- | --- | --- |
| Замысел | `PlanDocs/` | зачем и что задумано | все; до реализации |
| Технические спеки | `openspec/specs/<capability>/spec.md`, активные `openspec/changes/<slug>/` | как система работает (требования и сценарии), что меняем сейчас | разработчики, агенты |
| Бизнес-база | `ProductDocs/` | как продукт работает с точки зрения бизнеса: правила, роли, граничные случаи | владельцы, сотрудники компании, админка |

Спеки живут своей жизнью: при archive delta вливается в `openspec/specs/`, папка change уходит в `openspec/changes/archive/`. `ProductDocs/` описывает то же простым языком и обновляется в каждом change.

## Порядок на типовом change

```text
/opsx:propose   → proposal, design, tasks; правила из openspec/config.yaml
product (гейт 1) → вердикт go до apply: change опирается на нормативный раздел PlanDocs
/opsx:apply     → реализация tasks в основном чате
/verify-change <slug> → шаг verify, каждая стадия — субагент со свежим контекстом, вход только slug:
                  1. spec-verifier (verify)  → gates/spec-verify.json   код против спеки change
                  2. code-reviewer ∥ security-reviewer → gates/code-reviewer.json + security-reviewer.json
                  3. qa                       → gates/qa.json            проверки и критерии приёмки
                  4. spec-verifier (docs-sync)→ gates/docs-sync.json     ProductDocs отражает реализованное
                  любой fail → стоп; чиним в основном чате → снова /verify-change
релиз, qa пост-деплой (когда появится деплой)
/opsx:archive   → хук guard-archive проверяет гейты и tasks.md; затем delta → specs, change → archive
```

**Verify только находит и сообщает.** «Не доделано» чинит основной чат. «Расхождение со спекой» решает владелец: править код или спеку. Ничего не менять без его ответа.

**Правило свежести.** Гейт не может быть «старше» предыдущего (по `reviewed_at`): после правки кода заново проходят стадию, на которой нашли проблему, и все после неё. Скрипт это проверяет.

## Гейты

| Гейт | Кто | Файл | Что проверяет |
| --- | --- | --- | --- |
| spec-verify | spec-verifier | `gates/spec-verify.json` | код соответствует requirements и scenarios change: полнота, правильность, согласованность |
| code-reviewer | code-reviewer | `gates/code-reviewer.json` | diff по `scope_files`; максимум 2 раунда, дальше эскалация владельцу |
| security-reviewer | security-reviewer | `gates/security-reviewer.json` | режим change; всегда для денег, коинов, выплат, видео, PII, прав доступа |
| qa | qa | `gates/qa.json` | реально запущенные проверки (unit, интеграционные, e2e) и критерии приёмки из proposal; на каждый сценарий WHEN/THEN есть тест; перед ручным тестированием: всё, что появилось в change, можно потрогать через «Тестовые инструменты» или сид, без доступа к базе |
| docs-sync | spec-verifier | `gates/docs-sync.json` | страницы ProductDocs соответствуют delta-спеке и реализованному коду |

## Гейт docs-sync

Это замок на актуальность бизнес-базы. Стадия идёт **последней**, когда код уже не меняется.

1. spec-verifier в режиме docs-sync читает delta-спеки change и страницы ProductDocs, которые указаны в tasks.md.
2. Проверяет: страница описывает реализованное поведение (не замысел), правила и роли совпадают со спекой, расхождения с PlanDocs записаны в «Отличия от замысла», в «Журнале обновлений» есть строка со slug change.
3. Вердикт `pass`, либо `waived` с причиной (не короче 20 символов), если бизнес-поведение не меняется, либо `fail`.

Скрипт `scripts/verify-change-gates.mjs` дополнительно проверяет механически: каждая страница из `pages` существует, лежит в `ProductDocs/` и **содержит slug change**. Смысл правки проверяет spec-verifier, а наличие записи не обойти.

## Формат gate JSON

```json
{
  "gate": "docs-sync",
  "change": "add-creator-studio",
  "round": 1,
  "verdict": "pass",
  "reviewed_at": "2026-11-04T10:15:00Z",
  "pages": ["ProductDocs/05-creator-studio.md"],
  "planDocsMarked": ["PlanDocs/05-creator-studio.md"],
  "findings": []
}
```

- Общие поля всех гейтов: `gate` (имя из таблицы), `change` (slug), `round`, `verdict` (`pass` или `fail`; для docs-sync ещё `waived`), `reviewed_at` (ISO), `findings`.
- Находка: `{ "kind": "not-done" | "mismatch", "where": "файл или requirement", "what": "..." }`.
- `docs-sync`: `pages` обязателен при `pass`; при `waived` обязателен `waiver_reason`.
- Скрипт проверяет `gate`, `change`, `reviewed_at`, вердикт, порядок и поля docs-sync. Остальные поля — для людей и агентов.

## Замок на archive

- **Скрипт:** `node scripts/verify-change-gates.mjs --change <slug> [--archive]`. Код возврата 0 только при зелёных гейтах; с `--archive` ещё все задачи в `tasks.md` закрыты и есть группа «ProductDocs».
- **Хук:** `scripts/hooks/guard-archive.mjs`, подключён в `.claude/settings.json` (PreToolUse, Bash) и `.cursor/hooks.json` (beforeShellExecution). Блокирует `mv`, `git mv` в `openspec/changes/archive/` и `openspec archive <slug>`, пока скрипт не вернул 0.
- Замок живёт в хуках и скрипте, а не в сгенерированных навыках OpenSpec, поэтому `openspec update` его не стирает.

**Чего замок не ловит (граница, не долг):**
- архив руками человека в обычном терминале: хук видит только команды агента. Позже это закроет CI;
- формальную правку страницы «для галочки»: смысл проверяет spec-verifier в стадии docs-sync.

## Шаблон блока в `tasks.md`

```markdown
## Гейты ролей (после кода)
- [ ] /verify-change <slug>: spec-verifier → code-reviewer ∥ security-reviewer → qa → docs-sync, все гейты pass

## Тесты
- [ ] Unit-тесты на реализованную логику; интеграционные для денег, коинов, доступа, возраста, вебхуков и расписаний
- [ ] E2E на пользовательские пути change; в списке указать, какой тест закрывает какой сценарий WHEN/THEN
- [ ] Данные для тестов и ручной проверки добавлены в сид; e2e проходят локально и на стенде
- [ ] Тесты помечены: smoke или регрессия

## Тестовые инструменты
- [ ] Добавить в раздел админки «Тестовые инструменты» (и скрипт сида) то, что нужно тестировщику для ручной проверки этого change
- [ ] Перечислить в `tasks.md`, что можно потрогать вручную и каким действием получить нужные данные
- [ ] Убедиться, что раздел отсутствует в боевом окружении

## ProductDocs
- [ ] Создать или обновить страницу ProductDocs/<раздел>.md по реализованному поведению
- [ ] Добавить строку в «Журнал обновлений» страницы со slug этого change
- [ ] Поставить в PlanDocs пометку «реализовано, см. ProductDocs/…»
- [ ] Обновить колонку «Обновлено» в ProductDocs/README.md
```

Если бизнес-поведение не меняется (рефакторинг), вместо четырёх пунктов — одна задача «подтвердить отсутствие бизнес-изменений» и вердикт `waived` с причиной в гейте.

## Что дальше

- После выбора стека (`PlanDocs/15-architecture.md`) заполнить `openspec/project.md` и контекст в `openspec/config.yaml`.
- Когда появятся код и деплой: перенести проверки `qa` в скрипты, добавить замок на push и CI-проверку гейтов.
