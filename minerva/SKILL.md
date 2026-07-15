---
name: minerva
description: "Minerva — мета-скилл: фабрика Agent-Native Data Warehouse. Scaffolding DWH-skills, эталонные контракты, compile-context-map. Consumer начинает с context-map, а не с fs-структуры."
contract:
  in: "Запрос на создание DWH для домена X или запрос данных из существующего DWH"
  out: "Scaffolded DWH-skill или данные через context-map + capabilities"
domains:
  - id: hardware
    bus_matrix: "warehouse/hardware/bus-matrix.yaml"
    context_map: "references/context-map.yaml"
    description: "PC-железо: GPU, CPU, игры, бенчмарки. 759 observation, 148 entities, 2 Laws."
capabilities:
  scaffolding:
    - id: "warehouse/scaffold-warehouse"
      contract: "Создать новый DWH-skill из шаблона. in: domain, domain_title, description → out: skill warehouse-{domain}"
  warehouse:
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
    - id: "warehouse/compile-context-map"
      contract: "Сгенерировать context-map.yaml из данных склада. in: domain → out: references/context-map.yaml"
  analysis:
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

# Minerva — Фабрика Agent-Native Data Warehouse

## Две роли

**Как мета-скилл (scaffolding).** Minerva порождает самодостаточные DWH-skills. Архитектор говорит: «создать склад для домена X» → Minerva выдаёт готовый DWH-skill со структурой, контрактами, compile-context-map. Процесс одноразовый для каждого домена.

**Как shared lib (references).** Consumer внутри DWH-skill использует контракты Minerva как эталон — но они уже скопированы в DWH при scaffolding. Consumer не знает о Minerva.

## Consumer workflow (как найти данные)

Раньше: consumer должен был знать fs-структуру — `warehouse/hardware/fact/observations/`. Это хрупко.

Теперь:

```
1. skill_view('minerva')
   → SKILL.md: «hardware-DWH: 759 obs, 148 entities, 2 Laws. Карта — references/context-map.yaml»
   → linked_files: [references/context-map.yaml, references/contracts/...]

2. skill_view('minerva', file_path='references/context-map.yaml')
   → Полный индекс: все GPU/CPU, игры, разрешения, законы
   → Consumer видит: «12 GPU, 28 CPU, 439 GPU obs + 320 CPU obs, игры от CS2 до Cyberpunk»

3. Consumer выбирает нужное — например, хочет comparison RTX 5060 vs RTX 4060:
   → capability 'analysis/comparison' уже доступен внутри DWH
```

**Consumer не знает о fs-структуре.** Он читает context-map → находит нужный capability → получает данные.

## Как устроен DWH

```
warehouse/{domain}/
├── bus-matrix.yaml        ← контракт домена: dimensions, facts, aliases
├── definitions/           ← семантика метрик
├── dim/{type}/{id}.yaml   ← Dimensions: сущности с атрибутами
└── fact/{type}/{id}.yaml  ← Facts: измерения. Source-значения → bus matrix → dim_id

marts/{domain}/
├── laws/                  ← Инженерные закономерности (с lineage)
└── patterns/              ← Повторяющиеся структуры

references/
└── context-map.yaml       ← АВТОГЕНЕРИРУЕМЫЙ индекс всего склада
```

**Context-map — автогенерируемый.** После любого изменения данных — `compile-context-map`. Consumer всегда видит актуальную картину.

## Ключевые архитектурные решения

- **Source Layer (ADR-025).** Fact хранит сырые source-значения, не dim_id. Резолвинг через bus matrix aliases — при чтении.
- **Fact-insert — единственная точка записи.** Валидация: mandatory dimensions, allowed measures, provenance (source_url).
- **Marts — Derived Layer.** Laws/Patterns с lineage до исходных observation. lineage-trace раскручивает цепочку.
- **Contract-based.** Dimension/Fact/SCD — инварианты, агент self-enforces. Capabilities — сложная оркестрация.
