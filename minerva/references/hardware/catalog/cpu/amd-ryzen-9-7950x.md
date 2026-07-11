---
id: amd-ryzen-9-7950x
type: cpu
title: AMD Ryzen 9 7950X (170W) — ФЛАГМАН AM5
vendor: amd
status: draft
tags:
- amd
- zen4
- am5
- ddr5
- 170w
- 16-core
- dual-ccd
last_updated: '2026-06-03'
external_audit_verification: planned
links:
  platform: catalog/motherboard/am5/index.md
  memory_type: catalog/memory/ddr5.md
  family: catalog/cpu/amd-ryzen-7000.md
  down_variant: catalog/cpu/amd-ryzen-9-7900.md
  down_variant_x: catalog/cpu/amd-ryzen-9-7900x.md
  x3d_alt: catalog/cpu/amd-ryzen-9-7950x3d.md
  competitor_intel: catalog/cpu/intel-core-14900k.md
  concepts:
  - concepts/power-budget.md
  - concepts/dual-ccd.md
specs:
  socket: AM5 (LGA1718)
  architecture: Zen 4 (Raphael), dual-CCD
  lithography: TSMC 5nm (CCD ×2) + 6nm (IOD)
  cores: 16
  threads: 32
  base_clock: 4.5 GHz
  boost_clock: 5.7 GHz
  l2_cache: 16 MB (1 MB × 16)
  l3_cache: 64 MB (32 MB × 2 CCD)
  tdp: 170W
  ppt: 230W (default)
  tjmax: 95°C
  pcie_lanes: 28 (24 usable), PCIe 5.0
  memory: DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO
  max_memory: 128 GB (4×32 GB или 2×48 GB)
  igpu: RDNA 2 (2 CUs, 2200 MHz, базовый вывод)
  box_cooler: null
  package: Retail (BOX, без кулера)
  release_date: Q3 2022
profiles:
  multi_ccd_disaggregated:
    power_envelope: high
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
    power_envelope: high
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
    power_envelope: high
    steel_man_desc: Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления.
    failure_mode_desc: Разгон с V > 1.35В → ускоренная электромиграция и выход из
      строя.
    optimal_for_intents:
    - sff_build
    - silent_build
    failure_for_intents: []
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
verdict: Флагманская 16-ядерная рабочая станция на AM5. Boost до 5.7 GHz — рекорд
  для Zen 4. Многопоточная производительность сопоставима с Threadripper предыдущего
  поколения. Требует мощного охлаждения (AIO 360 мм минимум). Для игр — избыточен,
  dual-CCD latency вредит фреймтайму. Чисто рабочий инструмент высшего уровня.
price_ru:
  min: 55000
  median: 62000
  max: 70000
  source: price.ru
  date: '2026-06-04'
---

# AMD Ryzen 9 7950X (170W) — ФЛАГМАН AM5

## Позиционирование

Ryzen 9 7950X — флагманский процессор AMD на платформе AM5: 16 ядер, 32 потока, boost до 5.7 GHz. Это абсолютный максимум производительности в потребительском сегменте AMD до выхода Threadripper 7000.

7950X позиционируется для профессионалов: рендеринг, компиляция, научные расчёты, виртуализация, тяжёлый видеомонтаж. Два CCD по 8 ядер дают 64 MB L3-кэша и колоссальную многопоточную производительность.

170W TDP (PPT 230W) означает, что для 7950X необходимо серьёзное охлаждение — AIO на 360 мм как минимум. В штатном режиме процессор намеренно греется до 95°C TJmax, выжимая максимум частоты из доступного термобюджета. Это нормальное поведение, а не дефект.

Для игр 7950X избыточен: dual-CCD архитектура даёт межчиплетную latency, которая вредит фреймтайму. Игровой флагман — 7800X3D (или 7950X3D, если нужны и игры, и работа).

## Характеристики

- Архитектура: Zen 4 (Raphael), dual-CCD
- Техпроцесс: TSMC 5nm (2× CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 16C/32T (2× CCD по 8 ядер)
- Базовая частота: 4.5 GHz
- Boost: 5.7 GHz (на 1–2 ядрах) — рекорд для Zen 4
- All-core нагрузка: ~5.0–5.2 GHz (зависит от охлаждения)
- L2-кэш: 16 MB (1 MB × 16)
- L3-кэш: 64 MB (32 MB × 2 CCD)
- TDP / PPT: 170W / 230W
- TJmax: 95°C — процессор намеренно работает на этом пределе для максимальной частоты
- iGPU: RDNA 2, 2 CU, 2200 MHz — базовый вывод
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU)
- Поддержка AVX-512: да
- Разблокированный множитель: да

## Производительность

### Cinebench R23
- Single-core: ~2 000 баллов
- Multi-core (stock 170W): ~37 500 баллов
- Multi-core (PBO, без лимитов): ~40 000+ баллов

### Cinebench 2024
- Single-core: ~122 балла
- Multi-core (stock): ~2 200 баллов

### Рабочие нагрузки
- Blender Classroom: ~250 секунд (7900: ~480 сек, **в 1.9 раза быстрее**)
- 7-Zip Compression: ~210 000 MIPS (7900: ~130 000, **+62%**)
- V-Ray Benchmark: ~32 000 баллов
- Компиляция Linux Kernel (defconfig): ~30 секунд (7900: ~55 сек, **+45%**)

