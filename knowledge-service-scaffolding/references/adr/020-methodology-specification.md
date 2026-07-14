---
id: adr-020
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [methodology, kimball, star-schema, scd, etl-rules, data-marts, design-rules]
based_on: [adr-014, adr-015, adr-016, adr-017, adr-018, adr-019]
---

# ADR-020: Methodology Specification — правила проектирования для minerva

## Контекст

ADR-014 принял Data Warehouse как методологический фундамент. ADR-015–019 определили системную архитектуру, модель данных, lineage, ETL и query model. Теперь нужно ответить на практический вопрос: **как именно мы применяем Kimball/Inmon в рамках minerva?** Какие конкретные правила проектирования действуют при построении Warehouse, ETL и Data Marts?

Этот ADR — мост между «DW — наша методология» и «вот как это работает в файлах». Здесь нет схем данных — они в ADR-016. Здесь нет архитектуры компонентов — она в ADR-015. Здесь — **правила, которым следует разработчик (человек или агент) при проектировании в рамках minerva.**

## Решение

### 1. Что мы берём у Kimball и как адаптируем

Kimball — основной источник. Inmon и Data Vault — rejected (см. секцию 5).

#### 1.1 Star Schema (Kimball, Chapter 2)

**Kimball:** Fact table в центре, Dimension tables вокруг. Fact → Dimension = many-to-one. Каждая Dimension — единая таблица (не нормализованная — «wide table»).

**В minerva:**

```
Правило: Fact → Dimension через dimension_refs (ADR-016)
         Dimension — один файл со всеми атрибутами (wide)
         Никакой нормализации Dimension (не snowflake)

Файловая проекция:
  fact/observations/{fact}.yaml
    dimensions:
      gpu: "dim/gpu/nvidia-rtx-5060.yaml"         ← одна ссылка, не join
      game: "dim/game_title/cyberpunk-2077.yaml"
```

**Правила:**
- **Dimension — wide.** Все атрибуты GPU в одном файле. Не разносить vendor, architecture, lithography по отдельным Dimension (это snowflake, не star)
- **Исключение — иерархии.** Архитектура → GPU (один Architecture Dimension, много GPU Dimensions ссылаются на него через `relationships.architecture_ref`). Это единственное нормализованное отношение — иерархия, не snowflake
- **Fact ссылается на Dimensions на самом низком уровне.** Fact наблюдения ссылается на конкретный GPU, не на архитектуру. Архитектура — через Dimension иерархию

#### 1.2 Fact Table Granularity (Kimball, Chapter 3)

**Kimball:** каждая запись в Fact table — одно бизнес-событие на атомарном уровне. Никакой пре-аггрегации. «Продажа» — строка, не «продажи за день».

**В minerva:**

```
Правило: Observation Fact = одно измерение в конкретных условиях.
         Никогда не «средний FPS RTX 5060 в 1440p».
         Всегда «FPS RTX 5060 в CP2077 1440p High на драйвере 572.16».

Пример:
  ✅ fact/observations/rtx5060-cp2077-1440p-high-driver572.yaml
     → один FPS, одна игра, один пресет, один драйвер

  ❌ fact/metrics/rtx5060-average-fps-1440p.yaml
     → аггрегация. Результат сравнения — в Data Marts, не в Warehouse
```

**Правила:**
- **Observation Fact — атомарен.** Одно измерение в уникальных условиях
- **Metric Fact — additive.** FP32 TFLOPS, bandwidth — это тоже атомарно: один GPU, одна метрика
- **Никакой пре-аггрегации в Warehouse.** «Средний FPS RTX 5060 в 1440p» — это вычисление в Data Mart (`comparison` capability), не хранение
- **Исключение — Materialized View.** Artifact хранит результат аггрегации, но помечен как derived и `stale_if`

#### 1.3 Fact Additivity (Kimball, Chapter 3)

**Kimball:** различает additive (можно суммировать — продажи), semi-additive (можно суммировать по одним измерениям, не по другим — баланс), non-additive (не суммируется — цена за единицу).

**В minerva:**

| Тип Fact | Additivity | Правило |
|---|---|---|
| **Observation (FPS)** | Semi-additive | FPS нельзя суммировать (два FPS не дают «общий FPS»). Можно усреднять по game_title, driver_version. Нельзя — по resolution |
| **Metric (TFLOPS, bandwidth)** | Additive | TFLOPS двух GPU можно суммировать (total compute) |
| **Metric (price)** | Non-additive | Цена не суммируется. Можно усреднять |

