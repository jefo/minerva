---
id: adr-016
status: accepted
date: 2026-07-11
supersedes: [adr-002, adr-004]
superseded_by: []
tags: [data-model, dimensional-modeling, schemas, scd, bus-matrix, facts, dimensions]
based_on: [adr-014, adr-015]
---

# ADR-016: Data Model — dimensional schemas, SCD, Bus Matrix

## Контекст

ADR-015 определил Dimensional Modeling как модель данных. Теперь нужно определить конкретные схемы: что значит быть Dimension, Fact, как работает SCD, как устроен Bus Matrix.

ADR-002 (Five-level hierarchy) и ADR-004 (Primitive types) спроектированы для Atomic Design — композиционной витрины, не для warehouse. Они заменяются DW-моделью.

## Решение

### 1. Две фундаментальные сущности

Warehouse знает только два типа сущностей. Все остальное — производное:

| Сущность | Назначение | Пример | Хранится |
|---|---|---|---|
| **Dimension** | Описательный атрибут. Отвечает на «что», «кто», «где», «когда» | Конкретная GPU-карта, игра, драйвер, разрешение | `warehouse/{domain}/dim/` |
| **Fact** | Измеряемая величина. Отвечает на «сколько» | FPS в конкретной игре, FP32 TFLOPS, цена | `warehouse/{domain}/fact/` |

Правило: Fact ссылается на Dimensions. Dimension НЕ ссылается на Facts. Dimension может ссылаться на другие Dimensions (иерархия: GPU → Архитектура → Производитель).

### 2. Dimension schema

```yaml
# warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml
---
dimension:
  id: "nvidia-rtx-5060"              # уникальный slug
  type: "gpu"                         # подтип dimension'а (gpu, cpu, game_title, driver_version, ...)
  canonical_name: "NVIDIA GeForce RTX 5060 8GB"
  aliases: ["RTX 5060", "5060"]
  scd_type: 0                         # 0 = immutable, 1 = overwrite, 2 = track history

attributes:                           # описательные атрибуты (НЕ измерения — измерения в Facts)
  vendor: "nvidia"
  architecture: "Blackwell"
  lithography: "TSMC 5nm"
  vram:
    size_gb: 8
    type: "GDDR7"
    bus_width_bit: 128
    bandwidth_gb_s: 355
  compute:
    cuda_cores: 3840
    rt_cores: 30
    tensor_cores: 120
    generation: 5
  clock:
    boost_ghz: 2.50
  power:
    tdp_w: 150
    connector: "1× 8-pin"
  interface:
    pcie: "5.0 x8"
  software:
    upscaler: "DLSS 4"
    frame_gen: "MFG 4×"
    encoder: "NVENC Gen 9"

relationships:                        # ссылки на другие Dimensions (иерархия)
  architecture_ref: "dim/gpu_architecture/blackwell.yaml"
  vendor_ref: "dim/vendor/nvidia.yaml"

meta:
  source: "NVIDIA ARK — RTX 5060 Specifications"
  source_url: "https://www.nvidia.com/en-us/geforce/graphics-cards/rtx-5060/"
  acquired_at: "2026-07-11"
  acquired_by: "acquisition/nvidia-ark-connector"
```

**Правила Dimension:**
- `id` — уникален в пределах контекста. Формат: `{vendor}-{model}` для GPU, `{slug}` для остальных
- `attributes` — только описательные поля. Никаких измерений (FPS, TFLOPS) — это Facts
- `scd_type` — обязателен. Определяет стратегию изменений (см. секцию 3)
- `relationships` — только ссылки на другие Dimensions. Не на Facts

### 3. SCD (Slowly Changing Dimensions)

| SCD Type | Стратегия | Когда применять | Файловая реализация |
|---|---|---|---|
| **Type 0** — immutable | Никогда не менять. При изменении — это новый Dimension | Architecture generation, lithography, vendor | Без изменений. При «Blackwell 2» → новый файл `blackwell-2.yaml` |
| **Type 1** — overwrite | Перезаписать атрибут. История не важна | MSRP, рыночная цена | Git-history хранит предыдущее значение. Файл перезаписывается |
| **Type 2** — track history | Создать новую версию Dimension. Старая сохраняется | Observations при смене драйвера, FPS при патче игры | Заголовочный файл + файлы-версии (см. ниже) |

**SCD Type 2 — файловая реализация:**

```
warehouse/hardware/dim/driver_version/
├── nvidia-geforce-572.16.yaml            # заголовочный файл: current version pointer
├── nvidia-geforce-572.16_v2026-03.yaml   # версия: март 2026
├── nvidia-geforce-572.42_v2026-04.yaml   # версия: апрель 2026
└── nvidia-geforce-575.10_v2026-06.yaml   # версия: июнь 2026 (current)
```

