---
id: adr-031
status: accepted
date: 2026-07-14
accepted: 2026-07-14
tags: [cpu, warehouse-model, entities, relationships, master-data, engineering-lab]
based_on: [adr-016, adr-025, adr-026, adr-030]
---

# ADR-031: CPU Data Model — Warehouse Model для инженерной лаборатории

## Контекст

ADR-030 зафиксировал CPU как критический data debt: 0 dimensions, 0 entities, 0 связей. Warehouse знает о видеокартах, но не о процессорах.

Но «добавить CPU» — недостаточно. Нужно понять: **какая модель данных нужна инженерной лаборатории, а не читателю.** Читателю нужен ответ «какой CPU купить». Лаборатории нужно понимать архитектурные решения, находить паттерны между поколениями, сопоставлять design tradeoffs.

Консультант определил Слой 5 (Warehouse Model) как «сущности и связи. DW знает что существует, но не знает что лучше.» Это правильная граница: мы строим слой фактов о процессорах, не слой выводов о них.

## Решение

### 1. Отличие CPU от GPU — почему нельзя copy-paste модель

GPU-модель (ADR-016) построена вокруг gaming performance: фиксированный CPU + варьируемый GPU → FPS в играх. Эта модель работает для GPU потому что:
- В 1440p/4K сцена практически всегда GPU-bound
- Главная метрика — average FPS
- Конкуренты определяются ценовой категорией

CPU принципиально иначе:
- Сценарий определяет bound: 1080p Low → CPU-bound, Cinebench → all-core MT, Factorio → cache-sensitive ST
- Главных метрик несколько: ST perf, MT perf, gaming FPS (1080p), efficiency (perf/W), platform cost
- Конкуренты определяются не только ценой, но и сокетом, платформой, апгрейд-путём

→ CPU требует более богатой модели сущностей и связей, чем GPU. Особенно важны связи: CPU → Socket → Chipset → Motherboard, CPU → Architecture → Microarchitecture.

### 2. Сущности (Entities)

#### 2.1 CPU

Процессор как продукт. Центральная сущность.

```yaml
dimension:
  id: "amd-ryzen-7-7800x3d"
  type: "cpu"
  canonical_name: "AMD Ryzen 7 7800X3D"
  aliases: ["7800X3D", "R7 7800X3D"]
  scd_type: 0
attributes:
  vendor: "amd"
  family: "Ryzen 7"
  generation: 7000
  architecture: "zen-4"           # → Architecture entity
  socket: "am5"                   # → Socket entity
  lithography: "TSMC 5nm"
  compute:
    cores: 8
    threads: 16
    base_clock_mhz: 4200
    boost_clock_mhz: 5000
    boost_clock_single_core_mhz: 5050
  cache:
    l1_kb: 512                    # 8 × 64KB L1I + 8 × 32KB L1D, здесь суммарно
    l2_kb: 8192                   # 8 × 1024KB
    l3_kb: 98304                  # 96MB (32MB CCD + 64MB 3D V-Cache)
    l3_type: "3d-v-cache"         # stacked | standard
  memory:
    type: "DDR5"
    max_official_speed_mt_s: 5200
    channels: 2
    ecc_support: false
  pcie:
    version: "5.0"
    lanes: 28                     # usable lanes
  graphics:
    integrated: true
    igpu_model: "RDNA 2 (2 CUs)"
  power:
    tdp_w: 120
    ppt_w: 162                    # Package Power Tracking
    tjmax_c: 89
  release:
    date: "2023-04-06"
    msrp_usd: 449
  platform:
    overclocking:
      cpu_ratio: true
      memory: true
      pbo: true
```

**Принципы атрибутов:**
- **Измеряемые величины — числа с единицами.** Не «большой кэш», а `l3_kb: 98304`.
- **Провалы данных — явные.** Если неизвестна максимальная частота памяти — поле отсутствует, не «скорее всего 5200».
- **Vendor-specific — в отдельных полях.** `tdp_w` vs `ppt_w` (Intel vs AMD power limits). Не нормализуем под общий знаменатель — теряем инженерную точность.
- **SCD Type 0** для большинства CPU. SCD Type 2 — только если меняются спецификации (stepping, ревизия).

#### 2.2 Socket

Физический интерфейс. Привязывает CPU к платформе.

