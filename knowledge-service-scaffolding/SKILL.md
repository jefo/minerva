---
name: knowledge-services-scaffolding
description: SSOT для проекта knowledge-services. Архитектурные решения (ADR), конвенции, структура проекта. Хранится в репо knowledge-services, не внутри Hermes.
version: 0.1.0
status: draft
triggers:
  - Работа в репо knowledge-services
  - Запрос ADR по knowledge-services
  - Архитектурные решения по проекту
  - Вопросы о структуре/конвенциях knowledge-services
---

# knowledge-services — Project SSOT

Единый источник правды о проекте `knowledge-services`. Содержит архитектурные решения, конвенции разработки и структуру проекта.

## Назначение проекта

**Knowledge Services** — композиционный движок знаний. База знаний, в которой статьи, обзоры и гайды не пишутся с нуля, а собираются из переиспользуемых инженерных моделей. Atomic Design, адаптированный для знаний: Primitives → Components → Modules → Views → Artifacts.

DDD определяет онтологию (что существует), Atomic Design — композицию (как представления собираются из сущностей). Это две ортогональные оси.

Подробнее: [`docs/prd.md`](docs/prd.md)

## Структура репозитория

```
minerva/                              # Корень монорепо
├── README.md
├── knowledge-service-scaffolding/    # Мета-проект (эта директория)
│   ├── SKILL.md                      # SSOT проекта
│   ├── README.md
│   ├── docs/
│   │   └── prd.md                    # Product Requirements Document
│   └── references/
│       ├── taxonomy-and-semantics.md  # Канон таксономии и семантики
│       └── adr/                      # Architecture Decision Records
│           ├── template.md
│           ├── 001-two-axis-architecture.md
│           ├── 002-five-level-hierarchy.md
│           ├── 003-downward-visibility.md
│           ├── 004-primitives-taxonomy.md
│           ├── 005-capabilities.md
│           ├── 006-filesystem-premises.md
│           ├── 007-workspace-structure.md
│           ├── 008-context-map.md
│           ├── 009-mvp-capabilities.md
│           └── 010-skill-native-knowledge-base.md
└── minerva/                          # Имплементация — skill-native KB
    ├── SKILL.md                      # Оркестратор
    ├── capabilities/                 # 4 capabilities MVP
    │   ├── workspace-orientation/SKILL.md
    │   ├── context-exploration/SKILL.md
    │   ├── level-browsing/SKILL.md
    │   └── knowledge-retrieval/SKILL.md
    └── references/                   # = workspace
        ├── context-map.md
        └── coffee/                   # bounded context
            ├── index.md
            ├── primitives/           # 6 primitives (Concept, Metric, Spec, Obs, Law, Relation)
            ├── components/
            ├── modules/
            ├── views/
            └── artifacts/
```

## ADR

Архитектурные решения фиксируются в `references/adr/`. Формат: Markdown с YAML frontmatter.

### Статусы ADR

| Статус | Значение |
|--------|----------|
| `proposed` | Предложено, ждёт обсуждения |
| `accepted` | Принято, действует |
| `superseded` | Заменено более новым ADR |
| `deprecated` | Больше не применяется |

### Индекс ADR

| ID | Заголовок | Статус | Дата |
|----|-----------|--------|------|
| 001 | Two-axis architecture: DDD + Atomic Design | accepted | 2026-07-11 |
| 002 | Five-level knowledge composition hierarchy | accepted | 2026-07-11 |
| 003 | Downward-visibility rule | accepted | 2026-07-11 |
| 004 | Knowledge Primitives taxonomy (6 типов) | accepted | 2026-07-11 |
| 005 | Capabilities как composable-единицы minerva skill | accepted | 2026-07-11 |
| 006 | Knowledge Base as filesystem — фундаментальные premises | accepted | 2026-07-11 |
| 007 | Структура workspace — файловая проекция bounded contexts | accepted | 2026-07-11 |
| 008 | Намерение использовать Context Map для интеграции контекстов | accepted | 2026-07-11 |
| 009 | MVP — capabilities навигации по workspace | accepted | 2026-07-11 |
| 010 | Bounded contexts как references скилла — skill-native KB | accepted | 2026-07-11 |

## References

Канонические справочные документы — не ADR, а стабильные описания системы.

| Файл | Назначение |
|---|---|
| [`references/taxonomy-and-semantics.md`](references/taxonomy-and-semantics.md) | Таксономия уровней (Primitives → Artifacts), типы Primitives (6 типов), правила композиции. Основан на ADR-002, ADR-003, ADR-004. Загружается агентами как SSOT семантики Knowledge Services |

## Конвенции

> *Заполняется по мере принятия решений.*

- Язык: русский для ADR и документации, английский для кода
- Формат дат: YYYY-MM-DD
- Именование веток: `feature/...`, `fix/...`, `adr/...`

## Связанные скиллы

- `knowledge-base-construction` — методология построения файловых БЗ
- `llm-wiki` — Karpathy wiki pattern для связанных markdown-страниц