**Правило для агента:** capability `comparison` знает additivity каждого fact_type и применяет корректную аггрегацию. «Сравни bandwidth RTX 5060 и RTX 4060» — additive, сравнивает значения. «Сравни FPS» — semi-additive, сравнивает в рамках одного game_title + resolution.

#### 1.4 Conformed Dimensions + Bus Architecture (Kimball, Chapter 4)

**Kimball:** все Data Marts используют одни и те же Dimensions (conformed). Bus Matrix показывает какие Dimensions используются в каких Data Marts. Это позволяет cross-mart queries.

**В minerva:**

```
Правило: bus-matrix.yaml — SSOT Dimensions.
         Data Mart НЕ создаёт свой вариант «CP2077».
         Использует canonical_dim из Bus Matrix.

Реализация в ADR-016: bus-matrix.yaml.
```

**Правила:**
- **Единственный источник имён.** Bus Matrix — SSOT. Никаких «CP2077» в одном View и «Cyberpunk 2077» в другом
- **Aliases только для Acquisition.** Когда ETL парсит «CP2077», резолвит через Bus Matrix. Data Marts всегда используют canonical
- **Conformed Dimension — файл с атрибутами.** `dim/game_title/cyberpunk-2077.yaml` содержит все атрибуты игры (жанр, год, движок). Все Data Marts ссылаются на него
- **Новый Dimension → Bus Matrix.** Без регистрации Data Marts его не видят

#### 1.5 Slowly Changing Dimensions (Kimball, Chapter 5)

**Kimball:** SCD Types 0–7. Основные: Type 1 (overwrite), Type 2 (track history), Type 3 (add previous value column).

**В minerva (адаптировано из ADR-016):**

| SCD Type | Когда | Файловая реализация | Правило |
|---|---|---|---|
| **Type 0** — immutable | Architecture, lithography | Никаких версий. При изменении → новый Dimension | «Blackwell» → новый файл |
| **Type 1** — overwrite | MSRP, цена | Git-history хранит. Файл перезаписывается | Только для volatile атрибутов |
| **Type 2** — track history | Driver version, game patch | Заголовочный файл + файлы-версии | Для Dimensions где важна история |
| **Type 3** — current + previous | Критические метрики | В одном файле: `value` + `value_prev` | Редко: только для трендов |

**Правила:**
- **Каждый Dimension-файл имеет `scd_type`. Обязательно**
- **SCD Type 2 — заголовочный файл содержит `current_version`.** Нельзя обновлять Fact, ссылающийся на старую версию — Fact всегда ссылается на конкретную версию
- **Impact analysis при SCD Type 2.** Новая версия Dimension → `impact-analysis` → какие Laws затронуты?
- **SCD Type 4 (mini-dimension) — rejected.** Для GPU с rapidly changing attributes используем Type 2, не разносим на mini-Dimensions

#### 1.6 Surrogate Keys (Kimball, Chapter 2)

**Kimball:** каждая Dimension и Fact имеет DW-generated surrogate key, независимый от source system ID.

**В minerva — адаптировано:**

```
Правило: наш «surrogate key» = относительный путь к файлу.

  dim/gpu/nvidia-rtx-5060.yaml     ← это и идентификатор, и адрес
  dim/gpu/nvidia-rtx-4060.yaml     ← уникален в пределах контекста

  Преимущество: путь к файлу = ключ. Никакого mapping'а
  Ограничение: переименование файла = новый ключ (git может отследить)
```

**Правила:**
- **id в frontmatter = последний сегмент пути.** `nvidia-rtx-5060.yaml` → id: `nvidia-rtx-5060`
- **Переименование = новый Dimension.** Git-history отслеживает. Старые ссылки — битые → `LINEAGE_BROKEN`
- **Нет числовых суррогатов.** Путь файла — достаточный идентификатор для масштаба minerva

#### 1.7 Degenerate Dimensions (Kimball, Chapter 2)

**Kimball:** иногда Dimension не имеет собственных атрибутов — только ключ (например, номер транзакции). Такие ключи хранятся прямо в Fact без отдельной Dimension-таблицы.

**В minerva:**

```
Пример: resolution (1080p, 1440p, 4K).
  Это Dimension (есть canonical_values в bus-matrix.yaml).
  Но атрибутов у него нет — только значение.
  Реализация: файл dim/resolution/1440p.yaml с единственным атрибутом value: "1440p".
  Не degenerate в классическом смысле, но близко.
```

