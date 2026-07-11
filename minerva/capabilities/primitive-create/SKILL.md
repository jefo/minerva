---
name: primitive-create
type: capability
tier: 1
skill: minerva
contract:
  input: "context + type + title + type-specific fields"
  output: "путь к созданному .md файлу с валидным frontmatter"
based_on: [adr-002, adr-004, adr-007, adr-010, adr-011]
---

# Primitive Creation

Создать новый Primitive — неделимую единицу знания — в заданном контексте workspace.

## Контракт

**Вход:**
- `context` — имя bounded context (например `coffee`)
- `type` — один из 6 типов: Concept, Metric, Specification, Observation, Law, Relation
- `title` — человекочитаемое название
- Тип-специфичные поля (см. ниже)

**Выход:**
- Путь к созданному файлу: `references/{context}/primitives/{slug}.md`
- Подтверждение: создан файл с валидным frontmatter

## Правила

1. Slug генерируется из title: lowercase, дефисы, английская транслитерация.
2. Slug должен быть уникален в пределах `references/{context}/primitives/`. Если конфликт — добавить суффикс `-2`, `-3`.
3. Frontmatter создаётся по схеме для данного типа. Все обязательные поля должны быть заполнены.
4. Если обязательное поле не предоставлено — запросить у пользователя.
5. Файл создаётся через `write_file`. После создания — провалидировать через `primitive-validate`.
6. Поля `created` и `updated` устанавливаются на текущую дату.

## Frontmatter-схемы по типам

### Общие поля (все типы)

```yaml
id: "{context}-{slug}"        # уникальный ID
title: "{title}"
type: Concept|Metric|Specification|Observation|Law|Relation
status: draft
tags: []
context: "{context}"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
```

### Concept

```yaml
---
id: "coffee-espresso"
title: "Espresso"
type: Concept
status: draft
tags: [coffee, beverage]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
definition: "Концентрированный кофейный напиток..."
synonyms: [эспрессо]
---

# Espresso

[определение и контекст использования]
```

**Обязательные:** definition
**Опциональные:** synonyms

### Metric

```yaml
---
id: "coffee-extraction-yield"
title: "Extraction Yield"
type: Metric
status: draft
tags: [coffee, extraction]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
value: 20
unit: "%"
formula: "TDS × brew_weight / dose"
---

# Extraction Yield

[описание метрики, типичный диапазон, оптимальное значение]
```

**Обязательные:** value, unit
**Опциональные:** formula

### Specification

```yaml
---
id: "coffee-pump-pressure"
title: "Pump Pressure 9 bar"
type: Specification
status: draft
tags: [coffee, espresso, equipment]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
value: "9 bar"
source: "Rancilio Silvia datasheet"
source_url: "https://..."
---

# Pump Pressure 9 bar

[контекст: стандарт SCA, допуски, производители]
```

**Обязательные:** value, source
**Опциональные:** source_url

### Observation

```yaml
---
id: "coffee-bloom-30s"
title: "Bloom phase: 30s at grind size 15"
type: Observation
status: draft
tags: [coffee, filter, extraction]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
value: "30 s"
conditions: "помол 15 (Baratza Encore), 93°C, доза 18g, V60"
source: "измерение, VST рефрактометр"
date_observed: "2026-06-15"
---

# Bloom Phase Observation

[контекст измерения, сравнение с другими помолами]
```

**Обязательные:** value, conditions, source, date_observed

### Law

```yaml
---
id: "coffee-extraction-law"
title: "Extraction Law"
type: Law
status: draft
tags: [coffee, extraction, physics]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
formula: "extraction ∝ surface_area × contact_time / particle_size"
explanation: "Чем мельче помол — тем быстрее экстракция при прочих равных"
---

# Extraction Law

[граница применимости, связанные величины]
```

**Обязательные:** formula, explanation

### Relation

```yaml
---
id: "coffee-espresso-requires-fine-grind"
title: "Espresso requires Fine Grind"
type: Relation
status: draft
tags: [coffee, espresso, grind]
context: "coffee"
created: "2026-07-11"
updated: "2026-07-11"
subject: "Espresso"
predicate: "requires"
object: "Fine Grind"
---

# Espresso —[requires]→ Fine Grind

[обоснование связи]
```

**Обязательные:** subject, predicate, object

## Реализация

```bash
# Функция: генерация slug из title
slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//'
}

CONTEXT="$1"
TYPE="$2"
TITLE="$3"
SLUG=$(slugify "$TITLE")
FILE="references/$CONTEXT/primitives/$SLUG.md"
DATE=$(date +%Y-%m-%d)
ID="$CONTEXT-$SLUG"

# Проверить, что контекст существует
test -d "references/$CONTEXT" || { echo "ERROR: context '$CONTEXT' not found"; exit 1; }
test -d "references/$CONTEXT/primitives" || { echo "ERROR: primitives/ not found in context '$CONTEXT'"; exit 1; }

# Проверить уникальность slug
if test -f "$FILE"; then
  # Добавить суффикс
  N=2
  while test -f "references/$CONTEXT/primitives/${SLUG}-${N}.md"; do N=$((N+1)); done
  SLUG="${SLUG}-${N}"
  FILE="references/$CONTEXT/primitives/$SLUG.md"
fi

# Создать файл с frontmatter на основе типа
# (поля заполняются агентом на основе пользовательского ввода)
case "$TYPE" in
  Concept)
    cat > "$FILE" << 'TEMPLATE'
---
id: "ID_PLACEHOLDER"
title: "TITLE_PLACEHOLDER"
type: Concept
status: draft
tags: []
context: "CONTEXT_PLACEHOLDER"
created: "DATE_PLACEHOLDER"
updated: "DATE_PLACEHOLDER"
definition: ""
synonyms: []
---

# TITLE_PLACEHOLDER

[определение]
TEMPLATE
    ;;
  # ... аналогично для других типов
esac

echo "Created: $FILE"
```

После создания — автоматический вызов `primitive-validate` для проверки.
