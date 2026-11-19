# Legko — конституция проекта

## 1. Продукт

Legko — обёртка над [Keitaro](https://keitaro.io) для управления рекламными кампаниями (тестовое задание). Замысел и scope MVP будут зафиксированы в `PlanDocs/` после проработки с владельцем. Пока нормативного `PlanDocs/00-product-overview.md` нет — вход через `PlanDocs/README.md`.

## 2. Память проекта

- `PlanDocs/` — замысел («зачем и что»), по нему делается реализация. Начинать с `PlanDocs/README.md`.
- `openspec/` — технические спеки («как работает»): `specs/` после archive и активные `changes/`. Индекс — `openspec/README.md`.
- `ProductDocs/` — бизнес-база знаний: как продукт работает **сейчас**; обновляется в каждом change; **в MVP отдаётся пользователю на `/docs`**. Индекс — `ProductDocs/README.md`. См. `PlanDocs/32-product-docs-in-app.md`.
- `ProjectDocs/roles/` — роли агентов; `.claude/agents/` — адаптеры субагентов.
- `ProjectDocs/design/` — бренд, **design-system.md**, **ux-principles.md**; `artifacts/prototypes/legko-corporate-prototype.html` — эталон UI. Все итерации UI — только компоненты из design-system.
## 3. Процесс

**До кода:** фазы A–F в `PlanDocs/28-pre-implementation-process.md` (product → designer → product → developer → план этапов). **Project-manager не используется.**

**После точки готовности §28:** OpenSpec change — `/opsx:propose` → `/opsx:apply` → `/verify-change <slug>` → `/opsx:archive`. Гейты — `ProjectDocs/roles/openspec-gates.md`. Роли — `ProjectDocs/roles/README.md`.

## 4. Правила

- Решения по продукту сначала фиксируются в `PlanDocs`, потом в ролях и спеках.
- Change не архивируется, пока не обновлена страница `ProductDocs` (гейт docs-sync).
- Три слоя не смешивать: замысел (`PlanDocs`), техническая норма (`openspec/specs`), бизнес-описание «как есть» (`ProductDocs`).
- Не выдумывать цифры, статусы и часы.
- Язык документации — русский.

## 5. Технический стек

**FastAPI**, **SQLAlchemy 2**, **Alembic**, **SQLite**, **Jinja2**, **HTMX**, **httpx** → Keitaro. Детали и модули — `PlanDocs/15-architecture.md`, `openspec/project.md`.