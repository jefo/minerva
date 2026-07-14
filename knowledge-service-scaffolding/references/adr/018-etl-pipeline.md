---
id: adr-018
status: superseded
date: 2026-07-11
supersedes: []
superseded_by: [adr-029]
tags: [etl, acquisition, pipeline, extraction, transformation, loading]
based_on: [adr-012, adr-015, adr-016]
---

# ADR-018: ETL Pipeline — Acquisition как capabilities

## Контекст

ADR-015 определил Acquisition как ETL-слой. ADR-016 определил схемы Dimension и Fact — целевые форматы для загрузки. Теперь нужно спроектировать сам ETL-пайплайн: как capabilities организуют извлечение, трансформацию и загрузку данных.

Acquisition — механический слой. Никакой интерпретации. Никаких выводов. Только: взять сырые данные → нормализовать → записать в Warehouse.

## Решение

### 1. ETL как последовательность capabilities

```
EXTRACT                    TRANSFORM                 LOAD
   │                           │                       │
   ▼                           ▼                       ▼
source-extract           transform-normalize      warehouse-load
   │                           │                       │
   ├── youtube-connect         ├── schema-map           ├── dim-upsert
   ├── url-scrape              ├── unit-convert         ├── fact-insert
   ├── api-fetch               ├── conflict-detect      ├── scd-apply
   └── manual-import           └── alias-resolve        └── bus-register
```

Каждый этап — независимая capability с контрактом. Этапы связаны через файлы: output Extract = input Transform, output Transform = input Load.

### 2. Extract: source connectors

**Ответственность:** получить сырые данные из источника в структурированном, но не нормализованном виде.

| Connector | Источник | Вход | Выход |
|---|---|---|---|
| `youtube-connect` | YouTube transcript | URL видео | `acquisition/raw/{source}/transcript.md` |
| `url-scrape` | Веб-страницы (TechPowerUp, Guru3D, etc.) | URL | `acquisition/raw/{source}/page.md` |
| `api-fetch` | API (NVIDIA ARK, ценовые агрегаторы) | API endpoint + params | `acquisition/raw/{source}/data.yaml` |
| `manual-import` | Ручной ввод/файлы | Пользовательский ввод | `acquisition/raw/{source}/import.yaml` |

**Формат сырых данных (после Extract):**

```yaml
# acquisition/raw/nvidia-ark/rtx-5060-extract.yaml
---
source: "nvidia-ark"
source_url: "https://www.nvidia.com/en-us/geforce/graphics-cards/rtx-5060/"
extracted_at: "2026-07-11"
extracted_by: "api-fetch"

raw:
  product_name: "GeForce RTX 5060 8GB"
  cuda_cores: "3840"
  memory: "8 GB GDDR7"
  memory_interface: "128-bit"
  memory_bandwidth: "355 GB/s"
  boost_clock: "2.50 GHz"
  tdp: "150 W"
  # ... остальные поля как они пришли из источника
```

**Правила Extract:**
- Никакой трансформации кроме парсинга в структуру. «8 GB» остаётся строкой, не числом 8
- Каждый источник — отдельная директория в `acquisition/raw/`
- Источник + URL = уникальный идентификатор сырых данных. Повторный extract перезаписывает

### 3. Transform: normalisation pipeline

**Ответственность:** преобразовать сырые данные в Warehouse-совместимую форму.

#### 3.1 schema-map

Сопоставить поля источника с internal schema:

```yaml
# acquisition/mappings/nvidia-ark-to-gpu-dim.yaml
---
mapping:
  source: "nvidia-ark"
  target_dim: "dim/gpu"
  field_map:
    product_name: "canonical_name"
    cuda_cores: "attributes.compute.cuda_cores"       # строка → число
    memory: "attributes.vram"                           # "8 GB GDDR7" → {size_gb: 8, type: "GDDR7"}
    memory_interface: "attributes.vram.bus_width_bit"   # "128-bit" → 128
    memory_bandwidth: "attributes.vram.bandwidth_gb_s"  # "355 GB/s" → 355
    boost_clock: "attributes.clock.boost_ghz"           # "2.50 GHz" → 2.50
    tdp: "attributes.power.tdp_w"                       # "150 W" → 150
```

