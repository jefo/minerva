---
id: amd-ryzen-9-7900
type: cpu
title: AMD Ryzen 9 7900 (65W) — 12 ЯДЕР, 65W
vendor: amd
status: draft
tags:
- amd
- zen4
- am5
- ddr5
- 65w
- 12-core
- dual-ccd
- box-cooler
last_updated: '2026-06-03'
external_audit_verification: planned
links:
  platform: catalog/motherboard/am5/index.md
  memory_type: catalog/memory/ddr5.md
  family: catalog/cpu/amd-ryzen-7000.md
  up_variant: catalog/cpu/amd-ryzen-9-7950x.md
  down_variant: catalog/cpu/amd-ryzen-7-7700.md
  x_variant: catalog/cpu/amd-ryzen-9-7900x.md
  concepts:
  - concepts/power-budget.md
  - concepts/dual-ccd.md
specs:
  socket: AM5 (LGA1718)
  architecture: Zen 4 (Raphael), dual-CCD
  lithography: TSMC 5nm (CCD ×2) + 6nm (IOD)
  cores: 12
  threads: 24
  base_clock: 3.7 GHz
  boost_clock: 5.4 GHz
  l2_cache: 12 MB (1 MB × 12)
  l3_cache: 64 MB (32 MB × 2 CCD)
  tdp: 65W
  ppt: 88W (default)
  tjmax: 95°C
  pcie_lanes: 28 (24 usable), PCIe 5.0
  memory: DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO
  max_memory: 128 GB (4×32 GB или 2×48 GB)
  igpu: RDNA 2 (2 CUs, 2200 MHz, базовый вывод)
  box_cooler: Wraith Prism (в коробке, на грани возможностей)
  package: Retail (BOX)
  release_date: Q1 2023
profiles:
  multi_ccd_disaggregated:
    power_envelope: mid
    capability_level: 3
    steel_man_desc: 'Параллельные многопоточные: 3D-рендеринг, компиляция. 12–16 ядер
      без HEDT-тарифа.'
    failure_mode_desc: Игры. Межчиплетная задержка ≥ 70 нс → frametime spike при перебросе
      потока между CCD.
    optimal_for_intents:
    - 3d_rendering_cpu
    - scientific_computing
    - heavy_compilation
    failure_for_intents:
    - esports_1080p_240hz
    - esports_1080p_360hz
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
  dense_thermal_concentration:
    power_envelope: mid
    capability_level: 2
    steel_man_desc: 'Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту
      до того как тепло преодолеет IHS. Максимальный буст на 2–3 секунды.'
    failure_mode_desc: Длительная нагрузка. Тепловое сопротивление толстой IHS (≥
      1.7 мм, AM5) → 89–95°C даже под СЖО. Thermal throttling 5–8%.
    optimal_for_intents:
    - office_productivity
    - software_development
    failure_for_intents:
    - 3d_rendering_cpu
    - scientific_computing
    - heavy_compilation
    - silent_build
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
  sub_5nm_lithography:
    power_envelope: mid
    steel_man_desc: Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления.
    failure_mode_desc: Разгон с V > 1.35В → ускоренная электромиграция и выход из
      строя.
    optimal_for_intents:
    - sff_build
    - silent_build
    failure_for_intents: []
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
verdict: 'Уникальный процессор: 12 ядер / 24 потока с TDP всего 65W. Идеален для тихих
  рабочих станций и компактных сборок (SFF). Два CCD дают 64 MB L3. В играх уступает
  однокристальным Ryzen 7 из-за межчиплетной latency — это чисто рабочий инструмент
  с феноменальной энергоэффективностью.'
price_ru:
  min: 38000
  median: 42000
  max: 48000
  source: price.ru
  date: '2026-06-04'
---

# AMD Ryzen 9 7900 (65W) — 12 ЯДЕР, 65W

## Позиционирование

Ryzen 9 7900 — **уникальный процессор**, аналогов которому нет ни у Intel, ни у самой AMD в предыдущих поколениях. 12 ядер и 24 потока упакованы в теплопакет 65W TDP (PPT 88W). Это настоящий инженерный подвиг: Zen 4 на двух кристаллах CCD (по 6 ядер каждый) работает в паспортном тепловыделении, которое ещё 5 лет назад считалось нормой для 4-ядерников.

