---
capability: cross-reference
layer: warehouse
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware', 'memory'"
      - name: dim_type
        type: string
        required: true
        description: "Тип dimension: gpu, game_title, ..."
      - name: dim_id
        type: string
        required: true
        description: "ID dimension ИЛИ source-значение"
      - name: fact_type
        type: string
        required: false
        default: "all"
        description: "observation | metric | all"
  out:
    result: fact_set
    format: "ordered by confidence descending"
  errors:
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
    - code: NO_FACTS
      meaning: "Нет Facts для данного Dimension"
idempotency: "read"
---

# cross-reference — все Facts для Dimension

## Model

Находит все Fact-файлы типа `fact_type` в `warehouse/{domain}/fact/{fact_type}/`, где `source.{dim_type}` матчится с `dim_id` (прямо или через bus matrix aliases). Резолвит source-значения в dimension_refs. Сортирует по confidence (убывание).

## Invariants

- Dimension существует (dim-read проходит)
- fact_type валиден ("observation", "metric", "all")
- Все Facts в fact_set имеют зарезолвленные dimension_refs
- Сортировка по confidence (убывание)

## Пример

```
cross-reference(domain="hardware", dim_type="gpu", dim_id="nvidia-rtx-5060")
→ bus-matrix: alias "RTX 5060" → "nvidia-rtx-5060"
→ поиск в warehouse/hardware/fact/observations/: source.gpu == "RTX 5060"
→ fact_set: [{fps_avg: 88, game: "cyberpunk-2077", confidence: 0.85}, ...]
```
