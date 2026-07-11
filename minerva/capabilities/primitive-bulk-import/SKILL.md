---
name: primitive-bulk-import
type: capability
tier: 1
skill: minerva
status: scaffolding
contract:
  input: "structured source (JSON/YAML/CSV) + context + type"
  output: "N созданных Primitives с отчётом: создано, пропущено, ошибки"
based_on: [adr-004, adr-011]
---

# Primitive Bulk Import

Массовое создание Primitives из structured source.

## Контракт

**Вход:**
- Источник: JSON/YAML/CSV с массивом записей
- `context` — куда импортировать
- `type` — тип всех импортируемых Primitives (однородный импорт) ИЛИ поле `type` внутри каждой записи (разнородный)

**Выход:**
- Отчёт: `created: N, skipped: M (duplicates), errors: K`
- Список созданных файлов с путями

## Правила

1. Каждая запись импортируется через `primitive-create`. Не дублировать логику создания.
2. Дубликат определяется по `id`: если файл с таким slug уже существует — skip.
3. При ошибке в одной записи — продолжить импорт остальных, зафиксировать ошибку в отчёте.
4. После импорта — массовый `primitive-validate` всех созданных файлов.
5. Минимальные обязательные поля в source: `title` + тип-специфичные (см. `primitive-create`).

## Поддерживаемые форматы

```json
[
  {
    "title": "Espresso",
    "type": "Concept",
    "definition": "Концентрированный кофейный напиток...",
    "synonyms": ["эспрессо"],
    "tags": ["coffee", "beverage"]
  }
]
```

```yaml
- title: "Extraction Yield"
  type: Metric
  value: 20
  unit: "%"
  formula: "TDS × brew_weight / dose"
  tags: [coffee, extraction]
```
