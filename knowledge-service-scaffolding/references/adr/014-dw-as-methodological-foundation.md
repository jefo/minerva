---
id: adr-014
status: accepted
date: 2026-07-11
supersedes: [adr-002, adr-004]
superseded_by: []
tags: [architecture, data-warehouse, methodology, kimball, dimensional-modeling, lineage, scd]
based_on: [adr-012, adr-013, observation-003]
---

# ADR-014: Data Warehouse как методологический фундамент minerva

## Контекст

Observation 003 выявил полный структурный изоморфизм между архитектурой minerva (после ADR-012 + ADR-013) и методологией Data Warehouse (Kimball/Inmon). Совпадение не поверхностное: мы решаем ту же задачу — «разрозненные источники → согласованная аналитика» — просто с файлами и LLM-агентами вместо SQL и BI-дашбордов.

Текущий фундамент (ADR-002 — Five-level hierarchy, ADR-004 — Primitive types) спроектирован без осознанной опоры на DW. В результате: терминология нестандартна, lineage — плоское а не DAG, SCD отсутствует, Dimensions не конформированы.

Принятие DW как методологической основы даёт нам: (1) проверенную архитектурную модель, (2) терминологию, понятную AI-агенту без дополнительных объяснений, (3) готовые решения для краевых случаев, которые мы ещё не встретили.

## Решение

**Data Warehouse (Kimball) принимается как методологический фундамент minerva.**

Структура и терминология системы приводятся в соответствие с DW-концепциями. При этом реализация остаётся agent-native: файлы в git, LLM-агенты как потребители, markdown/YAML как формат хранения.

### DW-принципы: что принимаем как есть

#### 1. Single Source of Truth

**DW:** все данные имеют один авторитетный источник. Derived данные не хранятся — пересчитываются.

**В minerva:** Backend — SSOT. Frontend Primitives не дублируют backend-данные (`derived_from` вместо копирования). Уже зафиксировано в ADR-013, теперь явно называется SSOT.

#### 2. Dimensional Modeling (Star Schema)

**DW:** данные моделируются как Facts (измеряемые события) + Dimensions (контекст). Star Schema: Fact table в центре, Dimension tables вокруг.

**В minerva:** Primitives делятся на Fact-подобные и Dimension-подобные:

```
Fact-like Primitives (измеряемые):
  - Observation: «CP2077 1440p High = 68 fps на RTX 5060 с драйвером 572.16»
  - Metric: «FP32: 15.1 TFLOPS»
  - (Law — derived fact)

Dimension-like Primitives (контекст):
  - Specification: «RTX 5060: 8GB GDDR7, 128-bit, 355 GB/s»
  - Concept: «Blackwell Architecture»
  - Relation: «RTX 5060 → requires → PCIe 5.0 x8»
```

Это не просто переименование — это **структурное решение**: Fact всегда имеет ссылки на Dimensions (какой GPU, какой драйвер, какая игра), а Dimension не ссылается на Fact. Star Schema в файлах.

#### 3. Data Lineage как DAG

**DW:** каждый производный элемент знает точную цепочку transformation от исходных данных.

**В minerva:** `derived_from` становится не плоским списком, а направленным ациклическим графом (DAG) с типами рёбер:

```yaml
# Law: GDDR7 Bandwidth Compensation
lineage:
  - from: backend/hardware/gpu/nvidia-rtx-5060.yaml     # Observation: 355 GB/s
    type: observes
  - from: backend/hardware/gpu/nvidia-rtx-4060.yaml     # Observation: 272 GB/s
    type: observes
  - from: backend/hardware/gpu/nvidia-rtx-4070.yaml     # Observation: 504 GB/s
    type: observes
  - from: frontend/primitives/comparisons/rtx5060-vs-4060-bandwidth.yaml
    type: derived_from
    role: intermediate_comparison
```

Типы рёбер: `observes`, `derived_from`, `generalizes`, `contradicts`, `supports`, `refines`.

