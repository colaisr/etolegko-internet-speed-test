# Legko — конституция проекта

## 1. Продукт

Legko — обёртка над [Keitaro](https://keitaro.io) для управления рекламными кампаниями (тестовое задание). Замысел и scope MVP будут зафиксированы в `PlanDocs/` после проработки с владельцем. Пока нормативного `PlanDocs/00-product-overview.md` нет — вход через `PlanDocs/README.md`.

## 2. Память проекта

- `PlanDocs/` — замысел («зачем и что»), по нему делается реализация. Начинать с `PlanDocs/README.md`.
- `openspec/` — технические спеки («как работает»): `specs/` после archive и активные `changes/`. Индекс — `openspec/README.md`.
- `ProductDocs/` — бизнес-база знаний: как продукт работает **сейчас**, простым языком. Обновляется в каждом change. Индекс — `ProductDocs/README.md`.
- `ProjectDocs/roles/` — роли агентов; `.claude/agents/` — адаптеры субагентов.
- `ProjectDocs/design/` — бренд, голос, дизайн-система; `ProjectDocs/design/artifacts/` — прототипы и референсы в репозитории.
- `ProjectDocs/pm/` — рабочая память project-manager (статусы, отчёты).

## 3. Процесс

Поток и роли — `ProjectDocs/roles/README.md`.

Каждое изменение — OpenSpec change (`npx @fission-ai/openspec@latest <команда>`): `/opsx:propose` → `/opsx:apply` → `/verify-change <slug>` → релиз → `/opsx:archive`. Порядок, гейты и замок — `ProjectDocs/roles/openspec-gates.md`.

## 4. Правила

- Решения по продукту сначала фиксируются в `PlanDocs`, потом в ролях и спеках.
- Change не архивируется, пока не обновлена страница `ProductDocs` (гейт docs-sync).
- Три слоя не смешивать: замысел (`PlanDocs`), техническая норма (`openspec/specs`), бизнес-описание «как есть» (`ProductDocs`).
- Не выдумывать цифры, статусы и часы.
- Язык документации — русский.

## 5. Технический стек

Стек выбирается на этапе проработки и фиксируется в `PlanDocs/15-architecture.md` (файл появится в PlanDocs). До фиксации не придумывать технологии в design.md change.