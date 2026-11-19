---
description: Шаг verify Gloom между apply и релизом — spec-verifier → code-reviewer ∥ security-reviewer → qa → spec-verifier (docs-sync), каждый субагентом; гейты в gates/*.json; fail останавливает цепочку
argument-hint: <change-slug>
---

Шаг **verify** для OpenSpec change `$ARGUMENTS`. Цепочка процесса: `propose → apply → verify → релиз → archive` (`ProjectDocs/roles/openspec-gates.md`). Ты — **оркестратор**: запускаешь стадии, записываешь гейты, останавливаешься на первом fail. Сам код и спеки в этом шаге не правишь.

**Вход.** Slug из аргумента. Если его нет, выполни `npx openspec list --json` и спроси владельца, не угадывай.

**Независимость.** Каждой стадии передавай **только** slug (ревьюерам ещё `scope_files`). Не пересказывай, что сделано в apply, и не подсказывай ответ.

## Стадия 1 — спека

1. Субагент `spec-verifier`, промпт: `Change: <slug>. Режим: verify. Раунд: <N>.` (N = прошлый `round` из `gates/spec-verify.json` + 1, иначе 1).
2. Запиши его Gate JSON в `openspec/changes/<slug>/gates/spec-verify.json` (поле `reviewed_at` — текущее время ISO).
3. `node scripts/verify-change-gates.mjs --change <slug> --gate spec-verify`. Не 0 → **стоп**, переходи к «Итог».

## Стадия 2 — ревью (параллельно)

1. `scope_files` — все файлы, изменённые в change, кроме `openspec/changes/<slug>/**` и `ProductDocs/**` (по `git status` / `git diff --name-only` и tasks.md). Только файлы, не каталоги.
2. В одном сообщении два субагента: `code-reviewer` и `security-reviewer`, промпт обоим: `Change: <slug>. scope_files: [...]. Раунд: <N>.`
3. Запиши `gates/code-reviewer.json` и `gates/security-reviewer.json` по их ответам.
4. `node scripts/verify-change-gates.mjs --change <slug> --gate code-reviewer` и `--gate security-reviewer`. Любой не 0 → **стоп**.

## Стадия 3 — qa

1. Субагент `qa`, промпт: `Change: <slug>. Режим: гейт как стадия verify. Верни Gate JSON для gates/qa.json.`
2. Запиши `gates/qa.json`; в `checks` — только команды, которые qa реально запустил.
3. Не 0 по `--gate qa` → **стоп**.

## Стадия 4 — docs-sync

1. Субагент `spec-verifier`, промпт: `Change: <slug>. Режим: docs-sync. Раунд: <N>.` Он сверяет delta-спеки change и страницы `ProductDocs/` из tasks.md.
2. Запиши `gates/docs-sync.json`. Вердикт `waived` допустим только с `waiver_reason` (бизнес-поведение не меняется).
3. `node scripts/verify-change-gates.mjs --change <slug> --gate docs-sync`. Не 0 → **стоп**.

## Финал

`node scripts/verify-change-gates.mjs --change <slug>` (все пять гейтов и порядок). 0 → «verify зелёный, можно переходить к релизу и archive». `tasks.md` в этом шаге не трогай: галочки ставит исполнитель.

## Итог (всегда)

Короткая таблица стадий: pass / fail / не запускалась. Для fail — находки как есть:

- **не доделано** → «чинить в основном чате, затем снова `/verify-change <slug>`»;
- **расхождение со спекой** → вопрос владельцу: менять код или спеку; ничего не менять без ответа;
- **docs-sync fail** → «обновить страницу ProductDocs и добавить строку в её журнал, затем снова стадия 4»;
- **ревью fail на раунде 2** → эскалация владельцу.

Archive без зелёных гейтов заблокирует хук `scripts/hooks/guard-archive.mjs`.
