---
id: adr-013
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [architecture, backend-frontend, data-models, atomic-design, acquisition, layers]
based_on: [adr-012, observation-001, observation-002]
---

# ADR-013: Backend/Frontend split — разделение сырых данных и композиционной витрины

## Контекст

Observation 001 выявил напряжение: Atomic Design как файловая структура фрагментирует Аггрегат. GPU-карта, будучи единой сущностью для внешнего потребителя, распадается на 8+ отдельных файлов Primitives. Это не обслуживает progressive disclosure и не создаёт переиспользуемости для спецификаций.

Параллельно Observation 002 и ADR-012 определили слой Acquisition для exploratory synthesis над сырыми источниками — но оставили открытым вопрос: **куда попадают структурированные данные после extraction, но до compositional layer?**

Текущая архитектура minerva (Tier 0–4) смешивает две ответственности:
- **Хранение фактов:** «CUDA Cores: 20480» — это данные
- **Композиция знаний:** «это Specification типа такого-то, часть Component X» — это витрина

Из-за этого смешения:
1. Спецификации не переиспользуемы — потому что они погребены внутри Primitives, привязанных к конкретной карте
2. Cross-source discovery невозможен — чтобы найти паттерн «GDDR7 компенсирует 128-битную шину», нужно вручную сопоставить поля из разных файлов
3. Утверждение «спецификации не переиспользуемы» из Observation 001 оказалось ошибочным — оно было следствием архитектуры, а не природы данных

## Решение

Разделить minerva на **backend** (сырые данные) и **frontend** (композиционная витрина Atomic Design). Не в смысле клиент-сервер, а как разделение ответственности:

- **Backend** = модели данных с изолированными контекстами знаний. Чистые факты, без композиционной логики, без богатых моделей DDD. Один компонент = один файл.
- **Frontend** = витрина Atomic Design. Primitives, Components, Modules, Views, Artifacts — извлекаются из backend когда обнаружен переиспользуемый паттерн, Law или Relation.

### Трёхслойная архитектура

```
┌──────────────────────────────────────────────────────────────┐
│                    ACQUISITION LAYER                          │
│  Сырые источники → Извлечение → Exploratory reasoning         │
│  (PDF, URL, YT transcript, specs, benchmarks)                 │
│  Интерфейс: open-ended chat с source grounding               │
│  Продукт: candidate facts, patterns, contradictions           │
├──────────────────────────────────────────────────────────────┤
│                    BACKEND (raw data)                         │
│  Изолированные контексты знаний: hardware/gpu/, coffee/, ...  │
│  Чистые модели данных: один компонент = один файл             │
│  Никакой композиционной логики — только факты                 │
│  Поля нормализованы для cross-reference                       │
│  Продукт: structured facts                                    │
├──────────────────────────────────────────────────────────────┤
│                    FRONTEND (Atomic Design)                   │
│  Primitives → Components → Modules → Views → Artifacts        │
│  Извлекаются из backend когда обнаружен переиспользуемый      │
│  паттерн, Law или Relation                                    │
│  Primitives ссылаются на backend (`derived_from`),            │
│  не дублируют данные                                          │
│  Продукт: compositional knowledge, готовые артефакты          │
└──────────────────────────────────────────────────────────────┘
```

### Backend: спецификация

**Принцип:** один компонент = один файл. Аггрегат целостен. Никакой фрагментации.

```yaml
# backend/hardware/gpu/nvidia-rtx-5060.yaml
id: nvidia-rtx-5060
vendor: nvidia
architecture: Blackwell
specs:
  vram:
    size_gb: 8
    type: GDDR7
    bus_width_bit: 128
    bandwidth_gb_s: 355
  compute:
    cuda_cores: 3840
    rt_cores: 30
    tensor_cores: 120
  clock:
    boost_ghz: 2.50
  power:
    tdp_w: 150
observations:
  - {game: "CP2077", config: "1440p High", fps: 68, confidence: 0.95}
  - {game: "AW2", config: "1440p Medium", fps: 61, confidence: 0.90}
```

**Ключевые свойства backend:**
- **Поля нормализованы.** `specs.vram.bus_width_bit` называется одинаково во всех GPU-файлах. Это конвенция, не схема — достаточная для cross-reference
- **Нет композиции.** Backend не знает что такое Primitive, Component, Module. Он просто хранит факты
- **Изолированные контексты.** `hardware/gpu/`, `hardware/cpu/`, `coffee/` — каждый со своей структурой полей
- **Один файл на сущность.** GPU, CPU, кофейный напиток — каждый в одном файле. Observation 001 удовлетворено

### Frontend: спецификация

