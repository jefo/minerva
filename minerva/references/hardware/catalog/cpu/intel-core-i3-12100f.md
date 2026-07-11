---
id: "intel-core-i3-12100f"
type: "cpu"
title: "Intel Core i3-12100F (Alder Lake)"
vendor: "Intel"
status: "draft"
tags: ["intel", "alder-lake", "lga1700", "ddr4", "ddr5", "4c8t", "no-igpu", "budget", "58w", "pcie5"]
last_updated: "2026-07-06"
links:
  bigger_brother: "catalog/cpu/intel-core-i5-12400f.md"
  platform: "catalog/motherboard/lga1700/index.md"
  memory_type: "catalog/memory/ddr4.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "LGA1700"
  architecture: "Alder Lake (Intel 7)"
  architecture_generation: 12
  codename: "Alder Lake-S"
  sku: "i3-12100F"
  sku_family: "i3"
  release_date: "Q1 2022"
  status: "released"
  generation_in_platform: "12th Gen (1st of 3 on LGA1700)"

  total_cores: 4
  total_threads: 8
  p_cores: 4
  e_cores: 0
  p_core_arch: "Golden Cove"
  e_core_arch: null
  smt_ht: true
  thread_director: false

  l2_per_pcore: "1.25 MB"
  l2_total: "5 MB"
  l3_cache: "12 MB (shared Intel Smart Cache)"
  l3_topology_known: true
  l3_topology: "12 MB shared, inclusive, ring bus"

  base_clock_p: "3.3 GHz"
  boost_clock_p_max: "4.3 GHz"
  boost_clock_p_all: "4.1 GHz"

  tdp_pl1: "58W"
  tdp_pl2: "89W"
  tjmax: "100°C"
  typical_gaming_power: "40-50W"

  lithography: "Intel 7 (10nm Enhanced SuperFin)"
  die_topology: "monolithic"

  chipset_generation: "Intel 600/700 Series"
  memory_type: "DDR4 / DDR5"
  memory_channels: 2
  memory_max_official: "128 GB"
  jedec_max: "DDR4-3200 / DDR5-4800"

  pcie_version: "5.0 / 4.0"
  pcie_lanes_cpu: 20
  pcie_config_primary: "1x16 PCIe 5.0 + 1x4 PCIe 4.0"

  igpu_present: false
  igpu_arch: null
  igpu_execution_units: null
  quicksync: false

  npu_present: false

  avx512: false
  avx2: true

  box_cooler_included: true
  box_cooler_model: "Intel Laminar RM1"
  cooler_recommended: "Боксовый RM1 достаточен для 58W. Для тишины — односекционная башня (DeepCool AK400)"
  multiplier_locked: true
  contact_frame_recommended: false

  msrp_usd_launch: 97
  price_ru_min: 5800
  price_ru_median: 6500
  price_ru_max: 7500
  price_ru_date: "2026-07-06"
  price_ru_source: "price.ru / DNS / Ozon"
  segment: "entry-level"
