---
id: adr-017
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [lineage, dag, data-traceability, graph, provenance]
based_on: [adr-014, adr-015, adr-016]
---

# ADR-017: Lineage DAG — граф происхождения данных

## Контекст

ADR-015 требует Lineage DAG для всех производных элементов. ADR-016 определил `lineage:` в схеме Derived Fact. Теперь нужно определить структуру графа: типы узлов, типы рёбер, правила traversal и как lineage обеспечивает эпистемическую достоверность.

Предыдущий подход (`derived_from` — плоский список) не различал уровни вывода: Observation и Law были одинаковыми «родителями». Это делало lineage непригодным для проверки цепочек рассуждения.

## Решение

### 1. Lineage DAG — Directed Acyclic Graph

Граф, в котором:
- **Узлы** — элементы данных (Fact, Dimension, Law, Pattern, Artifact)
- **Рёбра** — типизированные отношения происхождения
- **Направление** — от производного к исходному (ребро: derived → source)
- **Ацикличность** — нельзя вывести A из B который выведен из A

### 2. Типы узлов

| Узел | Где хранится | Назначение | Пример |
|---|---|---|---|
| **Dimension** | `warehouse/{domain}/dim/` | Описательный атрибут | `dim/gpu/nvidia-rtx-5060.yaml` |
| **Fact: Observation** | `warehouse/{domain}/fact/` | Первичное измерение | `fact/observations/rtx5060-cp2077-1440p.yaml` |
| **Fact: Metric** | `warehouse/{domain}/fact/` | Аддитивная величина | `fact/metrics/rtx5060-fp32.yaml` |
| **Comparison** | `marts/{view}/` | Результат сравнения Facts | Сравнение bandwidth 5060 vs 4060 |
| **Law** | `marts/{view}/` | Вывод из Facts | GDDR7 Bandwidth Compensation |
| **Pattern** | `marts/{view}/` | Повторяющаяся структура | «NVIDIA использует GDDR7 для компенсации bus width» |
| **Artifact** | `artifacts/` | Готовая страница | `rtx-5060-review.md` |

**Иерархия узлов (уровни вывода):**

```
Level 0: Dimension, Fact (Observation, Metric)  ← первичные данные
Level 1: Comparison                             ← сопоставление первичных данных
Level 2: Pattern, Law                           ← интерпретация
Level 3: Artifact                               ← готовый продукт
```

Правило: узел уровня N может ссылаться ТОЛЬКО на узлы уровней < N. Law (L2) может ссылаться на Comparison (L1) и Facts (L0), но не на другой Law (L2) — для этого есть `refines`.

### 3. Типы рёбер

| Ребро | Направление | Семантика | Пример |
|---|---|---|---|
| **observes** | Fact → Dimension | Fact измерен в контексте этого Dimension | FPS Fact → GPU Dimension |
| **derived_from** | Comparison → Fact | Comparison построен на этих Facts | Bandwidth Comparison → bandwidth Facts |
| **generalizes** | Law → Fact / Comparison | Law обобщает несколько Facts | GDDR7 Law → три bandwidth Facts |
| **contradicts** | Fact → Fact | Два Fact противоречат друг другу | FPS 68 (user) vs FPS 72 (reviewer) → contested |
| **supports** | Fact → Law | Fact подтверждает Law (после вывода) | Новый Fact на драйвере 575 → Law всё ещё верен |
| **refines** | Law → Law | Новый Law уточняет существующий | «GDDR7 Law v2: верен только для xx60-класса» |
| **materializes** | Artifact → Law / Comparison | Artifact материализует эти выводы | Review page → GDDR7 Law + Bandwidth Comparison |

### 4. Структура lineage в каждом derived узле

Lineage встроен в сам файл, не вынесен в отдельный реестр:

```yaml
# marts/engineering/laws/gddr7-bandwidth-compensation.yaml
---
derived_fact:
  id: "gddr7-bandwidth-compensation"
  type: "law"
  level: 2

lineage:
  nodes:
    - {ref: "fact/observations/rtx5060-cp2077-1440p-driver572.yaml", role: "evidence", level: 0}
    - {ref: "fact/metrics/rtx5060-bandwidth.yaml", role: "evidence", level: 0}
    - {ref: "fact/metrics/rtx4060-bandwidth.yaml", role: "baseline", level: 0}
    - {ref: "fact/metrics/rtx4070-bandwidth.yaml", role: "reference", level: 0}

  edges:
    - {from: "fact/metrics/rtx5060-bandwidth", to: "gddr7-bandwidth-compensation", type: "generalizes"}
    - {from: "fact/metrics/rtx4060-bandwidth", to: "gddr7-bandwidth-compensation", type: "generalizes"}
    - {from: "fact/metrics/rtx4070-bandwidth", to: "gddr7-bandwidth-compensation", type: "generalizes"}
```

**Правила:**
- `nodes` перечисляет все элементы, участвующие в выводе. `role` — семантическая метка (evidence, baseline, reference, counterexample)
- `edges` перечисляет все рёбра с типами. Каждый Fact, использованный в выводе, должен иметь ребро
- `level` — уровень узла в иерархии. Используется для валидации: Law (L2) не может ссылаться на Artifact (L3)

