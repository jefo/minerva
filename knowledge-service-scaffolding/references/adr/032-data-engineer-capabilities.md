---
id: adr-032
status: proposed
date: 2026-07-13
supersedes: []
superseded_by: []
tags: [data-engineer, capabilities, design, build, operate, explore, integrity, etl]
based_on: [adr-015, adr-016, adr-018, adr-019, adr-025, adr-026]
---

# ADR-032: Data Engineer Capabilities — Design, Build, Operate, Explore

## Контекст

ADR-019 (Agent Query Model) спроектировал capabilities как интерфейс для LLM-агентов-потребителей: `dim-read`, `cross-reference`, `comparison`, `lineage-trace`. Эти capabilities решают задачу «агент читает warehouse для производства контента».

Но у warehouse есть второй потребитель: **data engineer**. Тот, кто проектирует схему, загружает данные, поддерживает целостность. Его задача — не «прочитай один Fact», а «загрузи 200 Observations из CSV», «проверь что все Facts валидны», «пойми где дыры в данных».

Data engineer работает на других абстракциях:

| Agent-consumer | Data engineer |
|---|---|
| Прочитать Fact + его Dimensions | Загрузить N Facts из источника |
| Сравнить два GPU | Проверить что все Facts ссылаются на существующие Dimensions |
| Пройти lineage от Law к Observation | Понять какие Facts сломаются при изменении Dimension |
| Прочитать определение метрики | Увидеть что 30% GPU не имеют Observations |

Текущие capabilities не покрывают этот профиль. Minerva как платформа (ADR-026) должна обслуживать обоих потребителей.

## Решение

### 1. Четыре capability-класса для Data Engineer

```
minerva/capabilities/
├── warehouse/             # Agent-consumer (ADR-019)
│   ├── dim-read/
│   ├── fact-read/
│   ├── cross-reference/
│   └── scd-version/
├── retrieval/             # Platform (ADR-026)
│   └── structured-search/
├── engineering/           # Data Engineer ← НОВЫЙ КЛАСС
│   ├── design/            # Проектирование схемы
│   ├── build/             # Загрузка данных
│   ├── operate/           # Целостность и мониторинг
│   └── explore/           # Понимание warehouse
└── ...
```

### 2. Design-time capabilities

#### `bus-matrix-validate`

Проверить bus-matrix на внутреннюю состоятельность. Не валидация отдельного Fact (это делает `fact-insert`), а валидация самого контракта.

```
Вход:
  bus_matrix_path: "warehouse/hardware/bus-matrix.yaml"

Проверки:
  - Все mandatory_dimensions каждого fact-типа → существуют в dimensions/
  - Все allowed_measures → имеют definition в definitions/
  - Нет aliases, конфликтующих между fact-типами в рамках одного dimension
  - Grain определён для каждого fact-типа
  - Нет dimension с SCD Type 2, но без scd_key_field
  - Нет циклических ссылок в lineage-правилах (если заданы)

Выход:
  status: PASS | WARN | FAIL
  issues:
    - level: FAIL
      fact_type: observation
      field: mandatory_dimensions.cpu
      message: "Dimension 'cpu' referenced but no dim/ directory exists"
```

#### `dimension-scaffold`

Сгенерировать boilerplate dimension-файла из контракта bus-matrix.

```
Вход:
  domain: hardware
  dimension_type: gpu
  dimension_id: nvidia-rtx-5070

Процесс:
  1. Прочитать bus-matrix → attributes для этого dimension_type
  2. Сгенерировать .yaml с заполненным frontmatter и пустыми значениями атрибутов
  3. SCD-стратегия из bus-matrix → в frontmatter

Выход:
  written: "warehouse/hardware/dim/gpu/nvidia-rtx-5070.yaml"
  frontmatter:
    dimension_type: gpu
    dimension_id: nvidia-rtx-5070
    scd_type: 0
  attributes:
    architecture: null       # ← заполнить
    vendor: nvidia           # ← предзаполнено из id_format
    vram:
      size_gb: null
      type: null
```

Data engineer не пишет YAML с нуля. Он заполняет атрибуты.

#### `schema-evolve`

Мигрировать существующие Facts при изменении bus-matrix контракта. Самая сложная capability.

```
Вход:
  domain: hardware
  fact_type: observation
  change:
    type: add_mandatory_dimension
    dimension: ray_tracing_mode
    migration_strategy: default_value
    default_value: "off"

Процесс:
  1. Обновить bus-matrix: добавить ray_tracing_mode в mandatory_dimensions
  2. Пройти по всем Facts типа observation
  3. Для каждого: добавить ray_tracing_mode = "off" в dimensions
  4. Валидировать все изменённые Facts по новому контракту

Выход:
  facts_modified: 230
  facts_validated: 230
  failed: 0
  bus_matrix_updated: true

Альтернативные migration_strategy:
  - backfill: указать mapping {old_dim_value → new_dim_value}
  - null_until_populated: добавить поле с null, integrity-check покажет как WARN
```

### 3. Build-time capabilities