**Принцип:** Primitives не дублируют backend. Они извлекаются когда обнаружен переиспользуемый паттерн и добавляют то, чего в данных нет — интерпретацию.

```yaml
# frontend/primitives/laws/gddr7-bandwidth-compensation.yaml
type: Law
title: "GDDR7 Bandwidth Compensation Law"
statement: >
  GDDR7 на 128-битной шине даёт bandwidth, сравнимый с GDDR6X на 192-битной
  (355 vs 360 GB/s соответственно). Это позволяет NVIDIA экономить на bus width
  без потери пропускной способности в целевом классе производительности.
derived_from:
  - backend/hardware/gpu/nvidia-rtx-5060.yaml     # 128-bit GDDR7 = 355 GB/s
  - backend/hardware/gpu/nvidia-rtx-4060-ti.yaml  # 128-bit GDDR6 = 288 GB/s
  - backend/hardware/gpu/nvidia-rtx-4070.yaml     # 192-bit GDDR6X = 504 GB/s
applies_to:
  - nvidia-rtx-5060
  - nvidia-rtx-5060-ti
  - nvidia-rtx-5070
```

Этот Law **не существовал** в backend. Он — emergent insight, обнаруженный при cross-source synthesis. Backend содержит факты (bandwidth значений для разных карт), frontend содержит открытие (паттерн, который их объединяет).

**Ключевые свойства frontend:**
- **Primitive = интерпретация + ссылка на данные.** Не дубликат факта
- **`derived_from` обязательно.** Primitive без traced источников невалиден
- **Переиспользуемость настоящая.** Law «500W GPU требует 1000W+ БП» ссылается на все 500W-карты в backend, не привязан к одной
- **Композиция на уровне интерпретаций, не фактов.** Component собирает Laws и Relations, не сырые спецификации

### Переходы между слоями

```
Acquisition → Backend:
  candidate fact extracted from raw source → validate against schema → write to backend

Backend → Frontend (PROMOTE):
  cross-source pattern discovered → verify against backend data → create Primitive
  с derived_from и applies_to

Acquisition → Frontend (DIRECT PROMOTE):
  candidate Law/Relation from exploratory synthesis → verify against backend → create Primitive
```

**Promote gate (Backend → Frontend):** capability `pattern-promote`. Проверяет:
1. Все `derived_from` ссылки ведут на существующие backend-файлы
2. `applies_to` не противоречит данным в backend
3. Primitive проходит `primitive-validate`

### Что происходит с текущим minerva

Текущий minerva (`primitives/`, `components/`, `modules/`, `views/`, `artifacts/`) — это **только Frontend**. Он остаётся без изменений структурно, но меняется семантически:

- `primitive-create` больше не принимает сырые значения — он принимает `derived_from` + интерпретацию
- Существующие Primitives в `hardware/primitives/` (RTX 5090) — кандидаты на реструктуризацию: спецификации возвращаются в backend, Laws и Relations остаются
- Coffee-контекст (`coffee/primitives/`) — пересматривается: что из этого данные (→ backend), а что интерпретация (→ frontend)?

**Новое в структуре minerva:**

```
minerva/
├── SKILL.md
├── capabilities/
│   ├── ... (Tier 0–4 без изменений)
│   └── pattern-promote/          # новый: Backend → Frontend gate
├── backend/                      # новый: сырые данные
│   ├── index.md                  # карта контекстов данных
│   ├── hardware/
│   │   ├── gpu/                  # один файл на GPU
│   │   ├── cpu/                  # один файл на CPU
│   │   └── ...
│   └── coffee/
│       ├── origins/              # один файл на страну происхождения
│       ├── varieties/            # один файл на сорт
│       └── ...
└── references/                   # = frontend (Atomic Design)
    ├── index.md
    ├── context-map.md
    ├── hardware/
    │   ├── primitives/
    │   ├── components/
    │   ├── modules/
    │   ├── views/
    │   └── artifacts/
    └── coffee/
        └── ...
```

## Коррекция ошибки

В Observation 001 и первоначальном анализе было утверждение: «спецификации не переиспользуемы. Спецификация "CUDA Cores: 20480" не переиспользуется другими картами — у каждой своё значение.»

Это утверждение **неверно.** Пример, который его опровергает:

> GDDR7 на 128-битной шине (RTX 5060: 355 GB/s) даёт bandwidth, сравнимый с GDDR6X на 192-битной шине (RTX 4070: 504 GB/s, но на бит — 2.6 vs 2.8 GB/s). И с GDDR6 на 128-битной (RTX 4060: 272 GB/s). Паттерн: NVIDIA использует GDDR7 чтобы компенсировать узкую шину на xx60-классе, экономя на стоимости чипа и PCB.

