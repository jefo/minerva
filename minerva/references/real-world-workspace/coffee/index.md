# Coffee Context

Модели заваривания кофе, параметры экстракции, напитки и техники.

## Границы

В этом контексте: понятия, связанные с приготовлением кофе как напитка. Оборудование (кофемолки, машины) — в отдельном контексте `equipment/` (будет добавлен).

## Сущности

- **Напитки:** Espresso, Filter Coffee, Cold Brew
- **Параметры:** Dose, Temperature, Pressure, Time, Ratio
- **Процессы:** Extraction, Bloom, Brewing

## Правила

- Primitives создаются строго по таксономии (ADR-004): Concept, Metric, Observation, Specification, Law, Relation
- Каждый Primitive — отдельный `.md` файл с YAML frontmatter
- Frontmatter обязателен: `title`, `type`, `status`
