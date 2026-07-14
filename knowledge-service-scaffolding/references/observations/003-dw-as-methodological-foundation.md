# Observation 003: Data Warehouse как методологический фундамент — структурный изоморфизм

**Date:** 2026-07-11
**Status:** open → accepted as architectural foundation
**Type:** architectural discovery — методологический изоморфизм

## Контекст

После ADR-012 (Acquisition layer) и ADR-013 (Backend/Frontend split) трёхслойная архитектура приобрела узнаваемую форму. При анализе этой формы обнаружился структурный изоморфизм с методологией Data Warehouse (Kimball, Inmon).

## Наблюдение: полный структурный изоморфизм

```
minerva (после ADR-013)          Data Warehouse (Kimball)

Acquisition                      Data Sources
  ↓                                ↓
Backend (raw data)               Staging → Integrated Warehouse
  ↓                                ↓
Frontend Views                   Data Marts
  Coverage View                  ← типичный Data Mart
  Engineering View               ← еще один Data Mart
  Competitive View               ← еще один Data Mart
  Narrative View                 ← еще один Data Mart
  ↓                                ↓
Artifact (страница)              Report / Dashboard
```

### 1. Понятийное совпадение

| minerva-понятие | DW-эквивалент | Совпадение |
|---|---|---|
| Observation Store | Staging Area | Полное |
| Backend (raw data) | Integrated Warehouse | Полное |
| Primitive (Specification) | Dimension table | Частичное |
| Primitive (Observation) | Fact table | Частичное |
| Coverage View | Data Mart | Полное |
| Engineering View | Data Mart | Полное |
| Competitive View | Data Mart | Полное |
| Narrative View | Data Mart | Полное |
| `derived_from` | Data Lineage | Частичное (плоское, не DAG) |
| `artifact-compile` | Materialized View | Полное |

### 2. DW-принципы, которые мы уже неявно реализовали

| DW-принцип | Где в minerva | Статус |
|---|---|---|
| Single Source of Truth | Backend — raw data, не дублируется | Неявно в ADR-013 |
| Data Lineage | `derived_from` в Primitives | Неявно, плоское |
| Materialized Views | `artifact-compile` | Неявно, без refresh |
| ETL pipeline | Acquisition → Backend → Frontend | Неявно, не названо ETL |
| Dimensional Modeling | Primitives делятся на Fact-подобные (Observation, Metric) и Dimension-подобные (Specification, Concept) | Неявно, без терминологии |

### 3. DW-принципы, которые мы НЕ реализовали — и теряем от этого

| Принцип | Что теряем | Пример |
|---|---|---|
| **Slowly Changing Dimensions** | История значений. FPS меняется с драйверами, MSRP — со временем. Без SCD теряем контекст открытия Laws | Law «GDDR7 Bandwidth Compensation» был открыт на драйвере 572.16. Драйвер 575.10 изменил FPS — Law всё ещё верен? Без SCD не проверить |
| **Conformed Dimensions** | Разные Views используют разные имена для одного измерения | «CP2077» в Coverage View vs «Cyberpunk 2077» в Competitive View — один dimension, но система не знает |
| **Lineage как DAG** | Не знаем порядок вывода. Observation → Comparison → Pattern → Law — это цепочка, а не плоский список родителей | `derived_from` не различает «это исходный Observation» и «это промежуточный Law» |
| **Materialized View staleness** | Artifact не знает что устарел. Backend изменился, страница — нет | RTX 5060 получила новый драйвер, FPS вырос. Обзор на сайте — старый |

### 4. Ключевое отличие: не инструмент, а потребитель

DW-сообщество строило системы для SQL-запросов и BI-дашбордов. minerva строит систему для **LLM-агентов** как потребителей. Но архитектурные принципы — те же:

- **Вместо SQL:** агент читает файлы и строит выводы
- **Вместо PowerBI:** `artifact-compile` собирает страницу
- **Вместо ETL-инструментов:** git-history как audit trail, файлы как транспорт
- **Вместо columnar storage:** markdown/YAML с LLM-friendly структурой

Архитектура — DW. Реализация — agent-native.

## Гипотеза

Data Warehouse как методологический фундамент даёт minerva:

1. **Проверенную архитектурную модель.** Kimball и Inmon решили задачу «разрозненные данные → согласованная аналитика» 30 лет назад. Их решения выдержали проверку временем
2. **Терминологию, понятную AI-агенту.** Когда агент видит «Fact table», «Dimension», «SCD Type 2», «Lineage DAG» — он мгновенно понимает архитектурный паттерн без дополнительных объяснений
3. **Решения для краевых случаев, которые мы ещё не встретили.** SCD, Conformed Dimensions, slowly changing hierarchy — DW community уже решило это. Не нужно изобретать
4. **Чёткую границу: что мы адаптируем, от чего отказываемся.** Файлы вместо SQL, агенты вместо BI — это осознанный выбор, не ignorance

## Следствия

1. **Текущий фундамент требует рефакторинга под DW-терминологию.** Структура директорий, имена файлов, frontmatter-схемы — всё должно сигнализировать агенту: «это Data Warehouse на файлах»
2. **ADR-002 (Five-level hierarchy) и ADR-004 (Primitive types) получают DW-прочтение.** Primitives — это не просто «6 типов», а Facts, Dimensions, и их производные
3. **Lineage должен стать DAG, не плоским списком.** Каждый узел знает не только родителей, но и тип отношения
4. **SCD нужно встроить в модель данных, не в реализацию.** Backend-файлы должны поддерживать историю значений без потери текущего состояния

## Связанные артефакты

- ADR-012: Acquisition layer — теперь читается как «Data Sources layer»
- ADR-013: Backend/Frontend split — теперь читается как «Warehouse + Data Marts»
- Observation 001: Atomic Design vs Aggregate — SCD и Dimensional Modeling дают альтернативный взгляд
- Observation 002: NotebookLM vs minerva — acquisition как ETL-extract решает этот gap
