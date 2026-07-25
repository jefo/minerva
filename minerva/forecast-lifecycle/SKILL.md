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
  pitfalls:
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

## Model

Центральная механика: `FrameTime_CPU(year, genre)` растёт со временем (engine complexity ↑, IPC relative gap ↑). `FrameTime_GPU(year)` падает (DLSS/FG generations, raster uplift). Bottleneck: `FrameTime_CPU > FrameTime_GPU`.

**Ключевая асимметрия (MFG):** Frame Generation снижает *воспринимаемую* GPU-нагрузку но НЕ снижает CPU-нагрузку. CPU считает мир на частоте базового рендера. Когда базовый рендер падает до 30-35 fps — MFG даёт артефакты. CPU умирает не потому что медленный, а потому что GPU с новыми поколениями DLSS становится *слишком* быстрым.

## Process

### 1. Anchor: загрузить данные из Minerva
- `dim/cpu/{id}.yaml` + `dim/gpu/{id}.yaml` — спецификации
- `assessment/cpu/profiles/{id}.yaml` — текущие бенчмарки (если есть)
- `engineering/laws/` — известные закономерности
- Если компонента нет в Minerva — proxy с явным указанием

### 2. Snapshot: снять текущее состояние
- CPU: архитектура, ядра, частоты, кэш, TDP, сокет + lifecycle, IPC relative position
- GPU: архитектура, DLSS gen, FG multiplier, RT/tensor gen, VRAM
- Бенчмарки: 1% low mean в 1080p low и 1440p ultra

### 3. Trajectory: построить per-year проекции
Для каждого года t ∈ [current, current + horizon]:

**CPU side:**
- IPC gap vs latest gen: current_year IPC × (1 − cumulative_gen_gains)
- Engine complexity multiplier: base × (1 + growth_rate)^(t−current)
- Per-genre modifier: genre_cpu_coefficient × complexity
- Parallelism headroom: min(P_cores, genre_ceiling) / P_cores

**GPU side:**
- DLSS gen at year t + FG multiplier
- Effective GPU throughput: raster × fg_multiplier × dlss_quality
- Bottleneck test: P(FrameTime_CPU > FrameTime_GPU) → per-year probability

### 4. Per-genre decomposition
Минимум 4 жанра с cpu_coefficient:
- aaa_shooter: 0.7 (GPU-тяжёлый)
- rts: 1.4 (simulation-heavy)
- city_builder: 1.6 (agent simulation)
- mmo: 1.2 (entities, server-authoritative)
- simulator: 1.3 (physics)
- esports: 0.9 (high-fps floor)

Для каждого жанра: inflection_year (bottleneck_prob > 0.5) + inflection_probability.

### 5. Epistemic markers
Каждый claim в assumptions имеет basis из словаря:
- `engineering_fact` — confidence ≥ 0.90
- `observed_trend` — confidence 0.80-0.90
- `extrapolation` — confidence 0.65-0.80
- `speculative_estimate` — confidence 0.40-0.60

### 6. Back-test calibration
Перед production-прогнозом — проверить на исторических парах:
- i5-2500K + GTX 560 Ti (2011 → death ~2016)
- i7-4790K + GTX 970 (2014 → death ~2019)
- i5-8400 + GTX 1060 (2017 → death ~2022)
- Ryzen 5 3600 + RTX 2060 (2019 → death ~2025)

Если systematic error >30% — понизить confidence_baseline глобально.

## Output

Полный контракт: `references/forecast-contract.yaml`.

Структура: combo → meta → snapshot → assumptions → forecast_by_year → forecast_by_genre → platform → disclaimers.

## Pitfalls

1. **Не экстраполировать линейно за 7+ лет.** ±20pp confidence interval для +6yr.
2. **MFG asymmetry.** FG не спасает CPU. Всегда explicit в assumptions.
3. **Overconfidence на speculative estimates.** AI NPC, UE6 — confidence ≤ 0.6.
4. **Platform lifecycle.** LGA1700 = legacy. Это часть прогноза — не только CPU bottleneck, но и TCO.
5. **Monitor target.** 60Hz vs 240Hz — разный inflection year. Учитывать target refresh rate.
