---
id: "intel-core-i5-12400f"
type: "cpu"
title: "Intel Core i5-12400F (Alder Lake)"
vendor: "Intel"
status: "draft"
tags: ["intel", "alder-lake", "lga1700", "6c12t", "no-igpu", "budget", "65w", "pcie5", "ddr4"]
last_updated: "2026-07-06"
links:
  smaller_brother: "catalog/cpu/intel-core-i3-12100f.md"
  bigger_brother: "catalog/cpu/intel-core-i5-14600k.md"
  platform: "catalog/motherboard/lga1700/index.md"
  memory_type: "catalog/memory/ddr4-3200-cl16-32gb.md"
specs:
  socket: "LGA1700"
  architecture: "Alder Lake (Intel 7)"
  architecture_generation: 12
  codename: "Alder Lake-S"
  sku: "i5-12400F"
  sku_family: "i5"
  release_date: "Q1 2022"
  status: "released"

  total_cores: 6
  total_threads: 12
  p_cores: 6
  e_cores: 0
  p_core_arch: "Golden Cove"
  smt_ht: true
  thread_director: false

  l2_per_pcore: "1.25 MB"
  l2_total: "7.5 MB"
  l3_cache: "18 MB (shared Intel Smart Cache)"

  base_clock_p: "2.5 GHz"
  boost_clock_p_max: "4.4 GHz"
  boost_clock_p_all: "4.0 GHz"

  tdp_pl1: "65W"
  tdp_pl2: "117W"
  tjmax: "100°C"
  typical_gaming_power: "50-65W"

  lithography: "Intel 7 (10nm Enhanced SuperFin)"
  die_topology: "monolithic"

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
  cooler_recommended: "Боксовый RM1 достаточен. Для тишины — DeepCool AK400"
  multiplier_locked: true

  msrp_usd_launch: 167
  price_ru_min: 9000
  price_ru_median: 10000
  price_ru_max: 11000
  price_ru_date: "2026-07-06"
  price_ru_source: "price.ru / DNS / Ozon"
  segment: "budget"
profiles:
  entry_level_cpu:
    power_envelope: "low"
    capability_level: 1
    steel_man_desc: "6 ядер Golden Cove — минимальный full-fledged gaming CPU. 65W TDP, PCIe 5.0 x16. Золотая середина: достаточно ядер чтобы не думать о фоне, но без E-core лишнего тепла."
    failure_mode_desc: "CPU-bound сценарии: 1080p high-FPS без DLSS. 4.0 GHz all-core против 5.1 GHz у 14600K — разница видна когда GPU не лимитер."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra_gpu_bound"]
    failure_for_intents: ["esports_1080p_240hz", "streaming_software_encode"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 9000
  median: 10000
  max: 11000
  source: "price.ru / DNS / Ozon"
  date: "2026-07-06"
  status: "verified"
platform_req:
  motherboard_min: "H610"
  motherboard_opt: "B660 / B760"
  cooler_min: "Боксовый Intel Laminar RM1"
  cooler_opt: "DeepCool AK400"
  memory_sweet_spot: "DDR4-3200 CL16"
  psu_min_system: "550W"
engineering_notes:
  - "6 P-cores Golden Cove без E-cores — нет проблем Thread Director. Все ядра равны."
  - "65W PL1 / 117W PL2 — на 52W горячее i3-12100F, но всё ещё холоднее любого K-процессора."
  - "All-core boost 4.0 GHz — ключевой параметр для игр. На 300 MHz ниже i5-14600K all-core."
  - "PCIe 5.0 x16 от CPU — идентично i9. Никакого компромисса по GPU bandwidth."
  - "DDR4-3200 sweet spot. DDR5 на Alder Lake даёт +0-3% FPS, не оправдывает разницу в цене."
verdict: "Лучший бюджетный 6-ядерник для GPU-bound гейминга. +50% ядер над i3-12100F при +40% цены. Для 1440p с RTX 5070 — GPU всё ещё лимитер, но запас по CPU-сценам значительно выше."
---

# Intel Core i5-12400F (Alder Lake, LGA1700)

## Позиционирование

Intel Core i5-12400F — 6-ядерный (6C/12T) процессор поколения Alder Lake, младшая модель i5 без E-ядер и без встроенной графики. Занимает нишу «достаточный CPU для любого GPU-bound гейминга»: 6 ядер Golden Cove, 65W TDP, PCIe 5.0 x16.

**Ключевое отличие от i3-12100F:** +2 ядра (+50%), +6MB L3 (+50%), +7W TDP (+12%). В GPU-bound 1440p разница минимальна (<5%), но запас по CPU-тяжёлым сценам (фон, стрим, симуляции) значительно выше.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Архитектура | Alder Lake (Golden Cove) |
| Техпроцесс | Intel 7 |
| Ядер / Потоков | 6C/12T (без E-cores) |
| Базовая частота | 2.5 GHz |
| Boost (1-2 ядра) | 4.4 GHz |
| All-core Boost | 4.0 GHz |
| L2-кэш | 7.5 MB |
| L3-кэш | 18 MB |
| TDP (PL1) | 65W |
| MTP (PL2) | 117W |
| iGPU | Отсутствует |

### Память и PCIe

| Параметр | Значение |
|---|---|
| Тип памяти | DDR4-3200 / DDR5-4800 |
| Режим | Dual-channel |
| Линии PCIe | 20 (16× PCIe 5.0 + 4× PCIe 4.0) |

## Сравнение

### i5-12400F vs i3-12100F

| Параметр | i5-12400F | i3-12100F | Разница |
|---|---|---|---|
| Ядер | 6C/12T | 4C/8T | +50% |
| L3 | 18 MB | 12 MB | +50% |
| All-core Boost | 4.0 GHz | 4.1 GHz | -100 MHz |
| TDP | 65W | 58W | +12% |
| Цена | ~10 000 ₽ | ~6 500 ₽ | +54% |

На 1440p с RTX 5070 — GPU-bound, разница 0-3% FPS. Но 6 ядер дают запас для фона и будущих игр.

## Для кого

**✅ Оптимально:** AAA 1440p с GPU среднего/высокого сегмента, бюджетные сборки с запасом ядер.

**❌ Не подходит:** киберспорт 240Hz+, тяжёлый стриминг, рабочие станции.