#### `bulk-import`

Source → Facts с mapping, alias resolution, валидацией и отчётом.

```
Вход:
  source:
    type: csv
    path: "acquisition/sources/techpowerup/gpu-specs-2026-07.csv"
  domain: hardware
  fact_type: metric
  mapping:
    column_mappings:
      - source_column: "GPU"
        target_dimension: gpu
        resolve: alias          # разрешить через bus matrix aliases
      - source_column: "FP32_TFLOPS"
        target_measure: fp32_tflops
      - source_column: "Memory_BW"
        target_measure: bandwidth_gb_s
    static_values:               # значения, не из source
      source_origin: "techpowerup"
      acquisition_date: "2026-07-13"

Процесс:
  1. Прочитать source
  2. Для каждой строки:
     a. Применить column_mappings
     b. Разрешить aliases через bus-matrix (source.gpu → canonical dim ID)
     c. Валидировать по bus-matrix контракту
     d. Определить SCD-стратегию
  3. Записать в warehouse

Выход:
  total_rows: 50
  created: 47
  updated: 12 (SCD Type 2)
  skipped: 3 (duplicates, grain collision)
  failed: 1
  failures:
    - row: 34
      reason: "missing_mandatory_dimension: game_title"
      source_values:
        GPU: "RTX 5060"
```

#### `dry-run`

Тот же `bulk-import`, но без записи в warehouse.

```
Вход: идентичен bulk-import
Выход:
  - тот же отчёт
  - diff: список что изменилось бы (created/updated/deleted)
  - warehouse untouched
```

#### `source-connector`

Скаффолд для нового типа источника. Не загрузка, а подготовка boilerplate.

```
Вход:
  source_type: web_api
  config:
    url: "https://api.steampowered.com/ISteamApps/..."
    auth: "api_key"

Выход:
  - Создан acquisition/sources/steam_api/extract.py (boilerplate)
  - Создан acquisition/sources/steam_api/mapping.yaml (шаблон mapping для bulk-import)
  - Создан acquisition/sources/steam_api/README.md (инструкция)
```

Data engineer заполняет mapping.yaml и запускает `bulk-import`.

### 4. Operate capabilities

#### `integrity-check`

Полный аудит warehouse. Не валидация одного Fact, а cross-cutting проверка всех связей.

```
Проверки:
  1. Fact→Dimension ссылочная целостность:
     Все dimension_refs в Facts указывают на существующие Dimension-файлы
  2. Bus matrix контракт:
     Все mandatory_dimensions присутствуют в каждом Fact
     Все measures есть в allowed_measures
     Нет дубликатов Facts с одинаковым grain
  3. SCD-целостность:
     Нет разрывов в valid_from/valid_to цепочках
     У каждого superseded_by есть встречная ссылка supersedes
  4. Definition-целостность:
     Все definition-ссылки в Facts ведут к существующим файлам
     Definitions без used_in_facts → WARN (мёртвая метрика)
  5. Alias-конфликты:
     Один source-алиас не резолвится в два разных dimension ID
  6. Orphan Dimensions:
     Dimensions без единого Fact → WARN

Выход:
  status: PASS | FAIL
  issues:
    - level: FAIL
      fact: "warehouse/hardware/fact/observations/rtx5060-cp2077-1440p.yaml"
      check: "fact_dimension_integrity"
      message: "dimension_ref 'dim/gpu/rtx-5060.yaml' not found (expected 'nvidia-rtx-5060')"
    - level: WARN
      dimension: "warehouse/hardware/dim/cpu/intel-core-i3-12100f.yaml"
      check: "orphan_dimension"
      message: "No Facts reference this dimension"
  summary:
    total_facts: 324
    total_dimensions: 53
    checks_passed: 8
    checks_failed: 0
    checks_warned: 2
```

#### `stale-report`

Какие данные требуют внимания.

```
Проверки:
  - Stale Facts: Facts без обновления > N дней (default: 90)
  - Unused Dimensions: Dimensions без Facts
  - Dead Definitions: Definitions без used_in_facts
  - SCD gaps: SCD Type 2 цепочки с истёкшим valid_to без преемника
  - Low-coverage Dimensions: dimensions с < 10% Fact-покрытием

Выход:
  ranked_issues:           # упорядочены по severity
    - severity: HIGH
      type: scd_gap
      dimension: "driver_version/572.16"
      message: "valid_to=2026-06-01, no successor. Facts referencing this driver are orphaned in time"
    - severity: MEDIUM
      type: low_coverage
      dimension_type: gpu
      coverage: "14/47 (30%)"
      message: "33 GPUs have no observations"
  summary:
    total_issues: 7
    high: 1
    medium: 3
    low: 3
```

#### `impact-analysis`

Перед изменением: «что сломается?»

