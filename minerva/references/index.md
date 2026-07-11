# Minerva Workspace

Карта всех контекстов знаний. Единая точка входа для discoverability — агент начинает здесь.

## Контексты

### coffee

- **Путь:** `references/coffee/`
- **Статус:** active (образцовый контекст)
- **Описание:** Модели заваривания кофе, параметры экстракции, напитки и техники.
- **Primitives (6):** Espresso (Concept), Extraction Yield (Metric), Bloom (Observation), Pump Pressure 9 bar (Specification), Extraction Law (Law), Espresso requires Fine Grind (Relation)
- **Связан с:** _пока нет (equipment будет отдельным контекстом)_

### hardware

- **Путь:** `references/hardware/`
- **Статус:** migrating (исходные данные + начато создание minerva Primitives)
- **Описание:** База знаний по компьютерному железу. GPU, CPU, материнские платы, память, блоки питания, аудиоинтерфейсы.
- **Структура:** `catalog/` (75+ legacy-записей), `concepts/` (12 концептов), `primitives/` (3 Primitives: Concept, Specification, Observation)
- **Связан с:** _пока нет_
- **Примечание:** Идёт миграция из legacy-формата (`type: gpu/cpu`) в minerva-таксономию. Legacy-записи сохраняются как reference.

## Связи контекстов

Пока workspace содержит два несвязанных контекста. Формат связей (ADR-008) — Partnership, Shared Kernel, Customer–Supplier, Conformist, ACL, OHS, Published Language, Separate Ways — будет применяться при появлении зависимостей.

## Навигация для агентов

```
1. skill_view("minerva") → SKILL.md (оркестратор)
2. skill_view("minerva", file_path="references/index.md") ← вы здесь
3. skill_view("minerva", file_path="references/{context}/index.md") → контекст
4. skill_view("minerva", file_path="references/{context}/{level}/{file}.md") → знание
```

**Правило:** агент всегда загружает `references/index.md` после SKILL.md для обнаружения контекстов. Никаких `ls` или `find`.
