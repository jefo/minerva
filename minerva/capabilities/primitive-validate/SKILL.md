---
name: primitive-validate
type: capability
tier: 1
skill: minerva
contract:
  input: "путь к .md файлу Primitives"
  output: "PASS с предупреждениями | FAIL с конкретными ошибками"
based_on: [adr-004, adr-011]
---

# Primitive Validation

Проверить Primitive на соответствие таксономии и правилам.

## Контракт

**Вход:** путь к `.md` файлу Primitives (относительно корня workspace или абсолютный).

**Выход:**
- `PASS` — файл валиден. Может содержать WARN-ы (опциональные поля не заполнены).
- `FAIL` — файл невалиден. Список конкретных ошибок с указанием поля.

## Правила валидации

### 1. Обязательные поля (FAIL если отсутствуют)

Для всех типов:
- `id` — непустой, формат `{context}-{slug}`
- `title` — непустой
- `type` — одно из: Concept, Metric, Specification, Observation, Law, Relation
- `status` — одно из: draft, review, verified, deprecated
- `context` — непустой, совпадает с именем директории контекста
- `created`, `updated` — формат YYYY-MM-DD

Тип-специфичные:

| Тип | Обязательные поля |
|---|---|
| Concept | `definition` |
| Metric | `value`, `unit` |
| Specification | `value`, `source` |
| Observation | `value`, `conditions`, `source`, `date_observed` |
| Law | `formula`, `explanation` |
| Relation | `subject`, `predicate`, `object` |

### 2. Структурные проверки (FAIL)

- Файл находится в `references/{context}/primitives/` — иначе не Primitive
- Файл не `index.md` — служебный, не знание
- `context` в frontmatter совпадает с родительской директорией

### 3. Семантические проверки (WARN)

- `tags` пуст — рекомендовать добавить
- `synonyms` пуст для Concept — рекомендовать заполнить
- `source_url` пуст для Specification — рекомендовать добавить ссылку
- `formula` пуст для Metric где значение могло быть вычислено
- `id` не соответствует паттерну `{context}-{slug}`

### 4. Downward visibility (WARN)

- Primitive не должен содержать ссылок на Components, Modules, Views, Artifacts
- Если в markdown-теле встречается `ref:component/` или `ref:module/` — WARN

## Реализация

```bash
FILE="$1"

# 0. Проверить существование
test -f "$FILE" || { echo "FAIL: file not found: $FILE"; exit 1; }

# 1. Извлечь frontmatter
FM=$(sed -n '/^---$/,/^---$/p' "$FILE" | sed '1d;$d')

# 2. Проверить базовые поля
check_field() {
  local name="$1" fm="$2" required="$3"
  local val=$(echo "$fm" | grep "^${name}:" | head -1 | sed "s/^${name}: *//")
  if [ "$required" = "required" ] && [ -z "$val" ]; then
    echo "FAIL: missing required field '$name'"
    return 1
  fi
  echo "$val"
}

TITLE=$(check_field "title" "$FM" "required") || exit 1
TYPE=$(check_field "type" "$FM" "required") || exit 1
STATUS=$(check_field "status" "$FM" "required") || exit 1
CONTEXT=$(check_field "context" "$FM" "required") || exit 1
ID=$(check_field "id" "$FM" "required") || exit 1
CREATED=$(check_field "created" "$FM" "required") || exit 1
UPDATED=$(check_field "updated" "$FM" "required") || exit 1

# 3. Проверить type из списка
case "$TYPE" in
  Concept|Metric|Specification|Observation|Law|Relation) ;;
  *) echo "FAIL: invalid type '$TYPE'. Must be one of: Concept, Metric, Specification, Observation, Law, Relation"; exit 1 ;;
esac

# 4. Проверить status
case "$STATUS" in
  draft|review|verified|deprecated) ;;
  *) echo "FAIL: invalid status '$STATUS'"; exit 1 ;;
esac

# 5. Проверить даты
echo "$CREATED" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || echo "FAIL: invalid created date '$CREATED'"
echo "$UPDATED" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || echo "FAIL: invalid updated date '$UPDATED'"

# 6. Тип-специфичные проверки
case "$TYPE" in
  Concept)
    check_field "definition" "$FM" "required" || exit 1
    check_field "synonyms" "$FM" "optional"
    ;;
  Metric)
    check_field "value" "$FM" "required" || exit 1
    check_field "unit" "$FM" "required" || exit 1
    ;;
  Specification)
    check_field "value" "$FM" "required" || exit 1
    check_field "source" "$FM" "required" || exit 1
    ;;
  Observation)
    check_field "value" "$FM" "required" || exit 1
    check_field "conditions" "$FM" "required" || exit 1
    check_field "source" "$FM" "required" || exit 1
    check_field "date_observed" "$FM" "required" || exit 1
    ;;
  Law)
    check_field "formula" "$FM" "required" || exit 1
    check_field "explanation" "$FM" "required" || exit 1
    ;;
  Relation)
    check_field "subject" "$FM" "required" || exit 1
    check_field "predicate" "$FM" "required" || exit 1
    check_field "object" "$FM" "required" || exit 1
    ;;
esac

# 7. WARN-проверки
echo "$FM" | grep -q '^tags:.*\[\]' && echo "WARN: tags are empty — consider adding tags"
echo "$FM" | grep -q '^synonyms:.*\[\]' && echo "WARN: synonyms empty for Concept"

echo "PASS: $TITLE [$TYPE] ($STATUS)"
```
