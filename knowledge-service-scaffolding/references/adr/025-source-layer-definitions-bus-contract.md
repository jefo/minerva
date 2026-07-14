---
id: adr-025
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [source-layer, definitions, bus-matrix, domain-contract, observation, fact, grain]
based_on: [adr-016, adr-018, observation-004]
---

# ADR-025: Source Layer, Definitions, Bus Matrix Contract

## Контекст

Observation 004 (внешний review) выявил три архитектурных проблемы текущей реализации:

1. **Observation знает DIM ID.** `dimensions.gpu: "dim/gpu/nvidia-rtx-5060.yaml"` — жёсткая связь. Смена структуры dim/ ломает все Facts.
2. **Метрики не определены.** «FPS avg: 68» — что такое avg? Какой инструмент? Какой проход? Через полгода невосстановимо.
3. **Bus Matrix — только имена.** Нет контракта: какие меры допустимы для fact-типа, какая гранулярность.

ADR-016 (Data Model) и ADR-018 (ETL Pipeline) нуждаются в уточнении.

## Решение

### 1. Source Layer — Observation не знает DIM ID

Observation записывает сырые значения источника. Разрешение в DIM ID происходит в `transform-normalize` через Bus Matrix.

**Было (Observation привязан к DIM ID):**

```yaml
dimensions:
  gpu: "dim/gpu/nvidia-rtx-5060.yaml"
  game: "dim/game_title/cyberpunk-2077.yaml"
```

**Стало (Observation содержит сырые значения):**

```yaml
source:
  gpu: "RTX 5060"
  game: "Cyberpunk 2077"
  resolution: "1440p"
  preset: "High"
  driver: "572.16"
```

**Процесс разрешения (transform-normalize):**

```
source.game: "Cyberpunk 2077"
    ↓ bus-matrix alias lookup
canonical: "cyberpunk-2077"
    ↓ dim path template
dimension_ref: "dim/game_title/cyberpunk-2077.yaml"
```

**Что это даёт:**
- Observation — чистый слепок источника. Независим от структуры Warehouse
- Смена dim/-структуры → правим bus-matrix, не трогаем Observations
- Один и тот же Observation может быть загружен в разные warehouses с разной структурой

### 2. Business Definitions

Каждая метрика и её производные имеют определение в `warehouse/definitions/`.

```
warehouse/definitions/
├── average-fps.yaml
├── one-percent-low-fps.yaml
├── frame-time-ms.yaml
├── frame-generation.yaml
└── vram-usage-gb.yaml
```

**Схема definition:**

```yaml
# warehouse/definitions/average-fps.yaml
definition:
  id: "average_fps"
  canonical_name: "Average FPS"
  domain: "gaming_performance"
  description: "Среднее арифметическое количество кадров в секунду по 3 прогонам бенчмарка"
  calculation:
    method: "arithmetic_mean"
    formula: "sum(fps_values) / count(fps_values)"
    unit: "fps"
  measurement:
    tool: "FrameView"
    tool_version: "1.5+"
    passes: 3
    excludes_first_run: true
    warmup_required: true
  interpretation:
    higher_is_better: true
    meaningful_difference: 5
    meaningful_difference_unit: "fps"
    notes: "Разница <5 fps — в пределах погрешности измерения"
  caveats:
    - "Не отражает стабильность (см. 1% low)"
    - "Зависит от сцены бенчмарка (см. определение сцены в игре)"
    - "DLSS/FSR меняет методологию (см. definition upscaled-fps)"
  used_in_facts: ["observation"]
  used_in_marts: ["coverage", "competitive", "engineering"]
```

**Что это даёт:**
- Агент, читающий Observation с `measures.fps_avg: 68`, загружает `definitions/average-fps.yaml` и знает: arithmetic mean, 3 прогона, FrameView, разница <5 fps незначима
- Разные источники (YouTube, TechPowerUp, свои замеры) используют одну методологию. Если нет — разные definitions
- Новый член команды через полгода не гадает «как мы считали FPS»

### 3. Bus Matrix → Domain Contract

Bus Matrix расширяется: для каждого fact-типа определяются обязательные dimensions, допустимые measures, grain.

**Было (только canonical-имена):**

```yaml
dimensions:
  gpu:
    canonical_dim: "dim/gpu/{vendor}-{model}.yaml"
    aliases: ...
```

