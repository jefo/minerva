---
name: workspace-orientation
type: capability
skill: minerva
contract:
  input: "путь к workspace (или текущая директория)"
  output: "карта workspace: список контекстов, путь к context-map.md, метаданные"
based_on: [adr-006, adr-007]
---

# Workspace Orientation

Понять устройство workspace: какие контексты существуют, где служебные файлы.

## Контракт

**Вход:** путь к workspace. Если не указан — текущая директория.

**Выход:**
- Список контекстов (имя директории + краткое описание из `index.md`)
- Наличие и путь к `context-map.md`
- Метаданные workspace (владелец, домен, версия схемы)

## Правила

1. Найти корневой `index.md`. Если его нет — это не workspace, ошибка.
2. Прочитать `index.md` → извлечь список контекстов и метаданные.
3. Контекст = поддиректория, содержащая `index.md`. Директории без `index.md` — не контексты.
4. Проверить наличие `context-map.md` — сообщить, есть или нет.

## Реализация

```bash
# 1. Проверить наличие workspace/index.md
test -f "$WORKSPACE/index.md" || echo "ERROR: not a workspace"

# 2. Прочитать карту workspace
read_file "$WORKSPACE/index.md"

# 3. Найти контексты (директории с index.md)
for dir in "$WORKSPACE"/*/; do
  test -f "$dir/index.md" && echo "context: $(basename $dir)"
done

# 4. Проверить context-map.md
test -f "$WORKSPACE/context-map.md" && echo "context-map: present" || echo "context-map: absent"
```
