---
id: "amd-ryzen-5-7600"
type: "cpu"
title: "AMD Ryzen 5 7600 (65W, BOX)"
vendor: "amd"
status: "draft"
tags: ["amd", "zen4", "am5", "ddr5", "65w", "box-cooler", "igpu", "6-core"]
last_updated: "2026-06-03"
external_audit_verification: planned
price_ru:
  min: 14500
  median: 16500
  max: 19000
  source: "price.ru"
  date: "2026-06-04"
links:
  platform: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/amd-ryzen-7000.md"
  up_variant: "catalog/cpu/amd-ryzen-5-7600x.md"
  down_variant: "catalog/cpu/amd-ryzen-5-7500f.md"
  multi_core_alt: "catalog/cpu/amd-ryzen-7-7700.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "AM5 (LGA1718)"
  architecture: "Zen 4 (Raphael)"
  lithography: "TSMC 5nm (CCD) + 6nm (IOD)"
  cores: 6
  threads: 12
  base_clock: "3.8 GHz"
  boost_clock: "5.1 GHz"
  l2_cache: "6 MB (1 MB × 6)"
  l3_cache: "32 MB"
  tdp: "65W"
  ppt: "88W (default)"
  tjmax: "95°C"
  pcie_lanes: "28 (24 usable), PCIe 5.0"
  memory: "DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO"
  max_memory: "128 GB (4×32 GB или 2×48 GB)"
  igpu: "RDNA 2 (2 CUs, 2200 MHz, базовый вывод)"
  box_cooler: "Wraith Stealth (в коробке)"
  package: "Retail (BOX)"
  release_date: "Q1 2023"
