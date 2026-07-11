---
name: knowledge-retrieval
type: capability
skill: minerva
contract:
  input: "путь к файлу знания (или контекст + уровень + имя файла)"
  output: "полное содержимое файла: frontmatter + markdown"
based_on: [adr-006]
---

# Knowledge Retrieval

Прочитать конкретное знание — Primitive, Component, Module, View или Artifact.

## Контракт

**Вход:**
- Полный путь к `.md` файлу, или
- Контекст + уровень + имя файла (без `.md`)

**Выход:**
- Полное содержимое файла: YAML frontmatter + markdown body
- Метаинформация: уровень композиции, контекст, тип (из frontmatter)

## Правила

1. Разрезолвить путь: если даны контекст + уровень + имя → собрать `{context}/{level}/{name}.md`.
2. Проверить, что файл существует и это `.md`.
3. Прочитать файл → вернуть содержимое.
4. Извлечь из frontmatter: `title`, `type`, `status`, `based_on`.
5. Файл не должен быть `index.md` — это служебный файл, не знание. Если запрошен `index.md` — перенаправить на Context Exploration.

## Реализация

```bash
# Разрезолвить путь
if [ $# -eq 1 ]; then
  FILE="$1"
elif [ $# -eq 3 ]; then
  CONTEXT="$1"
  LEVEL="$2"
  NAME="$3"
  FILE="$CONTEXT/$LEVEL/${NAME}.md"
else
  echo "Usage: knowledge-retrieval <path> | <context> <level> <name>"
  exit 1
fi

# Проверить существование
test -f "$FILE" || { echo "ERROR: file not found: $FILE"; exit 1; }

# Отклонить index.md
case "$(basename "$FILE")" in
  index.md) echo "ERROR: index.md is a structural file, not knowledge. Use Context Exploration instead."; exit 1 ;;
esac

# Прочитать файл (вызывающий агент делает read_file)
echo "=== $(basename "$FILE" .md) ==="
# read_file "$FILE"
```