### 5. Операции над Lineage DAG

#### 5.1 lineage-trace (вверх: от вывода к источнику)

```
Дано: Law "GDDR7 Bandwidth Compensation"
Задача: показать все исходные Facts, на которых он основан

Алгоритм:
  1. Загрузить Law → прочитать lineage.nodes
  2. Для каждого node с level=0 → это исходный Fact
  3. Для каждого node с level>0 → рекурсивно загрузить и повторить
  4. Вернуть дерево: Law → Comparisons → Facts → Dimensions
```

#### 5.2 impact-analysis (вниз: от факта к выводам)

```
Дано: Fact "rtx5060-cp2077-1440p-driver572" изменился (новый драйвер)
Задача: какие Laws и Artifacts нужно перепроверить?

Алгоритм:
  1. Поиск по всем derived-файлам: где этот Fact в lineage.nodes?
  2. Для каждого найденного Law → пометить как "requires review"
  3. Для каждого Artifact, который материализует этот Law → пометить stale
```

#### 5.3 lineage-validate (проверка целостности)

```
Дано: новый Law
Задача: корректен ли lineage DAG?

Проверки:
  - Все nodes.ref ведут на существующие файлы
  - Все edges ссылаются на nodes из этого же lineage
  - Нет циклов (B → A, A → B)
  - Уровни не нарушены (L2 не ссылается на L3)
  - Все Fact-узлы имеют level=0
  - Есть хотя бы один Fact-узел (Law не может быть выведен из ничего)
```

### 6. Contradiction tracking

Когда два Fact противоречат друг другу, ребро `contradicts` маркирует конфликт:

```yaml
# fact/observations/rtx5060-cp2077-1440p-user.yaml
---
fact:
  id: "rtx5060-cp2077-1440p-user"
  confidence: 0.95
  confidence_basis: "user_verified"

lineage:
  edges:
    - {from: "rtx5060-cp2077-1440p-user",
       to: "rtx5060-cp2077-1440p-reviewer",
       type: "contradicts",
       reason: "FPS расхождение: 68 (user) vs 72 (reviewer). Возможно разные участки бенчмарка"}
```

**Contradiction — не ошибка, а сигнал.** Система не разрешает противоречия автоматически. Она маркирует contested и ждёт разрешения (новый замер, уточнение условий).

### 7. SCD и lineage

SCD Type 2 создаёт новые версии Dimensions. Lineage должен учитывать версионность:

```yaml
# Law открыт на данных драйвера 572.16
lineage:
  nodes:
    - {ref: "dim/driver_version/nvidia-geforce-572.16_v2026-03.yaml",    # конкретная версия!
       role: "context"}

# Новый Fact на драйвере 575.10
fact:
  dimensions:
    driver: "dim/driver_version/nvidia-geforce-575.10_v2026-06.yaml"     # другая версия

# Law проверяется против нового Fact
lineage:
  edges:
    - {from: "rtx5060-cp2077-1440p-driver575",
       to: "gddr7-bandwidth-compensation",
       type: "supports",                                                 # Law подтверждён на новых данных
       note: "Закон верен и на драйвере 575.10. FPS вырос на 3, но пропорция bandwidth сохранилась"}
```

**Правило:** Dimensions в lineage.nodes всегда ссылаются на конкретную версию (файл-версию), не на заголовочный файл. Это даёт точную прослеживаемость: «этот Law выведен на драйвере 572.16 от марта 2026».

## Что НЕ фиксируем

- **Визуализацию DAG.** Полезно, но отдельная capability
- **Автоматическое построение lineage.** Агент или аналитик заполняет lineage при создании Law. Автоматический inference — будущее
- **Lineage между контекстами.** Cross-domain lineage (hardware Fact → coffee Law) — не поддерживается. Разные bounded contexts
- **Версионирование самого lineage.** Если Law пересмотрен, старый lineage сохраняется в git-history. Новая версия Law имеет новый lineage

## Последствия

**Что становится проще:**
- **Эпистемическая достоверность.** Любой Law можно проверить: `lineage-trace` → все исходные Facts → проверить confidence каждого
- **Impact analysis.** Fact изменился? `impact-analysis` → список затронутых Laws и Artifacts. Не гадание
- **Contradiction resolution.** Два Fact противоречат друг другу? Ребро `contradicts` маркирует конфликт. Laws, основанные на contested Facts, знают об этом
- **SCD-прозрачность.** Lineage всегда ссылается на конкретную версию Dimension. Агент знает: «этот Law — на данных марта 2026. Проверю на июньских»

**Что требует дисциплины:**
- **Lineage — не опционально.** Каждый derived элемент обязан иметь `lineage:`. Без lineage — не derived, а мнение. Capability `primitive-validate` проверяет наличие lineage
- **Ручное заполнение — временно.** Пока агент заполняет lineage вручную. В будущем `pattern-promote` может предлагать candidate lineage
- **Не злоупотреблять уровнями.** Level 0–3 достаточно. Попытка ввести 10 уровней сделает граф нечитаемым
