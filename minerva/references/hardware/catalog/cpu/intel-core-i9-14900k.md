---
id: "intel-core-i9-14900k"
type: "cpu"
title: "Intel Core i9-14900K"
vendor: "Intel"
status: "verified"
tags:
  - raptor-lake-refresh
  - lga1700
  - hybrid-architecture
  - unlocked
  - 253w
  - 24-core
  - 8p16e
specs:
  architecture: "Raptor Lake Refresh"
  socket: "LGA1700"
  lithography: "Intel 7 (10nm Enhanced SuperFin)"
  cores: 24
  threads: 32
  p_cores: 8
  e_cores: 16
  base_clock_p: "3.2 GHz"
  base_clock_e: "2.4 GHz"
  boost_clock_p: "6.0 GHz (Thermal Velocity Boost, 1-2 ядра), 5.8 GHz (Turbo Boost Max 3.0), 5.6 GHz (Max Turbo all P-cores)"
  boost_clock_e: "4.4 GHz"
  l2_cache: "32 MB (2 MB × 8 P-core + 4 MB × 4 clusters E-core)"
  l3_cache: "36 MB (Intel Smart Cache)"
  tdp: "125W"
  tdp_pl2: "253W"
  tjmax: "100°C"
  pcie_lanes: "20 (16× PCIe 5.0 + 4× PCIe 4.0)"
  memory: "DDR5-5600 / DDR4-3200, dual-channel"
  max_memory: "192 GB"
  igpu: "Intel UHD Graphics 770 (32 EU, 300–1650 MHz)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "2023-10 (Q4 2023)"
  multiplier: "unlocked"
  multiplier_source: "https://www.intel.com/content/www/us/en/products/sku/236773/intel-core-i9-processor-14900k-36m-cache-up-to-6-00-ghz/specifications.html"
links:
  predecessor: "intel-core-i9-13900k"
  platform: "catalog/motherboard/lga1700/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_power: "concepts/power-budget.md"
price_ru:
  min: 39999
  median: 42345
  max: 46990
  currency: "RUB"
  source: "price.ru"
binning:
  full_die: "Raptor Lake-S (8P+16E)"
  active_config: "8P+16E (полный кристалл)"
  disabled: "Нет — флагманский SKU"
  percent_active: 100
platform_req:
  motherboard_min: "B760 (VRM от 12 фаз)"
  motherboard_opt: "Z790"
  cooler_min: "360mm AIO"
  cooler_acceptable: "280mm AIO / двухбашенный воздух (требует PL2≤200W или undervolt -0.05V)"
  cooler_opt: "360mm AIO (Arctic Liquid Freezer III / EK-Nucleus)"
  memory_sweet_spot: "DDR5-6000 CL30 (1:1 с ring bus)"
  psu_min_cpu: "850W"
  psu_min_system: "1000W"
engineering_notes:
  - "⚠️ Vmin Shift: 13/14 поколение Intel подвержено деградации от повышенного напряжения на кольцевой шине. Требуется плата с микрокодом 0x12B или новее. Без обновлённого микрокода — риск физической деградации кристалла."
  - "Stock Vcore: ~1.35-1.40V на P-cores при max boost. Undervolt -0.05V снижает потребление на 15-25W без потери частот."
  - "TVB 6.0 GHz только при <70°C. All-core 5.6 GHz достижим с 360mm AIO. K-series разблокированный множитель. SOC voltage issue исправлена в AGESA-подобных обновлениях микрокода. Последнее поколение LGA1700 — нет пути апгрейда. V-F кривая: diminishing returns выше 5.5 GHz."
fetch_at: "2026-06-07"
last_updated: "2026-06-07"
profiles:
  hybrid_asymmetric_efficiency:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "Стриминг + фоновая многозадачность. E-ядра (16×Gracemont) разгружают P-ядра: OBS/Discord/browser на E-ядрах, игра/DAW на P-ядрах. Стабильный frametime."
    failure_mode_desc: "Среды без аппаратного планировщика (старые ОС, Linux без Intel Thread Director). Потоки реального времени могут попасть на E-ядра — падение ×2–3."
    optimal_for_intents:
      - streaming
      - software_development
      - video_editing_4k
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
external_audit_verification: passed
---

# Intel Core i9-14900K

## Позиционирование

Флагманский процессор Intel для настольной платформы LGA1700 на архитектуре Raptor Lake Refresh. Энтузиаст-класс: предназначен для heavy multitasking, профессионального рендеринга, стриминга и максимального FPS в играх без компромиссов. Заменяет i9-13900K с приростом частот на +200 МГц (P-core boost: 5.8 → 6.0 ГГц) и улучшенным Thermal Velocity Boost.

## Архитектура

Гибридная архитектура Raptor Lake Refresh с двумя типами ядер:

- **8 P-ядер (Raptor Cove)** — высокопроизводительные, с Hyper-Threading (16 потоков). Оптимизированы под однопоточные и чувствительные к задержкам задачи: игры, DAW, интерактивные приложения.
- **16 E-ядер (Gracemont)** — энергоэффективные, без HT (16 потоков). Разгружают P-ядра при фоновой многозадачности: OBS, Discord, фоновые сервисы, рендеринг.

Intel Thread Director (аппаратный планировщик) распределяет потоки: Windows 11 ≥ 22H2 использует его нативно. На Linux без Thread Director возможны проблемы — потоки реального времени могут попасть на E-ядра с падением производительности ×2–3.

## Характеристики

