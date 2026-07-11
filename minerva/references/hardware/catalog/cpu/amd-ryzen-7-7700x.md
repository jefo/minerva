---
id: "amd-ryzen-7-7700x"
type: "cpu"
title: "AMD Ryzen 7 7700X (105W)"
vendor: "amd"
status: "draft"
tags: ["amd", "zen4", "am5", "ddr5", "105w", "igpu", "8-core", "no-box-cooler"]
last_updated: "2026-06-03"
external_audit_verification: planned
price_ru:
  min: 21500
  median: 24000
  max: 27000
  source: "price.ru"
  date: "2026-06-04"
links:
  platform: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/amd-ryzen-7000.md"
  down_variant: "catalog/cpu/amd-ryzen-7-7700.md"
  up_variant: "catalog/cpu/amd-ryzen-9-7900x.md"
  x3d_alt: "catalog/cpu/amd-ryzen-7-7800x3d.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "AM5 (LGA1718)"
  architecture: "Zen 4 (Raphael)"
  lithography: "TSMC 5nm (CCD) + 6nm (IOD)"
  cores: 8
  threads: 16
  base_clock: "4.5 GHz"
  boost_clock: "5.4 GHz"
  l2_cache: "8 MB (1 MB × 8)"
  l3_cache: "32 MB"
  tdp: "105W"
  ppt: "142W (default)"
  tjmax: "95°C"
  pcie_lanes: "28 (24 usable), PCIe 5.0"
  memory: "DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO"
  max_memory: "128 GB (4×32 GB или 2×48 GB)"
  igpu: "RDNA 2 (2 CUs, 2200 MHz, базовый вывод)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "Q3 2022"
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
verdict: "Заводской максимум 8-ядерного Zen 4. 105W TDP, boost до 5.4 GHz. Отличный CPU для gaming + streaming/продакшн, но 7700 (65W) даёт 94% производительности с кулером в коробке и холоднее."
---

# AMD Ryzen 7 7700X (105W)

## Позиционирование

Ryzen 7 7700X — 8-ядерный 16-поточный процессор Zen 4 с TDP 105W, заводской максимум в линейке Ryzen 7 7000. Высокие базовые частоты (4.5 GHz) и boost до 5.4 GHz делают его привлекательным для геймеров-энтузиастов и создателей контента, которым нужны 8 ядер «из коробки» без разгона.

Плата за частоты: нет кулера в комплекте, 105W TDP требует серьёзного охлаждения, VRM бюджетных плат B650 работает на пределе. По сравнению с 7700 (65W) — выигрыш ~6% в многопотоке и ~1.5% в однопотоке при росте энергопотребления на 52W.

## Характеристики

- Архитектура: Zen 4 (Raphael)
- Техпроцесс: TSMC 5nm (CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 8C/16T
- Базовая частота: 4.5 GHz — на 700 MHz выше, чем у 7700 (3.8 GHz)
- Boost: 5.4 GHz (на 1–2 ядрах)
- All-core нагрузка: ~5.1–5.2 GHz
- L2-кэш: 8 MB (1 MB × 8)
- L3-кэш: 32 MB
- TDP / PPT: 105W / 142W
- TJmax: 95°C
- iGPU: RDNA 2, 2 CU, 2200 MHz — базовый вывод
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU) + 4 линии PCIe 4.0 на NVMe
- Поддержка AVX-512: да

## Производительность

### Cinebench R23
- Single-core: ~1 960 баллов
- Multi-core (stock 105W): ~19 700 баллов
- Multi-core (PBO, без лимитов): ~20 500 баллов

### Cinebench 2024
- Single-core: ~118 баллов
- Multi-core (stock): ~1 140 баллов

### Игры (1440p, RTX 4080)
Разница с 7700 (65W) — 1–3% в реальных игровых сценариях. Оба процессора упираются в архитектурные лимиты, а не в PPT.

- Cyberpunk 2077: ~144 fps
- Baldur's Gate 3: ~171 fps
- CS2: ~535 fps

Для гейминга на 1440p с любой видеокартой вплоть до RTX 5080 — процессор не bottleneck. В 1080p с топ-GPU разница с X3D заметнее, но 7700X всё равно выдаёт 200+ fps в киберспорте.

