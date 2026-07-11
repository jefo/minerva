---
name: minerva
description: Композиционный движок знаний — имплементация Knowledge Services. Skill-native: bounded contexts живут в references/ скилла. Агент получает KB через skill_view без дополнительного кода навигации.
version: 0.4.0
status: draft
triggers:
  - Работа с Knowledge Services workspace (references/ скилла minerva)
  - Навигация по knowledge base: «что в KB», «покажи контекст», «какие Primitives»
  - Чтение знаний: «прочитай espresso.md», «дай Extraction Law»
  - Создание workspace: «добавь контекст в references/»
  - Вопросы о структуре KB
---

# minerva — Skill-Native Knowledge Base

Композиционный движок знаний. Реализует архитектуру Knowledge Services: Primitives → Components → Modules → Views → Artifacts.

**Skill-native (ADR-010):** bounded contexts хранятся в `references/` скилла. Hermes раздаёт их через `skill_view` и `linked_files` — progressive disclosure работает без дополнительного кода.

## Структура

```
minerva/                              # Hermes skill = knowledge base
├── SKILL.md                          # entry point + оркестратор
├── capabilities/                     # операции над KB
│   ├── workspace-orientation/
│   ├── context-exploration/
│   ├── level-browsing/
│   └── knowledge-retrieval/
└── references/                       # = workspace
    ├── coffee/                       # = bounded context
    │   ├── index.md
    │   ├── primitives/               # 6 primitives всех типов
    │   ├── components/
    │   ├── modules/
    │   ├── views/
    │   └── artifacts/
    ├── context-map.md                # связи контекстов
    └── README.md                     # описание workspace (опционально)
```

## Навигационный flow (skill-native)

```
skill_view("minerva")
  → SKILL.md: карта KB, список контекстов
  → linked_files: все файлы references/ одним списком

skill_view("minerva", file_path="references/coffee/index.md")
  → описание контекста Coffee

skill_view("minerva", file_path="references/coffee/primitives/espresso.md")
  → содержимое знания
```

Ни одного `ls`, `find` или `read_file` напрямую. Вся навигация — через один механизм платформы.

## Capabilities

### Tier 0 — Навигация (MVP)

| Capability | Реализация | Статус |
|---|---|---|
| `workspace-orientation` | `skill_view("minerva")` → SKILL.md + linked_files | MVP |
| `context-exploration` | `skill_view("minerva", file_path="references/{context}/index.md")` | MVP |
| `level-browsing` | фильтр `linked_files` по префиксу `references/{context}/{level}/` | MVP |
| `knowledge-retrieval` | `skill_view("minerva", file_path="references/{context}/{level}/{file}.md")` | MVP |

### Tier 1 — Primitive Management

| Capability | Контракт | Статус |
|---|---|---|
| `primitive-create` | context + type + title + fields → новый .md с frontmatter | active |
| `primitive-validate` | путь к .md → PASS/WARN/FAIL | active |
| `primitive-bulk-import` | structured source → N созданных Primitives | scaffolding |
| `primitive-update` | путь + fields → обновлённый файл | scaffolding |
| `primitive-deprecate` | путь + reason → status: deprecated | scaffolding |

### Tier 2 — Composition

| Capability | Контракт | Статус |
|---|---|---|
| `component-compose` | context + title + 2+ Primitive IDs → новый Component | active |
| `module-assemble` | context + title + Component IDs + Primitive IDs → новый Module | active |
| `view-define` | context + title + 2+ sections → новый View | active |
| `artifact-compile` | context + title + View ID + Module/Component/Primitive IDs → новый Artifact | active |

## Оркестрация

### Tier 0 — навигация

| Интент пользователя | Действие |
|---|---|
| «Что есть в KB?» / «Какие контексты?» | `skill_view("minerva")` |
| «Расскажи про контекст coffee» | `skill_view("minerva", file_path="references/coffee/index.md")` |
| «Какие Primitives в coffee?» | фильтр `linked_files` → `references/coffee/primitives/*.md` |
| «Прочитай Extraction Law» | `skill_view("minerva", file_path="references/coffee/primitives/extraction-law.md")` |

### Tier 1 — создание знаний

| Интент пользователя | Действие |
|---|---|
| «Создай Primitive типа Concept» | `primitive-create` |
| «Проверь Primitive на валидность» | `primitive-validate` |
| «Импортируй 15 GPU из JSON» | `primitive-bulk-import` |
| «Обнови TDP у RTX 5070» | `primitive-update` |
| «Пометъ pump-pressure как устаревший» | `primitive-deprecate` |

### Tier 2 — композиция

| Интент пользователя | Действие |
|---|---|
| «Собери Component из этих Primitives» | `component-compose` |
| «Собери Module из Components и Primitives» | `module-assemble` |
| «Создай схему анализа GPU» | `view-define` |
| «Собери обзор RTX 5070 из GPU Analysis + GB205 Module» | `artifact-compile` |

## Правила

1. KB = `references/` скилла. Workspace — это инстанс minerva с заполненными references.
2. Навигация — через `skill_view` и `linked_files`. Не через `ls` и `read_file`.
3. Любой агент, загрузивший скилл, получает карту KB через `linked_files` (zero-cost discoverability).
4. Файлы остаются обычными `.md` (ADR-006). `skill_view` — convenience, не lock-in.
5. SKILL.md — entry point и оркестратор, не дамп содержимого KB.
6. Новый контекст = новая директория в `references/` + её `index.md`.

## Зависимости

- [ADR-002](../knowledge-service-scaffolding/references/adr/002-five-level-hierarchy.md) — 5 уровней
- [ADR-006](../knowledge-service-scaffolding/references/adr/006-filesystem-premises.md) — KB = файлы
- [ADR-010](../knowledge-service-scaffolding/references/adr/010-skill-native-knowledge-base.md) — skill-native KB
- [ADR-011](../knowledge-service-scaffolding/references/adr/011-capability-roadmap.md) — capability roadmap
