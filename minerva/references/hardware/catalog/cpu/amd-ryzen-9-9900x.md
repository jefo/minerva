---
id: "amd-ryzen-9-9900x"
type: "cpu"
title: "AMD Ryzen 9 9900X (Zen 5, 120W) — 12-ядерный dual-CCD"
vendor: "amd"
status: "draft"
tags:
  - "amd"
  - "zen5"
  - "am5"
  - "ddr5"
  - "120w"
  - "12-core"
  - "dual-ccd"
  - "avx-512"
last_updated: "2026-06-07"
links:
  platform: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/amd-ryzen-9000.md"
  predecessor: "catalog/cpu/amd-ryzen-9-7900.md"
  up_variant: "catalog/cpu/amd-ryzen-9-9950x.md"
  competitor_intel: "catalog/cpu/intel-core-i7-14700k.md"
  x3d_alt: "catalog/cpu/amd-ryzen-9-9900x3d.md"
  concepts:
    - "concepts/power-budget.md"
    - "concepts/dual-ccd.md"
specs:
  socket: "AM5 (LGA1718)"
  architecture: "Zen 5 (Granite Ridge), dual-CCD"
  lithography: "TSMC 4nm (CCD ×2) + 6nm (IOD)"
  cores: 12
  threads: 24
  base_clock: "4.4 GHz"
  boost_clock: "5.6 GHz"
  all_core_boost: "~4.9–5.1 GHz"
  l2_cache: "12 MB (1 MB × 12)"
  l3_cache: "64 MB (32 MB × 2 CCD)"
  tdp: "120W"
  ppt: "162W (stock) / до 200W+ (PBO)"
  tjmax: "95°C"
  pcie_lanes: "28 (24 usable), PCIe 5.0"
  memory: "DDR5 only, dual-channel, до 5600 JEDEC / 6000+ EXPO"
  max_memory: "128 GB (4×32 GB или 2×48 GB)"
  igpu: "RDNA 2 (2 CUs, 2200 MHz, базовый вывод)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "Q3 2024"
profiles:
  multi_ccd_disaggregated:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "Параллельные многопоточные нагрузки: 3D-рендеринг, компиляция, научные расчёты. 12 ядер Zen 5 с +16% IPC над Zen 4 — уровень 7950X предыдущего поколения в многопотоке."
    failure_mode_desc: "Игры. Межчиплетная задержка ≥ 70 нс → frametime spike при перебросе потока между CCD. Даже с Process Lasso проигрывает однокристальным Ryzen 7."
    optimal_for_intents:
      - "3d_rendering_cpu"
      - "scientific_computing"
      - "heavy_compilation"
    failure_for_intents:
      - "esports_1080p_240hz"
      - "esports_1080p_360hz"
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  dense_thermal_concentration:
    power_envelope: "high"
    capability_level: 2
    steel_man_desc: "Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту до того как тепло преодолеет IHS. Максимальный буст 5.6 GHz на 2–3 секунды."
    failure_mode_desc: "Длительная all-core нагрузка. Тепловое сопротивление толстой IHS (≥ 1.7 мм, AM5) + 120W TDP на двух CCD → 89–95°C даже под СЖО. Thermal throttling 5–8% без качественного охлаждения."
    optimal_for_intents:
      - "office_productivity"
      - "software_development"
    failure_for_intents:
      - "3d_rendering_cpu"
      - "scientific_computing"
      - "heavy_compilation"
      - "silent_build"
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  sub_5nm_lithography:
    power_envelope: "high"
    steel_man_desc: "Максимальная производительность на ватт среди high-TDP процессоров. TSMC 4nm — лучшая энергоэффективность в классе."
    failure_mode_desc: "Разгон с V > 1.35В → ускоренная электромиграция и выход из строя. 4nm техпроцесс чувствителен к перенапряжению."
    optimal_for_intents:
      - "sff_build"
      - "silent_build"
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
verdict: "12-ядерный Zen 5 на двух CCD — профессиональный многопоточный процессор с +16% IPC над Zen 4. Близок к 9950X (16C) в рабочих нагрузках, но существенно дешевле. Для DAW — отличный баланс ядер и низкого DPC latency. Для видеомонтажа 4K — уверенная производительность. Ожидается версия 9900X3D с 3D V-Cache — будет ещё быстрее для чувствительных к кэшу задач. Главный компромисс — dual-CCD latency в играх. Не для бюджетных сборок."
price_ru:
  min: 27725
  median: 33500
  max: 36289
  source: "price.ru"
  date: "2026-06-07"
  note: "Офферы: Гипер Трейд (27 725 ₽), Funny Play (32 990–36 289 ₽). 84 магазина."
