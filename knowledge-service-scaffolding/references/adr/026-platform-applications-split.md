---
id: adr-026
status: accepted
date: 2026-07-13
supersedes: []
superseded_by: []
tags: [platform, applications, agent-memory, retrieval, bounded-context, capabilities]
based_on: [adr-014, adr-015, adr-016, adr-020, adr-025]
---

# ADR-026: Minerva Platform / Applications Split

## Контекст

Текущая реализация minerva развёрнута для одного прикладного кейса — hardware knowledge base (GPU, CPU, бенчмарки). Вся структура warehouse, bus matrix, definitions спроектирована под hardware-домен. Возникает вопрос: minerva — это «DW для железа» или что-то более общее?

При обсуждении agent long-term memory как следующего прикладного кейса стало ясно: методологический фундамент (dimensional model, bus matrix, SCD, lineage DAG, definitions, capabilities) домен-нейтрален. Hardware KB — первый потребитель, не определение платформы.

## Решение

### 1. Два архитектурных слоя

```
┌──────────────────────────────────────────────┐
│              APPLICATIONS                     │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Hardware │  │  Agent   │  │    ...      │  │
│  │    KB    │  │  Memory  │  │             │  │
│  └────┬─────┘  └────┬─────┘  └──────┬──────┘  │
│       │              │               │         │
│       └──────────────┼───────────────┘         │
│                      │                         │
│       Каждое приложение определяет:            │
│       - свой bounded context (warehouse/{domain}/)│
│       - свою bus matrix                        │
│       - свои definitions                       │
│       - свою retrieval-стратегию               │
├──────────────────────┼─────────────────────────┤
│                      │                         │
│              MINERVA PLATFORM                  │
│                                               │
│  Домен-нейтральные сервисы:                    │
│  - Dimensional model (Fact + Dimension)        │
│  - Bus matrix contract                        │
│  - SCD Type 0/1/2                             │
│  - Source Layer / Warehouse split             │
│  - Lineage DAG                                │
│  - Definitions schema                         │
│  - Capabilities interface (dim-read,           │
│    cross-reference, fact-insert,              │
│    structured-search)                         │
│  - Структура warehouse/{domain}/dim/,fact/     │
└──────────────────────────────────────────────┘
```

**Minerva Platform** — методология и инфраструктура. Ни слова про GPU, preferences, или что-либо прикладное. Только абстракции: Fact, Dimension, SCD, bus matrix contract, lineage.

**Applications** — bounded contexts на платформе. Каждый определяет что является Fact и Dimension в его домене.

### 2. Что Platform даёт Applications

Platform предоставляет гарантии, не зависящие от домена:

| Гарантия | Механизм |
|---|---|
| **Целостность данных** | bus matrix как domain contract: mandatory dimensions, allowed measures, grain валидация |
| **Прослеживаемость** | Lineage DAG: каждое derived значение знает свой путь от source |
| **Историчность** | SCD Type 2: изменения во времени сохранены, не перетёрты |
| **Единый язык** | Definitions — SSOT метрик и понятий |
| **Agent-native доступ** | Capabilities как stored procedures, не SQL |

### 3. Граница ответственности

**Platform НЕ диктует:**
- Какие dimensions и facts существуют (это решение приложения)
- Какую retrieval-стратегию использовать (приложение выбирает)
- Как агент интерпретирует данные (агент — потребитель, не часть платформы)
- Business-логику конкретного домена

**Platform диктует:**
- Как структурированы dimensions и facts (dimensional model)
- Как валидируется integrity (bus matrix contract)
- Как отслеживается provenance (lineage DAG)
- Как организован доступ (capabilities)

### 4. Agent Memory как Application

Agent Memory — bounded context `warehouse/memory/` на платформе minerva. Первый PoC-кейс вне hardware.

**Что определяет Memory-приложение:**

```yaml
# warehouse/memory/bus-matrix.yaml (принадлежит приложению)

dimensions:
  user:         # кто
  session:      # в каком разговоре
  topic:        # о чём
  memory_type:  # preference | decision | correction | project-fact | context-state

facts:
  memory_entry:
    mandatory_dimensions: [user, memory_type]
    optional_dimensions: [session, topic]
    allowed_attributes: [value, confidence, extraction_method, valid_from, valid_to]
    grain: one-fact-per-user-per-domain
    validation_rules:
      - "memory_type=preference требует domain"
      - "confidence ∈ {high, medium, low}"
      - "SCD Type 2 для preference"
```