| Параметр | Значение |
|---|---|
| Ядра / Потоки | 8P+16E / 32 потока |
| P-core Boost (1–2 ядра) | 6.0 GHz (Thermal Velocity Boost) |
| P-core Boost (all-core) | 5.8 GHz (Turbo Boost Max 3.0), 5.6 GHz (Max Turbo) |
| E-core Boost | 4.4 GHz |
| L2 Cache | 32 MB |
| L3 Cache | 36 MB |
| P-core Base TDP | 125W |
| Max Turbo Power | 253W |
| iGPU | Intel UHD 770 |
| Память | DDR5-5600 / DDR4-3200, 2ch, до 192 GB |
| PCIe | 5.0 ×16 + 4.0 ×4 |
| Техпроцесс | Intel 7 |

## Сравнение

### vs i9-13900K (Raptor Lake)

- Частоты P-core: +200 МГц (5.8 → 6.0 ГГц на 1–2 ядрах)
- E-core boost: +100 МГц (4.3 → 4.4 ГГц)
- Тот же техпроцесс (Intel 7), тот же сокет (LGA1700)
- Прирост многопоточной производительности: ~3–5% (Cinebench R23)
- Прирост игровой: ~2–3% (GPU-bound сценарии — в пределах погрешности)

### vs Ryzen 9 9950X (Zen 5, AM5)

- 14900K: 32 потока (8P+16E) vs 9950X: 32 потока (16C/32T, симметричные)
- Однопоточная: 14900K ≈ паритет (зависит от задачи)
- Многопоточная: 9950X выигрывает на 8–12% (полноценные ядра, нет E-core penalty)
- Энергопотребление: 14900K (253W) vs 9950X (170W) — Zen 5 эффективнее на ~40%
- Платформа: LGA1700 (тупиковая) vs AM5 (апгрейд до Zen 6)

## Для кого подходит

- **Тяжёлый рендеринг** (Blender, V-Ray, Cinema 4D): 32 потока, sustained performance при адекватном охлаждении
- **Стриминг + гейминг**: E-ядра берут на себя OBS/Discord, P-ядра — игру. Стабильный frametime
- **DAW / аудиопродакшн**: высокие однопоточные частоты = минимальная DPC latency. iGPU достаточен для вывода без дискретной карты
- **Компиляция крупных проектов**: 32 потока сокращают время сборки
- **AI-инференс (CPU-bound)**: 24 физических ядра дают хороший параллелизм для инференса небольших моделей на CPU

## Для кого НЕ подходит

- **SFF / компактные сборки**: 253W TDP требует мощного охлаждения (360mm AIO минимум). Тепловыделение создаёт проблемы в ITX-корпусах
- **Тихие сборки**: sustained нагрузка → 90°C+ → вентиляторы на 80%+ PWM. Добиться < 30 dBA под нагрузкой практически невозможно
- **Бюджетные сборки**: высокая цена + обязательная СЖО 360mm + плата с мощным VRM (Z790/Z690) + БП 850W+
- **Домашний сервер 24/7**: idle power высокий, E-ядра не всегда корректно работают в гипервизорах

---

## Профили (ISO 15288 / SysML Satisfy)

```yaml
profiles:
  hybrid_asymmetric_efficiency:
    criteria_met: true
    power_envelope: "high"
    capability_level: 3  # high_core_count_cpu
    steel_man_desc: >
      Стриминг + фоновая многозадачность. E-ядра (16×Gracemont) разгружают
      P-ядра: OBS/Discord/browser на E-ядрах, игра/DAW на P-ядрах.
      Стабильный frametime, нулевой impact стрима на FPS.
    failure_mode_desc: >
      Среды без аппаратного планировщика (старые ОС, Linux без Intel Thread Director).
      Потоки реального времени могут попасть на E-ядра — падение ×2–3.
    optimal_for_intents:
      - streaming
      - software_development
      - video_editing_4k
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"

  cpu_power_envelope_high:
    criteria_met: true
    power_envelope: "high"   # TDP 253W ≥ 120W boundary
    capability_level: 3
    steel_man_desc: >
      Максимальная многопоточная производительность на потребительской платформе.
      32 потока, sustained boost 5.6+ ГГц на P-ядрах при адекватном охлаждении.
      Требует СЖО 360mm или двухбашенный кулер 250W+.
    failure_mode_desc: >
      253W TDP исключает SFF и тихие сборки. Без мощного охлаждения — thermal
      throttling 5–15%. Требует БП 850W+, плату с флагманским VRM.
    optimal_for_intents:
      - heavy_compilation
      - data_engineering
      - 3d_rendering_cpu
      - scientific_computing
      - video_editing_4k
      - llm_inference_7b
      - llm_inference_13b
      - llm_inference_20b
    failure_for_intents:
      - sff_build
      - silent_build
      - home_server_24_7
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
```

### Capability Level: 3 (high_core_count_cpu)

14900K удовлетворяет требованиям **high_core_count_cpu** (12+ ядер, 120W+ TDP).
Имеет excess margin над `balanced_multicore_cpu` (уровень 2) — gold plating для
сценариев, где достаточно 8 ядер.

### Margin Analysis

| Интент | Min Capability | Margin | Оценка |
|---|---|---|---|
| `streaming` | balanced_multicore_cpu (L2) | +1 | Satisficed with excess margin |
| `heavy_compilation` | high_core_count_cpu (L3) | 0 | Optimal |
| `3d_rendering_cpu` | high_core_count_cpu (L3) | 0 | Optimal |
| `sff_build` | (opposing requirement) | — | BLOCK: 253W incompatible |
| `silent_build` | (opposing requirement) | — | BLOCK: sustained ≤30 dBA impossible |
| `data_engineering` | balanced_multicore_cpu (L2) | +1 | Satisficed with excess margin |
| `llm_inference_7b` | balanced_multicore_cpu (L2) | +1 | Satisficed with excess margin |