profiles:
  balanced_monolithic_norm:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Универсальный процессор: 6–8 ядер, единый кристалл (1 CCD), TDP 65–105W. Игры, разработка, офис — всё на хорошем уровне без специализации."
    failure_mode_desc: "Отсутствие 3D V-Cache — проигрыш X3D в киберспорте на 15–25%. Отсутствие E-ядер — фоновая многозадачность менее эффективна."
    optimal_for_intents: ["software_development", "office_productivity", "aaa_1080p_ultra", "aaa_1440p_high", "streaming"]
    failure_for_intents: ["esports_1080p_360hz"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  dense_thermal_concentration:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту до того как тепло преодолеет IHS. Максимальный буст на 2–3 секунды."
    failure_mode_desc: "Длительная нагрузка. Тепловое сопротивление толстой IHS (≥ 1.7 мм, AM5) → 89–95°C даже под СЖО. Thermal throttling 5–8%."
    optimal_for_intents: ["office_productivity", "software_development"]
    failure_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation", "silent_build"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  sub_5nm_lithography:
    power_envelope: "mid"
    steel_man_desc: "Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления."
    failure_mode_desc: "Разгон с V > 1.35В → ускоренная электромиграция и выход из строя."
    optimal_for_intents: ["sff_build", "silent_build"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
verdict: "Золотая середина AM5: 6 ядер Zen 4, 65W, iGPU, боксовый кулер. Универсальный процессор для игровых сборок среднего уровня. На 3–4 тыс. ₽ дороже 7500F, но получаете iGPU и гарантию BOX."
---

# AMD Ryzen 5 7600 (65W, BOX)

## Позиционирование

Ryzen 5 7600 — 6-ядерный 12-поточный процессор Zen 4 с TDP 65W, встроенной графикой RDNA 2 и боксовым кулером Wraith Stealth в комплекте. Это самый доступный BOX-процессор AM5 с iGPU — минимальный порог входа в платформу для тех, кому нужна страховка на случай проблем с видеокартой.

От 7500F отличается наличием iGPU, +100 MHz boost и BOX-комплектацией. От 7600X — TDP 65W против 105W, комплектным кулером и ценой на 3–4 тыс. ₽ ниже. По сути — это 7600X в режиме Eco Mode с кулером в коробке.

## Характеристики

- Архитектура: Zen 4 (Raphael)
- Техпроцесс: TSMC 5nm (CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 6C/12T
- Базовая частота: 3.8 GHz
- Boost: 5.1 GHz (на 1–2 ядрах)
- All-core нагрузка: ~4.8–4.9 GHz
- L2-кэш: 6 MB (1 MB × 6)
- L3-кэш: 32 MB (единый)
- TDP / PPT: 65W / 88W
- TJmax: 95°C
- iGPU: RDNA 2, 2 CU, 2200 MHz — базовый вывод изображения, не для игр
- Кулер в коробке: Wraith Stealth (алюминий, низкопрофильный)
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU) + 4 линии PCIe 4.0 на NVMe

## Производительность

### Cinebench R23
- Single-core: ~1 870 баллов
- Multi-core (stock 65W): ~14 500 баллов
- Multi-core (PBO, PPT ~120W): ~15 500 баллов

### Cinebench 2024
- Single-core: ~112 баллов
- Multi-core: ~830 баллов

### Игры (1440p)
В реальных игровых сценариях 7600 практически идентичен 7600X — разница в пределах 1–3%. Для любого гейминга вплоть до RTX 5070 / RX 9070 на 1440p процессор не является узким местом.

- Cyberpunk 2077: ~130 fps
- Baldur's Gate 3: ~155 fps
- CS2: ~460 fps

## Память

Как все Zen 4 — **DDR5 only**. Оптимальная частота: DDR5-6000 CL30 с MCLK:UCLK = 1:1. 7600 без проблем держит DDR5-6000 на большинстве плат B650. Для бюджетных сборок DDR5-5600 CL36 — достаточный минимум (разница с 6000 CL30 — 2–4% в играх).

## Охлаждение

65W TDP — холодный процессор. Wraith Stealth из коробки справляется, но на грани: под Cinebench — 80–85°C, вентилятор слышен. Рекомендуется замена на башенный кулер за 1 500–2 500 ₽:

- ID-COOLING SE-224-XTS
- Deepcool AK400
- Thermalright Assassin X 120

С башенным кулером температуры падают до 60–68°C под полной нагрузкой, вентилятор практически не слышен.

## Сравнение с 7500F и 7600X

- **7500F:** 7600 = 7500F + iGPU + 100 MHz boost + BOX-комплектация. Переплата ~3 000–4 000 ₽. Оправдана, если нужен iGPU или BOX-гарантия.
- **7600X:** 7600X выигрывает ~3–5% в многопотоке за счёт 105W TDP, но не имеет кулера в коробке. Переплата ~3 000–4 000 ₽ + стоимость кулера. 7600 — прагматичный выбор, 7600X — для тех, кто в любом случае ставит мощное охлаждение.

## Для кого

**Идеален:**
- Игровые сборки среднего уровня с дискретной GPU
- Первый ПК на AM5 с заделом под апгрейд до Zen 5/6
- Системы, где iGPU нужен как страховка (диагностика, работа без GPU)
- Сборщики, не желающие заморачиваться с мощным охлаждением

**Не подходит:**
- Экстремальный бюджет — смотрите 7500F (экономия 3–4 тыс. ₽)
- Максимальный FPS в киберспорте — нужен 7800X3D
- Многопоточные рабочие нагрузки — нужен Ryzen 7/9
- Сборки без дискретной GPU для игр — iGPU только для вывода, не для 3D

## Связки

**Бюджетная:**
- MB: GIGABYTE B650M S2H / ASRock B650M-HDV
- Кулер: Wraith Stealth (из коробки) или ID-COOLING SE-224-XTS
- RAM: 32 GB DDR5-6000 CL30

**Оптимальная:**
- MB: MSI B650 Tomahawk Wi-Fi
- Кулер: Deepcool AK400
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5060 Ti / RX 9070

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная, BOX-версия у всех крупных ритейлеров
- Конкуренты: Intel Core i5-14400F (LGA1700, DDR4/DDR5, тупиковая)

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. TechPowerUp — Ryzen 5 7600 Review (2023)
3. Gamers Nexus — Ryzen 5 7600 CPU Review & Benchmarks (2023)
4. Hardware Unboxed — Ryzen 5 7600 vs 7600X (2023)
