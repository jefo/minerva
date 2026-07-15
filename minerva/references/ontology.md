# Ontology — Gaming Performance DWH

## Core Entities

### Dimension
Описательный атрибут. То, **про что** мы измеряем.
- `gpu` — видеокарта (RTX 5060, RX 9060 XT)
- `cpu` — процессор (7800X3D, 14900K)
- `game_title` — игра, в которой делался замер
- `resolution` — разрешение (1080p, 1440p, 4K)
- `graphics_preset` — настройки графики (Low, Medium, Ultra)
- `benchmark_scenario` — тип сценария (1080p-low, 1440p-ultra, synthetic-mt)
- `architecture` — микроархитектура (Zen 4, Raptor Lake, Blackwell)
- `socket` — сокет (AM5, LGA1700)
- `chipset` — чипсет (B650, Z790)
- `driver_version` — версия драйвера

### Observation
Факт замера. **Что** измерили.
- Всегда ссылается на Dimensions через source-значения (не dim_id)
- Source-значения — человеческие имена: "RTX 5060", "Cyberpunk 2077", "1080p"
- Резолвинг source → dim_id происходит при чтении через bus-matrix aliases

### Law
Производный факт. Инженерная закономерность, выведенная из нескольких Observation.
- Имеет lineage — цепочку observation, на которых основан
- confidence — оценка достоверности (0.75 training_data, 0.9+ реальные замеры)
- Хранится в marts/engineering/laws/

### Pattern
Повторяющаяся структура в данных. Слабее чем Law — не доказанная закономерность, а наблюдаемый шаблон.

## Relationships

```
Dimension ←── source-значение ──→ Observation
                                       │
                                  lineage (↓↑)
                                       │
                                       ▼
                                     Law
```

## Bus Matrix
SSOT-контракт домена. Определяет:
- Какие dimension types существуют
- Какие fact types разрешены
- Aliases для резолвинга source-значений
- Validation rules
