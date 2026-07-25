---
name: forecast-lifecycle
description: "Прогноз остаточного ресурса связки CPU+GPU. Reasoning model на исторических трендах IPC, движков, DLSS. Возвращает LifecycleForecast — per-year вероятность CPU bottleneck с доверительным интервалом и per-genre inflection points."
type: capability
capability:
  input:
    cpu_id: "string — Minerva dim ID или свободное имя (резолвится через context-map aliases)"
    gpu_id: "string — аналогично"
    settings: "string — '1440p-ultra', '1080p-low'. Default: '1440p-ultra'"
    horizon_years: "integer — горизонт прогноза от текущего года. Default: 6"
  output: "LifecycleForecast (YAML/structured) — per-year bottleneck probability + per-genre inflection points + explicit assumptions with epistemic markers"
  invariants:
    - "Каждый прогнозный claim имеет epistemic_marker: observed_trend / extrapolation / speculative_estimate"
    - "confidence не завышается — calibration enforced через back-test на исторических CPU"
    - "GPU-специфичные данные (DLSS generation, FG multiplier, tensor gen) используются при наличии в dim/gpu"
    - "Если CPU/GPU нет в Minerva — модель reasoning-extrapolates из ближайшего известного (с явным указанием proxy)"
    - "Per-genre forecast обязателен — минимум 4 жанра: aaa_shooter, rts, city_builder, mmo"
  pitfals:
    - "Не экстраполировать линейно за пределы 7-8 лет — исторический предел жизни CPU"
    - "Не игнорировать MFG asymmetry: FG снижает GPU-load, НЕ CPU-load. Это центральная механика прогноза."
    - "Не давать точечных прогнозов — всегда доверительный интервал"
    - "Back-test обязателен перед первым production-прогнозом"
  contract_ref: "references/forecast-contract.yaml"
  calibration_ref: "references/epistemic-calibration.md"
  triggers:
    - "прогноз жизненного цикла"
    - "когда процессор устареет"
    - "bottleneck forecast"
    - "остаточный ресурс сборки"
    - "CPU bottleneck prediction"
    - "когда CPU станет ограничителем"
    - "lifecycle forecast"
    - "прогноз для сборки"
---

# Forecast Lifecycle — Capability

Прогнозирует момент, когда CPU перестанет успевать готовить кадры быстрее, чем GPU сможет их рисовать — с учётом DLSS/Frame Generation.

## Model (как устроен мир)

### Центральная механика

```
FrameTime_CPU(year, genre)  — растёт со временем (engine complexity ↑, IPC relative gap ↑)
FrameTime_GPU(year)          — падает со временем (DLSS/FG generations, raster uplift)

Bottleneck: FrameTime_CPU > FrameTime_GPU  →  CPU — ограничитель
```

**Ключевая асимметрия (MFG):** Frame Generation снижает *воспринимаемую* GPU-нагрузку но НЕ снижает CPU-нагрузку. CPU считает мир на частоте базового рендера. Когда базовый рендер падает до 30-35 fps — MFG даёт артефакты (input lag, interpolation artefacts). CPU умирает не потому что медленный, а потому что GPU с новыми поколениями DLSS становится *слишком* быстрым.

### Переменные модели

| Переменная | Источник | Тип знания |
|---|---|---|
| CPU IPC (текущий) | Minerva dim/cpu + assessment profile | training_data / benchmark |
| GPU perf (текущий) | Minerva dim/gpu + training data | training_data / spec |
| CPU IPC trajectory (12-18%/gen) | Training data — исторический тренд 2008-2025 | observed_trend |
| GPU raster/FG trajectory (25-30%/gen raster, DLSS gen ~2yr) | Training data — NVIDIA/AMD generational data | observed_trend |
| Engine complexity growth (15-20% per 2-3yr) | Training data — historical minimum specs, DF analysis | observed_trend |
| AI NPC overhead (+30-50% step change) | Экспертная оценка | speculative_estimate |
| Per-genre CPU scaling | Training data — benchmark patterns per genre | observed_trend |
| Console generation cycle (7yr) | Training data — PS3→PS4→PS5→PS6 | extrapolation |
| Diminishing returns ceiling (>8 threads AAA) | Training data — NVIDIA CPU scaling research | observed_trend |

## Process

### 1. Разрешить CPU и GPU

```
context-map.yaml (aliases) → dim_id → dim/cpu/{id}.yaml + dim/gpu/{id}.yaml
                                 → assessment/cpu/profiles/{id}.yaml (если есть)
```

