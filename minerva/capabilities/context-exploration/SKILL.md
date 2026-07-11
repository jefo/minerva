---
name: context-exploration
type: capability
skill: minerva
contract:
  input: "имя контекста или путь к директории контекста"
  output: "описание контекста (index.md) + список непустых уровней"
based_on: [adr-002, adr-007]
---

# Context Exploration

Войти в изолированный контекст и понять его устройство.

## Контракт

**Вход:** имя контекста (например `coffee`) или путь к директории контекста.

**Выход:**
- Описание контекста из `index.md`: назначение, границы, сущности, правила
- Список пяти уровней с пометкой: пустой / непустой (сколько файлов)
- Для непустых уровней — краткий состав (имена файлов)

## Правила

1. Найти директорию контекста → проверить наличие `index.md`. Без `index.md` — не контекст.
2. Прочитать `index.md` → извлечь описание контекста.
3. `index.md` не содержит связей с другими контекстами. Если содержит — это нарушение изоляции, предупредить.
4. Проверить пять стандартных директорий: `primitives/`, `components/`, `modules/`, `views/`, `artifacts/`.
5. Отсутствующие директории — ошибка структуры, сообщить.
6. Для каждой директории: количество `.md` файлов (исключая `index.md`).

## Реализация

```bash
CONTEXT="$1"

# 1. Проверить, что это контекст
test -f "$CONTEXT/index.md" || { echo "ERROR: not a context (no index.md)"; exit 1; }

# 2. Прочитать описание контекста
echo "=== Context: $(basename $CONTEXT) ==="
# read_file контекста — вызывающий агент читает index.md

# 3. Проверить уровни
for level in primitives components modules views artifacts; do
  dir="$CONTEXT/$level"
  if test -d "$dir"; then
    count=$(find "$dir" -maxdepth 1 -name '*.md' ! -name 'index.md' | wc -l)
    if [ "$count" -gt 0 ]; then
      echo "  $level/ — $count files"
    else
      echo "  $level/ — empty"
    fi
  else
    echo "  $level/ — MISSING (structure error)"
  fi
done
```