#### 4. Conformed Dimensions (Kimball Bus Architecture)

**DW:** все Data Marts используют одинаковые определения Dimensions. «Customer» в Sales Mart и «Customer» в Support Mart — одна и та же сущность.

**В minerva:** `context-map.md` становится **Bus Matrix**:

```yaml
# Bus Matrix: Dimensions × Views
dimensions:
  game_title:        # Conformed Dimension
    canonical: "Cyberpunk 2077"
    aliases: ["CP2077", "Cyberpunk"]
    used_in: [coverage-view, competitive-view, narrative-view]
  resolution:
    canonical_values: ["1080p", "1440p", "4K"]
    used_in: [coverage-view, engineering-view]
  driver_version:
    format: "XXX.XX"
    used_in: [coverage-view, narrative-view]
```

#### 5. Slowly Changing Dimensions (SCD)

**DW:** данные меняются во времени. SCD определяет стратегию: перезаписать (Type 1), сохранить историю (Type 2), хранить предыдущее значение (Type 3).

**В minerva:** Backend-файлы поддерживают SCD:

| SCD Type | Применение в minerva | Пример |
|---|---|---|
| **Type 0** — immutable | Architecture generation, lithography | «Blackwell» никогда не изменится |
| **Type 1** — overwrite | MSRP, рыночная цена | $299 → $279 |
| **Type 2** — new version | Observations при смене драйвера | `nvidia-rtx-5060_v572.16.yaml` → `nvidia-rtx-5060_v575.10.yaml` |
| **Type 3** — current + previous | Критические метрики где нужно видеть тренд | `fps_cp2077: 73`, `fps_cp2077_prev_driver: 68` |

Ключевое: SCD Type 2 для Observations. Каждый Observation привязан к версии драйвера/прошивки. Law, выведенный из Observations на драйвере 572.16, может быть перепроверен когда появляется драйвер 575.10. Lineage DAG сохраняет эту связь.

#### 6. Materialized Views с refresh policy

**DW:** предвычисленные представления для производительности. Знают когда устарели.

**В minerva:** `artifact-compile` → Artifact = Materialized View:

```yaml
# frontend/artifacts/rtx-5060-review.yaml
type: Artifact
materialized_from:
  - view: coverage-view
  - module: gb206-analysis
materialized_at: "2026-07-11"
data_as_of: "2026-07-10"        # на какой момент данные
stale_if:
  - backend/hardware/gpu/nvidia-rtx-5060.yaml  # изменился backend → stale
  - frontend/primitives/laws/gddr7-bandwidth-compensation.yaml  # новый Law → stale
status: fresh                     # fresh | stale | regenerating
```

### DW-принципы: что адаптируем

#### ETL → File-based pipeline с git

**DW:** Extract → Transform → Load через ETL-инструменты.

**В minerva:** ETL реализован файловым пайплайном. Git-history = audit trail. Acquisition capabilities = Extract. Backend schema conventions = Transform. Frontend Views = Load.

#### SQL → LLM-agent queries

**DW:** аналитика через SQL-запросы к warehouse.

**В minerva:** аналитика через LLM-агентов, читающих файлы. `skill_view` = аналог `SELECT`. Capabilities = аналог stored procedures.

#### BI Dashboards → Artifacts

**DW:** потребители — BI-инструменты (PowerBI, Tableau).

**В minerva:** потребители — `artifact-compile`, собирающий страницы. И LLM-агенты, строящие выводы напрямую из Backend + Views.

### DW-принципы: от чего отказываемся

- **Columnar storage.** Наши «таблицы» — markdown/YAML файлы в git. Масштаб (сотни, не миллиарды записей) не требует колоночного хранения
- **Real-time ETL.** Git-based pipeline по определению batch. Принимаем eventual consistency
- **OLAP-кубы.** Аггрегации живут в агентских выводах, не в предвычисленных кубах
- **Строгая нормализация (3NF).** Dimensional modeling (star schema) достаточно. Полная нормализация избыточна для масштаба minerva

