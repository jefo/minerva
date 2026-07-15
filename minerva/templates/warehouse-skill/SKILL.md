---
name: warehouse-{domain}
description: "Data Warehouse для домена {domain}: {description}. {dim_count} dimensions, {obs_count} observation, {law_count} Laws. Самодостаточный DWH-skill — consumer начинает с context-map."
contract:
  in: "Запрос данных домена {domain}: сущности, замеры, сравнения, закономерности"
  out: "Структурированные данные через context-map + capabilities"
domain:
  id: {domain}
  description: "{description}"
  context_map: "references/context-map.yaml"
  bus_matrix: "warehouse/{domain}/bus-matrix.yaml"
capabilities:
  warehouse:
    - compile-context-map
    - dim-read
    - bus-lookup
    - cross-reference
    - fact-read
    - fact-insert
    - coverage-matrix
  analysis:
    - comparison
    - pattern-promote
    - lineage-trace
    - impact-analysis
    - stale-check
    - contradiction-detect
contracts:
  - dimension-contract
  - fact-contract
  - scd-contract
---

# Warehouse: {domain_title}

**{description}**

## Как найти данные

```
1. skill_view('warehouse-{domain}')
   → SKILL.md (этот файл): что есть в DWH

2. skill_view('warehouse-{domain}', file_path='references/context-map.yaml')
   → Полный индекс: все сущности, замеры, законы

3. Выбрать нужное:
   → comparison: сравнить две сущности
   → cross-reference: все замеры для сущности
   → lineage-trace: проследить происхождение закона
```

**Consumer не знает о fs-структуре.** Он читает context-map → находит capability → получает данные.

## Структура склада

```
warehouse/{domain}/
├── bus-matrix.yaml        ← контракт домена: dimensions, facts, aliases
├── definitions/           ← семантика метрик
├── dim/{type}/{id}.yaml   ← Dimensions: сущности с атрибутами
└── fact/{type}/{id}.yaml  ← Facts: измерения

marts/{domain}/
├── laws/                  ← Инженерные закономерности (с lineage)
├── patterns/              ← Повторяющиеся структуры
└── comparisons/           ← Результаты сравнений

references/
├── context-map.yaml       ← АВТОГЕНЕРИРУЕМЫЙ индекс склада
└── contracts/             ← Контракты Dimension, Fact, SCD
```

## Ключевые правила

1. **Fact-insert — единственная точка записи.** Валидация по bus-matrix.
2. **Source Layer.** Fact хранит source-значения, не dim_id. Резолвинг через bus-lookup.
3. **Lineage — обязательно.** Law → observation → source_url.
4. **Context-map — автогенерируемый.** После любого изменения → compile-context-map.
5. **Provenance.** source_url обязателен в каждом observation.

## Возможности (capabilities)

### Складские
| Capability | Что делает |
|---|---|
| `compile-context-map` | Перегенерировать индекс склада |
| `dim-read` | Прочитать dimension по id |
| `bus-lookup` | Найти dimension по названию |
| `cross-reference` | Все замеры для сущности |
| `fact-read` | Прочитать замер с контекстом |
| `fact-insert` | Добавить observation |
| `coverage-matrix` | Матрица покрытия: сущность × игра × разрешение |

### Аналитические
| Capability | Что делает |
|---|---|
| `comparison` | Сравнить две сущности по метрикам |
| `pattern-promote` | Сохранить обнаруженный закон |
| `lineage-trace` | Проследить observation → law |
| `impact-analysis` | Что затронет изменение данных |
| `stale-check` | Найти устаревшие observation |
| `contradiction-detect` | Найти конфликтующие замеры |

## Создан

Scaffolded Minerva {version} на {date}. Обновление структуры — `maintain-warehouse` в Minerva.