Platform не знает что такое «preference». Platform знает что memory_entry — это Fact с mandatory_dimensions [user, memory_type].

### 5. Retrieval как новый capability-класс Platform

Retrieval — не свойство конкретного приложения, а capability-класс платформы. Любое приложение может нуждаться в поиске Facts по dimensions + terms.

```
minerva/capabilities/
├── warehouse/
│   ├── dim-read/           # «дай Dimension по ID»
│   ├── cross-reference/    # «все Facts для Dimension»
│   └── fact-insert/        # «запиши Fact с валидацией по bus matrix»
├── retrieval/              # ← новый capability-класс
│   └── structured-search/  # «найди Facts по dimensions + key_terms»
```

**`structured-search` контракт:**

```
Вход:
  domain: string            # bounded context
  fact_type: string         # тип факта (memory_entry, observation, ...)
  dimension_filters: {       # сужение по dimensions
    user: "eugene",
    memory_type: "preference"
  }
  key_terms: [string]       # FTS5-термины
  recency: "recent" | "all" # временной фильтр
  limit: integer

Выход:
  ranked Facts с confidence, lineage, SCD-статусом

Процесс:
  1. Dimensional Narrowing: фильтр по dimension_filters через bus matrix
  2. FTS5: поиск по тексту Fact
  3. Rank: confidence ↑, is_current ↑, recency ↓
```

**Почему это платформенный capability, не прикладной:**
- Контракт домен-нейтрален: `dimension_filters` — generic, любой тип dimensions
- Использует bus matrix (платформенный сервис) для валидации фильтров
- Любое приложение может вызвать `structured-search` со своей схемой

### 6. Прикладные retrieval-стратегии

Приложения могут надстраивать над `structured-search` домен-специфичные стратегии. Это НЕ платформа:

```
Agent Memory:
  retrieval-intent-extract (LLM) → structured-search → rerank (LLM, optional)

Hardware KB:
  dim-read → cross-reference  (key-based, retrieval не нужен)
  ИЛИ: structured-search(fact_type=observation, dimension_filters={gpu: "nvidia-rtx-5060"})
```

Platform даёт `structured-search`. Приложение решает, вызывать ли его напрямую или обернуть в retrieval-intent-extract.

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Minerva = hardware-only DW | Проще: одна схема, один домен | platform/application смешаны. Каждый новый кейс — форк или переделка bus matrix | Ограничивает ценность методологии одним доменом |
| Каждое приложение — отдельный Hermes skill со своей DW-реализацией | Изоляция, независимая эволюция | Дублирование platform-логики. Capabilities, bus matrix, SCD — пишем заново | Platform — это SSOT методологии. Размножение — технический долг |
| Platform = библиотека (Python package), не skill | Статическая типизация, тесты, pip install | Агентам нужны файлы и capabilities, не Python-функции. skill-native — осознанный выбор (ADR-010) | Файлы — родной интерфейс LLM |

## Последствия

**Что нужно изменить в текущей реализации:**
- `warehouse/hardware/` — остаётся как application-level bounded context
- `warehouse/bus-matrix.yaml` — вынести hardware-специфичные секции в `warehouse/hardware/bus-matrix.yaml`. Platform-level bus matrix содержит только общие dimensions (если появятся)
- Capabilities: `dim-read`, `cross-reference`, `fact-insert` — уже платформенные. Новый `structured-search` — платформенный
- Создать `warehouse/memory/` — новый bounded context для Agent Memory PoC

**Что становится проще:**
- Новый прикладной кейс → новый `warehouse/{domain}/` + своя bus matrix. Platform не трогаем
- Retrieval-стратегия — выбор приложения. Platform не навязывает вектора или FTS5
- Capabilities растут от потребностей приложений, но остаются домен-нейтральными

**Что требует дисциплины:**
- Platform не должна знать о прикладных типах Fact. `structured-search` принимает `dimension_filters`, не `preference_type`
- Приложения не должны дублировать platform-логику. Валидация — через bus matrix платформы, не свою
- Capabilities сохраняют domain-neutral contract даже если спроектированы под конкретный кейс
