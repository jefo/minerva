---
name: minerva
description: Композиционный движок знаний — имплементация Knowledge Services. Навигация, создание и валидация знаний в файловых workspace-ах.
version: 0.1.0
status: draft
triggers:
  - Работа с Knowledge Services workspace (директория с index.md и контекстами)
  - Навигация по knowledge base: «что в workspace», «покажи контекст», «какие Primitives»
  - Чтение знаний: «прочитай espresso.md», «дай Extraction Model»
  - Создание workspace: «создай workspace», «добавь контекст»
  - Вопросы о структуре KB: «как устроен workspace», «где лежат Primitives»
---

# minerva — Knowledge Services Implementation

Композиционный движок знаний. Реализует архитектуру Knowledge Services: Primitives → Components → Modules → Views → Artifacts в файловом workspace.

Живёт в монорепо [jefo/minerva](https://github.com/jefo/minerva).

## Быстрый старт

Reference workspace для изучения и тестирования:

```
references/real-world-workspace/
├── index.md                 # карта workspace
├── context-map.md           # связи контекстов
└── coffee/                  # контекст «Кофе»
    ├── index.md             # описание контекста
    ├── primitives/          # 6 primitives (Concept, Metric, Specification, Observation, Law, Relation)
    ├── components/          # пусто
    ├── modules/             # пусто
    ├── views/               # пусто
    └── artifacts/           # пусто
```

## Capabilities

| Capability | Контракт | Статус |
|---|---|---|
| `workspace-orientation` | workspace → карта контекстов | MVP |
| `context-exploration` | контекст → описание + уровни | MVP |
| `level-browsing` | контекст + уровень → список файлов с аннотациями | MVP |
| `knowledge-retrieval` | путь к файлу → содержимое | MVP |

Подробные контракты, правила и reference-реализации: [`capabilities/`](capabilities/)

## Оркестрация

| Интент пользователя | Capability |
|---|---|
| «Что есть в этой KB?» / «Какие контексты?» | `workspace-orientation` |
| «Расскажи про контекст coffee» / «Что внутри?» | `context-exploration` |
| «Какие Primitives в coffee?» / «Покажи Modules» | `level-browsing` |
| «Прочитай espresso.md» / «Дай мне Extraction Law» | `knowledge-retrieval` |

## Правила

1. Оркестратор не реализует операции — маршрутизирует к capabilities.
2. При неоднозначности — уточнить у пользователя.
3. Работа с файлами — напрямую (`ls`, `read_file`), без промежуточного API (ADR-006).
4. Navigation flow: orientation → exploration → browsing → retrieval (ADR-007).
5. `index.md` — служебный файл, не знание. Запрашивать через Context Exploration.
6. Reference workspace: `references/real-world-workspace/` — для демонстрации и тестов.

## Зависимости

- [ADR-002](../knowledge-service-scaffolding/references/adr/002-five-level-hierarchy.md) — 5 уровней
- [ADR-006](../knowledge-service-scaffolding/references/adr/006-filesystem-premises.md) — filesystem premises
- [ADR-007](../knowledge-service-scaffolding/references/adr/007-workspace-structure.md) — структура workspace
- [ADR-009](../knowledge-service-scaffolding/references/adr/009-mvp-capabilities.md) — MVP capabilities