external_audit_verification: planned
---

# AMD Ryzen 9 9900X (Zen 5, 120W) — 12-ядерный dual-CCD

## Позиционирование

Ryzen 9 9900X — 12-ядерный 24-поточный процессор на архитектуре Zen 5 (Granite Ridge), прямой наследник Ryzen 9 7900X. Два CCD по 6 ядер дают 64 MB L3-кэша и отличную многопоточную производительность для профессиональных рабочих нагрузок: DAW, видеомонтаж, рендеринг, компиляция.

Ключевое преимущество перед предшественником 7900X: **+16% IPC** благодаря архитектуре Zen 5. В многопоточных задачах 9900X приближается к уровню 7950X (16C Zen 4) при меньшем энергопотреблении.

9900X позиционируется как **профессиональный 12-ядерник** между Ryzen 7 9700X (8C) и флагманским Ryzen 9 9950X (16C). Он близок к 9950X в большинстве рабочих нагрузок (особенно при нагрузках, не масштабирующихся идеально на 16 ядер), но стоит заметно дешевле.

**Важное ожидание:** AMD анонсировала версию 9900X3D с 3D V-Cache — это будет ещё быстрее для низких буферов в DAW и чувствительных к кэшу рабочих нагрузок. Если вы не спешите — стоит подождать X3D-версию.

Главный компромисс: **dual-CCD архитектура** — межчиплетная latency (~75–80 ns) вызывает микростаттеры в играх при перебросе потоков между CCD. 9900X — **рабочий инструмент**, а не игровой процессор. Для игр лучше 9800X3D или 7800X3D.

## Характеристики

- Архитектура: Zen 5 (Granite Ridge), dual-CCD
- Техпроцесс: TSMC 4nm (2× CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718) — обратная совместимость с B650/X670
- Ядер / потоков: 12C/24T (2× CCD по 6 ядер)
- Базовая частота: 4.4 GHz
- Boost: 5.6 GHz (на 1–2 ядрах)
- All-core нагрузка: ~4.9–5.1 GHz (зависит от охлаждения и PPT)
- L2-кэш: 12 MB (1 MB × 12)
- L3-кэш: 64 MB (32 MB × 2 CCD)
- TDP / PPT: 120W / 162W (stock); до 200W+ с PBO
- TJmax: 95°C
- iGPU: RDNA 2, 2 CU, 2200 MHz — базовый вывод
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel; JEDEC до 5600
- PCIe: 5.0 (×16 или 2×8 от CPU)
- Поддержка AVX-512: да, с улучшенным IPC

## Производительность

### Cinebench R23
- Single-core: ~2 150 баллов (+12% над 7900X: ~1 920)
- Multi-core (stock 120W): ~28 500 баллов (+10% над 7900X: ~26 000)
- Multi-core (PBO, PPT ~200W): ~30 500+ баллов

### Cinebench 2024
- Single-core: ~135 баллов (7900X: ~118)
- Multi-core: ~1 650 баллов (7900X: ~1 500)

### Рабочие нагрузки
- Blender Classroom: ~350 секунд (7900X: ~410 сек, **на 15% быстрее**)
- 7-Zip Compression: ~175 000 MIPS (7900X: ~150 000, **+17%**)
- Компиляция Linux Kernel (defconfig): ~38 секунд (7900X: ~47 сек, **+19%**)
- DaVinci Resolve 4K Render: ~420 секунд (7900X: ~490 сек, **+14%**)

### Игры (1440p)
В играх dual-CCD архитектура даёт о себе знать — 9900X уступает однокристальным процессорам:

- Cyberpunk 2077: ~142 fps (9700X: ~148 fps, −4%; 9800X3D: ~175 fps, −19%)
- CS2: ~510 fps (9700X: ~555 fps, −8%; 9800X3D: ~720 fps, −29%)
- Baldur's Gate 3: ~165 fps (9700X: ~175 fps, −6%; 9800X3D: ~200 fps, −18%)

**Для игр не рекомендуется.** Если нужен компромисс «игры + работа» — дождитесь 9900X3D с 3D V-Cache.

## Охлаждение

120W TDP / 162W PPT — значительно холоднее 7900X (170W / 230W), но всё ещё требует серьёзного охлаждения:

- **Минимум (сток, без PBO):** двухбашенный кулер (NH-D15, Peerless Assassin 120) — температуры 78–85°C под Cinebench, частоты ~4.8–4.9 GHz
- **Рекомендуется:** AIO 280 мм (Arctic Liquid Freezer III 280) — температуры 68–75°C, частоты ~5.0–5.1 GHz
- **Оптимально (с PBO):** AIO 360 мм — температуры 60–68°C, максимальные частоты
- **Воздух с PBO не рекомендуется:** даже NH-D15 будет держать 90–95°C с пониженными частотами

По сравнению с 7900X (170W TDP): 9900X выделяет на 30% меньше тепла при более высокой производительности. Это главное достижение Zen 5 — та же или лучшая производительность при существенно меньшем тепловыделении.

### Eco Mode

В BIOS можно включить Eco Mode (105W или 65W):
- **Eco 105W:** ~24 000 R23 multi, температуры ~60–70°C, можно охлаждать башней
- **Eco 65W:** ~19 000 R23 multi, температуры ~50–60°C, практически бесшумен

Eco 105W = производительность ~85% от стока при температуре на 15–20°C ниже.

## Dual-CCD: нюансы

9900X использует два CCD по 6 ядер. Это даёт:

**Плюсы:**
- 64 MB L3-кэша (против 32 MB у 9700X)
- Отличная многопоточная производительность
- Если задача умещается в один CCD (6 ядер) — работает как однокристальный процессор с бустом 5.6 GHz

**Минусы:**
- Межчиплетная latency ~75–80 ns (против ~60 ns у однокристального 9700X)
- Планировщик Windows может распределить потоки между CCD, вызывая микростаттеры
- Требует Process Lasso / Game Bar для оптимальной работы в latency-чувствительных задачах
- Даже с оптимизацией уступает однокристальным Ryzen 7 в играх

**Для DAW:** dual-CCD latency НЕ равна DPC latency. ASIO-драйвер работает через один CCD, если DAW настроена правильно. 12 ядер Zen 5 дают огромный запас для тяжёлого микширования с плагинами. Process Lasso рекомендуется для привязки ASIO-потоков к одному CCD.

## Память

Zen 5 улучшил контроллер памяти:

- JEDEC: до DDR5-5600 (против 5200 у Zen 4)
- **DDR5-6000 CL30** — золотой стандарт, MCLK:UCLK 1:1
- **DDR5-6400** — Zen 5 держит 1:1 значительно лучше Zen 4. На многих экземплярах стабильно
- DDR5-6800+ — уже 1:2, latency растёт. Не рекомендуется

Для рабочих станций объём часто важнее частоты. 128 GB DDR5-5200 лучше для работы, чем 32 GB DDR5-6000.

## Сравнение с Ryzen 9 7900X (Zen 4, 170W)

- Архитектура: Zen 5 vs Zen 4 (+16% IPC)
- Техпроцесс: TSMC 4nm vs 5nm
- Boost: 5.6 vs 5.6 GHz (одинаково!)
- All-core: ~5.0 vs ~5.0 GHz (схоже)
- TDP/PPT: 120W/162W vs 170W/230W (−29% TDP)
- R23 multi: 28 500 vs 26 000 (+10%)
- R23 single: 2 150 vs 1 920 (+12%)
- JEDEC память: DDR5-5600 vs DDR5-5200
- DDR5-6400 1:1: лучше у Zen 5
- Кулер: AIO 280 vs AIO 360 (меньше требования к охлаждению)

**Вывод:** 9900X на 10–17% быстрее 7900X при на 29% меньшем TDP. Если разница в цене ≤20% — однозначно 9900X.

## Сравнение с Intel Core i7-14700K

- Ядра/потоки: 12C/24T Zen 5 vs 20C/28T (8P+12E) Raptor Lake
- R23 multi: 28 500 vs ~36 000 (−21% в синтетике)
- R23 single: 2 150 vs ~2 230 (−4%)
- Реальная работа: 9900X сопоставим или быстрее в DAW/видеомонтаже благодаря лучшему IPC
- Потребление (Cinebench): 162W vs 253W (−36%)
- Платформа: AM5 (живая до Zen 6) vs LGA1700 (тупиковая)
- QuickSync: нет vs есть (аппаратное ускорение видео)
- AVX-512: есть vs нет
- Цена: ~33 500 ₽ vs ~45 000 ₽ (−26%)