**Стало (domain contract):**

```yaml
bus_matrix:
  domain: hardware

  dimensions:
    gpu:
      canonical_dim: "dim/gpu/{vendor}-{model}.yaml"
      id_format: "{vendor}-{model}"
      aliases:
        "RTX 5060": "nvidia-rtx-5060"
      scd_default: 0
      attributes:            # ← semantic layer (задел)
        - architecture
        - vendor
        - vram.size_gb
        - vram.type
        - compute.cuda_cores
      used_in_marts: [coverage, engineering, competitive, narrative, compatibility]
    # ... остальные dimensions

  facts:
    observation:
      description: "Единичный замер производительности в игре"
      grain: "single_benchmark_run"
      mandatory_dimensions: [gpu, game_title, resolution, graphics_preset, driver_version]
      optional_dimensions: [cpu]
      allowed_measures:
        - average_fps
        - fps_1_low
        - fps_0_1_low
        - frametime_ms_avg
      measure_definitions:                  # ← ссылки на definitions
        average_fps: "definitions/average-fps.yaml"
        fps_1_low: "definitions/one-percent-low-fps.yaml"
      cardinality:
        per_gpu_per_game_per_preset_per_driver: 1
      validation_rules:
        - "Не может быть двух Observation с одинаковыми mandatory_dimensions"
        - "fps_avg должен быть больше fps_1_low"

    metric:
      description: "Аддитивная метрика (TFLOPS, bandwidth, цена)"
      grain: "single_gpu_spec"
      mandatory_dimensions: [gpu]
      allowed_measures:
        - fp32_tflops
        - bandwidth_gb_s
        - price_rub
```

**Что это даёт:**
- `fact-insert` валидирует Observation: все mandatory dimensions заполнены? Допустимые меры? Нет дубликата с теми же dimensions?
- Агент, планирующий новый fact-тип, проверяет bus-matrix: «можно ли добавить temperature в observation?» → «нет, не в allowed_measures. Создать новый fact-тип thermal_observation»
- Grain — защита от ошибок: «observation имеет grain single_benchmark_run, нельзя аггрегировать до создания comparison»

### 4. Структура warehouse/ после изменений

```
warehouse/
├── bus-matrix.yaml              # domain contract: dimensions + facts + measures + grain
├── definitions/
│   ├── average-fps.yaml
│   ├── one-percent-low-fps.yaml
│   └── frame-generation.yaml
├── sources/                     # acquisition staging
│   ├── youtube/
│   ├── techpowerup/
│   └── manual/
├── hardware/
│   ├── dim/
│   │   ├── gpu/
│   │   ├── game_title/
│   │   ├── resolution/
│   │   ├── graphics_preset/
│   │   ├── driver_version/
│   │   └── cpu/
│   └── fact/
│       ├── observations/        # source: сырые значения, dimensions: разрешены при load
│       └── metrics/
```

## Что НЕ фиксируем

- **Warehouse API (Engine).** Абстракция хранилища (YAML → DuckDB) — когда масштаб потребует. Сейчас файлы
- **Semantic queries.** «Покажи все Blackwell» — когда dimensions получат structured taxonomy
- **OLAP-capabilities.** `aggregate`, `slice`, `drill-down` — после базовых query-capabilities

## Последствия

**Что нужно изменить в текущей реализации:**
- Observation `rtx5060-cp2077-1440p-high-driver572.yaml` → заменить `dimensions:` на `source:` (сырые значения)
- `warehouse-load` → добавить шаг разрешения: `source` → `dimensions` через bus-matrix aliases
- Создать `warehouse/definitions/average-fps.yaml`
- Расширить `bus-matrix.yaml` → facts section с mandatory_dimensions, allowed_measures, grain

**Что становится проще:**
- Меняем структуру dim/ → правим bus-matrix. Observations не трогаем
- Метрики определены раз и навсегда. Definitions — SSOT
- Валидация Fact — автоматическая: bus-matrix как схема

**Что требует дисциплины:**
- Каждая новая метрика → definition. Без definition — невалидна
- Каждый новый fact-тип → регистрация в bus-matrix. Без регистрации — rejected
- Source-значения должны совпадать с aliases в bus-matrix. «CP2077» ≠ «CP 2077»