Mapping — декларативный. Не код. Файл YAML, который читает `transform-normalize`.

#### 3.2 unit-convert

Нормализовать единицы измерения:

| Вход (из источника) | Выход (в Warehouse) | Правило |
|---|---|---|
| «355 GB/s» | 355 | Убрать «GB/s», оставить число |
| «2.50 GHz» | 2.50 | Убрать «GHz» |
| «150 W» | 150 | Убрать «W» |
| «$299» | 299 | Убрать «$» |
| «22 000 ₽» | 22000 | Убрать «₽», пробел |

#### 3.3 alias-resolve

Распознать имена источников через Bus Matrix:

| Вход (из источника) | Bus Matrix alias | Каноническое имя |
|---|---|---|
| «CP2077» | game_title | «Cyberpunk 2077» → `dim/game_title/cyberpunk-2077.yaml` |
| «Alan Wake II» | game_title | «Alan Wake 2» → `dim/game_title/alan-wake-2.yaml` |
| «572.16» | driver_version | → `dim/driver_version/nvidia-geforce-572.16_v2026-03.yaml` |

Если alias не найден в Bus Matrix → новый Dimension → ручная регистрация.

#### 3.4 conflict-detect

Два источника дали разные значения для одного поля:

```
Источник A (NVIDIA ARK):  bandwidth = 355 GB/s
Источник B (TechPowerUp): bandwidth = 352 GB/s
```

**Стратегия:**

| Ситуация | Действие |
|---|---|
| Расхождение < 5% | Принять более авторитетный источник (manufacturer > reviewer > user) |
| Расхождение ≥ 5% | Маркировать поле `contested: true`, сохранить оба значения, создать `contradicts` ребро в lineage |
| Один источник | Принять как есть, `confidence: single_source` |

```yaml
# acquisition/conflicts/rtx-5060-bandwidth.yaml
---
conflict:
  field: "attributes.vram.bandwidth_gb_s"
  sources:
    - {value: 355, source: "nvidia-ark", authority: "manufacturer"}
    - {value: 352, source: "techpowerup", authority: "reviewer"}
  resolution: "accepted_primary"        # accepted_primary | contested | manual_review
  resolved_value: 355
  note: "Расхождение 0.8% — в пределах погрешности измерения"
```

### 4. Load: Warehouse writers

**Ответственность:** записать нормализованные данные в Warehouse с соблюдением SCD-стратегии.

#### 4.1 dim-upsert

Создать или обновить Dimension:

```
Дано: нормализованные данные GPU
Если Dimension с таким id не существует:
  → создать новый файл dim/gpu/{id}.yaml
Если существует:
  → проверить scd_type:
    Type 0: пропустить (immutable)
    Type 1: перезаписать attributes
    Type 2: создать новую версию, обновить заголовочный файл
```

#### 4.2 fact-insert

Создать Fact:

```
Дано: нормализованные данные Observation
→ проверить что все dimension_refs ведут на существующие файлы
→ создать fact/observations/{id}.yaml
→ факт всегда создаётся новый (Facts не обновляются — только новые Observations)
```

#### 4.3 scd-apply

Применить SCD-стратегию:

```
Дано: изменение в Dimension с scd_type: 2
→ создать файл-версию: {dim_id}_v{date}.yaml
→ обновить заголовочный файл: current_version → новый файл
→ запустить impact-analysis: какие Laws затронуты?
→ НЕ менять существующие Observations (они ссылаются на старую версию)
```

#### 4.4 bus-register

Зарегистрировать новый Dimension в Bus Matrix:

```
Дано: создан новый Dimension
→ проверить bus-matrix.yaml: есть ли этот dimension-тип?
→ если новый dimension (не новый экземпляр, а новый тип): добавить в bus-matrix
→ если новый экземпляр существующего типа: не требуется
```

### 5. ETL-сессия: полный пример