**Правило:** даже degenerate Dimensions имеют файл. Это сохраняет единообразие: все Dimension → файлы. Bus Matrix отслеживает canonical_values.

### 2. Как мы делаем ETL (правила, адаптированные под файлы)

#### 2.1 Extract: source system independence

**Kimball:** ETL должен быть независим от source systems. Изменение схемы источника не ломает warehouse.

**В minerva:**

```
Правило: source-extract производит acquisition/raw/ (сырые).
         transform-normalize преобразует в acquisition/staged/ (near-warehouse).
         warehouse-load пишет в warehouse/.

         Источник изменил схему → правим mapping, не warehouse.
```

#### 2.2 Transform: late-arriving data

**Kimball:** данные могут прийти позже. Например, FPS для игры, которая вышла месяц назад.

**В minerva:**

```
Правило: Fact всегда инсертится, никогда не обновляется.
         Late-arriving Observation → новый Fact файл.
         date_observed в Fact = когда измерено, не когда загружено.

  fact/observations/rtx5060-aw2-1440p-driver572.yaml
    meta:
      observed_at: "2026-02"        # когда измерено
      acquired_at: "2026-07-11"     # когда попало в Warehouse
```

#### 2.3 Transform: data quality

**Kimball:** ETL должен проверять качество: completeness, validity, consistency.

**В minerva:**

| Проверка | Где | Действие при fail |
|---|---|---|
| Все dimension_refs ведут на существующие файлы | warehouse-load | Ошибка, не загружать |
| Значения в ожидаемом диапазоне (FPS > 0, FPS < 1000) | transform-normalize | Маркировать `confidence: low`, загрузить |
| Дубликат Fact (те же условия, те же значения) | transform-normalize | Пропустить (idempotent) |
| Противоречие (те же условия, разные значения) | transform-normalize | `conflict-detect` → contested |

#### 2.4 Load: transaction integrity

**Kimball:** ETL должен быть restartable и не оставлять partial data.

**В minerva:**

```
Правило: warehouse-load атомарен на уровне одного файла.
         Cross-file consistency — через git commit всех изменений одной операцией.

  dim-upsert → создан файл
  fact-insert → создан файл
  git add dim/... fact/...
  git commit -m "acquisition: RTX 5060 CP2077 1440p observation"

  Если git commit failed → git reset, повторить
```

### 3. Как мы проектируем Data Marts

#### 3.1 Data Mart = View над Warehouse-данными

**Kimball:** Data Mart — это подмножество warehouse, организованное под конкретную бизнес-задачу. Может содержать агрегаты, не хранящиеся в warehouse.

**В minerva:**

```
Правило: Data Mart = директория в marts/ + capability для построения.
         Data Mart НЕ дублирует данные из Warehouse.
         Содержит: derived Facts (Laws, Comparisons), указатели на Warehouse-файлы.
```

#### 3.2 Какие Data Marts нам нужны

Из ADR-015:

| Data Mart | Бизнес-задача | На каких данных | Тип |
|---|---|---|---|
| **Coverage** | Что покрыто измерениями, что нет | Fact: Observations × Dim: Game, Resolution | Conformed |
| **Engineering** | Инженерные решения и компромиссы | Dim: GPU/CPU + Fact: Metrics + Laws | Derived |
| **Competitive** | Сравнение с конкурентами | Dim: GPU (все vendor) + Fact: Observations | Cross-vendor |
| **Narrative** | Когнитивная траектория для статьи | Dim: GPU + Fact: Laws + Lineage DAG | Presentation |
| **Tradeoff** | Что пришлось пожертвовать | Fact: Observations × Dim: Price, Platform | Derived |
| **Compatibility** | Что с чем работает | Dim: GPU, CPU, MB + Relations | Topology |

#### 3.3 Правила проектирования Data Mart

**Правило 1: Data Mart начинается с вопроса.** Не «какие данные у нас есть?», а «на какой вопрос отвечает этот Data Mart?»

- Coverage View → «В каких играх и разрешениях у нас есть данные для RTX 5060?»
- Engineering View → «Какие инженерные решения определяют характер RTX 5060?»
- Competitive View → «Где RTX 5060 выигрывает/проигрывает конкурентам?»
- Narrative View → «Какие misconceptions читателя разрушает RTX 5060?»

**Правило 2: Data Mart = capability + данные.** Capability строит представление из Warehouse-данных по запросу. Не пре-вычисляется (кроме Artifacts).

