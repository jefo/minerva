---
name: artifact-compile
type: capability
tier: 2
skill: minerva
status: active
contract:
  input: "context + title + View ID + Module IDs + Component IDs + Primitive IDs"
  output: "путь к скомпилированному Artifact .md — композиции существующих знаний"
based_on: [adr-002, adr-003, adr-011]
---

# Artifact Compilation

Собрать Artifact — конечный продукт: статью, обзор, сравнение, гайд. Artifact почти ничего своего не содержит — он композиция существующих знаний.

Это ключевая capability Tier 2. Она демонстрирует, зачем нужна вся архитектура: страница не пишется с нуля, а собирается из переиспользуемых моделей.

## Контракт

**Вход:**
- `context` — bounded context
- `title` — название Artifact
- `view` — ID существующего View (обязательно)
- `modules` — список ID существующих Modules (опционально)
- `components` — список ID существующих Components (опционально)
- `primitives` — список ID существующих Primitives (опционально)
- `tags` — теги

**Выход:**
- Путь: `references/{context}/artifacts/{slug}.md`
- Frontmatter с декларацией композиции
- Markdown-тело: структура из View + контент из Modules/Components/Primitives

## Правила

1. **View обязателен.** Artifact без View — самостоятельный документ, не композиция. Это нарушение модели.
2. **Все ссылки должны существовать.** Проверить View, каждый Module, Component и Primitive.
3. **Artifact ничего своего не содержит.** Если из Artifact убрать все ссылки на нижние уровни и остаётся полноценный документ — нарушение.
4. **Downward visibility:** Artifact ссылается на View, Modules, Components, Primitives (все уровни ниже). Не ссылается на другие Artifacts.
5. **Компиляция = сборка, не копирование.** Artifact не дублирует содержимое Module. Он ссылается на Module. При обновлении Module — Artifact получает обновление автоматически.
6. **Редакторский слой:** Artifact может содержать *минимальный* связующий текст (переходы между секциями, введение, заключение). Но основное содержание — из нижних уровней.

## Frontmatter-схема

```yaml
---
id: "coffee-espresso-brewing-guide"
title: "Espresso Brewing Guide"
type: Artifact
status: draft
tags: [coffee, espresso, guide]
context: "coffee"
view: "coffee-brewing-method-analysis"
modules:
  - "coffee-espresso-extraction-model"
components:
  - "coffee-brewing-parameters"
  - "coffee-grind-quality"
primitives:
  - "coffee-espresso"
  - "coffee-extraction-law"
created: "2026-07-11"
updated: "2026-07-11"
---

# Espresso Brewing Guide

[Введение: editorial content — 2-3 предложения]

## Principle
[Контент из Espresso Extraction Model + Extraction Law]

## Equipment
[Контент из Grind Quality Component]

## Parameters
[Контент из Brewing Parameters Component]

## Technique
[Контент из Espresso Extraction Model — секция Technique]

## Taste Profile
[Редакторский контент + ссылки на Observations]

## Recommendations
[Редакторский контент]
```

## Что делает компилятор

1. Читает View → получает массив секций `[Principle, Equipment, Parameters, ...]`
2. Для каждой секции — ищет релевантный контент в Modules, Components, Primitives
3. Собирает markdown: заголовок секции → контент из источника → редакторская связка
4. Генерирует `based_on` — список всех ID, использованных в компиляции

**На данном этапе:** компилятор не автоматический. Агент читает View, Modules, Components, Primitives и собирает Artifact вручную, следуя структуре View. Полная автоматизация — будущее (потребует семантического mapping секций на источники).

## Реализация

```bash
CONTEXT="$1"
TITLE="$2"
VIEW_ID="$3"
# Остальные аргументы — списки ID через --modules, --components, --primitives

# 1. Проверить View
VIEW_FILE="references/$CONTEXT/views/${VIEW_ID}.md"
test -f "$VIEW_FILE" || { echo "FAIL: View '$VIEW_ID' not found"; exit 1; }

# 2. Проверить все ссылки
for mid in $MODULE_IDS; do
  test -f "references/$CONTEXT/modules/${mid}.md" || { echo "FAIL: Module '$mid' not found"; exit 1; }
done
# ... аналогично для components и primitives

# 3. Создать Artifact
# Frontmatter с массивами view, modules, components, primitives
# Тело: структура из View, контент from references
```

## Пример для hardware

```
Artifact: RTX 5070 Review
  view: gpu-analysis
  modules: [gpu-gb205-architecture, gpu-blackwell-memory]
  components: [gpu-memory-subsystem, gpu-power-delivery]
  primitives: [gpu-rtx-5070, gpu-tdp-250w, gpu-16gb-gddr7, ...]
```

Структура из GPU Analysis View (Architecture → Memory → Power → Performance → Tradeoffs → Recommendations), контент из GB205 Architecture Module, Memory Subsystem Component, отдельных Specification и Observation Primitives.