```yaml
dimension:
  id: "am5"
  type: "socket"
  canonical_name: "Socket AM5 (LGA 1718)"
  aliases: ["AM5"]
  scd_type: 0
attributes:
  vendor: "amd"
  type: "LGA"
  pin_count: 1718
  release_year: 2022
  compatible_memory: ["DDR5"]
  predecessor: "am4"             # → Socket entity
  platform_lifespan:
    promised_until_year: 2027
    current_status: "active"     # active | mature | eol
```

#### 2.3 Architecture / Microarchitecture

Архитектурное поколение. Самая важная сущность для инженерной лаборатории: именно здесь живут design decisions.

```yaml
dimension:
  id: "zen-4"
  type: "architecture"
  canonical_name: "AMD Zen 4"
  aliases: ["Zen 4", "Zen4"]
  scd_type: 0
attributes:
  vendor: "amd"
  predecessor: "zen-3"          # → Architecture entity
  successor: "zen-5"
  isa: "x86-64"
  node: "TSMC N5 (5nm)"
  release_year: 2022
  design:
    decoder_width: 4             # instructions/cycle decoded
    dispatch_width: 6            # micro-ops/cycle dispatched
    rob_entries: 320             # Reorder Buffer size
    integer_register_file: 224
    floating_point_register_file: 192
    load_store_queue:
      load: 128
      store: 72
  cache:
    l1i_kb_per_core: 64
    l1d_kb_per_core: 32
    l2_kb_per_core: 1024
    l3_shared: true
    l3_kb_per_ccd: 32768        # 32MB per CCD
  features:
    - "AVX-512 (256-bit dual-pumped)"
    - "BMI1/BMI2"
    - "TBM"
  branch_prediction:
    predictor_type: "perceptron" # или TAGE, hybrid, etc.
    btb_entries: null            # неизвестно — оставляем null
  key_improvements_over_predecessor:
    - "+13% IPC"
    - "AVX-512 support"
    - "Front-end: doubled L1 BTB"
    - "Load/store: 22% wider queue"
```

**Это инженерное сердце модели.** Архитектура — не тег на процессоре, а самостоятельная сущность со своей внутренней структурой. Два процессора на одной архитектуре (7600X и 7950X) разделяют эти атрибуты.

**Почему `key_improvements_over_predecessor` — список, а не relationship:** это qualitative claims, не links. Они не образуют формальный граф. Для machine-checkable связей — `predecessor`/`successor`.

#### 2.4 Chipset

Чипсет материнской платы. Связывает сокет с конкретными платами.

```yaml
dimension:
  id: "amd-b650"
  type: "chipset"
  canonical_name: "AMD B650"
  aliases: ["B650"]
  scd_type: 0
attributes:
  vendor: "amd"
  socket: "am5"                 # → Socket entity
  pcie:
    total_lanes: 36
    pcie_5_lanes: 0             # B650: только 4.0
    pcie_4_lanes: 8
  usb:
    usb_3_2_gen2x2: 1
    usb_3_2_gen2: 6
  sata_ports: 4
  overclocking:
    cpu: true
    memory: true
  multi_gpu: false
  release_year: 2022
```

#### 2.5 Memory Kit

Модули памяти как продукты. Нужны реже, но для инженерного анализа «какая частота DDR5 реально достижима на Zen 5» — критичны.

```yaml
dimension:
  id: "gskill-trident-z5-6000-cl30-32gb"
  type: "memory"
  canonical_name: "G.Skill Trident Z5 DDR5-6000 CL30 32GB (2×16GB)"
  scd_type: 0
attributes:
  vendor: "gskill"
  type: "DDR5"
  speed_mt_s: 6000
  cas_latency: 30
  timings: "30-38-38-96"
  capacity_gb: 32
  kit_config: "2×16GB"
  voltage_v: 1.35
  xmp_expo: "EXPO"
  form_factor: "DIMM"
```

### 3. Связи (Relationships)

Связи моделируются через поля-ссылки (`socket: "am5"` — ссылка на dimension типа socket). Не через отдельный графовый слой. Причина: на текущем масштабе (десятки CPU) связи в dimension-файлах читаемы и проверяемы без графовой БД. Если масштаб вырастет до тысяч — мигрируем.

