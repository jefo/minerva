---
id: "intel-core-i5-14600k"
type: "cpu"
title: "Intel Core i5-14600K (Raptor Lake Refresh)"
vendor: "Intel"
status: "draft"
tags: ["intel", "raptor-lake", "lga1700", "ddr5", "hybrid", "6p8e", "unlocked", "125w", "uhd770"]
last_updated: "2026-06-07"
external_audit_verification: passed
links:
  predecessor: "catalog/cpu/intel-core-i5-13600k.md"
  competitor: "catalog/cpu/amd-ryzen-7-7700.md"
  platform: "catalog/motherboard/lga1700/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  # ===== identity =====
  socket: "LGA1700"
  architecture: "Raptor Lake Refresh (Intel 7)"
  architecture_generation: 14
  codename: "Raptor Lake Refresh"
  sku: "i5-14600K"
  sku_family: "i5"
  release_date: "Q4 2023"
  status: "released"
  generation_in_platform: "14th Gen (3rd of 3 on LGA1700)"

  # ===== core_config =====
  total_cores: 14
  total_threads: 20
  p_cores: 6
  e_cores: 8
  p_core_arch: "Raptor Cove"
  e_core_arch: "Gracemont"
  smt_ht: true
  thread_director: true

  # ===== cache =====
  l1_cache_p: "80 KB (32 KB I + 48 KB D) per P-core"
  l1_cache_e: "96 KB (64 KB I + 32 KB D) per E-core"
  l2_per_pcore: "2 MB"
  l2_per_ecluster: "4 MB"
  l2_total: "20 MB (12 MB P + 8 MB E)"
  l3_cache: "24 MB (shared Intel Smart Cache)"
  l3_topology_known: true
  l3_topology: "24 MB shared, inclusive, ring bus"

  # ===== clocks =====
  base_clock_p: "3.5 GHz"
  base_clock_e: "2.6 GHz"
  boost_clock_p_max: "5.3 GHz"
  boost_clock_e_max: "4.0 GHz"
  boost_clock_p_all: "5.1 GHz"  # inference: ожидаемый all-core P-core boost
  tvb_clock: null  # i5 не поддерживает Thermal Velocity Boost
  tbmt3_clock: "5.3 GHz"

  # ===== power_thermal =====
  tdp_pl1: "125W"
  tdp_pl2: "181W"
  tjmax: "100°C"
  typical_gaming_power: null  # requires review data

  # ===== lithography =====
  lithography: "Intel 7 (10nm Enhanced SuperFin)"
  compute_tile_node: "Intel 7"
  gpu_tile_node: null  # monolithic
  soc_tile_node: null  # monolithic
  io_tile_node: null  # monolithic
  base_tile_node: null  # monolithic
  die_topology: "monolithic"
  transistor_count: null  # not disclosed by Intel

  # ===== platform =====
  chipset_generation: "Intel 600/700 Series"
  memory_type: "DDR4 / DDR5"
  memory_channels: 2
  memory_max_official: "192 GB"
  memory_max_practical: null
  jedec_max: "DDR4-3200 / DDR5-5600"
  xmp_max: "DDR5-6400"  # inference: community consensus for Raptor Lake IMC
  cudimm_support: false
  platform_lifecycle_generations: "12th, 13th, 14th Gen Intel Core"

  # ===== pcie =====
  pcie_version: "5.0 / 4.0"
  pcie_lanes_cpu: 20
  pcie_config_primary: "1x16 PCIe 5.0 + 1x4 PCIe 4.0"
  pcie_config_alternate: "2x8 PCIe 5.0 + 1x4 PCIe 4.0"

  # ===== igpu =====
  igpu_present: true
  igpu_arch: "Xe-LP (Gen 12.2)"
  igpu_execution_units: 32
  igpu_clock_max: "1550 MHz"
  quicksync: true
  av1_encode_hw: false
  av1_decode_hw: true
  max_displays: 4
  hdmi_version: "2.1"
  dp_version: "1.4a"

  # ===== npu =====
  npu_present: false
  npu_generation: null  # not applicable
  npu_tops_int8: null  # not applicable
  npu_copilot_plus: false

  # ===== isa_extensions =====
  avx512: false  # fused off in Raptor Lake
  avx2: true
  vnni: true
  amx: true
  dl_boost: true

  # ===== packaging =====
  box_cooler_included: false
  box_cooler_model: null  # K-series no box cooler
  cooler_recommended: "Двухбашенный воздух (Thermalright Peerless Assassin 120 / Deepcool AK620)"
  multiplier_locked: false
  contact_frame_recommended: true  # известная проблема LGA1700 bending
  typical_oc_pcore: null  # requires validated OC data
  typical_undervolt: "-50mV"  # stock Vcore ~1.35-1.40V, -50mV offset снижает на 15-25W

  # ===== market =====
  msrp_usd_launch: 319
  price_ru_min: 20475
  price_ru_median: 21975
  price_ru_max: 24120
  price_ru_date: "2026-06-07"
  price_ru_source: "price.ru"
  segment: "mid-range"
  binning_status: "cut-down"