```
Вход:
  target: "warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml"
  change: "delete" | "rename" | "modify_attributes"

Выход:
  affected:
    facts:
      count: 23
      paths: [...]           # первые 10, остальные — count
    data_marts:
      count: 3
      names: [coverage, competitive, engineering]
    artifacts:
      count: 1
      paths: ["artifacts/rtx-5060-review.md"]
    bus_matrix_aliases:
      count: 2
      aliases: ["RTX 5060", "5060"]
    lineage_edges:
      count: 47             # рёбра DAG, проходящие через этот dimension
  cascade_depth: 3           # Fact → Data Mart → Artifact
  estimated_fix_time: "manual review: ~23 files"
```

### 5. Explore capabilities

#### `domain-overview`

Статистика домена одним взглядом. Data engineer не хочет читать 50 YAML-файлов.

```
Вход:
  domain: hardware

Выход:
  dimensions:
    - type: gpu
      count: 47
      scd_type_0: 45
      scd_type_2: 2 (driver_version)
      last_updated: "2026-07-12"
    - type: game_title
      count: 12
    - type: resolution
      count: 4
    - type: graphics_preset
      count: 4
    - type: driver_version
      count: 8
    - type: cpu
      count: 6
  fact_types:
    - type: observation
      count: 230
      last_updated: "2026-07-12"
      dimensions_used: [gpu, game_title, resolution, graphics_preset, driver_version]
    - type: metric
      count: 94
      last_updated: "2026-06-30"
      dimensions_used: [gpu]
  definitions:
    count: 3
    names: [average-fps, 1%-low-fps, frame-generation]
  freshness:
    facts_older_than_30d: 2
    facts_older_than_90d: 0
  integrity:
    last_check: null           # integrity-check не запускался
    issues_known: null
```

#### `fact-distribution`

Как данные распределены по dimensions.

```
Вход:
  domain: hardware
  fact_type: observation

Выход:
  by_dimension:
    gpu:
      "nvidia-rtx-5060": 34
      "nvidia-rtx-4060": 28
      "nvidia-rtx-5070": 22
      ... (топ-10, остальные — grouped)
    resolution:
      "1440p": 82
      "1080p": 45
      "4K": 31
    graphics_preset:
      "High": 67
      "Ultra": 52
      "Medium": 23
  coverage:
    gpu: "14/47 (30%)"
    game_title: "10/12 (83%)"
  gaps:
    - dimension: gpu
      uncovered: [nvidia-rtx-5090, amd-radeon-rx-9070-xt, ...]
      count: 33
```

### 6. Приоритеты реализации

Data engineer capabilities — не «всё сразу». Приоритет:

| Приоритет | Capability | Почему |
|---|---|---|
| **P0** | `bulk-import` + `dry-run` | Без этого data engineer вручную пишет YAML. Сразу разблокирует ETL |
| **P0** | `integrity-check` | Сейчас ноль гарантий целостности. Первый же bulk-import выявит проблемы |
| **P1** | `bus-matrix-validate` | Контракт должен быть проверен до загрузки данных |
| **P1** | `domain-overview` | Data engineer должен видеть warehouse целиком |
| **P2** | `impact-analysis` | Нужно когда warehouse >100 Facts |
| **P2** | `stale-report` | Нужно когда данные живут >30 дней |
| **P3** | `schema-evolve` | Нужно при первом breaking change bus-matrix |
| **P3** | `dimension-scaffold` | Экономия 2 минут на boilerplate — приятно, не критично |
| **P3** | `source-connector` | Имеет смысл при 3+ типах источников |

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Data engineer работает напрямую с YAML-файлами | Ноль затрат на разработку capabilities. Полный контроль | Ручная работа: integrity, валидация, отчёты — всё в голове. Не масштабируется за пределы одного инженера | Minerva — платформа. Платформа без tooling для оператора — не платформа |
| Data engineer использует внешние инструменты (dbt, Great Expectations) | Зрелые, проверенные инструменты | Другой интерфейс: SQL/models, не файлы. Агентам всё ещё нужны файлы. Два источника правды | Держать синхронизацию между внешним tool и warehouse — источник ошибок |
| Data engineer capabilities = agent-consumer capabilities | Простота: один класс capabilities | Разные профили: агент читает один Fact, data engineer оперирует сотнями | Перегрузка агентских capabilities инженерной логикой |

## Последствия

**Что нужно создать:**
- `capabilities/engineering/` с четырьмя подкатегориями: design, build, operate, explore
- Каждый capability — SKILL.md с контрактом (вход/выход) как в ADR-019
- `integrity-check` как первый implemented capability (даже до bulk-import — сначала аудит существующего warehouse)

**Что становится проще:**
- Data engineer загружает 200 Facts одной командой, а не 200 вызовами `fact-insert`
- Целостность warehouse проверяется до того как агенты начнут читать битые данные
- Схема эволюционирует без ручной правки сотен файлов

**Что требует дисциплины:**
- Data engineer capabilities используют bus-matrix как SSOT валидации — bus-matrix должна быть актуальной
- Каждый `bulk-import` обязан пройти `integrity-check` после. Без этого — technical debt в данных
- Capabilities инженерные ≠ capabilities агентские. Не смешивать: агент вызывает `dim-read`, data engineer — `integrity-check`
