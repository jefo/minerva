---
name: level-browsing
type: capability
skill: minerva
contract:
  input: "контекст + уровень (primitives | components | modules | views | artifacts)"
  output: "список файлов на уровне с аннотациями из frontmatter"
based_on: [adr-002, adr-007]
---

# Level Browsing

Посмотреть, какие знания есть на конкретном уровне композиции внутри контекста.

## Контракт

**Вход:**
- Контекст (имя или путь)
- Уровень: `primitives`, `components`, `modules`, `views` или `artifacts`

**Выход:**
- Список `.md` файлов на уровне
- Для каждого файла — аннотация из frontmatter: `title`, `type` (для Primitives), `status`

## Правила

1. Проверить, что уровень — одно из пяти валидных имён. Иначе ошибка.
2. Проверить, что директория `{context}/{level}/` существует. Иначе ошибка структуры.
3. Список файлов: только `.md`, исключая `index.md`.
4. Для каждого файла прочитать YAML frontmatter → извлечь `title` и `type` (или `status`).
5. Файлы без frontmatter или без `title` — предупредить, но включить в список.
6. Если уровень пуст — сообщить, что знаний этого уровня пока нет.

## Реализация

```bash
CONTEXT="$1"
LEVEL="$2"

# 1. Валидация уровня
case "$LEVEL" in
  primitives|components|modules|views|artifacts) ;;
  *) echo "ERROR: invalid level '$LEVEL'. Must be: primitives, components, modules, views, artifacts"; exit 1 ;;
esac

DIR="$CONTEXT/$LEVEL"
test -d "$DIR" || { echo "ERROR: directory '$DIR' not found"; exit 1; }

# 2. Список файлов
files=$(find "$DIR" -maxdepth 1 -name '*.md' ! -name 'index.md' | sort)
if [ -z "$files" ]; then
  echo "Level '$LEVEL' is empty — no knowledge files yet."
  exit 0
fi

# 3. Аннотации из frontmatter
echo "=== $LEVEL ($(echo "$files" | wc -l) files) ==="
for f in $files; do
  name=$(basename "$f" .md)
  # Извлечь title из YAML frontmatter (между --- и ---)
  title=$(sed -n '/^---$/,/^---$/p' "$f" | grep '^title:' | head -1 | sed 's/^title: *//' | sed 's/"//g')
  type=$(sed -n '/^---$/,/^---$/p' "$f" | grep '^type:' | head -1 | sed 's/^type: *//')
  status=$(sed -n '/^---$/,/^---$/p' "$f" | grep '^status:' | head -1 | sed 's/^status: *//')
  
  annotation=""
  [ -n "$title" ] && annotation="$title"
  [ -n "$type" ] && annotation="$annotation [$type]"
  [ -n "$status" ] && annotation="$annotation ($status)"
  [ -z "$annotation" ] && annotation="(no frontmatter)"
  
  echo "  $name.md — $annotation"
done
```
