---
id: adr-021
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [validation, walkthrough, end-to-end, thought-experiment, verifiability]
based_on: [adr-012, adr-013, adr-014, adr-015, adr-016, adr-017, adr-018, adr-019, adr-020]
---

# ADR-021: Architecture Validation — end-to-end walkthrough (RTX 5060)

## Контекст

ADR-012–020 определили полную архитектуру minerva на DW-фундаменте. Теперь нужно проверить её связность на конкретном сквозном сценарии: от поступления сырых данных до опубликованного артефакта и его обновления при изменении реальности.

Этот ADR — не решение, а **верификация решений**: демонстрация того что архитектура связна, прослеживаема и выдерживает поток изменений.

## Сценарий: RTX 5060 — полный жизненный цикл данных

### Фаза 1: Acquisition — первый источник (ETL)

**Действие:** аналитик импортирует RTX 5060 из NVIDIA ARK.

```
capability: source-extract(source_type="api", source_params={url: "nvidia.com/rtx-5060-spec"})
```

**Extract:** `acquisition/raw/nvidia-ark/rtx-5060-extract.yaml` — сырые данные как они пришли. Строки, не числа. «8 GB GDDR7», «128-bit», «355 GB/s», «150 W».

**Transform:** `transform-normalize` применяет mapping `nvidia-ark-to-gpu-dim.yaml`:
- «8 GB GDDR7» → `vram: {size_gb: 8, type: "GDDR7"}`
- «128-bit» → `bus_width_bit: 128`
- «355 GB/s» → `bandwidth_gb_s: 355`
- «150 W» → `tdp_w: 150`

Выход: `acquisition/staged/dim/gpu/nvidia-rtx-5060.yaml`.

**Load:** `warehouse-load` → `dim-upsert`. SCD Type 0 (архитектура не меняется). Создан первый Dimension:

```
warehouse/hardware/dim/gpu/
└── nvidia-rtx-5060.yaml
```

Git commit: `"acquisition: import RTX 5060 from NVIDIA ARK"`.

### Фаза 2: Конфликт источников (ETL data quality)

**Действие:** импорт RTX 5060 из TechPowerUp. Тот же GPU, но `bandwidth: 352 GB/s` (NVIDIA ARK: 355 GB/s).

`conflict-detect`: расхождение 0.8% (< 5%). Принят manufacturer source. Разрешено автоматически. В lineage добавляется запись о двух источниках.

Warehouse не изменился. Конфликт задокументирован: `acquisition/conflicts/rtx-5060-bandwidth.yaml`.

### Фаза 3: Первые Observations (Fact creation)

**Действие:** импорт пользовательского бенчмарка: RTX 5060 + CP2077 1440p High на драйвере 572.16.

`fact-insert`: создан Observation. Попутно `dim-upsert` для Dimensions, которых ещё нет: `game_title/cyberpunk-2077.yaml`, `resolution/1440p.yaml`, `graphics_preset/high.yaml`, `driver_version/nvidia-geforce-572.16.yaml`.

```
warehouse/hardware/fact/observations/
└── rtx5060-cp2077-1440p-high-driver572.yaml
    measures: {fps_avg: 68, fps_1pct_low: 52}
    confidence: 0.95 (user_verified)
    dimensions: {gpu, game, resolution, preset, driver}
```

После нескольких импортов — аналогичные Observations для RTX 4060 (52 fps) и RTX 4070 (78 fps) в той же игре.

### Фаза 4: Cross-source discovery — рождение Law

**Действие:** агент-аналитик замечает паттерн в bandwidth.

```
capability: cross-reference(dim_ref="nvidia-rtx-5060", fact_type="observation")
           → 3 Observation
capability: cross-reference(dim_ref="nvidia-rtx-4060", fact_type="observation")
           → 2 Observation
```

```
capability: comparison(dim_a="nvidia-rtx-5060", dim_b="nvidia-rtx-4060",
                        metrics=["bandwidth_gb_s", "vram.type", "vram.bus_width_bit"])
           → {bandwidth: +30.5%, type: GDDR7 vs GDDR6, bus_width: 128 vs 128}

capability: comparison(dim_a="nvidia-rtx-5060", dim_b="nvidia-rtx-4070",
                        metrics=["bandwidth_gb_s", "vram.type", "vram.bus_width_bit"])
           → {bandwidth: -29.6%, type: GDDR7 vs GDDR6X, bus_width: 128 vs 192}
```

Агент видит: GDDR7 на 128-bit даёт bandwidth, сравнимый с GDDR6X на 192-bit. Формулирует Law.

```
capability: pattern-promote(
    type="law",
    statement="GDDR7 Bandwidth Compensation: 128-bit GDDR7 ≈ 192-bit GDDR6X",
    applies_to=["nvidia-rtx-5060", "nvidia-rtx-5060-ti", "nvidia-rtx-5070"],
    lineage={
      nodes: [
        {ref: "fact/metrics/rtx5060-bandwidth", role: "evidence"},
        {ref: "fact/metrics/rtx4060-bandwidth", role: "baseline"},
        {ref: "fact/metrics/rtx4070-bandwidth", role: "reference"}
      ],
      edges: [
        {from: "rtx5060-bandwidth", to: "gddr7-law", type: "generalizes"},
        {from: "rtx4060-bandwidth", to: "gddr7-law", type: "generalizes"},
        {from: "rtx4070-bandwidth", to: "gddr7-law", type: "generalizes"}
      ]
    })
```

`pattern-promote` → `lineage-validate` → ✅ PASS. Создан:

```
marts/engineering/laws/
└── gddr7-bandwidth-compensation.yaml
```

