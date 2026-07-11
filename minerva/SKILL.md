---
name: minerva
description: Композиционный движок знаний — имплементация Knowledge Services. Skill-native: bounded contexts живут в references/ скилла. Агент получает KB через skill_view без дополнительного кода навигации.
version: 0.5.0
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

**Skill-native (ADR-010):** bounded contexts хранятся в `references/` скилла. Discoverability — через `references/index.md` (карта контекстов). Агент загружает его после SKILL.md и знает всё, что есть в workspace.

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
    ├── index.md                      # карта всех контекстов (discoverability)
    ├── coffee/                       # = bounded context
    │   ├── index.md
    │   ├── primitives/               # 6 primitives всех типов
    │   ├── components/
    │   ├── modules/
    │   ├── views/
    │   └── artifacts/
    ├── hardware/                     # = bounded context (bind mount)
    └── context-map.md                # легенда связей (ADR-008)
```

## Навигационный flow (skill-native)

```
skill_view("minerva")
  → SKILL.md: оркестратор, список capabilities

skill_view("minerva", file_path="references/index.md")
  → карта всех контекстов: coffee (6 Primitives), hardware (legacy, 75+ entries)

skill_view("minerva", file_path="references/coffee/index.md")
  → описание контекста Coffee, границы, сущности

skill_view("minerva", file_path="references/coffee/primitives/espresso.md")
  → содержимое знания
```

**Правило:** после SKILL.md агент всегда загружает `references/index.md` — это карта всего workspace. Без неё агент не знает, какие контексты существуют.

## Capabilities

### Tier 0 — Навигация (MVP)

| Capability | Реализация | Статус |
|---|---|---|
| `workspace-orientation` | `skill_view("minerva")` → SKILL.md, затем `skill_view("minerva", file_path="references/index.md")` | MVP |
| `context-exploration` | `skill_view("minerva", file_path="references/{context}/index.md")` | MVP |
| `level-browsing` | `skill_view("minerva", file_path="references/{context}/{level}/")` — агент читает index.md контекста, находит нужный уровень | MVP |
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
| «Что есть в KB?» / «Какие контексты?» | `skill_view("minerva")` → `skill_view("minerva", file_path="references/index.md")` |
| «Расскажи про контекст coffee» | `skill_view("minerva", file_path="references/coffee/index.md")` |
| «Какие Primitives в coffee?» | читаем `references/coffee/index.md` → секция Primitives |
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
2. Discoverability — через `references/index.md`. Агент загружает его после SKILL.md и знает все контексты.
3. Навигация — через `skill_view`. Не через `ls`, `find` или `read_file` напрямую.
4. Файлы остаются обычными `.md` (ADR-006). `skill_view` — convenience, не lock-in.
5. SKILL.md — entry point и оркестратор, не дамп содержимого KB.
6. Новый контекст = новая директория в `references/` + её `index.md` + запись в `references/index.md`.

## Зависимости

- [ADR-002](../knowledge-service-scaffolding/references/adr/002-five-level-hierarchy.md) — 5 уровней
- [ADR-006](../knowledge-service-scaffolding/references/adr/006-filesystem-premises.md) — KB = файлы
- [ADR-010](../knowledge-service-scaffolding/references/adr/010-skill-native-knowledge-base.md) — skill-native KB
- [ADR-011](../knowledge-service-scaffolding/references/adr/011-capability-roadmap.md) — capability roadmap