Для обнаружения этого паттерна нужны спецификации из **четырёх разных GPU-файлов**. Они переиспользуемы — но не как самостоятельные сущности, а как **исходные данные для вывода Laws**. Переиспользуемость не в дублировании значений, а в том что одно значение служит evidence для нескольких выводов.

Утверждение «не переиспользуемы» было артефактом архитектуры, которая хоронила спецификации внутри Primitives, не давая им участвовать в cross-source discovery. Backend/frontend split это исправляет: спецификации лежат в backend как первые-class граждане, доступные для cross-reference.

## Что НЕ фиксируем

- **Формат backend-файлов.** YAML? JSON? Markdown с frontmatter? Решается при реализации. Важны свойства: machine-readable, нормализованные имена полей, один файл на сущность
- **Схема полей для каждого контекста.** `hardware/gpu/` имеет свою структуру, `coffee/` — свою. Конвенции, не глобальная схема
- **Механизм cross-reference в backend.** query.py? Структурные запросы? Graph DB? Tier 4 capabilities будут определены позже
- **Миграция существующих данных.** `catalog/` (75+ файлов) → `backend/` — отдельный проект

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Оставить всё в одном слое (текущий minerva) | Проще ментальная модель | Смешивает данные и композицию, убивает переиспользуемость и cross-source discovery | Утверждение «спецификации не переиспользуемы» оказалось ошибкой, порождённой именно этим смешением |
| Backend как часть Frontend (спецификации = Primitives) | Меньше файлов, меньше слоёв | Primitive без интерпретации — это не Primitive, а факт в костюме. Концептуальный мусор | Backend-файлы должны быть свободны от композиционной таксономии чтобы использоваться в разных выводах |
| Единая схема данных для всех контекстов | Cross-reference тривиален («все GPU имеют поле bandwidth») | Разные контексты имеют разную природу — coffee не имеет bandwidth. Единая схема либо слишком абстрактна, либо ломается на разных доменах | Конвенции на уровень контекста, не глобальная онтология |

## Связь

- **ADR-012:** определяет Acquisition layer. ADR-013 добавляет Backend/Frontend split под ним
- **Observation 001:** напряжение Atomic Design vs Aggregate — разрешается: backend хранит Аггрегат целостно, frontend даёт композицию когда она нужна
- **Observation 002:** gap NotebookLM vs minerva — закрывается: backend даёт нормализованные данные для cross-source discovery, acquisition — интерфейс для exploration
- **ADR-002:** Five-level hierarchy (Primitives → Artifacts) — теперь это чисто Frontend-концепт
- **ADR-004:** Six Primitive types — остаются без изменений, но Primitives теперь всегда имеют `derived_from`
- **ADR-006:** KB = файлы — подтверждается. Backend и Frontend — оба файловые

## Последствия

**Что становится проще:**
- **Аггрегат целостен.** Backend: один файл на GPU. Читается сверху вниз. Progressive disclosure естественный
- **Переиспользуемость реальна.** Одна спецификация в backend служит evidence для множества Primitives в frontend. Law связывает несколько backend-файлов
- **Cross-source discovery возможен.** Backend поля нормализованы → machine может сравнивать bandwidth 5060 и 4060 без ручного сопоставления
- **Разные домены — разные схемы.** Backend coffee не обязан иметь `specs.vram.bus_width_bit`. Каждый контекст со своей структурой
- **Acquisition получает ясную цель.** Extract → Backend. Discover → Frontend. Два разных перехода

**Что усложняется:**
- **Три слоя вместо одного.** Acquisition → Backend → Frontend. Ментальная модель сложнее
- **Два promote gate.** Acquisition → Backend (validation) и Backend → Frontend (pattern-promote). Нужны критерии для каждого
- **Согласованность.** Если backend-факт изменился (TDP с 250W на 280W), frontend Laws должны быть проверены — не сломало ли это вывод?
- **Миграция.** 75+ legacy-файлов в `catalog/` нужно перенести в `backend/`. 3 существующих Primitives — пересмотреть: что данные (→ backend), что интерпретация (→ frontend)

**Что требует внимания:**
- **Promote gate не должен стать bottleneck.** Если каждый Law требует ручного promote, cross-source discovery не масштабируется. Нужен semi-automated promote: candidate pattern → agent проверяет против backend → предлагает promote
- **Backend не должен пытаться стать «единой онтологией». Hardware и coffee — принципиально разные контексты. Попытка унифицировать их схему убьёт домен-агностичность**
- **Приоритет миграции.** Coffee-контекст имеет 6 Primitives — простой кандидат для первого backend/frontend split. Hardware — 75+ файлов, сложнее