### Фаза 5: Меняется реальность — SCD в действии

**Действие:** NVIDIA выпускает драйвер 575.10. Patch notes: «Cyberpunk 2077 +3 FPS».

ETL для драйвера → `scd-apply` создаёт новую версию Dimension:

```
dim/driver_version/
├── nvidia-geforce-572.16.yaml              # заголовочный: current_version обновлён
├── nvidia-geforce-572.16_v2026-03.yaml     # старая версия
└── nvidia-geforce-575.10_v2026-06.yaml     # ← новая
```

`impact-analysis` → `affected_derived: [gddr7-bandwidth-compensation]`. Law требует проверки.

Новый замер: RTX 5060 + CP2077 1440p High на драйвере 575.10 → 71 fps (+3).

Новый Fact: `rtx5060-cp2077-1440p-high-driver575.yaml` (driver → новая версия).

Проверка Law: bandwidth — Dimension-атрибут, не Observation. Не изменился. Law подтверждён. Добавлено ребро `supports` в lineage. Status: `requires_review` → `confirmed`.

### Фаза 6: Сборка артефакта

**Действие:** редактор собирает страницу обзора.

```
capability: artifact-compile(
    view="narrative-view",
    modules=["rtx-5060-engineering", "rtx-5060-competitive"],
    title="RTX 5060: GDDR7 на 128 битах — обзор")
```

Собирает из: Narrative View (схема) + Engineering Mart (GPU + Metrics + Laws) + Competitive Mart (сравнения). Для каждого derived Fact → `lineage-trace` → подтягивает исходные Observations.

```
artifacts/
└── rtx-5060-review.md
    stale_if:
      - "warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml"
      - "marts/engineering/laws/gddr7-bandwidth-compensation.yaml"
      - "warehouse/hardware/fact/observations/rtx5060-cp2077-1440p-high-driver575.yaml"
    status: "fresh"
```

### Фаза 7: Stale detection и регенерация

**Действие:** месяц спустя. Новый драйвер 580.xx с DLSS 4.1. Новые Observations.

```
capability: stale-check()
```

Возвращает: `rtx-5060-review.md → stale`. Причины: новый Observation заменил использованный в артефакте; Law `gddr7-bandwidth-compensation` требует перепроверки.

Редактор: `artifact-regenerate` → страница пересобрана с актуальными данными. Новый `materialized_at` и `data_as_of`.

## Верификация архитектурных решений

### Что подтвердилось

| ADR | Решение | Как проявилось в сценарии |
|---|---|---|
| 012 — Acquisition | ETL Extract слой | Фаза 1: источник → extract → transform → load. Граница чистая |
| 013 — Backend/Frontend | Warehouse ≠ Data Marts | Law (marts/) ссылается на Fact (warehouse/), не дублирует |
| 014 — DW фундамент | Kimball как основа | Star Schema, SCD, Conformed Dimensions — все задействованы |
| 015 — System Architecture | Компоненты + data flow | Acquisition → Warehouse → Data Marts → Artifacts. Поток однонаправленный |
| 016 — Data Model | Fact + Dimension + SCD | Observation Fact атомарен. Dimension — wide table. SCD Type 2 для driver |
| 017 — Lineage DAG | Граф с типами рёбер | Law → generalizes → Facts. Потом supports от нового Fact. DAG расширяется |
| 018 — ETL Pipeline | Extract → Transform → Load | Конфликт источников (фаза 2) обнаружен и разрешён на стадии Transform |
| 019 — Agent Query | Capabilities как stored procedures | cross-reference → comparison → pattern-promote. Контракты соблюдены |
| 020 — Methodology | Правила проектирования | Факты атомарны. Data Marts не дублируют. Bus Matrix — SSOT имён |

### Что проявило слабые места

**1. Conflict resolution — semi-automated.** Фаза 2: расхождение 0.8% разрешилось автоматически. Но если бы расхождение было 8%, потребовалось бы ручное решение. Механизм есть (`contested`), но процесс не определён: кто разрешает, за какое время?

**2. Impact analysis — потенциальный шум.** Фаза 5: impact-analysis вернул Law как affected. Но Law оказался не затронут (bandwidth не изменился). Анализ консервативен: «ссылается на driver → требует проверки». Это лучше чем пропустить, но может создавать ложные срабатывания при массовых обновлениях драйверов.

**3. Artifact staleness — каскад.** Фаза 7: новый драйвер → новые Observations → Law требует проверки → Artifact stale. При массовом обновлении (новый драйвер для 15 GPU) — каскад stale по всем артефактам. Механизм есть, но регенерация может быть дорогой.

## Сквозная прослеживаемость (полная цепочка)

```
nvidia.com/rtx-5060-spec                     # URL источника
    ↓ ETL (2026-07-11, commit a1b2c3)
warehouse/dim/gpu/nvidia-rtx-5060.yaml       # Dimension
    ↓ fact-insert
warehouse/fact/observations/rtx5060-cp2077-*.yaml  # Fact
    ↓ pattern-promote
marts/engineering/laws/gddr7-bandwidth-compensation.yaml  # Derived
    ↓ artifact-compile
artifacts/rtx-5060-review.md                 # Published
```

Каждый шаг: файл + git commit + lineage DAG. Любой вывод проверяем до исходного URL за O(depth) вызовов `lineage-trace`.

## Заключение

Архитектура связна. Поток данных однонаправлен. Прослеживаемость полная. Слабые места идентифицированы, но не блокируют: conflict resolution — процесс, не архитектура; impact analysis conservative — допустимо для v1; stale cascades — решается приоритезацией регенерации.

Проект готов к реализации.
