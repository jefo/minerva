---
name: minerva
description: "Minerva Data Warehouse — agent-native, файловый DW по Kimball + AI-driven Research. Входная точка: bus matrix + capabilities. LLM ориентируется по fs как по графу."
contract:
  in: "Любой вопрос о данных: сущности, замеры, сравнения, инженерные закономерности"
  out: "Structured data через capabilities. Laws/Patterns — через analysis-возможности"
domains:
  - id: hardware
    bus_matrix: "warehouse/hardware/bus-matrix.yaml"
    description: "PC-железо: GPU, CPU, игры, бенчмарки"
capabilities:
  - id: "warehouse/dim-read"
    contract: "Прочитать Dimension. in: domain, dim_type, dim_id → out: dimension_data"
  - id: "warehouse/bus-lookup"
    contract: "Резолвить source-значение в dim_id. in: domain, dim_type, alias → out: resolved_dim_id"
  - id: "warehouse/cross-reference"
    contract: "Все Facts для Dimension. in: domain, dim_type, dim_id → out: fact_set"
  - id: "warehouse/fact-read"
    contract: "Прочитать Fact с полным контекстом (dimensions + definitions). in: domain, fact_type, fact_id → out: fact_data"
  - id: "warehouse/fact-insert"
    contract: "Создать Fact. in: domain, fact_type, source, measures, meta → out: fact_id. Write. Единственная точка записи."
  - id: "warehouse/coverage-matrix"
    contract: "Матрица покрытия: GPU/CPU × игры × разрешения. in: domain, dim_type → out: coverage_matrix"
  - id: "analysis/comparison"
    contract: "Сравнить два Dimension по метрикам. in: domain, dim_type, dim_a, dim_b, metrics → out: comparison_table"
  - id: "analysis/pattern-promote"
    contract: "Сохранить обнаруженный Law/Pattern. in: domain, derived_type, statement, lineage_nodes, confidence → out: derived_ref. Write."
  - id: "analysis/lineage-trace"
    contract: "Проследить происхождение вывода. in: derived_id, direction(up|down) → out: lineage_tree"
  - id: "analysis/impact-analysis"
    contract: "Найти всё, затронутое изменением observation. in: fact_ref → out: affected_derived_list"
  - id: "analysis/stale-check"
    contract: "Найти устаревшие observation и затронутые Law. in: domain, fact_type → out: staleness_report"
  - id: "analysis/contradiction-detect"
    contract: "Найти observation с одинаковыми dims но разными значениями. in: domain, fact_type → out: contradiction_report"

contracts:
  - id: "dimension-contract"
    path: "references/contracts/dimension-contract.md"
    description: "Инварианты создания/изменения Dimension. Агент self-enforces."
  - id: "fact-contract"
    path: "references/contracts/fact-contract.md"
    description: "Инварианты любого Fact: grain, mandatory dims, source layer, provenance."
  - id: "scd-contract"
    path: "references/contracts/scd-contract.md"
    description: "SCD Type 0 vs Type 2, формат версионирования, связь с lineage."
---

# Minerva — Data Warehouse для ИИ-агентов

## Что это

Agent-native Data Warehouse. Данные в YAML-файлах на файловой системе. Агент читает fs как граф: имена директорий = типы сущностей, имена файлов = id сущностей. Методология — Dimensional Modeling по Kimball.

## Как устроен

```
warehouse/{domain}/
├── bus-matrix.yaml        ← контракт домена. Какие dimensions, facts, aliases, allowed_measures
├── definitions/           ← семантика метрик (average-fps.yaml, ...)
├── dim/{type}/{id}.yaml   ← Dimensions: сущности с атрибутами
└── fact/{type}/{id}.yaml  ← Facts: измерения. Source-значения резолвятся через bus matrix
```

**Bus Matrix — SSOT.** Загрузи `warehouse/{domain}/bus-matrix.yaml` и ты знаешь всё о домене:
- Какие dimension types существуют (gpu, cpu, game_title, socket, architecture, ...)
- Какие fact types существуют (observation, cpu_observation, metric)
- Какие меры допустимы для каждого fact type
- Какие бизнес-правила валидации
- Все aliases для резолвинга source-значений

**Marts — Derived Layer (ADR-017).** Производные данные: Laws, Patterns, Comparisons.
В отличие от Facts (первичные измерения), Marts хранят выводы агента с lineage до исходных observation.
`marts/engineering/laws/` — инженерные закономерности.
`marts/engineering/patterns/` — повторяющиеся структуры.
Агент загружает Law → lineage-trace → видит все observation, на которых Law основан.

**Source Layer (ADR-025).** Fact хранит сырые значения источника (`source.gpu: "RTX 5060"`), не dim_id. Резолвинг через bus matrix aliases — при чтении, не при записи. Fact не знает о структуре dim/.

**Fact-insert — единственная точка записи.** Любой ingest проходит через этот capability. Валидация: mandatory dimensions, allowed measures, бизнес-правила. Разделение: платформа даёт контракт, прикладной слой — данные.

## Как с этим работать

1. Загрузи bus matrix домена. Узнай dimension types, fact types, aliases.
2. Для поиска сущности: `bus-lookup` → `dim-read`.
3. Для поиска замеров: `cross-reference` → `fact-read`.
4. Для сравнения: `comparison`.
5. Для записи: `fact-insert` (dimensions создаются отдельно — пока вручную).
6. **Для инженерного анализа:** `comparison` → обнаружил закономерность → `pattern-promote` → сохранил Law.
7. **Для проверки вывода:** `lineage-trace` → раскрути Law до исходных observation.
8. **При изменении данных:** `impact-analysis` → узнай какие Law нужно перепроверить.
9. Иерархия fs = структура данных. `dim/gpu/` = все GPU. `fact/cpu_observations/` = все замеры CPU. `marts/engineering/laws/` = все Laws.

## Ограничения (текущее состояние)

- **Discovery — через bus matrix.** Нет отдельного каталога. Что в bus matrix — то и существует.
- **Provenance — confidence только.** Source tracing (URL, видео) не структурировано. ADR-017 (lineage DAG) не реализован.
- **Write path — dimensions вручную.** dim-upsert capability отсутствует. Новые сущности создаются прямым созданием файлов.
- **Нет cross-domain queries.** Hardware и другие домены изолированы.
- **Нет SCD Type 2** (кроме одного драйвера). Исторические версии не поддерживаются.
- **Нет freshness.** Stale-check отсутствует. Система не знает что устарело.

## Grounding

- Методология: Dimensional Modeling (Kimball), Bus Matrix, Star Schema
- Source layer: ADR-025 (Observation не знает DIM ID)
- Platform/App split: ADR-026 (платформенные capabilities vs прикладные ingestion-скрипты)
- Agent-native ETL: ADR-029 (один reasoning-проход агента, не staged pipeline)