| От | К | Поле | Назначение |
|---|---|---|---|
| CPU | Socket | `cpu.socket` | Совместимость. «Все CPU под AM5» |
| CPU | Architecture | `cpu.architecture` | Группировка. «Все CPU на Zen 5» |
| CPU | Integrated GPU | `cpu.graphics.igpu_model` | Инженерный анализ iGPU |
| Socket | Chipset | `chipset.socket` | Платформа. «Какие чипсеты для AM5» |
| Socket | Memory | `socket.compatible_memory` | Типы памяти |
| Architecture | Architecture | `architecture.predecessor` / `successor` | Эволюция. «Что изменилось от Zen 4 к Zen 5» |
| Memory | — | — | Автономная сущность, не ссылается на CPU напрямую |

**Связь CPU → Chipset — опосредованная:** CPU → Socket → Chipset. Этого достаточно для инженерного анализа платформы. Прямая связь CPU → Chipset не нужна: совместимость определяется сокетом.

**Связь CPU → Memory — опосредованная:** CPU → Architecture → IMC (Integrated Memory Controller) → supported memory speeds. Но IMC — это атрибут архитектуры, не отдельная сущность на текущем масштабе.

### 4. Интеграция в существующий склад

**Файловая структура:**

```
warehouse/hardware/dim/
  cpu/                    # 10-50 файлов со временем
    amd-ryzen-7-7800x3d.yaml
    amd-ryzen-5-7600x.yaml
    intel-core-i5-13400f.yaml
    ...
  socket/                 # 5-10 файлов
    am5.yaml
    lga-1700.yaml
    ...
  architecture/           # 10-20 файлов
    amd-zen-4.yaml
    amd-zen-5.yaml
    intel-raptor-cove.yaml
    intel-lion-cove.yaml
    ...
  chipset/                # 20-40 файлов
    amd-b650.yaml
    amd-x670.yaml
    intel-z790.yaml
    ...
  memory/                 # по мере необходимости
    gskill-trident-z5-6000-cl30-32gb.yaml
    ...
```

**Bus Matrix расширение:**

```yaml
bus_matrix:
  dimensions:
    cpu:
      canonical_dim: dim/cpu/{vendor}-{model}.yaml
      id_format: '{vendor}-{model}'
      description: Процессор
      scd_default: 0
      aliases: [...]           # Ryzen 7 7800X3D → amd-ryzen-7-7800x3d
      attributes:
        - vendor, family, generation
        - architecture, socket, lithography
        - compute.{cores, threads, base_clock_mhz, boost_clock_mhz}
        - cache.{l1_kb, l2_kb, l3_kb, l3_type}
        - memory.{type, max_official_speed_mt_s, channels}
        - pcie.{version, lanes}
        - graphics.{integrated, igpu_model}
        - power.{tdp_w, ppt_w, tjmax_c}
        - release.{date, msrp_usd}
        - platform.overclocking.*

    socket:
      canonical_dim: dim/socket/{slug}.yaml
      attributes:
        - vendor, type, pin_count
        - compatible_memory, predecessor
        - platform_lifespan.{promised_until_year, current_status}

    architecture:
      canonical_dim: dim/architecture/{vendor}-{name}.yaml
      attributes:
        - vendor, predecessor, successor, isa, node
        - design.{decoder_width, dispatch_width, rob_entries, ...}
        - cache.{l1i, l1d, l2, l3}
        - features, branch_prediction, key_improvements
```

### 5. Что НЕ в этой модели

Граница Слоя 5 — факты о мире, не выводы. В этой модели нет:

- **Performance claims.** «7600X на 9% быстрее 13400F» — это вывод на основе evidence (Слой 2), не атрибут сущности. Хранится в Evidence (CPU benchmarks), интерпретируется в Semantic Layer.
- **Recommendations.** «7800X3D — лучший игровой процессор» — это Decision (Слой 3). Не в Warehouse Model.
- **Pricing dynamics.** MSRP_at_launch — да (атрибут `release.msrp_usd`). Текущая розничная цена — нет, это Evidence со своим источником и датой.
- **Benchmark results.** Cinebench R23, Geekbench 6 — это observations (warehouse/fact/). Не атрибуты CPU.
- **Market positioning.** «Конкурент 13400F» — это аналитический вывод, не связь в модели. Определяется через сравнение evidence.

### 6. Почему Architecture — отдельная сущность, а не атрибут CPU

GPU-модель хранит `architecture: "Blackwell"` как строку-атрибут. Этого достаточно когда architecture — просто тег для группировки.

Для инженерной лаборатории architecture — не тег. Это объект с собственной внутренней структурой: decoder width, ROB size, branch predictor type, cache hierarchy. Два инженера обсуждают «Zen 4 vs Zen 5», не «7600X vs 9600X». Architecture — самостоятельная единица анализа.

