---
name: module-assemble
type: capability
tier: 2
skill: minerva
status: active
contract:
  input: "context + title + список Component ID + список Primitive ID"
  output: "путь к созданному Module .md — законченной инженерной модели"
based_on: [adr-002, adr-003, adr-011]
---

# Module Assembly

Собрать Module — законченную модель подсистемы, процесса или продукта. Module — это то, что может быть independently verified специалистом.

## Контракт

**Вход:**
- `context` — bounded context
- `title` — название Module
- `components` — список ID существующих Components (опционально, но должен быть хотя бы один Component ИЛИ Primitive)
- `primitives` — список ID существующих Primitives (опционально)
- `tags` — теги

**Выход:**
- Путь: `references/{context}/modules/{slug}.md`
- Frontmatter со ссылками на Components и Primitives
- Markdown-тело с полным описанием модели

## Правила

1. **Хотя бы один Component или Primitive.** Module не может быть пустым.
2. **Все ссылки должны существовать.** Проверить каждый Component ID в `components/` и каждый Primitive ID в `primitives/`.
3. **Кросс-контекстные ссылки — через context-map.** Module не ссылается на Components/Primitives из другого контекста.
4. **Downward visibility:** Module ссылается на Components и Primitives (уровни < 3). Не ссылается на Views или Artifacts.
5. **Полнота:** markdown-тело должно быть достаточным для понимания подсистемы без обращения к внешним источникам (ADR-002, п. 4.3).
6. **После создания** — валидация всех ссылок.

## Frontmatter-схема

```yaml
---
id: "coffee-espresso-extraction-model"
title: "Espresso Extraction Model"
type: Module
status: draft
tags: [coffee, espresso, extraction]
context: "coffee"
components:
  - "coffee-brewing-parameters"
  - "coffee-grind-quality"
primitives:
  - "coffee-extraction-law"
created: "2026-07-11"
updated: "2026-07-11"
---

# Espresso Extraction Model

[Полное описание: как параметры заваривания, качество помола и закон
экстракции вместе образуют модель, предсказывающую результат заваривания]

## Состав

### Components
- **Brewing Parameters** — управляемые переменные
- **Grind Quality** — характеристика помола

### Primitives
- **Extraction Law** — физическая модель экстракции
```

**Обязательные поля:** `components` ИЛИ `primitives` (хотя бы один непустой)
