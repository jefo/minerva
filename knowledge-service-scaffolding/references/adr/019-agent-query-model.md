---
id: adr-019
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [query-model, capabilities, agent-interface, stored-procedures, contracts]
based_on: [adr-015, adr-016, adr-017]
---

# ADR-019: Agent Query Model — capabilities как stored procedures

## Контекст

ADR-015 определил agent-native query model: агенты взаимодействуют с minerva через capabilities, не через SQL. Теперь нужно определить как устроены capabilities: контракты, pre/post-conditions, orchestration, обработка ошибок.

Capabilities — это stored procedures в мире файлов. Как хранимые процедуры в БД, они инкапсулируют логику доступа к данным и гарантируют целостность. Но вместо SQL они оперируют файлами и графами.

## Решение

### 1. Capability = контракт + правила + idempotency

Каждая capability имеет:

```yaml
# capability contract
contract:
  in:                         # входной контракт: что capability ожидает
    params:                   # обязательные параметры
      - {name: "gpu_id", type: "dimension_ref", required: true}
    context:                  # опциональный контекст
      - {name: "include_historical", type: "boolean", default: false}
  out:                        # выходной контракт: что capability производит
    result: "fact_set"        # тип результата
    side_effects: ["none"]    # изменяет ли capability состояние?
  errors:                     # известные ошибки
    - {code: "DIM_NOT_FOUND", meaning: "Dimension не существует"}
    - {code: "NO_FACTS", meaning: "Нет Facts для данного Dimension"}

rules:                        # pre/post-conditions
  pre:
    - "gpu_id ссылается на существующий Dimension типа gpu"
  post:
    - "Все возвращённые Facts имеют валидный lineage"
    - "Факты отсортированы по confidence (убывание)"

idempotency: "read"           # read | write | idempotent_write
```

### 2. Категории capabilities

#### 2.1 Read capabilities (idempotency: read)

Не изменяют состояние. Могут вызываться когда угодно, параллельно.

| Capability | Операция | Контракт |
|---|---|---|
| `dim-read` | Прочитать Dimension по id | in: dim_ref → out: dimension_data |
| `fact-read` | Прочитать Fact по id | in: fact_ref → out: fact_data + dimensions |
| `cross-reference` | Все Facts для Dimension | in: dim_ref, fact_type? → out: fact_set |
| `lineage-trace` | Пройти DAG вверх | in: derived_ref → out: lineage_tree |
| `impact-analysis` | Пройти DAG вниз | in: fact_ref → out: affected_derived |
| `comparison` | Сравнить два Dimension | in: dim_a, dim_b, metrics[] → out: comparison_table |
| `stale-check` | Найти устаревшие Artifacts | in: (none) → out: stale_artifact_list |
| `bus-lookup` | Найти Dimension по alias | in: alias → out: canonical_dim_ref |

#### 2.2 Write capabilities (idempotency: write)

Изменяют состояние. Требуют pre-condition checks. Непараллельны.

| Capability | Операция | Контракт |
|---|---|---|
| `dim-upsert` | Создать/обновить Dimension | in: dim_data → out: dim_ref + scd_action |
| `fact-insert` | Создать Fact | in: fact_data → out: fact_ref |
| `pattern-promote` | Создать Law из Facts | in: law_data + lineage → out: law_ref |
| `artifact-compile` | Собрать Artifact | in: view_ref + module_refs → out: artifact_ref |
| `artifact-regenerate` | Пересобрать stale Artifact | in: artifact_ref → out: new_artifact_ref |
| `bus-register` | Зарегистрировать Dimension в Bus Matrix | in: dim_type + canonical_name → out: bus_entry |

### 3. Pre/post-condition enforcement

Каждая capability проверяет pre-conditions до выполнения и post-conditions после. При нарушении — structured error.

```
dim-read(gpu_id="nvidia-rtx-5090")

PRE:
  ✓ dim_ref существует → warehouse/hardware/dim/gpu/nvidia-rtx-5090.yaml найден

EXECUTE:
  → загрузить файл
  → резолвить relationships (встроенные Dimensions)

POST:
  ✓ dimension.type == "gpu"
  ✓ attributes не пустые
  → вернуть dimension_data
```