### Игры (1440p)
В играх 7950X уступает однокристальным процессорам и X3D:

- Cyberpunk 2077: ~135 fps (7800X3D: ~158 fps, −15%)
- CS2: ~490 fps (7800X3D: ~680 fps, −28%)
- Baldur's Gate 3: ~160 fps (7800X3D: ~195 fps, −18%)

**Для игр не рекомендуется.** Dual-CCD latency + отсутствие 3D V-Cache = неигровой процессор. Если нужен компромисс «игры + работа» — 7950X3D.

## Охлаждение

170W TDP / 230W PPT — это серьёзно. 7950X спроектирован работать при 95°C под полной нагрузкой:

- **Минимум (будет throttling):** Arctic Liquid Freezer III 280 — температуры 90–95°C, частоты ~4.9–5.0 GHz
- **Рекомендуется:** Arctic Liquid Freezer III 360 / Deepcool LT720 — температуры 85–92°C, частоты ~5.1–5.2 GHz
- **Оптимально:** Кастомная СВО (custom loop) с радиатором 360+ мм — температуры 75–85°C, максимальные частоты
- **Воздух не рекомендуется:** даже NH-D15 будет держать 95°C с пониженными частотами

**Важно:** 95°C для 7950X — это **штатный режим**, не баг. Процессор использует термобюджет до последнего градуса для максимального boost. Но это означает, что в корпусе будет жарко, и видеокарта получит дополнительный нагрев.

### Eco Mode

В BIOS можно включить Eco Mode (105W или 65W):

- **Eco 105W:** ~30 000 R23 multi, температуры ~65–75°C, можно охлаждать башней
- **Eco 65W:** ~24 000 R23 multi, температуры ~55–65°C, практически бесшумен

Фактически Eco 105W = производительность 7900X, Eco 65W = производительность 7900. Гибкость огромная.

## Память

DDR5 only. 7950X чувствителен к частоте памяти из-за dual-CCD архитектуры:

- **DDR5-6000 CL30** — золотой стандарт для 1:1
- **DDR5-6400** — возможно на некоторых экземплярах в 1:1, но не гарантирован
- **4 планки (4×16 или 4×32 GB):** частота падает до DDR5-5200–5600. Если нужен большой объём памяти, лучше 2×48 GB (96 GB total) на DDR5-6000

Для рабочих станций объём памяти часто важнее частоты. 128 GB DDR5-5200 лучше для работы, чем 32 GB DDR5-6000.

## Сравнение с Intel Core i9-14900K

- Ядра/потоки: 16C/32T Zen 4 vs 24C/32T (8P+16E) Raptor Lake
- R23 multi: 37 500 vs ~40 000 (−6%)
- R23 single: 2 000 vs ~2 300 (−13%)
- Потребление (Cinebench): 230W vs 300W+ (−23%)
- AVX-512: есть vs нет
- Платформа: AM5 (живая до Zen 6) vs LGA1700 (тупиковая)
- Стабильность: без деградации vs известные проблемы Raptor Lake

**Вывод:** 14900K чуть быстрее в пике, но горячее, с проблемами стабильности и на тупиковой платформе. 7950X — более рациональный выбор для профессионалов.

## Для кого

**Идеален:**
- Профессиональный рендеринг (Blender, V-Ray, Cinema 4D, Octane)
- Видеомонтаж 4K/8K (Premiere Pro, DaVinci Resolve)
- Компиляция больших проектов (AOSP, Linux kernel, Chromium, Unreal Engine)
- Научные расчёты (MATLAB, CFD, молекулярная динамика)
- Виртуализация (множество VM, Docker-контейнеров)
- Рабочие станции, где время = деньги, и каждый процент производительности окупается

**Не подходит:**
- **Игровые сборки** — берите 7800X3D. 7950X медленнее в играх и горячее
- **Тихие сборки** — 170W TDP требует шумного охлаждения
- **Бюджетные сборки** — цена высокая, нужна дорогая материнская плата и охлаждение
- **SFF-корпуса** — 7950X требует AIO 360 мм, не влезет в компактный корпус
- **Домашний сервер 24/7** — 170W TDP в простое неоправданно; лучше 7900 (65W)

## Связки

**Профессиональная рабочая станция:**
- MB: ASRock X670E Taichi / GIGABYTE X670E AORUS Master (мощный VRM)
- Кулер: Arctic Liquid Freezer III 360 / Deepcool LT720
- RAM: 64–128 GB DDR5-5600 (стабильность > частота)
- GPU: RTX 4090/5090 (для GPU-рендеринга)
- Блок питания: 1000W+ (CPU 230W + GPU 450–600W)

**Компромиссная (Eco Mode 105W):**
- MB: MSI B650 Tomahawk Wi-Fi
- Кулер: Thermalright Peerless Assassin 120
- RAM: 64 GB DDR5-6000 CL30
- Производительность: ~80% от стока, но холодно и тихо

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная
- Конкуренты: Intel Core i9-14900K (LGA1700), Core Ultra 9 285K (LGA1851)

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. TechPowerUp — Ryzen 9 7950X Review (2022)
3. Gamers Nexus — Ryzen 9 7950X CPU Review & Benchmarks (2022)
4. Hardware Unboxed — 7950X Productivity Benchmarks (2022)
5. Puget Systems — Ryzen 9 7950X for Content Creation (2023)
6. Der8auer — 7950X Direct-Die Cooling & Overclocking (2022)
