# Observation 004: External review — разделение слоёв, Source Layer, Definitions, Semantic Queries

**Date:** 2026-07-11
**Status:** open
**Type:** external review — architectural feedback

## Контекст

Архитектура minerva (ADR-012–024) показана внешнему инженеру. Получен структурированный feedback, затрагивающий несколько архитектурных слоёв.

## Наблюдения ревьюера

### 1. Ментальная модель: DW как память агента, не «AI со встроенным DW»

> «То, что ты строишь — это не "AI агент со встроенным Data Warehouse". Скорее это Data Warehouse как долговременная память агента. Агент — лишь один из клиентов этого хранилища. Потом у тебя появятся Research Agent, Planner, Writer, Fact Checker, Visualizer — и все они будут работать с одним DW.»

**Следствие:** DW не должен быть привязан к конкретному агенту или даже к Hermes skill. DW — самостоятельный компонент с API.

### 2. Warehouse API как прослойка

> «Агент никогда не читает yaml напрямую. Agent → Capability → Warehouse Engine → YAML/SQLite/DuckDB/Postgres. Тогда завтра ты сможешь заменить YAML на DuckDB вообще без изменения агентов.»

**Текущее состояние:** агент читает файлы через `skill_view`. **Риск:** смена хранилища ломает всех агентов.

### 3. Source Layer — Observation не должен знать DIM ID

> «Observation не должен знать DIM ID. Observation пишет "RTX 5060", а Warehouse делает cross-reference. Иначе Observation становится зависимым от структуры DW.»

**Текущее состояние:** Observation содержит `dimensions.gpu: "dim/gpu/nvidia-rtx-5060.yaml"` — жёсткая связь. **Риск:** переименование директории = битые ссылки во всех Facts.

### 4. Business Definitions

> «Average FPS — что это? Arithmetic mean? Geometric mean? FrameView? CapFrameX? Какой проход? Какая сцена? Через полгода сам забудешь что именно означает каждая метрика.»

**Текущее состояние:** метрики определены неявно. **Риск:** inconsistency между разными источниками и разными агентами.

### 5. Bus Matrix как domain contract

> «Сейчас Bus Matrix просто перечисляет измерения. Но она может стать контрактом: для fact_type observation — mandatory dimensions, allowed measures, grain. Тогда агент сможет проверить: Observation имеет правильную гранулярность?»

**Текущее состояние:** bus-matrix.yaml содержит только canonical-имена и aliases. **Потенциал:** стать валидирующим контрактом.

### 6. Capabilities → SQL-like (OLAP)

> «find-dimension, resolve-alias, query-facts, aggregate, slice, drill-down. Потому что потом LLM сможет строить запросы как OLAP.»

**Текущее состояние:** `dim-read`, `cross-reference`. **Потенциал:** композабельные OLAP-операции для агентов.

### 7. Semantic Layer над Dimensions

> «DIM становится почти Knowledge Graph: id, attributes, relationships, aliases, taxonomy. Тогда агент сможет: "покажи все Blackwell" или "покажи все карты с 8GB".»

**Текущее состояние:** Dimensions имеют `attributes`, но нет structured taxonomy. **Потенциал:** semantic queries без знания DIM ID.

## Что принято немедленно

1. Source Layer: Observation → `source:` (сырые значения) вместо `dimensions:` (DIM ID)
2. Business Definitions: `warehouse/definitions/` для каждой метрики
3. Bus Matrix → domain contract: measures + grain для fact-типов

## Что отложено

1. Warehouse API (Engine) как прослойка — когда масштаб потребует смены хранилища
2. Semantic Layer (Knowledge Graph) — Tier 4 аналитика, требует наполненных данных
3. OLAP-capabilities — после реализации базовых query-capabilities

## Связанные артефакты

- ADR-016: Data Model (Dimension/Fact схемы)
- ADR-019: Agent Query Model (capabilities)
- Будет ADR-025: Source Layer + Definitions + Bus Matrix contract
