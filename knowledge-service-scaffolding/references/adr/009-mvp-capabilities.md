---
id: adr-009
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [mvp, capabilities, navigation, workspace]
based_on: [adr-002, adr-005, adr-006, adr-007]
---

# ADR-009: MVP — capabilities навигации по workspace

## Контекст

ADR-005 определил capabilities как composable-единицы minerva skill — Use Cases на DDD-оси, выраженные языком бизнес-операций. ADR-006 зафиксировал premises: KB — это файлы, агенты работают без посредников. ADR-007 определил структуру workspace с progressive disclosure через `index.md`.

MVP minerva — это минимальный набор capabilities, достаточный для того, чтобы агент мог понимать workspace и путешествовать по нему. Никакого создания, редактирования или валидации знаний — только навигация.

## Решение

Четыре capabilities, покрывающие полный цикл навигации: от входа в workspace до чтения конкретного знания.

### Capability 1: Workspace Orientation

**Бизнес-операция:** понять устройство workspace — какие контексты в нём существуют, как они называются, где служебные файлы.

**Контракт:**
- Вход: путь к workspace (или текущая директория, если агент уже в workspace)
- Выход: карта workspace — список контекстов с краткими описаниями, путь к `context-map.md`, метаданные workspace

**Реализуется через:** чтение корневого `index.md`.

**ADR:** 006 (файлы), 007 (workspace/index.md)

### Capability 2: Context Exploration

**Бизнес-операция:** войти в изолированный контекст и понять его устройство — какие сущности в нём живут, какие правила действуют, что есть на каждом уровне композиции.

**Контракт:**
- Вход: имя контекста (или путь к директории контекста)
- Выход: описание контекста из его `index.md` + список непустых уровней (на каких уровнях уже есть знания)

**Реализуется через:** чтение `{context}/index.md` + `ls` по пяти стандартным директориям.

**ADR:** 007 (context/index.md), 002 (5 уровней)

### Capability 3: Level Browsing

**Бизнес-операция:** посмотреть, какие знания есть на конкретном уровне композиции внутри контекста.

**Контракт:**
- Вход: контекст + уровень (primitives | components | modules | views | artifacts)
- Выход: список файлов на уровне с краткими аннотациями (из frontmatter: title, type, status)

**Реализуется через:** `ls {context}/{level}/` + чтение frontmatter каждого файла для аннотаций.

**ADR:** 002 (уровни), 007 (стандартные директории)

### Capability 4: Knowledge Retrieval

**Бизнес-операция:** прочитать конкретное знание — Primitive, Component, Module, View или Artifact.

**Контракт:**
- Вход: путь к файлу знания (или контекст + уровень + имя файла)
- Выход: полное содержимое файла — frontmatter + markdown

**Реализуется через:** `read_file`.

**ADR:** 006 (KB = файлы, read_file = retrieval)

### Композиция capabilities в навигационный flow

```
Workspace Orientation
    ↓
Context Exploration   ←── пользователь выбирает контекст
    ↓
Level Browsing        ←── пользователь выбирает уровень
    ↓
Knowledge Retrieval   ←── пользователь выбирает файл
```

Это не жёсткий pipeline — пользователь (человек или агент) может начать с любого уровня. Но типичный путь: orientation → exploration → browsing → retrieval.

## Что НЕ входит в MVP

- Создание знаний (Primitive Creation) — следующий этап
- Валидация (Integrity Gate) — следующий этап
- Редактирование (Change Proposal) — следующий этап
- Кросс-контекстная навигация (Context Map resolution) — требует ADR по формату context-map.md
- Query layer («найди все Metric типа X») — требует индексации, следующий этап

MVP отвечает ровно на один вопрос: **«агент может понять, что есть в workspace, и прочитать любое знание»**.

## Связь с ADR-005 (структура capability)

Каждая capability оформляется как директория внутри `minerva/capabilities/`:

```
minerva/
├── SKILL.md                            # оркестратор
└── capabilities/
    ├── workspace-orientation/
    │   └── SKILL.md
    ├── context-exploration/
    │   └── SKILL.md
    ├── level-browsing/
    │   └── SKILL.md
    └── knowledge-retrieval/
        └── SKILL.md
```

Каждая `SKILL.md` — это локальный скилл: правила, шаблоны, контракт capability. Оркестратор (`minerva/SKILL.md`) маршрутизирует запросы к нужной capability.

## Последствия

**Что становится проще:**
- Проверка MVP: создать workspace, заполнить один контекст, пройти навигационный flow
- Наращивание: следующая capability (Primitive Creation) просто добавляется в `capabilities/`, оркестратор узнаёт о ней
- Независимая разработка: четыре capabilities можно делать параллельно

**Что требует внимания:**
- Capabilities не должны дублировать друг друга. Если Level Browsing начинает читать index.md контекста — это нарушение границы Context Exploration
- Контракты должны быть стабильными. Изменение контракта Context Exploration ломает оркестратор
