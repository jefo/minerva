---
capability: lineage-trace
layer: analysis
contract:
  in:
    params:
      - name: derived_id
        type: string
        required: true
        description: "ID derived-факта: '3d-vcache-cpu-bound-advantage'"
      - name: direction
        type: string
        required: false
        default: "up"
        description: "'up' — от вывода к источникам. 'down' — от fact ко всем выводам"
      - name: max_depth
        type: integer
        required: false
        default: 3
        description: "Максимальная глубина traversal"
  out:
    result: lineage_tree
    format: |
      {
        root: {id, type, level, statement},
        tree: [
          {ref, type, level, role, data_summary},
          ...
        ],
        stats: {total_nodes: N, levels: [0,1,2], fact_count: N}
      }
  errors:
    - code: DERIVED_NOT_FOUND
      meaning: "Derived-файл не существует"
    - code: LINEAGE_EMPTY
      meaning: "lineage.nodes пуст"
idempotency: "read"
---

# lineage-trace — проследить происхождение вывода

Раскручивает lineage DAG: от Law → Comparison → Observation → Source.
Отвечает на вопрос «почему мы так решили?» с полной прослеживаемостью.

Это главная операция эпистемической достоверности DW. Без неё любой вывод —
«потому что я так сказал». С ней — «вот 6 observation, вот их source_url,
вот confidence каждого».

## Model

Lineage DAG (ADR-017): граф, где узлы — элементы данных (Fact, Comparison,
Law, Artifact), рёбра — типизированные отношения происхождения.

`lineage-trace` идёт от derived-файла вверх по графу (direction="up"),
загружая каждый узел и строя дерево до исходных observation.

Для каждого Fact в дереве:
- Загружается observation-файл через fact-read
- Извлекается source_url, confidence, measures
- Возвращается в data_summary

## Invariants

- Все узлы в lineage.nodes резолвятся (файлы существуют)
- Траверсал не зацикливается (DAG по определению ацикличен)
- Исходные Fact-узлы (Level 0) — терминальные
- Если узел ссылается на другой derived — рекурсивный trace

## Пример

```
lineage-trace(derived_id="3d-vcache-cpu-bound-advantage", direction="up")

→ root: Law "3D V-Cache даёт +15-20% FPS в CPU-bound" (Level 2, confidence 0.85)
→ tree:
    Level 0: observation 7800X3D-BG3-1080p (fps_avg=195, source=training_data)
    Level 0: observation 7700-BG3-1080p    (fps_avg=170, source=training_data)
    Level 0: observation 7800X3D-CS2-1080p (fps_avg=520, source=training_data)
    Level 0: observation 7700-CS2-1080p    (fps_avg=440, source=training_data)
    Level 0: observation 7800X3D-CP2077-1080p (fps_avg=170, source=training_data)
    Level 0: observation 7700-CP2077-1080p    (fps_avg=160, source=training_data)
→ stats: 7 nodes, levels [0,2], 6 facts

Ответ на вопрос «почему»:
  «Law основан на 6 observation (3 игры × 2 CPU) в сценарии 1080p Low.
   Все — training_data, confidence 0.75 каждый.
   Средняя дельта: 7800X3D быстрее 7700 на +13% по fps_avg.»
```

## Direction="down" (impact analysis)

```
lineage-trace(direction="down", derived_id="amd-ryzen-7-7800x3d-1080p-low-baldurs-gate-3-native")

→ Этот observation используется в:
    Law: "3D V-Cache даёт +15-20% FPS в CPU-bound"
    Law: "Zen 4 gaming performance ceiling"
→ Если observation изменится (новый драйвер, новый замер) — эти Law требуют ревью.
```

## Pitfalls

- **Траверсал не бесконечный.** max_depth ограничивает глубину. Для Law → Fact достаточно depth=2
- **Lineage может быть неполным.** Если observation ещё не привязаны к Law через pattern-promote — lineage-trace их не увидит
- **Не интерпретируй confidence Law.** Law может иметь confidence 0.85, но если один из Fact имеет confidence 0.5 — это красный флаг. Показывай minimum confidence в дереве