**Вывод:** 14700K выигрывает в сыром многопотоке (E-ядра + Hyper-Threading дают 28 потоков), но 9900X холоднее, на живой платформе, и дешевле. Для DAW 9900X предпочтительнее (нет проблем с гибридным планировщиком). Для видеомонтажа — 14700K имеет преимущество QuickSync, но 9900X компенсирует лучшим IPC.

## Для кого

**Идеален:**
- **DAW / тяжёлое микширование** — 12 ядер Zen 5, отличный single-core, низкий DPC latency
- **Видеомонтаж 4K** (DaVinci Resolve, Premiere Pro) — отличный баланс ядер и частоты
- **3D-рендеринг** (Blender, V-Ray, Cinema 4D) — близок к 7950X, но дешевле
- **Компиляция больших проектов** — +19% над 7900X
- **Профессионалы**, кому нужно больше 8 ядер, но 16 ядер 9950X избыточны
- **Апгрейд с AM4** (Ryzen 9 3900X/5900X) — радикальный прирост

**Не подходит:**
- **Игровые сборки** — берите 7800X3D или 9800X3D. Dual-CCD latency вредит фреймтайму
- **Бюджетные сборки** — процессор дорогой, нужна хорошая материнская плата и охлаждение
- **Тихие SFF-сборки** — 120W+ TDP требует мощного охлаждения
- **Максимальный многопоток любой ценой** — 9950X (16C) или Threadripper

## Связки

**Профессиональная рабочая станция:**
- MB: MSI MAG X670E Tomahawk Wi-Fi / ASRock X670E Steel Legend
- Кулер: Arctic Liquid Freezer III 280 / Deepcool LT720
- RAM: 64 GB DDR5-6000 CL30
- GPU: RTX 5070 Ti / RTX 5080 (для видеомонтажа и рендеринга)
- Блок питания: 850W+ (CPU 162W + GPU 300–360W)

**DAW-оптимизированная:**
- MB: ASRock B650E PG Riptide (стабильный VRM, минимум лишних контроллеров)
- Кулер: Noctua NH-D15 / be quiet! Dark Rock Pro 4 (низкий шум)
- RAM: 64 GB DDR5-6000 CL30 (низкая latency для ASIO)
- Аудиоинтерфейс: RME / Universal Audio (внешний, не зависит от чипсета)
- Process Lasso: обязательно для привязки ASIO-потоков к CCD0

**Компромиссная (Eco Mode 105W):**
- MB: MSI B650 Tomahawk Wi-Fi
- Кулер: Thermalright Peerless Assassin 120
- RAM: 32 GB DDR5-6000 CL30
- Производительность: ~85% от стока, но холодно и тихо

## Российский рынок

- Статус: **draft** — цены добавлены на основе price.ru (2026-06-07)
- Доступность: стабильная, 84 магазина на price.ru
- Цены: **27 725–36 289 ₽**, медиана ~33 500 ₽
- Офферы: Гипер Трейд (от 27 725 ₽), Funny Play (32 990–36 289 ₽)
- Конкуренты: Intel Core i7-14700K (~45 000 ₽), Ryzen 9 7900X (~42 000 ₽, Zen 4)
- Позиция на рынке: 9900X дешевле обоих конкурентов, холоднее и на живой платформе AM5

## Ожидаемая версия 9900X3D

AMD готовит Ryzen 9 9900X3D с 3D V-Cache (аналогично 7950X3D). Ожидается, что 3D-кэш будет на одном CCD (6 ядер с 96 MB L3), второй CCD — стандартный (6 ядер, 32 MB L3). Это даст:

- Радикальный прирост в чувствительных к кэшу задачах (DAW с низким буфером, компиляция)
- Лучшую игровую производительность (близко к 9800X3D на CCD с V-Cache)
- Ту же многопоточную производительность на втором CCD

Если вы можете подождать — 9900X3D будет лучшим выбором для компромисса «работа + игры».

## Источники

1. AMD Zen 5 Architecture Brief (amd.com, 2024)
2. TechPowerUp — Ryzen 9 9900X Review (2024)
3. Gamers Nexus — Ryzen 9 9900X CPU Review & Benchmarks (2024)
4. Hardware Unboxed — Zen 5 vs Zen 4 Productivity Comparison (2024)
5. Puget Systems — Ryzen 9 9900X for Content Creation (2024)
6. Scan Pro Audio — DAW Benchmark with Zen 5 (2024)
7. Price.ru — мониторинг цен (2026-06-07)
