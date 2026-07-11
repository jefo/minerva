# Coffee Context

Модели заваривания кофе, параметры экстракции, напитки и техники.

## Границы

В этом контексте: понятия, связанные с приготовлением кофе как напитка. Оборудование (кофемолки, машины) — в отдельном контексте `equipment/` (будет добавлен).

## Primitives (6)

| Файл | Тип | Суть |
|---|---|---|
| `espresso.md` | Concept | Базовый концепт: эспрессо как напиток |
| `extraction-yield.md` | Metric | Измеряемый параметр: процент экстракции |
| `bloom-observation.md` | Observation | Эмпирический факт: 30 сек при grind size 15 |
| `pump-pressure.md` | Specification | Техническое требование: 9 bar |
| `extraction-law.md` | Law | Инвариант: связь времени, температуры и помола |
| `espresso-requires-fine-grind.md` | Relation | Связь: эспрессо → мелкий помол |

## Components, Modules, Views, Artifacts

Пока пусты. Композиция начнётся на Tier 2+.

## Правила

- Primitives создаются строго по таксономии (ADR-004): Concept, Metric, Observation, Specification, Law, Relation
- Каждый Primitive — отдельный `.md` файл с YAML frontmatter
- Frontmatter обязателен: `title`, `type`, `status`
