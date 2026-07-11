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

> *Заполняется при определении scope проекта.*

## Структура репозитория

```
knowledge-services/
├── SKILL.md              # Этот файл — SSOT проекта
├── README.md             # Входная точка для контрибьюторов
├── references/
│   └── adr/              # Architecture Decision Records
│       ├── template.md   # Шаблон ADR
│       └── 001-example.md
├── src/                  # Исходный код
└── ...
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
| —  | —         | —      | —    |

## Конвенции

> *Заполняется по мере принятия решений.*

- Язык: русский для ADR и документации, английский для кода
- Формат дат: YYYY-MM-DD
- Именование веток: `feature/...`, `fix/...`, `adr/...`

## Связанные скиллы

- `knowledge-base-construction` — методология построения файловых БЗ
- `llm-wiki` — Karpathy wiki pattern для связанных markdown-страниц
