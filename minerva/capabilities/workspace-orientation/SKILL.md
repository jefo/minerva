---
name: workspace-orientation
type: capability
skill: minerva
version: 0.2.0
contract:
  input: "ничего (текущий скилл = текущий workspace)"
  output: "список контекстов с описаниями и статусом, наличие context-map.md"
based_on: [adr-006, adr-007, adr-010]
---

# Workspace Orientation

Понять, что есть в KB: загрузить `references/index.md` и показать все контексты.

## Контракт

**Вход:** не требуется — workspace = `references/` текущего скилла minerva.

**Выход:**
- Список контекстов (имя, путь, описание, статус, примечания)
- Ссылка на `context-map.md` (легенда связей)

## Реализация (skill-native)

```
skill_view("minerva", file_path="references/index.md")
```

`references/index.md` содержит:
- Заголовок «Minerva Workspace»
- Секцию «## Контексты» — перечисление всех контекстов с путями, статусом, описанием
- Секцию «## Связи контекстов»
- Навигационную подсказку для агентов

Агент читает этот файл и получает полную карту workspace. Никаких `ls` или `find`.

## Пример вывода

```
Workspace: Minerva

Контексты:
  coffee/     active    — Модели заваривания кофе (6 Primitives)
  hardware/   legacy    — База знаний по компьютерному железу (75+ entries, не minerva-таксономия)
```