## Охлаждение

105W / 142W PPT — процессор горячий. Без кулера в коробке. Что нужно:

- **Минимум (на грани):** Deepcool AK400 / Thermalright Assassin X 120 — Cinebench ~78–85°C, шумно
- **Рекомендуется:** Thermalright Peerless Assassin 120 / Deepcool AK620 — Cinebench ~65–72°C
- **Оптимально:** Arctic Liquid Freezer III 240/280 — Cinebench ~55–62°C, тихо
- **VRM на бюджетных B650:** греется до 75–80°C под Cinebench. Без радиаторов — throttling. Рекомендуются платы с нормальным VRM-охлаждением (B650 Tomahawk и выше)

## Память

DDR5 only. Оптимально: DDR5-6000 CL30, MCLK:UCLK = 1:1. 7700X стабильно держит DDR5-6000. Выше — негарантированный переход в 1:2 с ростом latency. Не гонитесь за DDR5-6400+ на Zen 4.

## Сравнение с 7700 (65W)

- Базовая частота: 4.5 vs 3.8 GHz (+700 MHz в базе)
- Boost: 5.4 vs 5.3 GHz (+100 MHz)
- All-core: ~5.15 vs ~4.95 GHz (+200 MHz)
- TDP/PPT: 105W/142W vs 65W/88W
- Кулер в коробке: нет vs Wraith Prism
- R23 multi: 19 700 vs 18 500 (+6.5%)
- R23 single: 1 960 vs 1 930 (+1.5%)
- Потребление под нагрузкой: ~140W vs ~88W (+52W)
- Температура с башенным кулером: ~78°C vs ~62°C (+16°C)
- Цена: +2 000–3 000 ₽ + стоимость кулера

**Вывод:** 7700X — для тех, кто хочет заводской максимум 8 ядер без PBO. 7700 — прагматичный выбор: 94% производительности, кулер в коробке, холоднее, тише, совместим с бюджетными B650.

## Сравнение с 7800X3D

7800X3D обходит 7700X в играх на 15–30% за счёт 96 MB L3-кэша, но уступает в рабочих частотах (boost 5.0 GHz vs 5.4 GHz). В рабочих задачах (рендеринг, компиляция) 7700X быстрее на 5–10%. Цена 7800X3D — значительно выше. Выбор: игры → 7800X3D, игры + работа → 7700X.

## Для кого

**Идеален:**
- Геймеры-энтузиасты, готовые платить за каждый процент производительности «из коробки»
- Стримеры: 8 ядер хватает на игру + кодирование x264 + OBS
- Сборки с заведомо мощным охлаждением (AIO или двухсекционная башня)
- Пользователи, которые не хотят возиться с PBO, а хотят включить и работать
- Рабочие станции начального уровня: компиляция, фотошоп, лёгкий видеомонтаж

**Не подходит:**
- Тихие сборки — 142W PPT требует шумного охлаждения
- Бюджетные платы B650 без VRM-радиаторов — throttling
- Прагматики — 7700 (65W) с PBO даёт ту же производительность за меньшие деньги
- Игровой максимум — 7800X3D в играх быстрее
- Многопоточная работа — Ryzen 9 7900/7950X

## Связки

**Оптимальная:**
- MB: MSI B650 Tomahawk Wi-Fi / ASRock B650E PG Riptide
- Кулер: Thermalright Peerless Assassin 120
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5070 Ti / RX 9070 XT

**Производительная:**
- MB: ASRock X670E Steel Legend
- Кулер: Arctic Liquid Freezer III 280
- RAM: 32 GB DDR5-6000 CL28
- GPU: RTX 5080

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная
- Конкуренты: Intel Core i7-14700K (LGA1700, больше ядер, тупиковая), Core Ultra 7 265K (LGA1851)

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. TechPowerUp — Ryzen 7 7700X Review (2022)
3. Gamers Nexus — Ryzen 7 7700X CPU Review & Benchmarks (2022)
4. Hardware Unboxed — Ryzen 7 7700 vs 7700X (2023)
