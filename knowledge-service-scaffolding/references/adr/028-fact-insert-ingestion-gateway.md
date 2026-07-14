---
id: adr-028
status: proposed
date: 2026-07-13
supersedes: []
superseded_by: []
tags: [platform, ingestion, fact-insert, bus-matrix, write-side, capabilities, structural-integrity]
based_on: [adr-016, adr-025, adr-026]
---

# ADR-028: Fact Insert — ingestion gateway как платформенный capability

## Контекст

ADR-026 зафиксировал `fact-insert` в списке платформенных capabilities, но не определил его контракт. Текущая практика импорта данных — ad-hoc скрипты (Python/execute_code), которые пишут observation-файлы напрямую в `warehouse/hardware/fact/observations/`.

**Проблема не в том что скрипты существуют.** Проблема в отсутствии write-side контракта, который гарантирует структурную целостность склада.

### Что происходит без ingestion gateway

1. **Structural contamination.** Разные сессии генерируют observation-файлы с разной структурой (присутствие/отсутствие полей, вариации в именовании, неконсистентные conditions). Следующий агент, читающий склад, воспримет разброс как часть модели данных.

2. **Silent drift.** Не фатальный сбой, а частичная несогласованность. Агент читает 80 observations одним способом, 20 — другим, усредняет и выдаёт рекомендацию. Ошибка невидима.

3. **Усложнение consumer-фич.** Аналитические capabilities (FPS/рубль, upgrade path) требуют строгих гарантий о структуре данных. Без ingestion gateway каждый аналитический запрос вынужден защищаться от structural drift.

4. **Нарушение platform/app split.** Ad-hoc скрипты смешивают платформенную логику (валидация, запись) с прикладной (какой GPU, какая игра). Это именно то смешение, против которого направлен ADR-026.

## Решение

### 1. `fact-insert` как единственная точка записи

`fact-insert` — платформенный capability. Единственный способ создать Fact (Observation, Metric, Memory Entry) в warehouse. Любая прикладная логика (hardware-бенчмарки, agent memory) проходит через этот gateway.

```
Приложение (Hardware KB)
  │
  │  Данные бенчмарка (сырой markdown)
  ▼
Прикладной ingestion-скрипт
  │  Парсинг, нормализация, domain-specific logic
  ▼
fact-insert (ПЛАТФОРМА)
  │  Валидация по bus matrix, резолвинг dimensions, запись
  ▼
warehouse/{domain}/fact/{type}/
```

**Что НЕ фиксируем:**
- Формат сырых данных на входе в прикладной скрипт (это решение приложения: markdown, CSV, JSON, YouTube transcript)
- Прикладную логику парсинга (как извлечь fps_avg из markdown-таблицы)
- Стратегию создания dimensions (автоматически vs запрос подтверждения)

### 2. Контракт fact-insert

```yaml
# Вход
fact_insert:
  domain: string            # bounded context: "hardware", "memory"
  fact_type: string         # тип факта: "observation", "metric", "memory_entry"
  source:                   # сырые source-значения (до резолвинга)
    dim_name: "raw_value"   # например: gpu: "RTX 5060"
  measures:                 # числовые значения
    measure_name: number
  conditions:               # опционально: контекст замера
    key: "value"
  meta:                     # provenance
    confidence: number
    confidence_basis: string
    observed_at: string
    observed_by: string
    source_channel: string

# Выход
result:
  fact_id: string           # уникальный ID созданного факта
  file_path: string         # путь к созданному файлу
  resolved_dimensions:      # как source-значения разрешились в Dimension ID
    dim_name: "canonical_id"
  warnings: [string]        # нефатальные проблемы
```

### 3. Процесс fact-insert

```
1. LOAD bus matrix  →  bus-matrix.yaml для указанного domain
2. VALIDATE mandatory dimensions  →  все обязательные dim'ы присутствуют в source
3. RESOLVE dimensions  →  source-значения → canonical Dimension ID через aliases
   ├─ Найден алиас → резолвим
   ├─ Dimension-файл существует → резолвим
   └─ НЕ найден → ERROR: unknown dimension value
4. VALIDATE measures  →  все measures есть в allowed_measures bus matrix
5. VALIDATE business rules  →  fps_avg > fps_1pct_low (из validation_rules)
6. VALIDATE uniqueness  →  нет существующего Fact с теми же mandatory_dimensions
7. GENERATE fact_id  →  {domain}-{fact_type}-{slugified_dimensions}
8. WRITE fact file  →  warehouse/{domain}/fact/{fact_type}/{fact_id}.yaml
   ├─ Структура строго по шаблону (задаётся платформой)
   └─ source-значения — оригинальные строки (ADR-025)
9. RETURN result  →  fact_id, file_path, resolved_dimensions, warnings
```

### 4. Структурная гарантия

`fact-insert` гарантирует идентичную структуру всех Fact-файлов одного типа. Шаблон определяется платформой, не приложением:

```yaml
# Всегда такая структура. Никаких вариаций.
fact:
  id: "..."
  type: "..."
source:
  dim1: "raw_value"
  dim2: "raw_value"
measures:
  measure1: number
conditions:
  key: "value"
meta:
  confidence: number
  ...
lineage:
  nodes: []
  edges: []
```

Приложение не может добавить поле, убрать поле, изменить порядок или вложенность. Это платформенный контракт.

### 5. Что fact-insert НЕ делает

- **Не парсит сырые данные.** Приложение должно нормализовать markdown/CSV/JSON в структуру `source + measures + conditions` до вызова `fact-insert`
- **Не создаёт Dimensions автоматически.** Если source-значение не резолвится — ошибка. Создание Dimensions — отдельная операция
- **Не интерпретирует данные.** `fps_avg: 22` — это «приемлемо» или «провал»? Это решение consumer-аналитики
- **Не обновляет существующие Facts.** SCD Type 2 для Facts — будущий ADR

### 6. Прикладной ingestion-скрипт (пример)

```python
# hardware_ingest.py — ПРИКЛАДНОЙ скрипт, не платформа
# Вызывается когда пользователь даёт бенчмарк-отчёт

def ingest_benchmark_report(markdown_text: str):
    rows = parse_markdown_table(markdown_text)  # прикладная логика
    
    for row in rows:
        result = fact_insert(
            domain="hardware",
            fact_type="observation",
            source={
                "gpu": row.gpu_name,           # "RTX 5060"
                "game_title": row.game,         # "Cyberpunk 2077"
                "resolution": row.resolution,   # "1080p"
                "graphics_preset": row.preset, # "Ultra"
                "driver_version": row.driver,   # "2026-Q2"
                "cpu": row.cpu,                 # "AMD Ryzen 7 8800X3D"
            },
            measures={
                "fps_avg": row.avg_fps,
                "fps_1pct_low": row.low_1pct,
                "fps_0_1pct_low": row.low_01pct,
                "frametime_ms_avg": row.frametime,
            },
            conditions={
                "upscaler": row.upscaler,
                "frame_gen": row.mfg_multiplier,
                "ray_tracing": row.rt_mode,
            },
            meta={...},
        )
        print(f"✓ {result.fact_id}")
```

Прикладной скрипт делает domain-specific работу (парсинг markdown-таблиц, знание что «DLSS 4 Quality» — это upscaler). Платформа делает structural work (валидация, запись).

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Ad-hoc скрипты (текущее состояние) | Быстро, гибко, не требует проектирования | Structural contamination, silent drift, каждый скрипт переизобретает валидацию | Это временная мера этапа наполнения склада, не архитектурное решение |
| fact-insert в каждом приложении отдельно | Приложение контролирует всё | Дублирование bus-matrix валидации. Разные приложения → разная структурная гарантия. Нарушение platform/app split | Платформа даёт гарантии. Приложения не должны переизобретать контракты |
| Ingestion = ETL capability (ADR-018) | ETL — признанный паттерн | ETL решает проблему acquisition (внешние API), не ingestion gateway (запись в склад). Разные слои | fact-insert — write-side интерфейс склада. ETL — слой выше, который может вызывать fact-insert |

## Связь

- **ADR-016 (Data Model):** fact-insert реализует write-side dimensional model. Структура Fact определена там, валидация — здесь
- **ADR-025 (Source Layer):** fact-insert записывает source-значения как сырые строки, не Dimension ID. Резолвинг — внутри capability
- **ADR-026 (Platform/App Split):** fact-insert — платформенный capability. Приложения вызывают его, но не определяют его поведение
- **ADR-018 (ETL Pipeline):** ETL — acquisition-слой. fact-insert — warehouse write-side. ETL может вызывать fact-insert

## Последствия

**Что становится проще:**
- Импорт данных: прикладной скрипт + fact-insert → структурная гарантия
- Consumer-аналитика: все Facts одной структуры → запросы без defensive programming
- Новые приложения (Agent Memory): тот же fact-insert, другая bus matrix
- Аудит: каждая запись проходит через одну точку → можно логировать, откатывать

**Что требует дисциплины:**
- fact-insert должен оставаться домен-нейтральным. Никаких `if domain == "hardware"` спец-правил
- Приложения обязаны нормализовать данные до вызова fact-insert. Нельзя передавать «RTX 5060 Ti (если 16GB то...)»
- Изменения в структуре Fact — через ADR. Не через патч в прикладном скрипте
- Bus matrix — living document. При добавлении нового measure нужно обновлять и его, и fact-insert валидацию

**Что требует будущих ADR:**
- SCD Type 2 для Facts (обновление существующих observations с историей)
- Batch fact-insert (много facts за один вызов — сейчас 86 вызовов для 86 строк)
- Dry-run mode (валидация без записи — «эти данные пройдут ingestion?»)