Если компонента нет в Minerva — взять ближайший proxy (тот же кристалл/архитектура) и явно указать substitution в output.

### 2. Снять текущий snapshot

Из Minerva: спецификации (ядра, частоты, кэш, TDP, сокет, архитектура), бенчмарки (1080p low, 1440p ultra — 1% low mean), platform lifecycle (socket_lifecycle, upgrade_note).

Из training data: GPU generational position (DLSS gen, FG multiplier, RT gen, tensor gen), relative perf vs competitors.

### 3. Построить траектории (per-year reasoning)

Для каждого года t ∈ [current, current + horizon]:

**CPU side:**
- IPC gap vs latest gen: current_year IPC × (1 - cumulative_gen_gains)
- Engine complexity multiplier: base_complexity × (1 + complexity_growth)^(t − current)
- Per-genre modifier: genre_cpu_coefficient × complexity_multiplier
- Parallelism headroom: min(effective_P_cores, genre_parallelism_ceiling) / effective_P_cores

**GPU side:**
- Raster baseline vs CPU: relative to current GPU capability
- DLSS gen at year t: which DLSS generation is available
- FG multiplier: frames generated per rendered frame
- Effective GPU throughput: raster_baseline × fg_multiplier × dlss_quality_factor

**Intersection test:**
- `bottleneck_prob(t) = P(FrameTime_CPU(t) > FrameTime_GPU(t))`
- Распределение из Monte Carlo reasoning по неопределённостям

### 4. Per-genre decomposition

Минимум 4 жанра. Для каждого:
- `cpu_coefficient`: AAA Shooter 0.7, RTS 1.4, City Builder 1.6, MMO 1.2, Simulator 1.3
- `inflection_year`: первый год где bottleneck_prob > 0.5
- `inflection_prob`: вероятность в inflection_year

### 5. Back-test calibration

Перед production-прогнозом — проверить модель на известных исторических парах:

| CPU | GPU | Год «смерти» | Предсказание модели |
|---|---|---|---|
| i5-2500K (2011) | GTX 560 Ti | ~2016 (5 лет) | ? |
| i7-4790K (2014) | GTX 970 | ~2019 (5 лет) | ? |
| i5-8400 (2017) | GTX 1060 | ~2022 (5 лет) | ? |
| Ryzen 5 3600 (2019) | RTX 2060 | ~2025 (6 лет) | ? |

Если модель систематически ошибается (предсказывает >7 лет когда реально 5) — понизить confidence baseline глобально.

## Output Contract

См. `references/forecast-contract.yaml` — полная структура LifecycleForecast.

**Ключевые требования:**
- `epistemic_markers` на каждый прогнозный claim
- `confidence_interval` для per-year вероятностей
- `substitutions` — явное указание proxy-CPU/GPU если целевого нет в Minerva
- `disclaimers` — что модель НЕ учитывает (новые ISA, heterogeneous computing, прорывы)

## Pitfalls

1. **Линейная экстраполяция за 7+ лет.** После 7-8 лет точность падает радикально. Confidence должен отражать это: ±8 п.п. для года +2, ±18 п.п. для года +6.

2. **Игнорирование MFG asymmetry.** Самая частая ошибка: «GPU станет быстрее → сборка проживёт дольше». Наоборот: GPU станет быстрее → CPU станет ограничителем РАНЬШЕ. FG не спасает CPU.

3. **Overconfidence на speculative estimates.** AI NPC, UE6 — speculative. confidence ≤ 0.6 на этих факторах.

4. **Забыть про platform lifecycle.** LGA1700 — legacy. Следующий апгрейд CPU требует новой платы. Это часть прогноза: не только «когда CPU устареет», но и «стоит ли апгрейдиться на этой платформе».

5. **Не учитывать монитор.** Если пользователь на 60Hz — bottleneck наступает позже. Если на 240Hz — раньше. Target refresh rate — входной параметр.

## Integration with Minerva

```
Minerva DWH
├── dim/cpu/{id}.yaml              → спецификации, архитектура, release date
├── dim/gpu/{id}.yaml              → спецификации, DLSS gen, FG multiplier
├── assessment/cpu/profiles/       → текущие бенчмарки (snapshot anchor)
└── engineering/laws/              → известные закономерности (3D V-Cache, Zen 5 uplift)

Model (reasoning engine)
├── Исторические тренды IPC        → training data
├── Engine complexity trajectory   → training data
├── DLSS/FG evolution              → training data
├── Per-genre scaling patterns     → training data
└── Console generation cycle       → training data

Output → LifecycleForecast (YAML/structured)
```
