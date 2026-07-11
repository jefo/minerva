# knowledge-service-scaffolding

Мета-проект Knowledge Services. Здесь живут PRD, архитектурные решения (ADR) и SSOT проекта.

## Что это

**Knowledge Services** — композиционный движок знаний. База знаний, в которой статьи, обзоры и гайды собираются из переиспользуемых инженерных моделей, а не пишутся с нуля.

Подробнее: [`docs/prd.md`](docs/prd.md)

## Структура

```
knowledge-service-scaffolding/
├── SKILL.md              # Project SSOT — загружается Hermes Agent
├── README.md             # Эта страница
├── docs/
│   └── prd.md            # Product Requirements Document
└── references/
    └── adr/              # Architecture Decision Records
        ├── template.md
        ├── 001-two-axis-architecture.md
        ├── 002-five-level-hierarchy.md
        ├── 003-downward-visibility.md
        └── 004-primitives-taxonomy.md
```

## Имплементация

Код проекта Knowledge Services находится в соседней директории: [`../minerva/`](../minerva/)
