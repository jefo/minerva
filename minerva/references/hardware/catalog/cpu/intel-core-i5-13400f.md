---
id: "intel-core-i5-13400f"
type: "cpu"
title: "Intel Core i5-13400F (Raptor Lake)"
vendor: "Intel"
status: "draft"
tags: ["intel", "raptor-lake", "lga1700", "6p4e", "16t", "no-igpu", "65w", "ddr4", "hybrid"]
last_updated: "2026-07-06"
links:
  smaller_brother: "catalog/cpu/intel-core-i5-12400f.md"
  bigger_brother: "catalog/cpu/intel-core-i5-14600k.md"
  platform: "catalog/motherboard/lga1700/index.md"
specs:
  socket: "LGA1700"
  architecture: "Raptor Lake (Intel 7)"
  architecture_generation: 13
  codename: "Raptor Lake-S (Alder Lake silicon)"
  sku: "i5-13400F"
  sku_family: "i5"
  release_date: "Q1 2023"
  status: "released"

  total_cores: 10
  total_threads: 16
  p_cores: 6
  e_cores: 4
  p_core_arch: "Golden Cove (Alder Lake silicon, rebranded)"
  e_core_arch: "Gracemont"
  smt_ht: true
  thread_director: true

  l2_per_pcore: "1.25 MB"
  l2_per_ecluster: "2 MB"
  l2_total: "9.5 MB (7.5 MB P + 2 MB E)"
  l3_cache: "20 MB (shared Intel Smart Cache)"

  base_clock_p: "2.5 GHz"
  base_clock_e: "1.8 GHz"
  boost_clock_p_max: "4.6 GHz"
  boost_clock_e_max: "3.3 GHz"
  boost_clock_p_all: "4.1 GHz"

  tdp_pl1: "65W"
  tdp_pl2: "148W"
  tjmax: "100°C"
  typical_gaming_power: "55-70W"

  lithography: "Intel 7 (10nm Enhanced SuperFin)"
  die_topology: "monolithic (Alder Lake C0 stepping)"

  chipset_generation: "Intel 600/700 Series"
  memory_type: "DDR4 / DDR5"
  memory_channels: 2
  jedec_max: "DDR4-3200 / DDR5-4800"

  pcie_version: "5.0 / 4.0"
  pcie_lanes_cpu: 20
  pcie_config_primary: "1x16 PCIe 5.0 + 1x4 PCIe 4.0"

  igpu_present: false

  avx512: false
  avx2: true

  box_cooler_included: true
  box_cooler_model: "Intel Laminar RM1"
  cooler_recommended: "DeepCool AK400 (достаточен для игр, слышен при PL2 148W)"
  multiplier_locked: true

  msrp_usd_launch: 196
  price_ru_min: 12000
  price_ru_median: 13500
  price_ru_max: 15000
  price_ru_date: "2026-07-06"
  price_ru_source: "price.ru / DNS / Ozon"
  segment: "budget-hybrid"
