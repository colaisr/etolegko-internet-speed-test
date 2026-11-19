# Субагенты Claude Code (Legko)

Каждый `<role>.md` — **адаптер** изолированного субагента. Поведение и чек-листы — в `ProjectDocs/roles/<role>.md`. Перед доработкой прочитай [`ProjectDocs/roles/README.md`](../../ProjectDocs/roles/README.md).

Адаптер обязан иметь: frontmatter (`name`, `description`, `tools`), в теле — принять роль → прочитать `ProjectDocs/roles/<role>.md` → маршрутизировать режим. Длинные процедуры в адаптеры не копировать.

Роль **project-manager** в Legko не используется (см. `PlanDocs/28-pre-implementation-process.md`).
