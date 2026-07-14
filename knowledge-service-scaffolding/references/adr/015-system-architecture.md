---
id: adr-015
status: accepted
date: 2026-07-11
supersedes: [adr-009, adr-011]
superseded_by: []
tags: [architecture, system-design, warehouse, components, data-flow, agent-native]
based_on: [adr-012, adr-013, adr-014]
---

# ADR-015: System Architecture — minerva как agent-native Data Warehouse

## Контекст

ADR-014 принял Data Warehouse как методологический фундамент. Теперь нужно спроектировать архитектуру самой системы: компоненты, их ответственности, потоки данных и ключевые архитектурные решения, определяющие характер реализации.

Предыдущий PoC (minerva v0.5.0 с Tiers 0–4) доказал жизнеспособность skill-native подхода (ADR-010) и файлового KB (ADR-006), но его архитектура была спроектирована до принятия DW-методологии и содержала концептуальные смешения, устранённые ADR-013 (Backend/Frontend split) и ADR-014 (DW-фундамент).

Строим новую архитектуру на DW-фундаменте. PoC — в историю.

## Решение

### 1. Системный контекст

minerva — **agent-native analytical data warehouse.** Хранит факты и измерения в файлах, обслуживает LLM-агентов через capabilities (stored procedures), производит готовые страницы (materialized views) через композиционный движок.

```
                        ┌──────────────────────┐
                        │   LLM AGENTS          │
                        │   (Writer, Analyst,   │
                        │    Reviewer, etc.)    │
                        └──────────┬───────────┘
                                   │ skill_view, capabilities
        ┌──────────────────────────┼──────────────────────────┐
        │                    MINERVA                          │
        │                                                     │
        │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
        │  │ACQUISITION│  │ WAREHOUSE│  │   DATA MARTS     │  │
        │  │  (ETL)    │──│ (backend)│──│   (frontend)     │  │
        │  └──────────┘  └──────────┘  └──────────────────┘  │
        │        │              │                │            │
        │        └──────────────┼────────────────┘            │
        │                       │                             │
        │  ┌────────────────────┼──────────────────────┐      │
        │  │           CROSS-CUTTING SERVICES           │      │
        │  │  Lineage DAG │ Bus Matrix │ Materializer  │      │
        │  └────────────────────────────────────────────┘      │
        └─────────────────────────────────────────────────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │   PUBLISHED ARTIFACTS │
                        │   (страницы, обзоры,  │
                        │    гайды на сайте)    │
                        └──────────────────────┘
```

### 2. Компонентная модель

#### 2.1 Acquisition Layer (ETL Extract + Transform)

**Ответственность:** вытянуть данные из внешних источников, нормализовать, разрешить конфликты, записать в Warehouse.

**Не ответственность:** интерпретация данных, построение выводов. Acquisition — механический слой.

| Элемент | Описание |
|---|---|
| **Source Connectors** | Скрипты/агенты для каждого типа источников: YouTube транскрипты, TechPowerUp, NVIDIA specs, Reddit, ценовые агрегаторы |
| **Extract Pipeline** | Извлечение сырых данных: парсинг HTML, PDF, API, транскрипция |
| **Transform Pipeline** | Нормализация к внутренней схеме: единицы измерения, имена полей, разрешение конфликтов (два источника → разные цифры → маркировать contested) |
| **Load Pipeline** | Запись в Warehouse: создать/обновить Dimension и Fact файлы, применить SCD-стратегию |

**Граница:** Acquisition НЕ пишет в Data Marts. Только в Warehouse. Data Marts — это производные представления, не первичное хранилище.

#### 2.2 Warehouse (Backend) — SSOT

**Ответственность:** хранить все первичные и слабо-производные данные в dimensional model. Быть единственным авторитетным источником для всей системы.

**Не ответственность:** композиционные представления (Views), готовые артефакты, аналитические выводы.

Структура:

```
warehouse/
├── bus-matrix.yaml              # Conformed Dimensions (Kimball Bus)
├── hardware/
│   ├── dim/                     # Dimensions
│   │   ├── gpu/                 # один файл на GPU
│   │   │   ├── nvidia-rtx-5090.yaml
│   │   │   ├── nvidia-rtx-5060.yaml
│   │   │   └── ...              # SCD Type 2: исторические версии
│   │   ├── cpu/
│   │   ├── game_title/          # Conformed Dimension
│   │   │   ├── cyberpunk-2077.yaml
│   │   │   ├── alan-wake-2.yaml
│   │   │   └── ...
│   │   └── driver_version/      # Conformed Dimension
│   └── fact/                    # Facts
│       ├── observations/        # Fact: измерение в конкретных условиях
│       │   ├── rtx5060-cp2077-1440p-driver572.yaml
│       │   └── ...
│       └── metrics/             # Fact: additive измерение
│           ├── rtx5060-fp32.yaml
│           └── ...
├── coffee/
│   ├── dim/
│   │   ├── origin/              # Ethiopia, Colombia, ...
│   │   ├── variety/             # Geisha, Bourbon, ...
│   │   └── roast_level/
│   └── fact/
│       ├── observations/        # cupping scores
│       └── metrics/             # extraction yields
└── ...
```