Заголовочный файл:
```yaml
---
dimension:
  id: "nvidia-geforce-572.16"
  type: "driver_version"
  scd_type: 2
  current_version: "nvidia-geforce-572.16_v2026-06"   # указатель на актуальную версию
  versions:
    - {file: "nvidia-geforce-572.16_v2026-03", date: "2026-03", changes: "Initial release"}
    - {file: "nvidia-geforce-572.42_v2026-04", date: "2026-04", changes: "RTX 5060 support, DLSS 4 optimization"}
    - {file: "nvidia-geforce-575.10_v2026-06", date: "2026-06", changes: "Cyberpunk 2077 perf fix, +3 FPS"}

attributes:                             # атрибуты актуальной версии
  branch: "GeForce Game Ready"
  supports_gpus: ["nvidia-rtx-5060", "nvidia-rtx-5070", "..."]
```

Файл-версия (`nvidia-geforce-575.10_v2026-06.yaml`):
```yaml
---
dimension_version:
  parent_id: "nvidia-geforce-575.10"
  version_id: "nvidia-geforce-575.10_v2026-06"
  date: "2026-06"
  changes: "Cyberpunk 2077 perf fix, +3 FPS average"
```

**Почему файлы-версии, а не append-only YAML:** агент, читающий заголовочный файл, видит список версий. Может загрузить конкретную версию по ссылке. Git-friendly: каждая версия — отдельный коммит.

### 4. Fact schema

#### 4.1 Observation (Fact: событие)

```yaml
# warehouse/hardware/fact/observations/rtx5060-cp2077-1440p-driver572.yaml
---
fact:
  id: "rtx5060-cp2077-1440p-high-driver572"
  type: "observation"

dimensions:                           # ССЫЛКИ на Dimensions — контекст измерения
  gpu: "dim/gpu/nvidia-rtx-5060.yaml"
  game: "dim/game_title/cyberpunk-2077.yaml"
  resolution: "dim/resolution/1440p.yaml"
  preset: "dim/graphics_preset/high.yaml"
  driver: "dim/driver_version/nvidia-geforce-572.16.yaml"           # именно версия, не заголовочный
  cpu: "dim/cpu/intel-core-ultra-5-225f.yaml"

measures:                             # измеряемые величины
  fps_avg: 68
  fps_1pct_low: 52
  fps_0_1pct_low: 41
  frametime_ms_avg: 14.7

conditions:                           # условия измерения
  upscaler: "DLSS 4 Quality"
  frame_gen: false
  ray_tracing: "High"

meta:
  confidence: 0.95                   # 0.0–1.0
  confidence_basis: "user_verified"  # user_verified | cross_ref_2sources | single_source | estimated
  observed_at: "2026-03"
  observed_by: "acquisition/user-benchmark-import"
  source_url: "https://..."

lineage:                              # опционально на уровне Fact: если Fact — результат сравнения
  derived_from: []                    # первичный Observation → пусто
```

#### 4.2 Metric (Fact: additive величина)

```yaml
# warehouse/hardware/fact/metrics/rtx5060-fp32.yaml
---
fact:
  id: "rtx5060-fp32"
  type: "metric"

dimensions:
  gpu: "dim/gpu/nvidia-rtx-5060.yaml"
  metric_type: "dim/metric_type/fp32_tflops.yaml"

measures:
  value: 15.1
  unit: "TFLOPS"

meta:
  confidence: 1.0
  confidence_basis: "manufacturer_spec"
  source: "NVIDIA ARK — RTX 5060 Specifications"
  source_url: "https://..."
```

#### 4.3 Law (Derived Fact)

Law — не хранится в Warehouse. Это производный элемент в Data Marts. Но его схема определена здесь для полноты модели.

```yaml
# marts/engineering/laws/gddr7-bandwidth-compensation.yaml
---
derived_fact:
  id: "gddr7-bandwidth-compensation"
  type: "law"

statement: >
  GDDR7 на 128-битной шине даёт bandwidth (355 GB/s), сравнимый с
  GDDR6X на 192-битной (504 GB/s; 2.63 GB/s на бит у GDDR7 vs
  2.63 GB/s на бит у GDDR6X). Это позволяет NVIDIA экономить на
  bus width без потери пропускной способности в xx60-классе.

applies_to_dimensions:               # к каким Dimensions применим
  - "dim/gpu/nvidia-rtx-5060.yaml"
  - "dim/gpu/nvidia-rtx-5060-ti.yaml"
  - "dim/gpu/nvidia-rtx-5070.yaml"

lineage:                              # DAG — см. ADR-017
  nodes:
    - {ref: "fact/observations/rtx5060-cp2077-1440p-driver572.yaml", role: "evidence"}
    - {ref: "fact/metrics/rtx5060-fp32.yaml", role: "evidence"}
    - {ref: "fact/observations/rtx4060-cp2077-1440p-driver546.yaml", role: "baseline"}
    - {ref: "fact/observations/rtx4070-cp2077-1440p-driver546.yaml", role: "reference"}
  edges:
    - {from: "rtx5060-cp2077-1440p-driver572", to: "gddr7-bandwidth-compensation", type: "supports"}
    - {from: "rtx4060-cp2077-1440p-driver546", to: "gddr7-bandwidth-compensation", type: "supports"}
    - {from: "rtx4070-cp2077-1440p-driver546", to: "gddr7-bandwidth-compensation", type: "supports"}

meta:
  confidence: 0.85
  discovered_at: "2026-07-11"
  discovered_by: "cross-source-synthesis"
```

