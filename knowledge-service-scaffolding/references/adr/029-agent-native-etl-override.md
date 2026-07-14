---
id: adr-029
status: proposed
date: 2026-07-13
supersedes: [adr-018]
superseded_by: []
tags: [etl, agent-native, architecture, acquisition, platform]
based_on: [adr-026, adr-028]
---

# ADR-029: Agent-Native ETL — отказ от классического staged pipeline

## Контекст

ADR-018 спроектировал ETL как классический staged pipeline: три слоя (Extract → Transform → Load), промежуточные файлы (`acquisition/raw/`, `acquisition/staged/`), декларативные mapping-файлы, отдельные вызовы для каждого этапа.

Эта архитектура корректна для системы, где каждый слой — изолированная программа (Python-скрипт, Spark job, Airflow DAG). Программы не делят память → нужны файлы для передачи состояния. Программы не рассуждают → нужны mapping-файлы для сопоставления полей.

Но minerva — agent-native система. Исполнитель — LLM-агент, который:
- Держит модель данных в контексте
- Рассуждает о соответствии source-значений dimensions
- Понимает bus matrix, aliases, dimensional model

Для агента staged pipeline — избыточная церемония, которая создаёт точки синхронизации без ценности.

## Решение

### 1. ETL = один агентский reasoning-проход

```
Классический ETL (ADR-018):
  program_extract → raw.yaml → program_transform → staged.yaml → program_load → warehouse

Agent-Native ETL:
  агент загружает capability
    → получает данные из источника (web_extract, чтение файла, пользовательский ввод)
    → держит в контексте
    → нормализует (bus matrix, aliases, dimensional model — в контексте)
    → вызывает fact-insert
```

Три слоя не исчезают концептуально — они коллапсируют в один reasoning-проход. Extract = инструмент получения данных. Transform = понимание агентом модели данных. Load = fact-insert.

### 2. Что уходит

| Элемент ADR-018 | Почему не нужен агенту |
|---|---|
| `acquisition/staged/` — промежуточные файлы | Агент держит нормализованные данные в контексте до вызова fact-insert. Staged-файл — синхронизационный долг: «загружен ли он уже?», «не устарел ли?» |
| `acquisition/mappings/` — декларативные mapping-файлы | Агент видит source-значение, bus matrix, dimensional model — и сам сопоставляет. Mapping — это reasoning, не конфигурация. Агент понимает что «8 GB» → `vram.size_gb: 8` без YAML-инструкции |
| Три раздельных вызова (source-extract → transform-normalize → warehouse-load) | Программы не делят память → нужны вызовы. Агент — делит. Один reasoning-проход |
| `schema-map`, `unit-convert` как отдельные шаги | Агент делает это неявно, понимая bus matrix и definitions |
| `bus-register` | Dimensions создаются вручную при обнаружении нового значения — это архитектурное решение (dimensions не создаются на лету) |

### 3. Что остаётся

- **fact-insert** — write-side gateway (ADR-028). Единственная точка записи в warehouse
- **Alias-resolve** — внутри fact-insert как integrity check (source-значение → dimension существует?)
- **Conflict detection** — агент, видя два источника, сравнивает значения. Это reasoning, не отдельный capability
- **SCD** — dim-upsert остаётся как концепт, но выполняется агентом, не программой

### 4. Extract-инструменты

Агент использует инструменты, не «коннекторы»:

| Источник | Инструмент агента |
|---|---|
| YouTube-бенчмарк | Пользователь даёт markdown → агент читает |
| TechPowerUp / Guru3D | `web_extract(url)` |
| NVIDIA ARK / AMD Specs | `web_extract(url)` |
| Ценовые агрегаторы | `web_extract(url)` или `web_search(query)` |
| Ручной ввод | Пользователь → сообщение агенту |

Инструменты универсальны. Не нужно писать `youtube-connect`, `url-scrape`, `api-fetch` как отдельные capabilities — агент использует `web_extract` и `web_search`.

### 5. Пример: импорт бенчмарка в agent-native

```
Пользователь: «Вот markdown-отчёт с бенчмарками RTX 5060»
Агент (загружен fact-insert + bus matrix в контексте):
  1. Читает markdown → извлекает строки таблицы
  2. Для каждой строки:
     - game_title = "Cyberpunk 2077: Phantom Liberty"
     - Смотрит bus matrix aliases → "cyberpunk-2077"
     - Проверяет что dim/game_title/cyberpunk-2077.yaml существует
     - fps_avg = 88 → в allowed_measures
     - 88 > 70 (1% low) → validation_rule ОК
     - Нет дубликата
     - fact-insert → файл создан
  3. Результат: «+11 observations, 1 warning: Silent Hill f 4K DLSS 4.5 Performance не резолвится»
```

Ни одного промежуточного файла. Ни одного mapping-файла. Один агент, один проход.

### 6. Когда классический ETL был бы нужен

Классический staged pipeline (ADR-018) становится оправданным когда:

- **Масштаб превышает контекст агента.** 10 000+ observations — агент не держит в контексте. Нужна пакетная обработка с промежуточными файлами
- **Источник требует сложного парсинга.** PDF с таблицами, изображения с графиками — нужен специализированный экстрактор до агента
- **Регулярный scheduled импорт.** Раз в неделю обновлять цены из API → cron job, не агент вручную

Но это будущие сценарии. Для текущего масштаба (сотни observations, ручной импорт) agent-native подход достаточен и правилен.

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Сохранить ADR-018 как есть, строить staged pipeline | Готовый дизайн, индустриальный стандарт | Архитектурный mismatch: файлы для передачи состояния между программами, когда исполнитель — агент с контекстом | ETL-паттерн правильный, но реализация должна соответствовать runtime-природе системы |
| Полностью отказаться от ETL, разрешить агенту писать в warehouse напрямую | Максимальная гибкость | Структурная контаминация, отсутствие write-side контракта | Уже решено: fact-insert — единственная точка записи (ADR-028) |
| Agent-native с fallback к staged при масштабировании | Честно: работает сейчас,留有 путь к автоматизации | Два режима → complexity | Это не «два режима». Это один подход (agent-native) с явным условием перехода к staged когда масштаб потребует |

## Последствия

**Что становится проще:**
- Импорт данных: пользователь дал markdown → агент сразу пишет в warehouse. Без промежуточных файлов и mapping'ов
- Добавление нового источника: не нужно писать mapping-файл. Агент понимает модель и сопоставляет сам
- Поддержка: меньше файлов, меньше точек отказа

**Что требует дисциплины:**
- Агент обязан загружать fact-insert capability перед любым импортом. Без него — ad-hoc запись
- Bus matrix должен быть актуальным. Если alias отсутствует → агент не резолвит → ошибка → нужно обновить bus matrix
- При масштабировании (1000+ observations) не пытаться «дожать» agent-native подход — честно перейти к staged

**Что отменяется из ADR-018:**
- `acquisition/staged/` директория — не создаётся
- `acquisition/mappings/` директория — не создаётся
- `transform-normalize`, `source-extract`, `warehouse-load` как отдельные capabilities
- Трёхфазный вызов (extract → transform → load)
