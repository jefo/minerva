---
name: context-exploration
type: capability
skill: minerva
version: 0.2.0
contract:
  input: "имя контекста (например 'coffee')"
  output: "описание контекста: границы, сущности, состав уровней"
based_on: [adr-002, adr-007, adr-010]
---

# Context Exploration

Войти в контекст и понять его устройство.

## Контракт

**Вход:** имя контекста — директория в `references/` (например `coffee`, `hardware`).

**Выход:**
- Описание контекста из его `index.md`: назначение, границы, сущности
- Состав уровней: перечень Primitives, Components, Modules, Views, Artifacts

## Реализация (skill-native)

```
skill_view("minerva", file_path="references/{context}/index.md")
```

Контекстный `index.md` содержит:
- Границы и назначение контекста
- Перечень сущностей/примитивов
- Правила контекста

Агент читает один файл и получает полную картину контекста.

## Для детализации

Чтобы увидеть конкретные файлы уровня, агент использует `level-browsing`:

```
# Какие Primitives?
skill_view("minerva", file_path="references/coffee/index.md") → секция Primitives
```