profiles:
  entry_level_cpu:
    power_envelope: "low"
    capability_level: 0
    steel_man_desc: "4 ядра Golden Cove — минимально достаточный CPU для GPU-bound гейминга. 58W TDP — не требует мощного охлаждения, подходит для SFF. PCIe 5.0 x16 от CPU."
    failure_mode_desc: "CPU-bound сценарии: 1080p high-FPS, esports, симуляции, стратегии. 4 ядра без E-cores — фоновая нагрузка (Discord, браузер) конкурирует с игрой за P-cores."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra_gpu_bound"]
    failure_for_intents: ["esports_1080p_240hz", "streaming", "video_editing_4k"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 5800
  median: 6500
  max: 7500
  source: "price.ru / DNS / Ozon"
  date: "2026-07-06"
  status: "verified"
platform_req:
  motherboard_min: "H610"
  motherboard_opt: "B660 / B760"
  cooler_min: "Боксовый Intel Laminar RM1"
  cooler_opt: "DeepCool AK400 (для тишины)"
  memory_sweet_spot: "DDR4-3200 CL16"
  psu_min_cpu: "350W"
  psu_min_system: "550W"
engineering_notes:
  - "4 P-cores Golden Cove без E-cores — чистый Alder Lake без Thread Director. Нет проблемы E-core affinity."
  - "58W PL1 / 89W PL2 — можно охлаждать пассивно в хорошо вентилируемом корпусе."
  - "PCIe 5.0 x16 от CPU — флагманские GPU работают без ограничений по bandwidth."
  - "Нет iGPU (F-серия) — система не включится без дискретной видеокарты."
  - "LGA1700 — апгрейд-путь до i5-14600K без смены платформы."
verdict: "Самый дешёвый CPU с PCIe 5.0 x16 для GPU-bound гейминга на 1440p. 4C/8T — компромисс по 1% Low в CPU-тяжёлых сценах. Для AAA с DLSS на RTX 5070 — достаточен."
---

# Intel Core i3-12100F (Alder Lake, LGA1700)

## Позиционирование

Intel Core i3-12100F — 4-ядерный (4C/8T) процессор поколения Alder Lake, младшая модель 12-го поколения без E-ядер и без встроенной графики (F-серия). Занимает нишу «минимально достаточный CPU для GPU-bound гейминга»: 4 ядра Golden Cove на частоте до 4.3 GHz, 58W TDP, PCIe 5.0 x16 от CPU.

**Ключевое преимущество:** цена. За ~6 500 ₽ получаем полноценный PCIe 5.0 x16 (не хуже i9-14900K для GPU) и апгрейд-путь в рамках LGA1700 до i5-14600K без смены платформы.

**Подходит для:**
- AAA-гейминг 1440p с GPU среднего/высокого сегмента (RTX 5070, RX 9070) — GPU-bound сценарий
- Бюджетная сборка с упором на GPU
- Офисная/домашняя станция без профессиональных нагрузок

**НЕ подходит для:**
- Киберспорт 240Hz+ (CPU-bound, нужен X3D или high-clocked i5/i7)
- Стриминг без аппаратного кодирования (NVENC на GPU решает)
- CPU-интенсивные рабочие нагрузки (компиляция, рендеринг)

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Архитектура | Alder Lake (Golden Cove) |
| Техпроцесс | Intel 7 |
| Ядер / Потоков | 4C/8T (4 P-cores, без E-cores) |
| Базовая частота | 3.3 GHz |
| Boost (1-2 ядра) | 4.3 GHz |
| All-core Boost | 4.1 GHz |
| L2-кэш | 5 MB (1.25 MB × 4) |
| L3-кэш | 12 MB (Intel Smart Cache) |
| TDP (PL1) | 58W |
| MTP (PL2) | 89W |
| TJmax | 100°C |
| iGPU | Отсутствует (F-серия) |

### Память и PCIe

| Параметр | Значение |
|---|---|
| Тип памяти | DDR4-3200 / DDR5-4800 |
| Режим | Dual-channel |
| Линии PCIe | 20 (16× PCIe 5.0 + 4× PCIe 4.0) |
| Конфигурация | 1×16 PCIe 5.0 |

## Для кого

### ✅ Оптимально
1. **Бюджетный AAA-гейминг 1440p** — GPU-bound сценарий, разница с i5/i7 схлопывается до 0-3%.
2. **Апгрейд с древних платформ** — старт на LGA1700 за 6.5K с возможностью замены на i5-14600K.

### ❌ Не подходит
1. **CPU-интенсивные игры** — Factorio, Stellaris, Cities Skylines 2 — 4 ядрам тяжело.
2. **Продуктивность** — компиляция, рендеринг, обработка данных — слишком мало ядер.

## Связи

- Платформа: LGA1700 — чипсеты H610/B660/B760/Z690/Z790
- Старший брат: Intel Core i5-12400F
- Память: DDR4 / DDR5

## Источники

- Intel ARK: i3-12100F specifications
- TechPowerUp CPU Database
- Price.ru / DNS / Ozon — рыночные цены (июль 2026)
