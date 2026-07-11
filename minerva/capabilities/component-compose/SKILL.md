---
name: component-compose
type: capability
tier: 2
skill: minerva
status: active
contract:
  input: "context + title + список Primitive ID (минимум 2)"
  output: "путь к созданному Component .md с frontmatter + ссылками на Primitives"
based_on: [adr-002, adr-003, adr-011]
---

# Component Composition

Собрать Component — устойчивую композицию Primitives. Первый уровень, где появляется семантика.

## Контракт

**Вход:**
- `context` — bounded context
- `title` — название Component
- `primitives` — список ID существующих Primitives (минимум 2)
- `tags` — теги (опционально)

**Выход:**
- Путь: `references/{context}/components/{slug}.md`
- Frontmatter со ссылками на Primitives
- Markdown-тело с описанием композиции

## Правила

1. **Минимум 2 Primitives.** Один Primitive — не Component, это сам Primitive.
2. **Все Primitives должны существовать.** Перед созданием — проверить каждый ID через файловую систему.
3. **Primitives должны быть из того же контекста.** Кросс-контекстные ссылки — через context-map (ADR-008), не внутри Component.
4. **Downward visibility:** Component ссылается на Primitives (уровень < 2). Не ссылается на Modules, Views, Artifacts.
5. **Семантика в теле:** markdown-тело объясняет, *почему* эти Primitives вместе образуют осмысленную единицу. Не просто список.
6. **После создания** — валидация: проверить, что все указанные Primitives существуют и доступны.

## Frontmatter-схема

```yaml
---
id: "coffee-brewing-parameters"
title: "Brewing Parameters"
type: Component
status: draft
tags: [coffee, brewing]
context: "coffee"
primitives:
  - "coffee-dose"
  - "coffee-temperature"
  - "coffee-pressure"
  - "coffee-time"
  - "coffee-ratio"
created: "2026-07-11"
updated: "2026-07-11"
---

# Brewing Parameters

[Объяснение: почему Dose + Temperature + Pressure + Time + Ratio образуют
единую систему параметров заваривания, а не пять несвязанных чисел]

## Состав

- **Dose** (coffee-dose): количество кофе
- **Temperature** (coffee-temperature): температура воды
- **Pressure** (coffee-pressure): давление при заваривании
- **Time** (coffee-time): длительность контакта
- **Ratio** (coffee-ratio): соотношение кофе/вода
```

**Обязательные поля:** `primitives` (массив минимум из 2 ID)

## Реализация

```bash
CONTEXT="$1"
TITLE="$2"
shift 2
PRIMITIVE_IDS="$@"  # список ID через пробел

# Проверить минимум 2
COUNT=$(echo "$PRIMITIVE_IDS" | wc -w)
[ "$COUNT" -ge 2 ] || { echo "FAIL: need at least 2 Primitives, got $COUNT"; exit 1; }

# Проверить существование каждого Primitive
for pid in $PRIMITIVE_IDS; do
  FILE="references/$CONTEXT/primitives/${pid}.md"
  test -f "$FILE" || { echo "FAIL: Primitive '$pid' not found at $FILE"; exit 1; }
done

# Создать Component
# (slug, frontmatter, файл — аналогично primitive-create)
```
