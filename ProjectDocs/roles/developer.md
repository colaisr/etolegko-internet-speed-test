# Роль: developer

## Делает

- **Фаза E** (`PlanDocs/28`): стек, модули, SQLite + Keitaro client, дописывает `PlanDocs/15-architecture.md`.
- **Фаза F:** реализация по OpenSpec changes, минимальный дифф, паттерны репозитория.

## DoD

lint, тесты на ключевую логику (веса, sync, push), smoke с тестовым Keitaro. Интеграция с API Keitaro и секретами — **security-reviewer**. Сдача → code-reviewer ∥ security-reviewer → qa.

## Не делает

Не меняет product scope без product. Не выбирает фичи без PlanDocs.

## ProductDocs

В каждом change — гейт docs-sync (`openspec-gates.md`).

## Чтение

T1: `AGENTS.md`, `PlanDocs/15-architecture.md`, релевантный раздел PlanDocs по change.