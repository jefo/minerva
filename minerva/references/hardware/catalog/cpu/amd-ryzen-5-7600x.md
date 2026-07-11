---
id: "amd-ryzen-5-7600x"
type: "cpu"
title: "AMD Ryzen 5 7600X (105W)"
vendor: "amd"
status: "draft"
tags: ["amd", "zen4", "am5", "ddr5", "105w", "igpu", "6-core", "no-box-cooler"]
last_updated: "2026-06-03"
external_audit_verification: planned
price_ru:
  min: 16000
  median: 18000
  max: 21000
  source: "price.ru"
  date: "2026-06-04"
links:
  platform: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/amd-ryzen-7000.md"
  down_variant: "catalog/cpu/amd-ryzen-5-7600.md"
  multi_core_alt: "catalog/cpu/amd-ryzen-7-7700x.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "AM5 (LGA1718)"
  architecture: "Zen 4 (Raphael)"
  lithography: "TSMC 5nm (CCD) + 6nm (IOD)"
  cores: 6
  threads: 12
  base_clock: "4.7 GHz"
  boost_clock: "5.3 GHz"
  l2_cache: "6 MB (1 MB × 6)"
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
verdict: "Самый быстрый 6-ядерник Zen 4 «из коробки». 105W TDP даёт высокие базовые частоты (4.7 GHz), но требует нормального кулера. Для прагматиков 7600 (65W) часто выгоднее — разница в играх минимальна."
---

# AMD Ryzen 5 7600X (105W)

## Позиционирование

Ryzen 5 7600X — 6-ядерный 12-поточный процессор Zen 4 с TDP 105W, ориентированный на геймеров, которые хотят максимальную производительность 6-ядерника без ручного разгона. Заводские частоты 4.7/5.3 GHz — самые высокие среди 6-ядерных Ryzen 7000.

Плата за высокие частоты: нет кулера в комплекте, 105W TDP требует нормального охлаждения, цена на 3–4 тыс. ₽ выше 7600. В играх разница с 7600 (65W) — 1–3%, поскольку boost-частоты отличаются всего на 200 MHz.

## Характеристики

- Архитектура: Zen 4 (Raphael)
- Техпроцесс: TSMC 5nm (CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 6C/12T
- Базовая частота: 4.7 GHz — значительно выше 3.8 GHz у 7600
- Boost: 5.3 GHz (на 1–2 ядрах)
- All-core нагрузка: ~5.1–5.2 GHz
- L2-кэш: 6 MB (1 MB × 6)
- L3-кэш: 32 MB (единый)
- TDP / PPT: 105W / 142W
- TJmax: 95°C
- iGPU: RDNA 2, 2 CU, 2200 MHz
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU) + 4 линии PCIe 4.0 на NVMe

## Производительность

### Cinebench R23
- Single-core: ~1 950 баллов
- Multi-core (stock 105W): ~15 300 баллов
- Multi-core (PBO, без лимитов): ~15 800 баллов

### Cinebench 2024
- Single-core: ~118 баллов
- Multi-core: ~880 баллов

### Игры (1440p)
Разница с 7600 — в пределах погрешности (1–3%). Преимущество 7600X проявляется только в 1080p с топ-видеокартами (RTX 4090/5080), где +200 MHz boost дают 3–5% прироста. В 1440p и выше — без разницы.

- Cyberpunk 2077: ~133 fps
- Baldur's Gate 3: ~158 fps
- CS2: ~480 fps

## Охлаждение

105W TDP / 142W PPT означает, что Wraith Stealth не справится — процессор уйдёт в throttling. Необходим башенный кулер:

- **Минимум:** ID-COOLING SE-224-XTS / Deepcool AK400 — Cinebench ~78–85°C, игры ~60–70°C
- **Рекомендуется:** Thermalright Peerless Assassin 120 / Deepcool AK620 — Cinebench ~65–72°C
- **Максимум:** Arctic Liquid Freezer III 240 — Cinebench ~55–62°C

VRM бюджетных плат B650 (без радиаторов) с 7600X греются до 75–80°C — на грани throttling. Для 7600X рекомендуется B650 с нормальным VRM-охлаждением.

## Память

DDR5 only. Оптимально: DDR5-6000 CL30, режим MCLK:UCLK = 1:1. 7600X без проблем держит DDR5-6000. Выше 6000 — негарантированный режим 1:2 с ростом latency.

## Сравнение с 7600 (65W)

- Boost: 5.3 vs 5.1 GHz (+200 MHz, +4%)
- All-core: ~5.15 vs ~4.85 GHz (+300 MHz, +6%)
- TDP/PPT: 105W/142W vs 65W/88W
- Кулер в коробке: нет vs Wraith Stealth
- R23 multi: 15 300 vs 14 500 (+5.5%)
- R23 single: 1 950 vs 1 870 (+4%)
- Игры 1440p: ~1–3% разницы
- Цена: +3 000–4 000 ₽ + стоимость кулера

**Вывод:** 7600X — для тех, кто готов платить за каждые 3–5% производительности и в любом случае ставит мощное охлаждение. 7600 (65W) — прагматичный выбор для 95% сборок.

## Для кого

**Идеален:**
- Энтузиасты, желающие заводской максимум 6-ядерника без возни с PBO
- Сборки с заведомо мощным охлаждением (AIO или двухсекционная башня)
- Геймеры на 1080p с топ-видеокартой (RTX 4090/5080)
- Бюджетные рабочие станции начального уровня (фотошоп, компиляция)

**Не подходит:**
- Тихие сборки — 105W тепловыделение требует активного охлаждения
- Бюджетные платы B650 без VRM-радиаторов — возможен throttling VRM
- Прагматичные сборки — 7600 (65W) даёт 95% производительности за меньшие деньги
- Киберспорт высшего уровня — нужен 7800X3D

## Связки

**Оптимальная:**
- MB: MSI B650 Tomahawk Wi-Fi / ASRock B650E PG Riptide
- Кулер: Thermalright Peerless Assassin 120
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5070 / RX 9070 XT

**Производительная:**
- MB: ASRock B650E Steel Legend / GIGABYTE B650 AORUS Elite
- Кулер: Arctic Liquid Freezer III 240
- RAM: 32 GB DDR5-6000 CL28
- GPU: RTX 5080

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная
- Конкуренты: Intel Core i5-14600K (LGA1700, больше ядер, тупиковая платформа)

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. TechPowerUp — Ryzen 5 7600X Review (2022)
3. Gamers Nexus — Ryzen 5 7600X CPU Review & Benchmarks (2022)
4. Hardware Unboxed — Ryzen 5 7600 vs 7600X (2023)