7900 позиционируется AMD как «эффективный многопоточный процессор» для создателей контента, разработчиков и пользователей, которым нужна серьёзная многопоточная производительность без шума, громоздкого охлаждения и огромных счетов за электричество.

Ключевой компромисс: **dual-CCD архитектура**. Два чиплета по 6 ядер дают 64 MB L3-кэша и отличный многопоток, но межчиплетная latency (~75–80 ns) вносит микростаттеры в играх, если планировщик Windows неудачно распределит потоки между CCD. Это чисто **рабочий процессор** — для игр лучше взять 7700 или 7800X3D.

## Характеристики

- Архитектура: Zen 4 (Raphael), dual-CCD
- Техпроцесс: TSMC 5nm (2× CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 12C/24T (2× CCD по 6 ядер)
- Базовая частота: 3.7 GHz
- Boost: 5.4 GHz (на 1–2 ядрах, лёгкая нагрузка)
- All-core нагрузка: ~4.3–4.5 GHz (ограничено PPT 88W на 12 ядер)
- L2-кэш: 12 MB (1 MB × 12)
- L3-кэш: 64 MB (32 MB × 2 CCD)
- TDP / PPT: 65W / 88W
- TJmax: 95°C
- iGPU: RDNA 2, 2 CU, 2200 MHz
- Кулер в коробке: Wraith Prism (на грани возможностей — см. раздел «Охлаждение»)
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU)
- Поддержка AVX-512: да

## Производительность

### Cinebench R23
- Single-core: ~1 950 баллов
- Multi-core (stock 65W / PPT 88W): ~24 000 баллов
- Для сравнения — 7700 (8C, 65W): ~18 500 баллов — **+30% многопотока за те же 65W**

### Cinebench 2024
- Single-core: ~117 баллов
- Multi-core: ~1 380 баллов

### Рабочие нагрузки
- Blender Classroom: ~480 секунд (7700: ~620 сек, **на 23% быстрее**)
- 7-Zip Compression: ~130 000 MIPS (7700: ~95 000, **+37%**)
- Компиляция Linux Kernel (defconfig): ~55 секунд (7700: ~75 сек, **+27%**)

### Игры (1440p)
В играх 7900 уступает однокристальным процессорам:

- Cyberpunk 2077: ~130 fps (7700: ~142 fps, −8%)
- CS2: ~460 fps (7700: ~520 fps, −12%)
- Baldur's Gate 3: ~155 fps (7700: ~168 fps, −8%)

Причина: межчиплетная latency ~75–80 ns (против ~60 ns у однокристального 7700). Планировщик Windows может распределить игровые потоки между двумя CCD, вызывая микростаттеры. Лечится через Process Lasso (ручная привязка к одному CCD) или Xbox Game Bar, но требует настройки.

## Охлаждение — важный нюанс

**65W TDP на 12 ядер** — феноменально низкое тепловыделение. Однако есть нюанс:

- **Wraith Prism в комплекте** — да, AMD кладёт его в коробку, и он справляется. Под Cinebench: 80–85°C на грани throttling. В играх: 65–72°C. Вентилятор слышен (45 dBA). **Работает, но на пределе.**
- **Башенный кулер за 2 000–3 000 ₽** (AK400, Assassin X 120): Cinebench — 62–68°C, тихо, с запасом. Рекомендуется даже для стокового режима.
- **AIO 240мм:** Cinebench — 52–58°C, полный запас для PBO.

PPT 88W на 12 ядер означает, что каждое ядро получает в среднем ~7W под полной нагрузкой — это экстремально энергоэффективно. Для сравнения: 7900X (170W TDP) — те же 12 ядер, но в 2.6 раза больше PPT.

## Dual-CCD: нюансы для геймеров

7900 использует два CCD по 6 ядер. Это даёт:

**Плюсы:**
- 64 MB L3-кэша (против 32 MB у 7700)
- Отличная многопоточная производительность
- Если игра умещается в один CCD (6 ядер), она работает как однокристальный процессор