→ Architecture = отдельный dimension type со своими атрибутами. CPU ссылается на Architecture.

**Цена решения:** +1 dimension type, +10-20 файлов. **Выгода:** инженерный анализ поколений становится возможным на уровне данных, не prose.

### 7. Наполнение: что первое

Склад растёт итеративно. Не пытаемся заполнить все атрибуты всех CPU.

**Первая итерация — 5 архитектурно значимых CPU:**

1. Ryzen 7 7800X3D — Zen 4, 3D V-Cache, игровой флагман
2. Ryzen 5 7600X — Zen 4, mainstream, базовая точка отсчёта
3. Ryzen 7 9800X3D — Zen 5, 3D V-Cache, новое поколение
4. Core i5-13400F — Raptor Cove (P-cores) + Gracemont (E-cores), hybrid architecture
5. Core Ultra 5 245K — Lion Cove + Skymont, новый hybrid, LGA 1851

Этот набор покрывает:
- AMD vs Intel
- Два поколения Zen (4, 5)
- Два поколения Intel (Raptor Lake, Arrow Lake)
- 3D V-Cache vs стандартный
- Гибридная vs гомогенная архитектура
- AM5 vs LGA 1700 vs LGA 1851

Плюс соответствующие Socket (AM5, LGA 1700, LGA 1851), Architecture (Zen 4, Zen 5, Raptor Cove, Lion Cove) и chipset-ы (B650, Z790).

## Альтернативы

| Альтернатива | Отвергнута потому что |
|---|---|
| **Архитектура как атрибут CPU** (как у GPU) | Инженерной лаборатории нужен анализ поколений. Строка-тег «Zen 4» этого не даёт. Нужны decoder width, ROB size, branch predictor — это атрибуты архитектуры, не процессора. |
| **Прямые связи CPU → Chipset** | Избыточно. Совместимость определяется сокетом. CPU → Socket → Chipset — транзитивная связь, её достаточно. |
| **Отдельный IMC (Memory Controller) как сущность** | На текущем масштабе IMC — атрибут архитектуры. Если появится cross-vendor memory benchmarking — выделим. |
| **Performance claims в атрибутах** | Смешивает Слой 1 (факты) и Слой 2 (evidence). «IPC» — это measurement, зависит от методики. Место — в observation, не в dimension. |
| **One big CPU dimension со всеми атрибутами** | Быстро становится bloated: P-core + E-core + boost tables + AVX offsets. Разделение CPU/Architecture/Socket даёт нормализацию и переиспользование. |

## Связь с другими ADR

- **ADR-025** (Source Layer): атрибуты CPU — это source-значения (из spec sheet, WikiChip, AnandTech). Не вычисляемые.
- **ADR-026** (Platform/App split): CPU dimension — hardware bounded context. Не платформенный.
- **ADR-028** (fact-insert): CPU-бенчмарки (Cinebench, Geekbench) пойдут через fact-insert. CPU dimensions — через dim-upsert (P1 в ADR-030).
- **ADR-030** (Debt Register): этот ADR закрывает data debt по CPU entities. Tech debt по dim-upsert capability остаётся.

## Последствия

**Что становится проще:**
- **Инженерный анализ поколений.** «Что изменилось в Zen 5 относительно Zen 4» → сравнение двух Architecture dimensions. Не prose, структурированные данные.
- **Cross-vendor сравнение на уровне архитектур.** «Lion Cove vs Zen 5: decoder width, ROB size, branch predictor».
- **Платформенный анализ.** «Какие CPU ставятся в AM5» → все CPU с `socket: "am5"`. «Сколько стоит платформа» → CPU + чипсет (в будущем — цены).
- **Группировка и фильтрация.** «Все 8-ядерные CPU с 3D V-Cache», «Все CPU с TDP до 65W».

**Что требует дисциплины:**
- **Архитектура — не тег.** Заполнять атрибуты архитектуры — инженерная работа. Не «Zen 4», а decoder width, ROB size, branch predictor. Требует sources (WikiChip, AnandTech, chipsandcheese.com).
- **Не смешивать слои.** Если кажется что «надо добавить поле IPC» — это observation, не атрибут. Performance — evidence, не entity.
- **CPU-бенчмарки ждут своей модели.** Этот ADR определяет entities, не evidence-модель. CPU benchmarks — отдельный ADR, потому что методология измерения CPU принципиально отличается от GPU.
