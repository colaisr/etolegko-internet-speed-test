# Субагенты Claude Code (Gloom)

Каждый `<role>.md` — **адаптер** изолированного субагента. Поведение и чек-листы — в `ProjectDocs/roles/<role>.md`. Перед доработкой прочитай [`ProjectDocs/roles/README.md`](../../ProjectDocs/roles/README.md).

Адаптер обязан иметь: frontmatter (`name`, `description`, `tools`), в теле — принять роль → прочитать `ProjectDocs/roles/<role>.md` → маршрутизировать режим. Длинные процедуры в адаптеры не копировать.

Исключение: у `project-manager` поле `tools` не задано — агент наследует MCP-инструменты task-системы (система будет выбрана позже).
