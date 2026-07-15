# Marts — Derived Data Layer (ADR-017)

Слой производных данных: Laws, Patterns, Comparisons.
Всё что здесь — вычислено из warehouse, не хранится как первичные данные.

Каждый derived-файл обязан иметь `lineage` — граф происхождения,
связывающий вывод с исходными observation.

## Структура

```
marts/
├── engineering/
│   ├── laws/           # Laws — инженерные выводы из Facts
│   └── patterns/       # Patterns — повторяющиеся структуры
├── competitive/
│   └── comparisons/    # Comparisons — сравнения Dimension
├── narrative/          # Narrative arcs (для контент-пайплайна)
└── compatibility/      # Совместимость сборок
```

## Law Schema

```yaml
derived_fact:
  id: "{unique-slug}"
  type: "law"                     # law | pattern | comparison
  level: 2                        # Level 2 = Law (ADR-017 hierarchy)
  statement: "{engineering finding}"
  confidence: {0-1}
  confidence_basis: "{training_data | observation | multi_source}"
  domain: "{engineering | competitive | compatibility}"

lineage:
  nodes:
    - ref: "fact/cpu_observations/{id}.yaml"
      role: "{evidence | baseline | reference | counterexample}"
      level: 0
  edges:
    - from: "fact/cpu_observations/{id}.yaml"
      to: "{law-id}"
      type: "generalizes"         # generalizes | supports | contradicts | derived_from | materializes | refines

relationships:
  contradicts: []                 # Law, которые этот Law оспаривает
  refines: []                     # Law, которые этот Law уточняет
  refined_by: []                  # Law, которые уточняют этот Law

meta:
  observed_at: "{iso-date}"
  observed_by: "{agent-id}"
  source_url: "{agent-session-reference}"
  note: "{context}"
```

## Уровни вывода (ADR-017)

```
Level 0: Dimension, Fact (Observation, Metric)  ← первичные данные
Level 1: Comparison                             ← сопоставление первичных данных
Level 2: Law, Pattern                           ← интерпретация
Level 3: Artifact                               ← готовый продукт
```

Правило: узел уровня N ссылается ТОЛЬКО на узлы уровней < N.
Law (L2) → Comparison (L1) → Fact (L0).