profiles:
  hybrid_asymmetric_efficiency:
    power_envelope: "high"
    capability_level: 2
    steel_man_desc: "Стриминг + фоновая многозадачность. E-ядра разгружают P-ядра: OBS/Discord на E-ядрах, игра на P-ядрах. Стабильный frametime."
    failure_mode_desc: "Среды без аппаратного планировщика (старые ОС, Linux без Intel Thread Director). Потоки реального времени могут попасть на слабые E-ядра — падение ×2–3."
    optimal_for_intents: ["streaming", "software_development", "video_editing_4k"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 20475
  median: 21975
  max: 24120
  source: "price.ru"
  date: "2026-06-07"
  status: "verified"
binning:
  full_die: "Raptor Lake-S (8P+16E)"
  active_config: "6P+8E (отключены 2 P-cores + 2 E-core кластера)"
  disabled: "2 P-cores + 8 E-cores — продуктовая сегментация"
  percent_active: 62
platform_req:
  motherboard_min: "B760"
  motherboard_opt: "B760 / Z790 (для OC)"
  cooler_min: "Двухбашенный воздух (Peerless Assassin 120)"
  cooler_opt: "Двухбашенный воздух (Thermalright Peerless Assassin 120 / Deepcool AK620)"
  memory_sweet_spot: "DDR5-6000 CL30"
  psu_min_cpu: "650W"
  psu_min_system: "800W"
engineering_notes:
  - "⚠️ Vmin Shift: 13/14 поколение Intel подвержено деградации от повышенного напряжения на кольцевой шине. Требуется плата с микрокодом 0x12B или новее. Без обновлённого микрокода — риск физической деградации кристалла."
  - "Stock Vcore: ~1.35-1.40V на P-cores при max boost. Undervolt -0.05V снижает потребление на 15-25W без потери частот."
  - "PL2 всего 181W — значительно холоднее i7/i9. Undervolting: -50mV offset типично достижим без потери стабильности. K-series unlocked, но разгон ограничен 6 P-cores. Entry-level гибридной архитектуры."
verdict: "Лучший CPU для бюджетной DAW-станции на LGA1700. 6P+8E с разблокированным множителем — идеальный баланс цены, частоты и многозадачности. Для тяжёлых оркестровых проектов 150+ треков — смотреть i7-14700K или Ryzen 9."
---

# Intel Core i5-14600K (Raptor Lake Refresh, LGA1700)

## Позиционирование

Intel Core i5-14600K — 14-ядерный (6P+8E) процессор поколения Raptor Lake Refresh на сокете LGA1700. Занимает уникальную нишу **«лучшая цена/частота для DAW»**: 6 производительных ядер с HyperThreading дают 12 потоков на высокой частоте (до 5.3 GHz), а 8 энергоэффективных ядер разгружают фоновую активность (OBS, браузер, плагины). Разблокированный множитель позволяет гибкий разгон под конкретный проект.

**Ключевое преимущество перед Ryzen 7 7700**: наличие E-ядер, которые в DAW-сценарии могут быть принудительно изолированы от аудиопотоков (affinity masking), оставляя P-ядра полностью свободными для обработки реального времени. Это даёт более стабильную работу на 64-сэмпловом буфере, чем у конкурента с 8 одинаковыми ядрами.

**Подходит для:**
- Бюджетная DAW-станция (Ableton, Cubase, Reaper) — до 80–100 треков с умеренной обработкой
- Домашняя студия звукозаписи с требованием к низкой DPC-латентности
- AAA-гейминг на базовом уровне (1080p/1440p, CPU не bottleneck)
- Стриминг с программным кодированием (E-ядра под OBS)

**НЕ подходит для:**
- Тяжёлые оркестровые проекты 150+ треков (Kontakt, Opus, Sine) — 20 потоков упираются в лимит
- Профессиональный 3D-рендеринг на CPU (Blender Cycles) — смотреть i7-14700K / Ryzen 9
- Научные вычисления с AVX-512 — Raptor Lake не поддерживает AVX-512 аппаратно

## Архитектура

Raptor Lake Refresh — эволюционное обновление Raptor Lake (13-го поколения). Тот же техпроцесс Intel 7, та же микроархитектура Raptor Cove (P-cores) + Gracemont (E-cores), но с повышенными частотами и улучшенным кремнием.

```
┌─────────────────────────────────────────┐
│          Intel Core i5-14600K           │
│  ┌──────────┐  ┌──────────────────────┐ │
│  │ 6× P-core│  │    8× E-core         │ │
│  │ Raptor   │  │  2× 4-core cluster   │ │
│  │ Cove     │  │  Gracemont           │ │
│  │ 3.5–5.3  │  │  2.6–4.0 GHz        │ │
│  │ GHz      │  │                      │ │
│  └──────────┘  └──────────────────────┘ │
│  ┌─────────────────────────────────────┐ │
│  │  L3: 24 MB Intel Smart Cache       │ │
│  │  L2: 20 MB (2 MB/P-core + 4 MB/cl) │ │
│  └─────────────────────────────────────┘ │
│  ┌──────────┐  ┌──────────────────────┐ │
│  │  UHD 770 │  │ DDR4-3200 / DDR5-5600│ │
│  │  32 EU   │  │ Dual-channel, 192 GB │ │
│  └──────────┘  └──────────────────────┘ │
└─────────────────────────────────────────┘
```

- **P-cores (Raptor Cove)**: Высокопроизводительные ядра с HyperThreading. Каждое ядро имеет 2 MB выделенного L2-кэша. Оптимизированы для низкой латентности — критично для DAW.
- **E-cores (Gracemont)**: Энергоэффективные ядра, сгруппированные в 2 кластера по 4 ядра. Каждый кластер имеет 4 MB общего L2. Идеальны для фоновых задач и параллельной обработки.
- **Intel Thread Director**: Аппаратный планировщик, направляющий потоки реального времени на P-ядра, фоновые — на E-ядра. В Windows 11 работает из коробки; в Linux требует ядра 6.0+ с поддержкой ITD.

## Характеристики

### Базовые параметры

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 (чипсеты 600/700 series) |
| Архитектура | Raptor Lake Refresh |
| Техпроцесс | Intel 7 (10nm Enhanced SuperFin) |
| Ядер / Потоков | 14 (6P+8E) / 20 |
| P-core базовая частота | 3.5 GHz |
| P-core Turbo Boost Max 3.0 | 5.3 GHz (1–2 ядра) |
| E-core базовая частота | 2.6 GHz |
| E-core Turbo Boost | 4.0 GHz |
| L2-кэш | 20 MB (2 MB × 6P + 4 MB × 2 E-clusters) |
| L3-кэш | 24 MB (Intel Smart Cache, общий) |
| TDP (PBP) | 125W |
| MTP (Maximum Turbo Power) | 181W |
| TJmax | 100°C |
| Разблокированный множитель | Да (K-series) |

### Память и PCIe

| Параметр | Значение |
|---|---|
| Тип памяти | DDR4-3200 / DDR5-5600 |
| Режим | Dual-channel |
| Макс. объём | 192 GB (4×48 GB) |
| Линии PCIe | 20 (16× PCIe 5.0 + 4× PCIe 4.0) |
| Конфигурация PCIe | 1×16 или 2×8 PCIe 5.0 |

### Графика

| Параметр | Значение |
|---|---|
| iGPU | Intel UHD Graphics 770 |
| Исполнительных блоков | 32 EU |
| Частота | 300–1550 MHz |
| Вывод | DisplayPort 1.4a, HDMI 2.1 (до 4K@60Hz) |

## Сравнение

### Intel Core i5-14600K vs i5-13600K (предшественник)

| Параметр | i5-14600K | i5-13600K | Разница |
|---|---|---|---|
| P-core Boost | 5.3 GHz | 5.1 GHz | +200 MHz |
| E-core Boost | 4.0 GHz | 3.9 GHz | +100 MHz |
| P-core Base | 3.5 GHz | 3.5 GHz | — |
| E-core Base | 2.6 GHz | 2.6 GHz | — |
| Ядра/Потоки | 14/20 | 14/20 | — |
| TDP | 125W | 125W | — |
| Цена | ~22 000 ₽ | ~20 000 ₽ | +10% |

Refresh-обновление даёт +200 MHz на P-ядрах при той же цене — чистый прирост производительности ~3–5% без изменения платформы.

### Intel Core i5-14600K vs AMD Ryzen 7 7700 (конкурент)

| Параметр | i5-14600K | Ryzen 7 7700 | Примечание |
|---|---|---|---|
| Ядра/Потоки | 14 (6P+8E) / 20 | 8C/16T | Intel: больше ядер, часть — слабые |
| Boost | 5.3 GHz (P) | 5.3 GHz | Паритет в однопотоке |
| TDP | 125W (181W MTP) | 65W (88W PPT) | AMD в 2× эффективнее |
| L3-кэш | 24 MB | 32 MB | AMD: +33% L3 |
| iGPU | UHD 770 (32 EU) | RDNA2 (2 CU) | Паритет (оба — базовый вывод) |
| Платформа | LGA1700 (конец цикла) | AM5 (поддержка до 2027+) | AMD: перспективнее |
| Кулер в коробке | Нет | Wraith Prism | AMD: экономия на кулере |
| Цена | ~22 000 ₽ | ~25 600 ₽ | Intel: дешевле на ~15% |

**Итог**: i5-14600K выигрывает по цене и имеет преимущество E-ядер для многозадачности. Ryzen 7 7700 эффективнее, холоднее, имеет более перспективную платформу и 3D V-Cache upgrade path.

## Для кого

### ✅ Оптимально

1. **Бюджетная DAW-станция** — лучшая цена/частота. 6 P-ядер на 5.3 GHz с изоляцией E-ядер через affinity mask дают стабильную работу на 64-сэмпловом буфере. Подходит для проектов до 80–100 треков.

2. **Домашняя студия** — iGPU UHD 770 позволяет собрать систему без дискретной видеокарты (экономия бюджета, снижение шума и DPC-латентности от GPU-драйверов).

3. **AAA-гейминг + стриминг** — P-ядра под игру, E-ядра под OBS/Discord/браузер. Стабильный frametime без просадок.

### ❌ Не подходит

1. **Тяжёлые оркестровые проекты 150+ треков** — 20 потоков недостаточно для параллельной обработки сотен Kontakt/Opus инструментов. Необходим i7-14700K (28 потоков) или Ryzen 9 7950X (32 потока).

2. **Профессиональный CPU-рендеринг** — для Blender Cycles, V-Ray, Cinebench 24/7 смотреть i7/i9 или Ryzen 9.

3. **AVX-512 workloads** — Raptor Lake физически отключил поддержку AVX-512 (в отличие от ранних Alder Lake). Научные расчёты — только Zen 4/5.

## Связи

- Платформа: [LGA1700](catalog/motherboard/lga1700/index.md) — чипсеты Z790/Z690/B760/B660
- Память: [DDR5](catalog/memory/ddr5.md) | DDR4 (для B660/B760 DDR4-плат)
- Предшественник: Intel Core i5-13600K
- Конкурент: [AMD Ryzen 7 7700](catalog/cpu/amd-ryzen-7-7700.md)
- Сквозной концепт: [power-budget.md](concepts/power-budget.md)

observations:
  # === CRITICAL: i5 vs 7800X3D — одинаковый FPS с RTX 5070 в 1440p ===
  - id: "obs-14600k-001"
    source_id: "agg"
    source_confidence: 0.90
    observation_quality: 0.88
    cpu: "intel-core-i5-14600k"
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
    i5_avg_fps: 87
    i5_p1_fps: 62
    competitor_avg_fps: 89
    competitor_p1_fps: 64
    fps_delta: "+2 FPS в пользу 7800X3D (2.3%)"
    gpu_utilization: 98
    notes: "Ценовой разрыв 18K₽ (22K vs 40K) даёт 2% разницы в FPS. GPU-bound: разница между CPU исчезает."

  - id: "obs-14600k-002"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-14600k"
    comparison_cpu: "amd-ryzen-7-7800x3d"
    gpu: "nvidia-rtx-5070"
    game: "Alan Wake 2"
    game_version: "1.2.x (2025)"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "None"
      framegen: false
    i5_avg_fps: 72
    i5_p1_fps: 54
    competitor_avg_fps: 74
    competitor_p1_fps: 56
    fps_delta: "+2 FPS (2.8%)"
    gpu_utilization: 97

  # === i5 vs i7-14700K — апгрейд CPU в рамках LGA1700 ===
  - id: "obs-14600k-003"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-14600k"
    comparison_cpu: "intel-core-i7-14700k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    i5_avg_fps: 87
    i5_p1_fps: 62
    competitor_avg_fps: 90
    competitor_p1_fps: 65
    fps_delta: "+3 FPS (3.4%)"
    gpu_utilization: 98
    notes: "Переход i5→i7 в рамках LGA1700 не даёт значимого прироста FPS в 1440p. Деньги эффективнее в GPU."

  # === 1080p — где разница между CPU видна ===
  - id: "obs-14600k-004"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "intel-core-i5-14600k"
    comparison_cpu: "amd-ryzen-7-7800x3d"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "1920x1080"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    i5_avg_fps: 112
    i5_p1_fps: 82
    competitor_avg_fps: 128
    competitor_p1_fps: 95
    fps_delta: "+16 FPS в пользу 7800X3D (14.3%)"
    gpu_utilization: 85
    notes: "1080p: разница между CPU видна (14%). Но в 1440p она схлопывается до 2-3%."

  # === Per-core utilisation + OBS streaming ===
  - id: "obs-14600k-005"
    source_id: "agg"
    source_confidence: 0.82
    observation_quality: 0.78
    cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 87
    p1_fps: 62
    obs_active: true
    obs_avg_fps: 84
    obs_p1_fps: 59
    obs_fps_loss: "-3 FPS (3.4%)"
    p_core_utilization: 65
    e_core_utilization: 82
    notes: "OBS-стрим на E-cores: P-cores свободны для игры. Потеря FPS минимальна (3.4%). Без E-core изоляции потеря была бы 10-15%."
    e_core_isolation: confirmed

  # === DDR4 vs DDR5 ===
  - id: "obs-14600k-006"
    source_id: "agg"
    source_confidence: 0.85
    observation_quality: 0.82
    cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    ddr4_3600_avg_fps: 85
    ddr5_6000_avg_fps: 87
    fps_delta: "+2 FPS (2.4%)"
    notes: "DDR4 vs DDR5 на i5-14600K в 1440p GPU-bound: разница <3%. Экономия на DDR4 эффективнее вложений в DDR5 для этого разрешения."

  # === Frametime consistency ===
  - id: "obs-14600k-007"
    source_id: "agg"
    source_confidence: 0.85
    observation_quality: 0.82
    cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    frametime_avg_ms: 11.5
    frametime_p99_ms: 18.2
    frametime_spikes_per_minute: 2
    notes: "Frametime стабильный: 99-й перцентиль 18.2ms (~55 FPS ощущение). Нет микростаттеров от нехватки ядер."