**Ключевые свойства:**
- **SSOT:** любой факт существует ровно в одном месте
- **SCD-native:** Dimensions поддерживают Type 0/1/2 через `scd_type` в frontmatter
- **Domain-isolated:** hardware/ и coffee/ — разные bounded contexts. Никакой общей схемы
- **Файлы — граждане первого сорта:** не SQL-таблицы, а .yaml файлы в git. Git-history = audit trail

#### 2.3 Data Marts (Frontend) — аналитические витрины

**Ответственность:** предоставлять пред-организованные представления данных для конкретных аналитических задач. Композиционные единицы (Component, Module) и аналитические схемы (View).

**Не ответственность:** хранение первичных данных. Data Marts — всегда derived.

| Data Mart | Назначение | Основан на |
|---|---|---|
| **Coverage View** | Что покрыто, что нет: game×config матрица | Fact: Observations + Dim: Game Title |
| **Engineering View** | Инженерные решения: архитектура, компромиссы | Dim: GPU/CPU + Fact: Metrics |
| **Competitive View** | Сравнение с конкурентами: позиционирование | Dim: GPU (NVIDIA + AMD + Intel) + Fact: Observations |
| **Narrative View** | Когнитивная траектория: misconceptions, predictions | Dim: GPU + Fact: Laws + Lineage DAG |
| **Tradeoff View** | Что пришлось пожертвовать: gains vs costs | Fact: Observations + Dim: Price + Dim: Platform |
| **Compatibility View** | Что с чем работает: socket, чипсет, PCIe | Dim: Relation |

**Ключевое правило:** Data Mart НЕ дублирует данные из Warehouse. Он содержит **указатели** (`derived_from`) и **композиционную структуру**. Данные всегда читаются из Warehouse по ссылкам.

#### 2.4 Cross-cutting Services

##### Lineage DAG

**Ответственность:** отслеживать цепочку вывода каждого производного элемента: Observation → Comparison → Pattern → Law → Insight → Artifact.

```
Lineage DAG:
  Типы узлов:    Fact (Observation, Metric), Dimension, Law, Pattern, Artifact
  Типы рёбер:    observes, derived_from, generalizes, contradicts, supports, refines
  Traversal:     вверх (от вывода к источнику), вниз (от факта к выводам, которые от него зависят)
```

Lineage — не отдельный файл, а свойство каждого derived элемента. Law содержит `lineage:` DAG. Capability `lineage-trace` обходит граф.

##### Bus Matrix (Conformed Dimensions)

**Ответственность:** гарантировать что «Cyberpunk 2077» в Coverage View и «CP2077» в Competitive View — один dimension.

```yaml
# bus-matrix.yaml
dimensions:
  game_title:
    canonical: "Cyberpunk 2077"
    aliases: ["CP2077", "Cyberpunk"]
    dim_file: warehouse/hardware/dim/game_title/cyberpunk-2077.yaml
    used_in: [coverage-view, competitive-view, narrative-view]
```

Bus Matrix — **SSOT имён.** Если Data Mart хочет использовать dimension, он использует canonical-имя. Aliases — только для acquisition (распознавание входных данных).

##### Materialization Engine

**Ответственность:** компилировать Data Marts + Warehouse-данные в готовые Artifacts (страницы). Отслеживать staleness.

- `artifact-compile`: View + Module + актуальные данные из Warehouse → готовая страница
- `stale-check`: пробегает по `stale_if` каждого Artifact, сравнивает с датами модификации Warehouse-файлов
- `artifact-regenerate`: пересобирает stale Artifact

### 3. Data Flow

```
ВНЕШНИЕ ИСТОЧНИКИ
  │
  ▼
ACQUISITION (ETL)
  │ Extract: YouTube transcript → текст
  │ Transform: текст → нормализованные поля
  │ Load: запись в Warehouse с SCD-стратегией
  │
  ▼
WAREHOUSE (SSOT)
  │ dim/gpu/nvidia-rtx-5060.yaml        ← SCD Type 2: новая версия при смене драйвера
  │ fact/observations/rtx5060-cp2077.yaml ← новый Fact
  │ bus-matrix.yaml                      ← обновлён (новый game_title?)
  │
  ├─────────────────────────────────────┐
  ▼                                     ▼
DATA MARTS (derived views)         LINEAGE DAG (cross-cutting)
  │ coverage-view/                  │ каждый новый Fact получает lineage:
  │   обновлён: новый Fact          │   observes → dim/gpu/rtx5060
  │                                 │   observes → dim/game/cp2077
  ▼                                 │
MATERIALIZATION ENGINE              ▼
  │ artifact-compile:            CAPABILITIES (stored procedures)
  │   View + Module              │ lineage-trace: пройти от Law к исходным Facts
  │   + свежие данные            │ stale-check: какие Artifacts устарели?
  │   → страница                 │ cross-reference: все Facts для GPU X
  ▼
PUBLISHED ARTIFACTS
  rtx-5060-review.md → сайт
```

