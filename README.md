# minerva

Монорепо проекта Knowledge Services.

## Структура

```
minerva/
├── knowledge-service-scaffolding/   # Мета-проект: PRD, ADR, SSOT
│   ├── SKILL.md                     # Hermes skill — точка входа
│   ├── docs/prd.md                  # Product Requirements Document
│   └── references/adr/              # Architecture Decision Records
└── minerva/                         # Имплементация knowledge-services
```

## Быстрый старт

```bash
git clone https://github.com/jefo/minerva.git
cd minerva
```

### Hermes

Скилл `knowledge-services-scaffolding` загружается автоматически при работе в репо. SSOT проекта: `knowledge-service-scaffolding/SKILL.md`.