### Рефакторинг текущей таксономии под DW

ADR-002 (Five-level hierarchy) и ADR-004 (Primitive types) перечитываются в DW-терминах:

| Было (ADR-002/004) | Стало (DW) | Семантика |
|---|---|---|
| Primitive: Concept | Dimension | Описательный атрибут |
| Primitive: Specification | Dimension | Структурный атрибут сущности |
| Primitive: Metric | Fact (additive) | Измеряемая величина |
| Primitive: Observation | Fact (event) | Измерение в конкретных условиях |
| Primitive: Law | Derived Fact | Вывод из Facts + Dimensions |
| Primitive: Relation | Dimension Relationship | Связь между Dimensions |
| Component | Aggregate Fact Table | Группа связанных Facts |
| Module | Star Schema | Fact + Dimensions для домена |
| View | Data Mart | Подмножество warehouse под задачу |
| Artifact | Materialized View | Предвычисленный результат |

### Структура minerva после рефакторинга

```
minerva/
├── SKILL.md                       # оркестратор
├── capabilities/                  # = stored procedures
├── acquisition/                   # = ETL Extract
│   └── sources/                   # сырые данные от поставщиков
├── backend/                       # = Integrated Warehouse (SSOT)
│   ├── bus-matrix.yaml            # Conformed Dimensions (Kimball Bus)
│   ├── hardware/
│   │   ├── dim/                   # Dimensions: GPU, CPU, Game Title, ...
│   │   │   ├── gpu/
│   │   │   │   ├── nvidia-rtx-5060.yaml       # SCD-enabled Dimension
│   │   │   │   ├── nvidia-rtx-5060_v572.16.yaml  # SCD Type 2: historical
│   │   │   │   └── nvidia-rtx-4070.yaml
│   │   │   └── game_title/
│   │   │       └── cyberpunk-2077.yaml        # Conformed Dimension
│   │   └── fact/                  # Facts: Observations, Metrics
│   │       └── observations/
│   │           └── rtx5060-cp2077-1440p.yaml  # Fact → ссылается на Dimensions
│   └── coffee/
│       ├── dim/
│       └── fact/
└── frontend/                      # = Data Marts (Atomic Design)
    ├── coverage-view/             # Data Mart
    ├── engineering-view/          # Data Mart
    ├── competitive-view/          # Data Mart
    ├── narrative-view/            # Data Mart
    └── artifacts/                 # Materialized Views
```

**Ключевые сигналы для AI-агента:**

- `backend/dim/` и `backend/fact/` → «это dimensional model. Facts ссылаются на Dimensions. Dimensions конформированы через bus-matrix.yaml»
- `bus-matrix.yaml` → «Kimball Bus Architecture. Все Data Marts разделяют эти Dimensions»
- `lineage:` DAG в каждом derived Fact → «полная прослеживаемость от вывода к исходному Observation»
- `scd_type:` в Dimensions → «это Slowly Changing Dimension. Смотри исторические версии»
- `stale_if:` в Artifacts → «Materialized View. Проверь не устарел ли»

Агент, загружающий `backend/dim/gpu/nvidia-rtx-5060.yaml`, видя `scd_type: 2`, понимает: «есть исторические версии. Посмотрю `nvidia-rtx-5060_v572.16.yaml` для контекста открытия Laws».

## Что НЕ фиксируем

