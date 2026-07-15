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

## ADR Index

| ID | Заголовок | Статус | Дата |
|----|-----------|--------|------|
| 001 | Two-axis architecture: DDD + Atomic Design | accepted | 2026-07-11 |
| 002 | Five-level knowledge composition hierarchy | accepted | 2026-07-11 |
| 003 | Downward-visibility rule | accepted | 2026-07-11 |
| 004 | Knowledge Primitives taxonomy (6 типов) | accepted | 2026-07-11 |
| 005 | Capabilities как composable-единицы | accepted | 2026-07-11 |
| 006 | KB as filesystem — фундаментальные premises | accepted | 2026-07-11 |
| 007 | Структура workspace — bounded contexts | accepted | 2026-07-11 |
| 008 | Context Map для интеграции контекстов | accepted | 2026-07-11 |
| 009 | MVP — capabilities навигации | accepted | 2026-07-11 |
| 010 | Bounded contexts как references скилла | accepted | 2026-07-11 |
| 011 | Capability roadmap — 4 тира | accepted | 2026-07-11 |
| 012 | Слой Acquisition — pre-structured research | accepted | 2026-07-11 |
| 013 | Backend/Frontend split | accepted | 2026-07-11 |
| 014 | Data Warehouse как методологический фундамент | accepted | 2026-07-11 |
| 015 | System Architecture — agent-native DW | accepted | 2026-07-11 |
| 016 | Data Model — dimensional schemas, SCD | accepted | 2026-07-11 |
| 017 | Lineage DAG — граф происхождения данных | accepted | 2026-07-11 |
| 018 | ETL Pipeline — Acquisition как capabilities | superseded → 029 | 2026-07-11 |
| 019 | Agent Query Model — capabilities как stored procedures | accepted | 2026-07-11 |
| 020 | Methodology Specification | accepted | 2026-07-11 |
| 021 | Architecture Validation — walkthrough (RTX 5060) | accepted | 2026-07-11 |
| 022 | AI Data Analyst Agent | accepted | 2026-07-11 |
| 023 | Consumer Analytics Roadmap | accepted | 2026-07-11 |
| 024 | Data Acquisition First | accepted | 2026-07-11 |
| 025 | Source Layer, Definitions, Bus Matrix Contract | accepted | 2026-07-11 |
| 026 | Platform / Applications Split | proposed | 2026-07-13 |
| 027 | CPU Decision-Centric ViewModel | accepted | 2026-07-13 |
| 028 | Fact Insert — Ingestion Gateway | accepted | 2026-07-13 |
| 029 | Agent-Native ETL Override | accepted | 2026-07-13 |
| 030 | Tech Debt & Data Debt Register | accepted | 2026-07-13 |
| 031 | CPU Data Model Engineering Lab | accepted | 2026-07-13 |
| 032 | Data Engineer Capabilities — Design, Build, Operate, Explore | proposed | 2026-07-13 |

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