```
Задача: импортировать RTX 5060 из NVIDIA ARK

1. EXTRACT
   api-fetch --source nvidia-ark --url "https://..." 
   → acquisition/raw/nvidia-ark/rtx-5060-extract.yaml

2. TRANSFORM
   transform-normalize --input acquisition/raw/nvidia-ark/rtx-5060-extract.yaml
     --mapping acquisition/mappings/nvidia-ark-to-gpu-dim.yaml
   → schema-map: поля сопоставлены
   → unit-convert: "8 GB" → 8, "355 GB/s" → 355
   → alias-resolve: имена проверены через bus-matrix
   → conflict-detect: конфликтов нет (один источник)
   → acquisition/staged/dim/gpu/nvidia-rtx-5060.yaml

3. LOAD
   warehouse-load --input acquisition/staged/dim/gpu/nvidia-rtx-5060.yaml
   → dim-upsert: создан warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml
   → scd-apply: scd_type=0, immutable — ок
   → bus-register: gpu уже в bus-matrix — ок
   → git commit: "acquisition: import RTX 5060 from NVIDIA ARK"
```

### 6. Capabilities-контракты

#### source-extract

```yaml
contract:
  in:
    source_type: "youtube" | "url" | "api" | "manual"
    source_params: {url: "...", ...}
  out:
    raw_file: "acquisition/raw/{source_type}/{slug}-extract.yaml"
  rules:
    - Никакой трансформации кроме парсинга в YAML
    - Повторный extract перезаписывает raw_file
    - При ошибке → acquisition/errors/{slug}-error.yaml
```

#### transform-normalize

```yaml
contract:
  in:
    raw_file: "acquisition/raw/{source_type}/{slug}-extract.yaml"
    mapping_file: "acquisition/mappings/{mapping}.yaml"  # опционально
  out:
    staged_file: "acquisition/staged/{dim|fact}/{slug}.yaml"
    conflicts: "acquisition/conflicts/{slug}.yaml"       # если обнаружены
  rules:
    - mapping_file обязателен для новых источников
    - conflict-detect всегда выполняется (даже для одного источника — проверка на дубликаты)
    - staged_file валидируется против Dimension/Fact schema (ADR-016)
```

#### warehouse-load

```yaml
contract:
  in:
    staged_file: "acquisition/staged/{dim|fact}/{slug}.yaml"
  out:
    warehouse_file: "warehouse/{domain}/{dim|fact}/{slug}.yaml"
    impact_report: "acquisition/reports/{slug}-impact.yaml"  # если SCD Type 2
  rules:
    - dim-upsert: следовать scd_type
    - fact-insert: всегда новый файл
    - После загрузки → git commit
    - При SCD Type 2 → impact-analysis автоматически
```

## Что НЕ фиксируем

- **Шедулинг ETL.** Cron или триггеры — implementation detail
- **Полный перечень source connectors.** Будут добавляться по мере необходимости
- **Обработка бинарных форматов (PDF, изображения).** Пока только текст
- **Incremental ETL.** Пока только full refresh. Incremental — когда масштаб потребует

## Последствия

**Что становится проще:**
- **Новый источник — только mapping.** Не нужно писать код. Декларативный YAML-mapping → `transform-normalize` делает остальное
- **Conflict detection — автоматически.** Каждый ETL-прогон проверяет на конфликты. Не нужно помнить «а что там TechPowerUp говорил?»
- **SCD — в потоке.** `warehouse-load` сам решает создать версию или перезаписать, на основе `scd_type`
- **Git-history = audit trail.** Каждый ETL-прогон → коммит. Всегда видно кто, когда и откуда принёс данные

**Что требует внимания:**
- **Mapping-файлы требуют поддержки.** При изменении структуры источника → обновить mapping. Автоматически не обновляется
- **Conflict resolution — semi-automated.** Расхождение ≥ 5% → ручное решение. Машина не знает какой источник авторитетнее
- **Alias-resolve зависит от Bus Matrix.** Если новый game_title не зарегистрирован → ETL останавливается с ошибкой, ждёт ручной регистрации
