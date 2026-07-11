---
name: view-define
type: capability
tier: 2
skill: minerva
status: active
contract:
  input: "context + title + список секций (упорядоченный)"
  output: "путь к созданному View .md — аналитической схеме без контента"
based_on: [adr-002, adr-011]
---

# View Definition

Создать View — аналитическую схему. View не содержит фактов, только структуру: из каких секций состоит анализ, в каком порядке.

## Контракт

**Вход:**
- `context` — bounded context
- `title` — название View
- `sections` — упорядоченный список названий секций (минимум 2)
- `tags` — теги

**Выход:**
- Путь: `references/{context}/views/{slug}.md`
- Frontmatter с массивом секций
- Markdown-тело с описанием назначения View и кратким комментарием к каждой секции

## Правила

1. **Минимум 2 секции.** Одна секция — не схема анализа.
2. **Порядок важен.** Секции идут в порядке, в котором они появляются в Artifact.
3. **Секции — это заголовки, не контент.** «Architecture» — валидная секция. «Архитектура GB205: 6144 CUDA Cores...» — невалидная (это уже контент Artifact).
4. **View не ссылается на конкретные Modules или Primitives.** View — это схема, не композиция. Ссылки на конкретные сущности — в Artifact.
5. **Один View может использоваться многими Artifacts.** GPU Analysis View → RTX 5070 Review, RTX 5060 Review, RX 9070 XT Review.

## Frontmatter-схема

```yaml
---
id: "coffee-brewing-method-analysis"
title: "Brewing Method Analysis"
type: View
status: draft
tags: [coffee, analysis]
context: "coffee"
sections:
  - "Principle"
  - "Equipment"
  - "Parameters"
  - "Technique"
  - "Taste Profile"
  - "Recommendations"
created: "2026-07-11"
updated: "2026-07-11"
---

# Brewing Method Analysis

[Назначение View: для каких типов Artifacts предназначена эта схема.
Что должен покрыть каждый раздел.]

## Секции

1. **Principle** — физический принцип метода заваривания
2. **Equipment** — необходимое оборудование
3. **Parameters** — ключевые параметры и их оптимальные значения
4. **Technique** — пошаговая техника
5. **Taste Profile** — ожидаемый вкусовой профиль
6. **Recommendations** — для кого этот метод, с чем сочетается
```

**Обязательные поля:** `sections` (массив минимум из 2 строк)