profiles:
  hybrid_entry_cpu:
    power_envelope: "low"
    capability_level: 1
    steel_man_desc: "6P+4E — младшая гибридная архитектура. E-ядра изолируют фоновый мусор (браузер, Discord, Docker-демоны, IDE-индексацию) от игровых P-ядер. 148W PL2 — кратковременный всплеск только при all-core билде."
    failure_mode_desc: "PL2=148W — AK400 слышен при sustained all-core. Alder Lake C0 silicon — не настоящий Raptor Lake. L2 меньше чем у 13600K."
    optimal_for_intents: ["aaa_1440p_high", "dev_docker_hybrid", "streaming_nvenc"]
    failure_for_intents: ["esports_1080p_240hz", "cpu_rendering"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 12000
  median: 13500
  max: 15000
  source: "price.ru / DNS / Ozon"
  date: "2026-07-06"
  status: "verified"
platform_req:
  motherboard_min: "B660 / B760"
  motherboard_opt: "B760 (гарантированная поддержка 13-gen из коробки)"
  cooler_min: "DeepCool AK400"
  cooler_opt: "DeepCool AK400 (для игр) / AK620 (для sustained all-core)"
  memory_sweet_spot: "DDR4-3200 CL16"
  psu_min_system: "550W"
engineering_notes:
  - "⚠️ Alder Lake C0 stepping с брендингом Raptor Lake. Не настоящий Raptor Cove — Golden Cove P-cores."
  - "6P+4E: ключевое преимущество над 12400F — 4 E-ядра для фоновой изоляции. Thread Director работает в Windows 11."
  - "PL2=148W — на 31W выше чем 117W у 12400F. AK400 становится слышен (1400 RPM) при sustained all-core билде."
  - "В играх (только P-cores) потребление 55-70W — идентично 12400F. Кулер на 800 RPM, бесшумен."
  - "DDR4-3200 sweet spot. DDR5 даёт +0-3% FPS, не оправдывает цену."
verdict: "i5-12400F с E-ядрами. +3 500 ₽ за +4 Gracemont ядра — покупка ради многозадачности, не FPS. Для dev-среды (Docker + IDE + браузер) E-cores дают реальную изоляцию фона от игры. Для чистого гейминга — переплата."
---

# Intel Core i5-13400F (Raptor Lake, LGA1700)

## Позиционирование

Intel Core i5-13400F — 10-ядерный (6P+4E/16T) процессор поколения Raptor Lake. Фактически: Alder Lake C0 silicon с брендингом Raptor Lake — P-cores Golden Cove, не Raptor Cove. Главное отличие от 12400F: 4 E-ядра Gracemont для фоновой изоляции.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Архитектура | 6P (Golden Cove) + 4E (Gracemont) |
| Ядер / Потоков | 10C/16T |
| P-core Boost | 4.6 GHz (1-2 ядра), 4.1 GHz (all-core) |
| E-core Boost | 3.3 GHz |
| L2-кэш | 9.5 MB (7.5 P + 2 E) |
| L3-кэш | 20 MB |
| TDP (PL1/PL2) | 65W / 148W |
| iGPU | Отсутствует |
| DDR4/DDR5 | 3200 / 4800 |

## Ключевое отличие от 12400F

| | i5-12400F | i5-13400F |
|---|---|---|
| Ядра | 6P/12T | 6P+4E/16T |
| L3 | 18 MB | 20 MB |
| PL2 | 117W | 148W |
| Цена | ~10 000 ₽ | ~13 500 ₽ |

E-ядра не дают FPS в играх. Они дают плавность интерфейса при Docker + IDE + браузер в фоне.

observations:
  # === 1440p GPU-bound baseline ===
  - id: "obs-13400f-001"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-13400f"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 85
    p1_fps: 60
    gpu_utilization: 97
    cpu_utilization: 42
    notes: "GPU-bound. P-cores на 4.1 GHz all-core. 13400F не bottleneck."

  # === 13400F vs 14600K delta ===
  - id: "obs-13400f-002"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-13400f"
    comparison_cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 85
    competitor_avg_fps: 87
    fps_delta: "+2 FPS (2.4%)"
    gpu_utilization: 97
    notes: "14600K (22K) vs 13400F (13.5K): +8.5K за +2 FPS. GPU-bound нивелирует разницу в архитектуре."

  # === 13400F vs 7800X3D delta ===
  - id: "obs-13400f-003"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-13400f"
    comparison_cpu: "amd-ryzen-7-7800x3d"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 85
    competitor_avg_fps: 89
    fps_delta: "+4 FPS (4.7%)"
    gpu_utilization: 97
    notes: "7800X3D (26-29K) vs 13400F (13.5K): +4 FPS за двойную цену. В 1440p GPU-bound разница минимальна."

  # === E-core isolation: Docker + IDE + gaming ===
  - id: "obs-13400f-004"
    source_id: "agg"
    source_confidence: 0.80
    observation_quality: 0.75
    cpu: "intel-core-i5-13400f"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 85
    p1_fps: 60
    background_load: "Docker (2 контейнера), IDE (индексация), Chrome (30 вкладок), Discord"
    avg_fps_with_bg: 83
    p1_fps_with_bg: 56
    fps_loss: "-2 FPS (2.4%)"
    e_core_utilization: 78
    p_core_utilization: 68
    notes: "E-cores забирают фон. P-cores свободны для игры. Без E-cores (12400F): микрофризы, вытеснение из L3."

  # === DDR4 vs DDR5 ===
  - id: "obs-13400f-005"
    source_id: "agg"
    source_confidence: 0.85
    observation_quality: 0.82
    cpu: "intel-core-i5-13400f"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    ddr4_3200_avg_fps: 85
    ddr5_5600_avg_fps: 87
    fps_delta: "+2 FPS (2.4%)"
    notes: "DDR4-3200 vs DDR5-5600: +2 FPS за +4.4K. MV не окупается в GPU-bound сценарии."

  # === Power draw in gaming ===
  - id: "obs-13400f-006"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-13400f"
    game: "Cyberpunk 2077: Phantom Liberty"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
    cpu_power_gaming_w: 62
    cpu_power_allcore_w: 148
    notes: "В играх — 62W (только P-cores). AK400 на 800 RPM — бесшумен. PL2=148W только при sustained all-core (билд, рендер)."
