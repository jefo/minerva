---
name: minerva
description: "Gaming Performance DWH — self-describing knowledge substrate. Any agent loads this skill to understand the world model."
identity: "Файловый Data Warehouse (Kimball dimensional model). Единый источник истины для gaming-бенчмарков."
purpose: "Provide a trustworthy analytical representation of gaming hardware performance."
domain: "PC hardware gaming benchmarks"
ontology:
  entities:
    - "Dimension: описательный атрибут. GPU, CPU, game_title, resolution, graphics_preset, architecture, socket, chipset, driver_version, benchmark_scenario."
    - "Observation: факт замера. Содержит source-значения, measures (fps_avg, fps_1_percent_low), conditions (upscaler, frame_gen)."
    - "Law: производный факт. Инженерная закономерность с lineage до observation."
    - "Pattern: повторяющаяся структура. Слабее Law — кандидат, не доказательство."
  relationships:
    - "Observation → ссылается на Dimensions через source-значения (человеческие имена), не dim_id."
    - "Law → lineage до Observation."
    - "Bus Matrix → SSOT-контракт: какие dimension types, fact types, aliases, validation rules."
architecture:
  layers:
    - "Source Layer: Observation хранит source-значения. Резолвинг → dim_id через bus-matrix aliases при чтении."
    - "Warehouse Layer: dim/ (сущности), fact/ (измерения), bus-matrix.yaml (контракт), definitions/ (семантика метрик)."
    - "Marts Layer: engineering/laws/, engineering/patterns/. Производные данные с lineage."
  index: "context-map.yaml — автогенерируемый индекс. Всегда актуален."
contracts:
  - "Dimension Contract: references/contracts/dimension-contract.md"
  - "Fact Contract: references/contracts/fact-contract.md"
  - "SCD Contract: references/contracts/scd-contract.md"
evolution:
  - "Observation: создаётся через YAML-файл в fact/. source_url обязателен. После создания → compile-context-map."
  - "Dimension: создаётся через YAML-файл в dim/. Регистрируется в bus-matrix с aliases."
  - "Law: promoted из pattern в marts/engineering/laws/. Требует lineage до observation."
  - "Duplicates: запрещены. Observation с идентичными source × game × resolution × preset × driver — дубликат."
  - "Staleness: observation устаревает при смене драйвера/патча игры. Старый не удаляется — помечается stale, создаётся новый."
self_description:
  context_map: "references/context-map.yaml"
  bus_matrix: "warehouse/hardware/bus-matrix.yaml"
  knowledge:
    - "references/ontology.md"
    - "references/mental-models.md"
    - "references/terminology.md"
  contracts: "references/contracts/"
  data: "warehouse/hardware/"
  marts: "marts/"
tools:
  - "compile-context-map: python3 tools/compile-context-map/generate.py --warehouse-root . --output references/context-map.yaml"
---

# Gaming Performance DWH

## What I Am

A file-based dimensional Data Warehouse (Kimball). I store gaming benchmark data for PC hardware: CPUs, GPUs, games, resolutions, presets.

I am a **knowledge substrate**, not an agent. I don't have a mission — I have a purpose. I don't make decisions — I describe the world.

## What I Power (ИгроЛаба)

Minerva — SSOT для 8 доменов фабрики контента:

### Content Production
Writer's Brief, Narrative Arc, review pages. Факты с provenance для писателя.

### GPU Analytics
Understanding Reports (7 sub-agents), Explorer/Detail/Comparator views.
439 GPU observations в DWH.

### Engineering Investigations
Forensic research reports. 15 аналитических линз.
Architectural Tension Discovery, Engineering Narrative Arc.

### PCBO Synthesis
FSM-синтез PC-сборок из 9 состояний. Компоненты → сборка.

### DSS — CPU Comparison
29 CPU profiles × 6 workloads + comparison framework.
Deltas, tradeoff axes, decision boundaries — без вердиктов.

### Competitor Landscape
Advantage/magnitude/boundary per CPU per intent.

### Build Economics (TCO)
9-section analysis: входной билет, структура бюджета, игровое ядро,
ликвидность, риск устаревания, TCO 6 лет. Сравнение стратегий (AM5 vs LGA1700 vs DDR4).
Реальные цены: price.ru, DNS.
См. `marts/build-economics/`

### Lifecycle Prediction
Per-year bottleneck probability с confidence intervals.
Per-genre прогноз (AAA shooter, RTS, city builder, MMO, simulator, esports).
MFG asymmetry model. Platform lifecycle integration.
См. `marts/lifecycle/`

```
warehouse/hardware/
├── bus-matrix.yaml      ← schema contract
├── definitions/         ← metric semantics
├── dim/                 ← 29 CPUs, 10 GPUs, 71 games, ...
└── fact/
    ├── observations/    ← 439 GPU observations
    └── cpu_observations/← 340 CPU observations

marts/engineering/
├── laws/                ← 2 Laws with lineage
└── patterns/

references/
├── context-map.yaml     ← auto-generated index (779 observations, 149 entities)
├── ontology.md          ← entity model
├── mental-models.md     ← coverage, confidence, lineage
├── terminology.md       ← glossary
└── contracts/           ← invariants
```

## How I Evolve

- **Observation added** → YAML in fact/ → compile-context-map → index updated
- **Dimension added** → YAML in dim/ → bus-matrix updated → compile-context-map
- **Law promoted** → YAML in marts/laws/ with lineage
- **Duplicate blocked** → same source × game × resolution × preset × driver = reject
- **Stale observation** → marked stale, new observation created. Old preserved for history.

## How to Read Me

1. `references/context-map.yaml` — what data exists right now
2. `warehouse/hardware/bus-matrix.yaml` — schema, types, aliases
3. `references/contracts/` — invariants

Knowledge: `references/ontology.md`, `mental-models.md`, `terminology.md`.
