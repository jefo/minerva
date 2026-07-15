---
capability: pattern-promote
layer: analysis
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware'"
      - name: derived_type
        type: string
        required: true
        description: "law | pattern | comparison"
      - name: statement
        type: string
        required: true
        description: "Инженерный вывод: '3D V-Cache даёт +15-25% FPS в CPU-bound сценариях'"
      - name: lineage_nodes
        type: array
        required: true
        description: "Список observation-файлов, на которых основан вывод"
      - name: confidence
        type: number
        required: true
        description: "Confidence вывода (0-1)"
      - name: confidence_basis
        type: string
        required: true
        description: "training_data | observation | multi_source | expert"
      - name: relationships
        type: map
        required: false
        default: "{}"
        description: "{contradicts: [law-id], refines: [law-id]}"
  out:
    result: derived_fact_ref
    format: "{derived_id: string, file_path: string, lineage_valid: bool}"
  errors:
    - code: LINEAGE_BROKEN
      meaning: "lineage_nodes ссылаются на несуществующие observation-файлы"
    - code: CIRCULAR_LINEAGE
      meaning: "Обнаружен цикл: A → B → A"
    - code: LEVEL_VIOLATION
      meaning: "Law ссылается на другой Law того же или более высокого уровня (должен ссылаться на Fact / Comparison)"
    - code: NO_EVIDENCE
      meaning: "Нет Fact-узлов в lineage (Law не может быть выведен из ничего)"
    - code: DUPLICATE_LAW
      meaning: "Law с таким statement уже существует"
idempotency: "write"
---

# pattern-promote — сохранить обнаруженный Law/Pattern

Агент обнаружил инженерную закономерность в данных. Этот capability сохраняет
её как derived fact с полным lineage — чтобы закономерность переиспользовалась,
а не переоткрывалась заново каждым агентом.

## Model

Агент анализирует observation, находит закономерность, вызывает pattern-promote.
Capability проверяет lineage (все узлы существуют, нет циклов, есть Fact-узлы),
создаёт derived-файл в `marts/`.

В отличие от fact-insert (который пишет сырые замеры), pattern-promote пишет
выводы. Но механика та же: единственная точка записи derived-фактов.

## Invariants

- Все lineage_nodes существуют (файлы на fs)
- Хотя бы один узел — Fact (Level 0). Law не может быть выведен из воздуха
- Нет циклов в lineage (A → B, B → A)
- Уровни не нарушены: Law (L2) не может ссылаться на другой Law (L2) — используй `refines`
- statement уникален (проверка по similarity)
- Lineage встроен в derived-файл, не в отдельный реестр

## Пример: агент обнаружил Law

Агент загрузил comparison 7800X3D vs 7700 в 1080p Low, увидел:

```
7800X3D: 195 fps (BG3), 520 fps (CS2), 170 fps (CP2077)
7700:    170 fps (BG3), 440 fps (CS2), 160 fps (CP2077)
Дельта:  +15%        +18%         +6%
```

Агент формулирует Law: "3D V-Cache даёт +15-20% FPS в CPU-bound сценариях
по сравнению с non-X3D аналогом того же поколения"

Вызов:
```
pattern-promote(
  domain="hardware",
  derived_type="law",
  statement="3D V-Cache даёт +15-20% FPS в 1080p Low по сравнению с non-X3D аналогом того же поколения Zen 4",
  lineage_nodes=[
    "fact/cpu_observations/amd-ryzen-7-7800x3d-1080p-low-baldurs-gate-3-native.yaml",
    "fact/cpu_observations/amd-ryzen-7-7700-1080p-low-baldurs-gate-3-native.yaml",
    "fact/cpu_observations/amd-ryzen-7-7800x3d-1080p-low-counter-strike-2-native.yaml",
    "fact/cpu_observations/amd-ryzen-7-7700-1080p-low-counter-strike-2-native.yaml",
    "fact/cpu_observations/amd-ryzen-7-7800x3d-1080p-low-cyberpunk-2077-native.yaml",
    "fact/cpu_observations/amd-ryzen-7-7700-1080p-low-cyberpunk-2077-native.yaml"
  ],
  confidence=0.85,
  confidence_basis="observation",
  relationships={}
)
```

Результат — файл `marts/engineering/laws/3d-vcache-cpu-bound-advantage.yaml`.

Теперь любой агент, анализирующий 7800X3D или 9800X3D, может загрузить этот Law
и не переоткрывать закономерность.

## Naming

derived_id — осмысленный slug на основе statement:
- `3d-vcache-cpu-bound-advantage`
- `zen5-ipc-improvement-over-zen4`
- `intel-hybrid-gaming-penalty`

Не `law-001` — без знания statement ID нечитаем.

## Pitfalls

- **Не заменяет observation.** Law — вывод, не данные. Новые observation могут подтвердить или опровергнуть Law
- **Confidence — как у observation.** Если Law основан на training_data (confidence 0.75), Law не может иметь confidence выше
- **Не злоупотреблять уровнями.** L0-L3 достаточно. Если нужно уточнить Law — `refines`, не новый Law
- **Statement должен быть фальсифицируем.** Не «7800X3D хорош», а «3D V-Cache даёт +15-20% FPS в CPU-bound относительно non-X3D Zen 4»