**Правило 3: Cross-mart consistency через Conformed Dimensions.** Coverage View и Competitive View используют один и тот же `dim/game_title/cyberpunk-2077.yaml`. Никаких «CP2077» vs «Cyberpunk 2077».

**Правило 4: Data Mart может содержать derived Facts.** Но derived Fact всегда имеет lineage DAG, уходящий в Warehouse. «GDDR7 Bandwidth Compensation Law» — в Engineering Mart. Его lineage → три Fact в Warehouse.

### 4. Антипаттерны (что НЕ делаем)

| Антипаттерн | Почему это плохо | Правильно |
|---|---|---|
| **Аггрегация в Warehouse** | Теряем атомарность. «Средний FPS» скрывает выбросы | Аггрегировать в Data Marts. Warehouse — атомарные Facts |
| **Разные имена для одного Dimension в разных Marts** | Ломает cross-mart анализ | Bus Matrix + canonical имена |
| **Derived Fact без lineage** | Непроверяемо. Мнение, не знание | Каждый Law — lineage DAG до исходных Facts |
| **SCD Type 2 для всего** | Взрыв версий. 100 драйверов = 100 файлов | SCD Type 2 только для Dimensions где история критична |
| **Fact с dimension-атрибутами** | Смешение. FPS + «GPU архитектура: Blackwell» | Атрибуты → Dimension. Fact → только измерения + ссылки |
| **Прямая запись в Data Mart минуя Warehouse** | Две копии данных. Какая — истина? | Все данные → Warehouse. Data Marts → derived |
| **ETL, который «чинит» данные молча** | Теряется traceability. «Откуда 355 GB/s?» | Все трансформации — в mapping. Конфликты — contested |

### 5. Что мы НЕ берём из DW

| Концепт | Почему rejected |
|---|---|
| **Inmon: 3NF Corporate Information Factory** | Нормализация до 3NF избыточна для масштаба сотен записей. Star Schema (денормализованные Dimensions) достаточно |
| **Data Vault: Hub/Link/Satellite** | Аудит и гибкость DV важны для enterprise-scale. Для minerva — overengineering. Три типа сущностей вместо двух |
| **Строгая типизация (Snowflake schema)** | Dimensions — wide tables. Агенты читают один файл и видят все атрибуты GPU. Join'ы через relationships — только для иерархий |
| **ETL-оркестраторы (Airflow, dbt)** | Capabilities + git workflow покрывают 100% наших ETL-потребностей |
| **Columnar storage (Parquet, ORC)** | Файлы формата YAML/Markdown. Масштаб не требует колоночного хранения |
| **OLAP-кубы** | Аггрегация — через capabilities, не pre-computed кубы |
| **Real-time/streaming ETL** | Batch достаточно. ИгроЛаба обновляет обзоры не ежеминутно |

### 6. Приоритет внедрения

Методология применяется немедленно при построении нового minerva. Порядок:

1. **Bus Matrix** — первый артефакт. Определить Dimensions для hardware-контекста
2. **Dimension-файлы** — первые 15 GPU + связанные Dimensions (game_title, resolution, driver_version)
3. **Fact-файлы** — Observations для мигрированных GPU
4. **Data Marts** — Coverage View (наиболее атомарный), затем Engineering, Competitive
5. **Lineage DAG** — по мере создания derived Facts

## Последствия

**Что становится проще:**
- **Проектирование.** Разработчик открывает ADR-020 и видит правила. «Как хранить FPS? Fact: Observation, атомарно, с dimension_refs.» Всё
- **Консистентность.** Все Data Marts ссылаются на одни Dimensions через Bus Matrix. Cross-mart анализ — естественно
- **Обучение агентов.** SKILL.md ссылается на ADR-020 как на «methodology specification». Агент знает не только ЧТО делать, но КАК проектировать
- **Отказ от лишнего.** Inmon 3NF, Data Vault, OLAP-кубы — явно rejected. Никаких «а может нам нормализовать?»

**Что требует дисциплины:**
- **Правила — ограничения, не предложения.** «Fact не содержит dimension-атрибутов» — это правило. Нарушение = баг
- **Bus Matrix — living.** Каждый новый Dimension → регистрация. Без этого Data Marts расходятся
- **Атомарность Facts.** Соблазн сохранить «средний FPS по 1440p» велик. Но это ломает гранулярность и делает невозможным пересчёт при новых данных