- **Конкретный формат SCD Type 2.** Отдельные файлы-версии? Append-only YAML с временными метками? Git-history как SCD? Решается при реализации
- **Степень нормализации Dimensions.** Snowflake (нормализованные) vs Star (денормализованные) — для масштаба minerva Star Schema достаточно
- **ETL-инструменты.** Остаёмся на файлах + git. Никаких Apache Airflow в обозримом будущем
- **Миграция существующих данных.** `catalog/` → `backend/dim/` + `backend/fact/` — отдельный проект

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Оставить текущую таксономию без DW-фундамента | Не требует рефакторинга | Терминология нестандартна, lineage плоское, SCD отсутствует, Dimensions не конформированы | Уже видим проблемы: Observation 001 (Atomic Design vs Aggregate), Observation 002 (NotebookLM gap) — все они решаются DW-подходом |
| Data Vault (Inmon) вместо Kimball | Лучше для rapidly changing schemas | Сложнее ментальная модель. Hub/Link/Satellite избыточны для масштаба сотен записей | Kimball проще для понимания и ближе к тому что мы уже построили |
| Entity-Relationship модель (OLTP) | Строгая нормализация | OLTP оптимизирован для транзакций, не аналитики. Нам нужна аналитика | Мы — analytical system, не transactional |
| Свой велосипед без оглядки на DW | Полная свобода | Изобретаем решения для проблем, которые DW-сообщество решило 20 лет назад | SCD, Conformed Dimensions, Lineage DAG — решённые проблемы. Глупо переизобретать |

## Связь

- **ADR-012 (Acquisition):** теперь читается как «ETL Extract layer»
- **ADR-013 (Backend/Frontend):** теперь читается как «Warehouse + Data Marts»
- **ADR-002 (Five-level hierarchy):** реинтерпретирован в DW-терминах (см. таблицу выше)
- **ADR-004 (Primitive types):** реинтерпретированы как Facts/Dimensions (см. таблицу выше)
- **Observation 001:** SCD Type 2 решает проблему «один файл vs много версий» для исторических Observations
- **Observation 002:** Acquisition как ETL-extract закрывает gap с NotebookLM
- **Observation 003:** структурный изоморфизм, обосновавший этот ADR

## Последствия

**Что становится проще:**
- **Терминология — стандартная.** AI-агент, видя `dim/`, `fact/`, `bus-matrix.yaml`, `lineage:`, `scd_type:` — мгновенно понимает архитектурный паттерн. Никаких объяснений «у нас тут Primitives шести типов, но некоторые — это на самом деле Dimensions, а другие — Facts»
- **SCD даёт честность.** Law «GDDR7 Bandwidth Compensation» открыт на драйвере 572.16 — и это явно. Если драйвер 575.10 меняет FPS, мы знаем что перепроверить
- **Conformed Dimensions.** «CP2077» в Coverage View и «Cyberpunk 2077» в Competitive View — один dimension. bus-matrix.yaml гарантирует согласованность
- **Stale detection.** Artifact знает когда устарел. Backend изменился → Artifact `stale`. Не нужно ручной проверки
- **Lineage — DAG, не список.** Каждый Law знает не только *что* его поддерживает, но и *как* (observes → comparison → derivation)

**Что требует рефакторинга:**
- **ADR-002 и ADR-004 реинтерпретированы, но не отменены.** Их нужно дополнить DW-терминологией, не удаляя
- **Структура директорий.** `hardware/primitives/` → `backend/dim/` + `backend/fact/`. `references/` → `frontend/` (Data Marts)
- **Frontmatter-схемы.** Каждый файл должен сигнализировать DW-роль: `dimension:`, `fact_type:`, `lineage:`, `scd_type:`, `stale_if:`
- **bus-matrix.yaml.** Создать как SSOT Conformed Dimensions
- **minerva SKILL.md.** Обновить под DW-терминологию (v0.6.0)
- **Coffee-контекст.** Простой кандидат для первого DW-рефакторинга: 6 Primitives → Dimensions + Facts

**Что требует дисциплины:**
- **SCD не должен усложнить без необходимости.** Не каждое поле требует истории. SCD Type 0 для immutable полей, Type 1 для volatile. Type 2 только для Observations
- **Conformed Dimensions — не бремя, а контракт.** Если новый View хочет использовать game_title, он обязан использовать bus-matrix.yaml, а не своё название
- **Lineage DAG — не опционально.** Каждый derived Fact обязан иметь lineage. Без lineage — не Fact, а мнение
