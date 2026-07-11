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
│       └── adr/                      # Architecture Decision Records
│           ├── template.md
│           ├── 001-two-axis-architecture.md
│           ├── 002-five-level-hierarchy.md
│           ├── 003-downward-visibility.md
│           ├── 004-primitives-taxonomy.md
│           └── 005-capabilities.md
└── minerva/                          # Имплементация knowledge-services
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

## Конвенции

> *Заполняется по мере принятия решений.*

- Язык: русский для ADR и документации, английский для кода
- Формат дат: YYYY-MM-DD
- Именование веток: `feature/...`, `fix/...`, `adr/...`

## Связанные скиллы

- `knowledge-base-construction` — методология построения файловых БЗ
- `llm-wiki` — Karpathy wiki pattern для связанных markdown-страниц
