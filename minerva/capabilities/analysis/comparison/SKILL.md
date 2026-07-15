---
capability: comparison
layer: analysis
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware'"
      - name: dim_type
        type: string
        required: true
        description: "Тип сравниваемых сущностей: 'gpu', 'cpu'"
      - name: dim_a
        type: string
        required: true
        description: "ID или alias первого Dimension"
      - name: dim_b
        type: string
        required: true
        description: "ID или alias второго Dimension"
      - name: metrics
        type: array[string]
        required: false
        default: "['fps_avg']"
        description: "Меры для сравнения: ['fps_avg', 'fps_1pct_low']"
      - name: filter
        type: map
        required: false
        default: "{}"
        description: "Фильтр: {resolution: '1440p', preset: 'Ultra'}"
  out:
    result: comparison_result
    format: |
      {
        dim_a: {id, canonical_name, attributes},
        dim_b: {id, canonical_name, attributes},
        shared_contexts: [
          {
            game_title: {id, canonical_name},
            resolution: {id, canonical_name},
            graphics_preset: {id, canonical_name},
            dim_a: {fps_avg: 78, fps_1pct_low: 62, conditions: {...}},
            dim_b: {fps_avg: 85, fps_1pct_low: 70, conditions: {...}},
            delta: {fps_avg: {absolute: +7, percent: +8.9}, fps_1pct_low: {absolute: +8, percent: +12.9}}
          },
          ...
        ],
        summary: {
          games_compared: 15,
          aggregate_delta: {fps_avg: +6.3%, fps_1pct_low: +8.1%},
          wins: {gpu_a: 10, gpu_b: 3, tie: 2},
          coverage: {gpu_a: "38/93 games", gpu_b: "25/93 games"}
        },
        warnings: ["Сравнение на разных драйверах: 572.16 vs 576.01", "..."],
        unmatched: {dim_a: ["game_x", "game_y"], dim_b: ["game_z"]}
      }
  errors:
    - code: DIM_NOT_FOUND
      meaning: "Dimension A или B не резолвится"
    - code: NO_FACTS
      meaning: "Нет observations ни для одного из Dimensions"
    - code: NO_SHARED_CONTEXTS
      meaning: "Есть observations, но нет общих игр/разрешений/пресетов"
idempotency: "read"
---

# comparison — сравнение двух сущностей по общим контекстам

Находит все observation для dim_a и dim_b, определяет общие контексты (игра × разрешение × пресет), вычисляет дельту по каждой метрике. Возвращает structured comparison_table — не prose, не выводы. Данные для принятия решения, не само решение.

## Model

Comparison работает в трёх шагах:

1. **Fetch:** cross-reference для dim_a и dim_b → два fact_set
2. **Match:** группировка по ключу контекста (game_title × resolution × graphics_preset). Общие контексты = те, где есть observation для обоих GPU.
3. **Delta:** для каждого общего контекста — вычислить абсолютную и процентную разницу по каждой метрике.

## Invariants

- Оба Dimension существуют (bus-lookup → dim-read)
- Хотя бы один общий контекст найден (если 0 → NO_SHARED_CONTEXTS)
- Дельта считается: dim_b относительно dim_a (+5% = dim_b быстрее dim_a на 5%)
- Если метрика отсутствует у одного GPU в общем контексте → этот контекст исключается из сравнения по этой метрике, warning
- Разные драйверы → warning (не ошибка — сравнение валидно, но с оговоркой)
- Разные условия (upscaler, frame_gen) → контекст исключается, warning

## Пример

```
comparison(
  domain="hardware", dim_type="gpu",
  dim_a="RTX 5060", dim_b="RTX 4060",
  metrics=["fps_avg", "fps_1pct_low"],
  filter={resolution: "1440p", preset: "Ultra"}
)

→ cross-reference для "nvidia-rtx-5060" → 35 observations
→ cross-reference для "nvidia-rtx-4060" → 15 observations
→ match: 8 общих игр (Cyberpunk 2077, Starfield, Hogwarts Legacy, ...)
→ delta:
    Cyberpunk 2077:
      dim_a (RTX 5060): fps_avg=68, fps_1pct_low=52
      dim_b (RTX 4060): fps_avg=72, fps_1pct_low=58
      delta: fps_avg=-5.6%, fps_1pct_low=-10.3%
    ...
→ summary: RTX 4060 в среднем на 6% быстрее по fps_avg, но на 8% по 1% low
→ warnings: ["Разные драйверы: 572.16 vs 546.33"]
```

## Matching Rules

**Точное совпадение:** game_title + resolution + graphics_preset. Если у одного GPU "Cyberpunk 2077 / 1440p / Ultra" а у другого "Cyberpunk 2077 / 1440p / High" → не match.

**Условия:** upscaler, frame_gen, ray_tracing должны совпадать. `native` ≠ `DLSS Quality`. `FG off` ≠ `FG 3x`. Исключение из сравнения с warning.

**Драйверы:** не блокируют match, но генерируют warning если разные. Агент решает учитывать или нет.

## Pitfalls

- **Comparison ≠ recommendation.** Этот capability возвращает таблицу дельт. Вывод «какая карта лучше» — responsibility агента или Decision Engine, не comparison.
- **Разные выборки игр.** Если у GPU A 35 игр, у GPU B 15 игр — общих может быть 5. Это не ошибка, но summary.coverage показывает асимметрию.
- **Не сравнивай разные fact_type.** Comparison для GPU ожидает `observation`, не `metric`. Если dim_type='cpu' — другие контексты.
- **Проценты от baseline.** `delta.percent` = ((dim_b - dim_a) / dim_a) × 100. Отрицательное = dim_b хуже dim_a.
- **Агент не должен вычислять дельту сам.** Comparison возвращает готовые дельты. Агент получает числа, не пересчитывает.