**Минусы:**
- Межчиплетная latency ~75–80 ns
- Планировщик Windows может распределить игровые потоки между CCD, вызывая микростаттеры
- Требует Process Lasso / Game Bar для оптимальной работы в играх
- Даже с оптимизацией — уступает однокристальным 7700/7800X3D в играх

**Для чисто рабочих станций** dual-CCD — не проблема. Рендеринг, компиляция, виртуализация прекрасно масштабируются на оба CCD.

## Память

DDR5 only. Оптимально: DDR5-6000 CL30. Межчиплетная latency делает 7900 чуть более чувствительным к частоте памяти, чем однокристальные Zen 4, но разница не критична. Не экономьте на памяти ниже DDR5-5600.

## Сравнение с 7900X (170W)

- Ядра: 12C/24T — идентично
- Boost: 5.4 vs 5.6 GHz (−200 MHz)
- All-core: ~4.4 vs ~5.0 GHz (−600 MHz)
- TDP/PPT: 65W/88W vs 170W/230W
- R23 multi: 24 000 vs ~29 000 (−17%)
- R23 single: 1 950 vs 1 980 (−1.5%)
- Потребление под нагрузкой: 88W vs 230W (−62%)
- Кулер: Wraith Prism в коробке vs нужна AIO 280/360

**Вывод:** 7900 даёт 83% производительности 7900X при 38% энергопотребления. Если вам не нужны последние 17% многопотока — 7900 объективно лучше: холоднее, тише, дешевле в сборке.

## Для кого

**Идеален:**
- **Тихие рабочие станции** — 65W TDP позволяет охлаждать пассивно или полупассивно
- **SFF-сборки** (Small Form Factor) — 12 ядер в корпусе объёмом 5–10 литров
- **Разработчики** — компиляция, виртуализация, Docker, WSL
- **Видеомонтаж и рендеринг** среднего уровня
- **Домашние серверы** — низкое энергопотребление 24/7
- **Создатели контента**, работающие из дома и ценящие тишину

**Не подходит:**
- **Геймеры** — берите 7700 или 7800X3D. Dual-CCD latency вредит играм
- **Тяжёлый рендеринг 24/7** — нужен 7950X (16 ядер) или Threadripper
- **Энтузиасты максимальной производительности** — смотрите 7900X/7950X
- **Бюджетные сборки** — процессор дорогой, оправдан только если нужны 12 ядер

## Уникальность на рынке

По состоянию на 2024–2026 год Ryzen 9 7900 **не имеет прямых конкурентов**. Ни один другой 12-ядерный процессор не работает с TDP 65W:

- Intel Core i7-14700 (65W) — 20 ядер (8P+12E), но в реальности потребляет 150W+ под нагрузкой
- AMD Ryzen 9 7900X — 170W TDP, требует AIO
- AMD Ryzen 9 5900 (65W, AM4) — предыдущее поколение, 12 ядер Zen 3, но AM4 тупиковая

Если вам нужно 12 ядер, тишина и энергоэффективность — 7900 единственный выбор.

## Связки

**Тихая рабочая станция:**
- MB: MSI B650 Tomahawk Wi-Fi (VRM с запасом даже без обдува)
- Кулер: Noctua NH-D15 / be quiet! Dark Rock Pro 4 (полупассивный режим)
- RAM: 64 GB DDR5-5600 (стабильность важнее частоты)
- Корпус: Fractal Design Define 7 (шумоподавление)

**SFF-рабочая станция:**
- MB: ASRock B650E PG-ITX
- Кулер: Thermalright AXP120-X67 (низкопрофильный)
- RAM: 64 GB DDR5-5600 (SODIMM или low-profile)
- Корпус: Cooler Master NR200 / Fractal Terra

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная, но менее популярен, чем X-версии
- Часто недооценён покупателями, которые автоматически берут 7900X «потому что X — значит быстрее»

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. TechPowerUp — Ryzen 9 7900 Review (2023)
3. Gamers Nexus — Ryzen 9 7900 CPU Review & Benchmarks (2023)
4. Hardware Unboxed — Ryzen 9 7900 vs 7900X Efficiency (2023)
5. ComputerBase — Dual-CCD Latency Analysis (2023)
