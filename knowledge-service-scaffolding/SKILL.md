---
name: knowledge-services-scaffolding
description: "SSOT для проекта knowledge-services. ADR, конвенции, структура."
version: 0.2.0
triggers:
  - "Работа в репо knowledge-services"
  - "Запрос ADR / архитектуры по knowledge-services"
  - "Вопросы о конвенциях проекта"
  - "Capability authoring"
  - "Pre-flight review"
---

# knowledge-services — Project SSOT

## Конвенции

### Capability Authoring

Capabilities для LLM-агентов — **модель + контракт + инварианты**, не step-by-step процедура.

LLM знает концепты dimensional model, bus matrix, aliasing, Kimball из training data. Не нужно объяснять «шаг 1: загрузи bus matrix, шаг 2: проверь dimensions». Нужно дать:
- **Model** — как устроена система (warehouse по Kimball, source layer, platform/app split)
- **Contract** — вход/выход, ошибки (в frontmatter)
- **Invariants** — что должно быть истинным всегда (source-значения — сырые строки, структура едина)
- **Template** — точный формат выходных данных
- **Pitfalls** — что capable LLM всё ещё может сделать не так (перепутать source-значения с dim_id)

Агент сам выстраивает execution plan из понимания модели. Пошаговая процедура — для калькулятора, не для reasoning engine. Антипаттерн: «Шаг 1. Загрузи bus matrix. Шаг 2. Проверь dimensions...».

### Agent-Native ETL

ETL в agent-native системе — **один reasoning-проход агента**, не staged pipeline. Агент держит bus matrix, dimensional model и данные в контексте. Промежуточные файлы, декларативные mapping-файлы, три раздельных вызова — не нужны. Extract = инструменты агента. Transform = reasoning. Load = fact-insert. ADR-018 (классический staged pipeline) superseded → ADR-029.

### Pre-Flight Review

После архитектурных изменений (ADR, новый capability, migration) — программная проверка: ADR vs реальность, capabilities vs файловая структура, данные vs контракты. Выполнять через поиск + yaml-парсинг, не вручную. Цель: найти расхождения до того как они заразят следующую сессию.
