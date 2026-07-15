---
capability: fact-read
layer: warehouse
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware', 'memory'"
      - name: fact_type
        type: string
        required: true
        description: "Тип факта: 'observation', 'metric'"
      - name: fact_id
        type: string
        required: true
        description: "ID факта: 'rtx-5060-cyberpunk-2077-1440p-ultra-native'"
  out:
    result: fact_data
    format: |
      {
        fact: {id, type, file_path},
        source: {dim_type: source_value, ...},
        resolved_dimensions: {dim_type: {id, canonical_name, attributes, ...}},
        measures: {measure_name: {value, definition}},
        conditions: {key: value, ...},
        meta: {confidence, confidence_basis, ...},
        lineage: {nodes: [], edges: []}
      }
  errors:
    - code: FACT_NOT_FOUND
      meaning: "Файл факта не существует"
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
    - code: UNRESOLVED_DIMENSION
      meaning: "source-значение не резолвится через bus-lookup"
idempotency: "read"
---

# fact-read — прочитать Fact с полным контекстом

Читает Fact-файл и резолвит все source-значения в dimension-данные, подгружает definitions мер. Агент получает не сырой YAML, а полностью контекстуализированный объект.

## Model

Fact-файлы хранятся по пути `warehouse/{domain}/fact/{fact_type}/{fact_id}.yaml`. Source-значения (ADR-025) резолвятся через bus-lookup в dimension-данные. Меры сверяются с definitions из bus matrix.

## Invariants

- Fact-файл существует и валиден (YAML парсится)
- Все source-значения резолвятся в dimension-файлы (bus-lookup)
- Меры возвращаются с definition-контекстом (если definition существует)
- Если definition для меры отсутствует — возвращается warning, не ошибка

## Процедура

1. Загрузить Fact-файл → извлечь `fact`, `source`, `measures`, `conditions`, `meta`, `lineage`
2. Для каждого source-значения → bus-lookup → dim-read → полные dimension-данные
3. Для каждой меры → найти definition в `measure_definitions` bus matrix → загрузить
4. Собрать ответ

## Пример

```
fact-read(domain="hardware", fact_type="observation", fact_id="rtx-5060-cyberpunk-2077-1440p-ultra-native")

→ fact: {id: "rtx-5060-cyberpunk-2077-1440p-ultra-native", type: "observation"}
→ source: {gpu: "RTX 5060", game_title: "Cyberpunk 2077", resolution: "1440p", ...}
→ resolved_dimensions:
    gpu: {id: "nvidia-rtx-5060", canonical_name: "NVIDIA GeForce RTX 5060 8GB", attributes: {vendor: "nvidia", architecture: "Blackwell", vram: {size_gb: 8, ...}, ...}}
    game_title: {id: "cyberpunk-2077", canonical_name: "Cyberpunk 2077", attributes: {developer: "CD Projekt Red", engine: "REDengine 4", ...}}
    ...
→ measures:
    fps_avg: {value: 68, definition: "Среднее арифметическое FPS по 3 прогонам, FrameView 1.5+, ..."}
    fps_1pct_low: {value: 52, definition: "Нижний перцентиль FPS, ..."}
→ meta: {confidence: 0.85, confidence_basis: "youtube_benchmark", observed_at: "2026-Q2"}
```

## Edge Cases

- **Legacy format (dimensions вместо source):** старые observation могут иметь `dimensions:` вместо `source:`. Обрабатывается аналогично — значения dimensions уже являются dim_id, резолвинг через dim-read напрямую.
- **Мера без definition:** не все меры в bus matrix имеют `measure_definitions`. Возвращается warning, факт читается.
- **Отсутствующий dimension-файл:** source-значение резолвится в dim_id, но dim-файл не существует → UNRESOLVED_DIMENSION. Не DIM_NOT_FOUND (это про alias), а именно отсутствие файла.

## Pitfalls

- **Не все меры обязаны иметь definition.** telemetry-меры (clock_core_mhz, power_draw_w) могут не иметь отдельных definitions. Это не ошибка.
- **Не путать source-значения и dim_id.** Source — это "RTX 5060", dim_id — "nvidia-rtx-5060". Файл хранит source, ответ возвращает оба.
- **lineage.nodes может быть пустым** — lineage ещё не заполнена. Это текущее состояние склада, не ошибка.