```
cross-reference(dim_ref="nvidia-rtx-5060", fact_type="observation")

PRE:
  ✓ dim_ref существует
  ✓ fact_type валиден ("observation", "metric")

EXECUTE:
  → поиск по fact/observations/: где dim_ref == "nvidia-rtx-5060"

POST:
  ✓ fact_set не пуст (3 observations найдены)
  → вернуть отсортированный список Facts
```

### 4. Оркестрация capabilities

Агент не вызывает capabilities напрямую. Он загружает `minerva/SKILL.md` — оркестратор. SKILL.md содержит mapping: интент пользователя → последовательность capabilities.

```yaml
# minerva/SKILL.md (фрагмент — orchestration rules)
orchestration:
  "что известно о RTX 5060":
    - dim-read: {dim_ref: "nvidia-rtx-5060"}
    - cross-reference: {dim_ref: "nvidia-rtx-5060"}

  "сравни RTX 5060 и RTX 4060":
    - comparison: {dim_a: "nvidia-rtx-5060", dim_b: "nvidia-rtx-4060", metrics: ["fps_avg", "bandwidth_gb_s"]}

  "проверь lineage этого Law":
    - lineage-trace: {derived_ref: "gddr7-bandwidth-compensation"}

  "какие обзоры устарели после обновления драйвера?":
    - stale-check: {}
    - for each stale artifact:
        - lineage-trace: {derived_ref: artifact_ref}  # показать что изменилось

  "импортируй RTX 5060 из NVIDIA ARK":
    - source-extract: {source_type: "api", source_params: {url: "..."}}
    - transform-normalize: {raw_file: "..."}
    - warehouse-load: {staged_file: "..."}
```

### 5. Обработка ошибок

Ошибки структурированы, не исключения:

```yaml
# error response
error:
  code: "DIM_NOT_FOUND"
  message: "Dimension 'nvidia-rtx-5090-ti' не найден в warehouse/hardware/dim/gpu/"
  suggestion: "Возможно, вы имели в виду: nvidia-rtx-5090, nvidia-rtx-5060-ti"
  candidates: ["nvidia-rtx-5090", "nvidia-rtx-5060-ti"]
```

**Стандартные коды ошибок:**

| Код | Значение | Действие агента |
|---|---|---|
| `DIM_NOT_FOUND` | Dimension не существует | Предложить candidates, спросить пользователя |
| `FACT_NOT_FOUND` | Fact не существует | Сообщить: «Нет данных. Запустить acquisition?» |
| `LINEAGE_BROKEN` | DAG содержит битые ссылки | Сообщить: «Lineage нарушен. Запустить lineage-validate» |
| `CONFLICT_DETECTED` | Два Fact противоречат друг другу | Показать оба Fact, спросить разрешение |
| `SCD_VERSION_MISSING` | Историческая версия Dimension не найдена | Сообщить: «Версия драйвера 572.16 не в Warehouse» |
| `BUS_ALIAS_UNKNOWN` | Alias не найден в Bus Matrix | Предложить зарегистрировать новый Dimension |
| `STALE_ARTIFACT` | Artifact устарел | Предложить пересобрать |
| `VALIDATION_FAILED` | Pre/post-condition нарушен | Показать какие условия не выполнены |

### 6. Транзакционность (насколько возможно в файлах)

Write-операции в файлах не транзакционны в ACID-смысле. Но мы обеспечиваем **логическую atomicity**:

```
pattern-promote(law_data, lineage)

1. PRE: проверить все lineage.nodes → существуют
2. WRITE: создать law файл в marts/
3. POST: проверить lineage целостность
4. Если POST failed → УДАЛИТЬ law файл (rollback)
5. COMMIT: git add + git commit

Если commit failed (конфликт):
  → git stash → повторить операцию
```

**Правило:** write-операции атомарны на уровне одного файла. Cross-file транзакции — через git (commit всех изменений одной операцией).

### 7. Агент читает Warehouse → строит вывод

Ключевое: агент НЕ получает данные через API. Он загружает файлы через `skill_view` и строит выводы сам. Capabilities только организуют доступ:

```
Агент: «сравни RTX 5060 и RTX 4060 по bandwidth»

1. Агент → capability: comparison(dim_a="nvidia-rtx-5060", dim_b="nvidia-rtx-4060", metrics=["bandwidth_gb_s"])
2. Capability:
   - dim-read: загружает оба Dimension файла
   - cross-reference: находит bandwidth Facts (если есть)
   - Возвращает: comparison_table {rows: [{gpu, bandwidth_gb_s, source}]}
3. Агент получает structured comparison_table
4. Агент строит вывод: «RTX 5060: 355 GB/s (GDDR7, 128-bit). RTX 4060: 272 GB/s (GDDR6, 128-bit). Разница: +30.5%»
5. Агент может предложить сохранить вывод как Law через pattern-promote
```

**Capabilities — не intelligence.** Они возвращают данные. Выводы строит агент. Capability `comparison` возвращает таблицу, не prose. Capability `lineage-trace` возвращает граф, не объяснение почему Law верен.

### 8. Capability → SKILL.md (реализация)

Каждая capability реализована как SKILL.md в `minerva/capabilities/`:

```
minerva/capabilities/
├── warehouse/
│   ├── dim-read/SKILL.md        # contract + rules + procedure
│   ├── fact-read/SKILL.md
│   ├── cross-reference/SKILL.md
│   └── scd-version/SKILL.md
├── analysis/
│   ├── comparison/SKILL.md
│   ├── lineage-trace/SKILL.md
│   ├── impact-analysis/SKILL.md
│   ├── pattern-promote/SKILL.md
│   └── stale-check/SKILL.md
├── acquisition/
│   ├── source-extract/SKILL.md
│   ├── transform-normalize/SKILL.md
│   └── warehouse-load/SKILL.md
└── materialize/
    ├── artifact-compile/SKILL.md
    └── artifact-regenerate/SKILL.md
```

**Структура capability SKILL.md** (на примере `cross-reference`):

```markdown
---
name: cross-reference
contract:
  in:
    params:
      - {name: "dim_ref", type: "dimension_ref", required: true}
      - {name: "fact_type", type: "string", required: false, default: "all"}
  out:
    result: "fact_set"
  errors: ["DIM_NOT_FOUND", "NO_FACTS"]
rules:
  pre:
    - "dim_ref → существующий Dimension"
  post:
    - "Все Facts имеют dim_ref в dimensions"
    - "Сортировка по confidence (убывание)"
idempotency: "read"
---

# cross-reference — все Facts для Dimension

## Процедура

1. dim-read(dim_ref) → проверить существование
2. Поиск по `warehouse/{domain}/fact/{fact_type}/`: все .yaml где dim_ref в dimensions
3. Для каждого Fact → fact-read → полные данные
4. Сортировать по meta.confidence (убывание)
5. Вернуть fact_set
```

## Что НЕ фиксируем

- **Механизм поиска Fact по dim_ref.** grep? query.py? Индекс? Implementation detail
- **Параллельное выполнение capabilities.** Пока последовательно. Параллельность — когда масштаб потребует
- **Кэширование результатов.** Read capabilities могут кэшироваться, но механизм не определён
- **Права доступа.** Все агенты имеют полный доступ. ACL — будущее

## Последствия

**Что становится проще:**
- **Контракты — явные.** Агент знает что подать на вход и что ожидать на выходе. Никаких «может вернуть Facts, а может Laws»
- **Pre/post-conditions — проверяемы.** Capability не исполняется если pre нарушен. Post проверяется после. Никаких молчаливых ошибок
- **Idempotency — в контракте.** Read можно вызывать повторно без последствий. Write — осторожно
- **Оркестрация — декларативна.** SKILL.md содержит mapping интентов на цепочки capabilities. Не код

**Что требует дисциплины:**
- **Контракты должны поддерживаться.** Изменилась схема Fact → обновить контракт `fact-read`. Без этого pre/post-condition ложные
- **Write capabilities — последовательно.** Два одновременных `dim-upsert` на один Dimension → git conflict. Пока масштаб не требует параллельности
- **Ошибки — обрабатывать явно.** Агент должен проверять error code после каждого capability-вызова. Не «что-то пошло не так», а «DIM_NOT_FOUND: candidates: [...]»