### 5. Bus Matrix (Conformed Dimensions)

```yaml
# warehouse/bus-matrix.yaml
---
bus_matrix:
  domains:
    hardware:
      dimensions:
        gpu:
          canonical_dim: "dim/gpu/{id}.yaml"
          id_format: "{vendor}-{model}"
          used_in_marts: [coverage, engineering, competitive, narrative, compatibility]

        game_title:
          canonical_dim: "dim/game_title/{slug}.yaml"
          id_format: "{slug}"
          aliases:                           # acquisition распознаёт эти имена
            - "CP2077 → cyberpunk-2077"
            - "Cyberpunk → cyberpunk-2077"
            - "AW2 → alan-wake-2"
          used_in_marts: [coverage, competitive]

        driver_version:
          canonical_dim: "dim/driver_version/{vendor}-{branch}-{version}.yaml"
          id_format: "{vendor}-{branch}-{version}"
          used_in_marts: [coverage, engineering]

        resolution:
          canonical_dim: "dim/resolution/{value}.yaml"
          canonical_values: ["1080p", "1440p", "4K"]
          used_in_marts: [coverage, engineering, competitive]

        graphics_preset:
          canonical_dim: "dim/graphics_preset/{slug}.yaml"
          canonical_values: ["low", "medium", "high", "ultra", "rt-overdrive"]
          used_in_marts: [coverage]

    coffee:
      dimensions:
        origin:
          canonical_dim: "dim/origin/{country}.yaml"
          used_in_marts: [tasting, sourcing]
        variety:
          canonical_dim: "dim/variety/{slug}.yaml"
          used_in_marts: [tasting]
        roast_level:
          canonical_dim: "dim/roast_level/{slug}.yaml"
          canonical_values: ["light", "medium-light", "medium", "medium-dark", "dark"]
          used_in_marts: [tasting, brewing]
```

**Правила Bus Matrix:**
- **SSOT имён.** Если Data Mart хочет использовать game_title, он использует `canonical_dim` путь. Никаких «CP2077» напрямую
- **Aliases — для acquisition, не для Data Marts.** Когда Acquisition парсит «CP2077», он резолвит через Bus Matrix в `game_title/cyberpunk-2077.yaml`
- **Новый Dimension → обязательная регистрация в Bus Matrix.** Без этого Data Marts не узнают о его существовании

### 6. Контраст с ADR-002/ADR-004 (PoC)

| Было (ADR-002/004) | Стало (ADR-016) | Причина |
|---|---|---|
| 6 типов Primitives | 2 типа сущностей (Fact, Dimension) + derived (Law) | Primitive types смешивали данные (Specification) и интерпретации (Law). DW разделяет: данные в Warehouse, интерпретации в Data Marts |
| Concept, Specification, Relation | Dimensions (с иерархией) | Все три — описательные атрибуты. Разные подтипы Dimension, а не разные типы сущностей |
| Observation, Metric | Facts (с подтипами) | Оба — измерения. Разные подтипы Fact |
| Law | Derived Fact (в Data Marts, не в Warehouse) | Law — не первичные данные. Это вывод. Хранится в Data Marts |
| `derived_from` (плоский список) | `lineage:` DAG (см. ADR-017) | Плоский список не различает «это исходный Fact» и «это промежуточный вывод» |

## Что НЕ фиксируем

- **Полный перечень Dimension-подтипов.** GPU, CPU, Game Title, Driver Version — это hardware-контекст. Coffee будет иметь свои. Подтипы определяются доменом
- **Формат значений в measures.** FPS = number, но другие метрики могут быть строками, массивами, диапазонами. Схема Fact не диктует тип values
- **Индексацию/поиск по Warehouse.** capability `cross-reference` решает это. Физическая индексация — implementation detail

## Последствия

**Что становится проще:**
- **Модель данных тривиальна.** Две сущности. Агент, читающий `warehouse/`, мгновенно понимает: `dim/` = описания, `fact/` = измерения
- **SCD — встроен в модель, не в реализацию.** `scd_type` в frontmatter определяет поведение при изменении. Агент знает где искать исторические версии
- **Bus Matrix — машиночитаемый контракт.** Агент, загружающий `bus-matrix.yaml`, знает все Dimensions и их canonical-имена
- **Domain isolation.** hardware/dim/ и coffee/dim/ имеют разные подтипы. Никакого конфликта

**Что требует внимания:**
- **SCD Type 2 не должен разрастись.** Каждый драйвер = новая версия? Или только значимые изменения? Критерий: «изменились ли Observations, использованные в активных Laws?»
- **Bus Matrix — living document.** Каждый новый Dimension → регистрация. Без дисциплины матрица устаревает
- **Dimension vs Fact — граница.** «TDP: 150W» — это Dimension (атрибут карты) или Fact (измерение)? Правило: если значение стабильно и получено от производителя → Dimension. Если измерено в тесте и может меняться → Fact