**Порядок записи (обязательный):**
1. Warehouse: создать/обновить Dimension
2. Warehouse: создать Fact (ссылается на Dimension)
3. Bus Matrix: проверить/добавить Dimension если новый
4. Lineage DAG: зафиксировать связи (Fact → Dimension)
5. Data Marts: перестроить затронутые представления
6. Materializer: пометить затронутые Artifacts как stale

### 4. Ключевые архитектурные решения

#### 4.1 Файлы — единственное хранилище

Никакой базы данных. Никакого API-сервера. Гигабайты — не наш масштаб. Сотни Dimensions, тысячи Facts — git справляется.

**Почему:** простота отладки (открыл файл — увидел данные), git-history = audit trail, LLM-friendly (агент читает файл напрямую), zero ops (никаких серверов).

**Цена:** нет конкурентного доступа, нет транзакций. Принимаем. Масштаб не требует.

#### 4.2 Dimensional Modeling (Kimball Star Schema)

Каждый bounded context содержит `dim/` (измерения) и `fact/` (факты). Facts ссылаются на Dimensions через `dimension_refs:`. Dimensions не ссылаются на Facts.

**Почему:** проверенная модель для аналитических нагрузок. Агент, читающий Fact, знает где искать контекст (по `dimension_refs`). Агент, читающий Dimension, знает что это описательный атрибут, не измерение.

#### 4.3 SCD Type 2 для Observations

Facts (Observations) исторически-зависимы: FPS меняется с драйверами. Каждый Observation привязан к версии контекста (драйвер, прошивка, патч игры).

**Реализация:** отдельный файл-версия для каждого значимого изменения контекста. `rtx5060-cp2077-1440p-driver572.yaml` → `rtx5060-cp2077-1440p-driver575.yaml`. Ссылка на текущую версию — в заголовочном файле.

**Почему:** без SCD Type 2 Laws теряют контекст открытия. «Этот Law был выведен на данных драйвера 572.16» — это эпистемическое утверждение. Без него Law — мнение.

#### 4.4 Lineage DAG — обязателен

Каждый derived элемент (Law, Pattern, Component, Artifact) имеет `lineage:` DAG с типизированными рёбрами. Не опционально.

**Почему:** без lineage Data Marts — это «потому что я так вижу». С lineage — «вот цепочка от исходного Observation до этого вывода, проверь каждый шаг».

**Типы рёбер:**
- `observes` — Fact ссылается на Dimension (контекст измерения)
- `derived_from` — Law/Pattern выведен из Facts
- `generalizes` — Law обобщает несколько Observations
- `contradicts` — Fact противоречит другому Fact (→ contested)
- `supports` — Fact подтверждает Law
- `refines` — Law уточняет другой Law

#### 4.5 Agent-Native Query Model

Агенты не пишут SQL. Они вызывают capabilities (stored procedures) через `skill_view`. Capability читает нужные файлы, агент строит вывод.

**Capabilities как интерфейс:**

| Capability | Аналог в DW | Операция |
|---|---|---|
| `warehouse-read` | `SELECT * FROM fact JOIN dim` | Прочитать Fact + его Dimensions |
| `cross-reference` | `SELECT * FROM fact WHERE dim.gpu = X` | Все Facts для данного GPU |
| `comparison` | `SELECT ... GROUP BY dim.gpu` | Сравнить Facts двух GPU |
| `lineage-trace` | Recursive CTE | Пройти DAG от вывода к источнику |
| `stale-check` | `SELECT * FROM artifacts WHERE stale = true` | Найти устаревшие Artifacts |
| `pattern-promote` | `INSERT INTO law` | Создать Law из Facts с lineage |

**Почему не SQL:** потребители — LLM-агенты. Им нужны файлы и графы, не реляционная алгебра. И масштаб не требует SQL-оптимизатора.

#### 4.6 Batch ETL — eventual consistency

ETL не real-time. Новые данные появляются когда Acquisition отработал. Между acquisition-сессиями данные могут устареть.

**Почему:** git-based pipeline по определению batch. ИгроЛаба обновляет обзоры не ежеминутно. Свежесть данных на момент публикации достаточна.

### 5. minerva как Hermes skill

minerva остаётся Hermes-скиллом (ADR-010). Структура:

```
minerva/                              # Hermes skill = DW implementation
├── SKILL.md                          # entry point + оркестратор
├── capabilities/                     # stored procedures (agent interface)
│   ├── acquisition/                  # ETL capabilities
│   │   ├── source-extract/
│   │   ├── transform-normalize/
│   │   └── warehouse-load/
│   ├── warehouse/                    # CRUD + query capabilities
│   │   ├── dim-read/
│   │   ├── fact-read/
│   │   ├── cross-reference/
│   │   └── scd-version/
│   ├── analysis/                     # analytical capabilities
│   │   ├── comparison/
│   │   ├── lineage-trace/
│   │   ├── pattern-promote/
│   │   └── stale-check/
│   └── materialize/                  # compilation capabilities
│       ├── artifact-compile/
│       └── artifact-regenerate/
├── warehouse/                        # = backend (SSOT)
│   ├── bus-matrix.yaml
│   └── {domain}/
│       ├── dim/
│       └── fact/
├── marts/                            # = frontend (Data Marts)
│   ├── coverage/
│   ├── engineering/
│   ├── competitive/
│   └── narrative/
└── artifacts/                        # materialized views
```

**Capabilities — не просто файлы.** Каждая capability имеет SKILL.md с контрактом (вход/выход) и rules (pre/post-conditions). Это stored procedures в мире файлов.

### 6. Что система НЕ делает

- **Не real-time.** Batch-архитектура. Данные обновляются по расписанию, не по событиям
- **Не multi-user concurrent.** Один агент — одна сессия. Git разрешает конфликты при коммите
- **Не data lake.** Не храним сырые PDF/HTML. Acquisition извлекает и выбрасывает original
- **Не заменяет NotebookLM/acquisition-фазу.** Acquisition — ETL, не exploratory synthesis. Exploration остаётся внешним инструментом, который поставляет structured candidates в Acquisition
- **Не инференс-движок.** Агенты делают выводы. minerva хранит данные, lineage и прослеживаемость

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Реляционная БД (SQLite/Postgres) вместо файлов | Транзакции, конкурентный доступ, SQL-запросы | Агентам нужны файлы для чтения. SQL — лишний слой трансляции. Git-history теряется | Файлы — родной интерфейс LLM. Не нужно учить агента SQL когда он уже умеет читать YAML |
| Стриминговая архитектура (Kafka) вместо batch | Real-time обновления | Гигантская сложность ради секундной свежести | ИгроЛаба обновляет обзоры раз в неделю/месяц. Eventual consistency более чем достаточна |
| Единая глобальная схема (единый bus-matrix для всех доменов) | Cross-domain аналитика тривиальна | Разные домены имеют разную природу. Coffee не имеет bandwidth | Domain isolation — осознанный выбор. Cross-domain анализ — редко, не оправдывает унификацию |
| Data Vault (Hub/Link/Satellite) вместо Star Schema | Лучше для rapidly changing schemas | Сложнее. Hub/Link/Satellite — три типа сущностей вместо двух (Fact/Dimension) | Star Schema проще. Для масштаба сотен записей — достаточно |

## Последствия

**Что становится проще:**
- **Архитектура прозрачна.** Три компонента (Acquisition, Warehouse, Data Marts) с явными границами и однонаправленным потоком данных. Никаких «Primitive это и данные и композиция»
- **Lineage — гражданин первого сорта.** Не `derived_from` как afterthought, а DAG в каждом derived элементе. Capability `lineage-trace` даёт полную прослеживаемость
- **SCD решает историчность.** Facts привязаны к версиям контекста. Laws сохраняют контекст открытия
- **Conformed Dimensions.** bus-matrix.yaml — SSOT имён. Больше никогда «CP2077» vs «Cyberpunk 2077» в разных Views
- **Agent-native.** Агент загружает `warehouse/dim/gpu/nvidia-rtx-5060.yaml` и сразу видит structured факты. Никакого промежуточного query layer

**Что требует новых ADR:**
- **ADR-016: Data Model** — схемы Dimension и Fact файлов, SCD-форматы, Bus Matrix schema
- **ADR-017: Lineage DAG** — структура графа, типы узлов и рёбер, правила traversal
- **ADR-018: ETL Pipeline** — Acquisition как capabilities: source connectors, transform rules, load strategies
- **ADR-019: Agent Query Model** — capabilities как stored procedures: контракты, pre/post-conditions, orchestration

**Что требует реализации:**
- **Новый minerva skill с нуля.** Текущий `minerva/` — PoC, спроектированный до DW-фундамента. Подлежит замене
- **bus-matrix.yaml** — первый артефакт: Dimensions для hardware-контекста
- **Warehouse-структура** — `warehouse/hardware/dim/gpu/` с первыми 15 GPU
- **Capabilities scaffolding** — acquisition, warehouse, analysis, materialize
