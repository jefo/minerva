---
id: amd-ryzen-9-9950x
type: cpu
title: AMD Ryzen 9 9950X (170W) — Zen 5 флагман, 16 ядер
vendor: AMD
status: draft
tags:
- amd
- zen5
- am5
- high-core-count
- ddr5
- 170w
- 16-core
- dual-ccd
- avx-512
last_updated: '2026-06-07'
links:
  predecessor: catalog/cpu/amd-ryzen-9-7950x.md
  competitor: catalog/cpu/intel-core-i9-14900k.md
  platform: catalog/motherboard/am5/index.md
  memory_type: catalog/memory/ddr5.md
  concepts:
  - concepts/power-budget.md
  - concepts/dual-ccd.md
specs:
  socket: AM5 (LGA1718)
  architecture: "Zen 5 (Granite Ridge), dual-CCD (2×8 ядер)"
  lithography: TSMC 4nm (CCD ×2) + 6nm (IOD)
  cores: 16
  threads: 32
  base_clock: "4.3 GHz"
  boost_clock: "5.7 GHz"
  l2_cache: "16 MB (1 MB × 16)"
  l3_cache: "64 MB (32 MB × 2 CCD)"
  tdp: "170W"
  ppt: "230W (default)"
  tjmax: "95°C"
  pcie_lanes: 28 (24 usable), PCIe 5.0
  memory: DDR5 only, dual-channel, до 5600 JEDEC / 6400+ EXPO
  max_memory: 192 GB (4×48 GB)
  igpu: RDNA 2 (2 CU, 2200 MHz, базовый вывод)
  box_cooler: null
  package: Retail (BOX, без кулера)
  release_date: Q3 2024
  multiplier: "unlocked"
  multiplier_source: "https://www.amd.com/en/products/processors/desktops/ryzen.html"
profiles:
  multi_ccd_disaggregated:
    power_envelope: high
    capability_level: 3
    steel_man_desc: 'Параллельные многопоточные: 3D-рендеринг, компиляция, AI-инференс. 16 ядер Zen 5 с AVX-512 на потребительской платформе без HEDT-тарифа.'
    failure_mode_desc: 'Игры и реалтайм-задачи. Межчиплетная задержка (≥ 70 нс inter-CCD) вызывает frametime spike при перебросе потока между CCD.'
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
    steel_man_desc: 'Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту до того как тепло преодолеет IHS. Максимальный буст на 2–3 секунды.'
    failure_mode_desc: 'Длительная нагрузка. Тепловое сопротивление толстой IHS (≥ 1.7 мм, AM5) → 89–95°C даже под СЖО. Thermal throttling 5–8%.'
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
    steel_man_desc: 'Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления.'
    failure_mode_desc: 'Разгон с V > 1.35В → ускоренная электромиграция и выход из строя.'
    optimal_for_intents:
    - sff_build
    - silent_build
    failure_for_intents: []
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
verdict: Флагманский 16-ядерный процессор Zen 5 на AM5 с выдающейся производительностью
  на ватт. +18% к Core Ultra 9 285K в DAWBench DSP при сравнимом потреблении — лучший выбор
  для профессиональной работы со звуком. AVX-512, 64 MB L3, PCIe 5.0 — серьёзный
  инструмент для рендеринга, компиляции и AI-инференса. Требует мощного охлаждения
  (AIO 360 мм минимум). Для игр — избыточен; если нужен компромисс «игры + работа»,
  смотреть 9950X3D.
external_audit_verification: planned
price_ru:
  min: 36750
  median: 40425
  max: 43650
  source: price.ru
  date: '2026-06-07'
---

# AMD Ryzen 9 9950X (170W) — Zen 5 флагман, 16 ядер

## Позиционирование

Ryzen 9 9950X — флагманский производительный процессор AMD на архитектуре Zen 5. 16 ядер, 32 потока на платформе AM5 с TDP 170W (средний 148W). Наследник 7950X, но с улучшенной энергоэффективностью: TSMC 4nm вместо 5nm, +16% IPC, улучшенный контроллер памяти DDR5-5600 native.

Ключевое преимущество 9950X — **+18% к Intel Core Ultra 9 285K в DAWBench DSP при схожем или меньшем энергопотреблении**. При этом 9950X холоднее Intel под sustained нагрузкой: 148W средний против 125–180W у конкурента с меньшим thermal density. Для профессиональной работы со звуком (микширование 500+ треков) — лучший CPU на рынке.

170W TDP (PPT 230W) означает серьёзные требования к охлаждению — AIO 360 мм как необходимый минимум для sustained нагрузки. В штатном режиме процессор стремится к 95°C TJmax, выжимая максимум частоты из доступного термобюджета.

**Не для SFF:** 170W теплопакет несовместим с компактными корпусами без серьёзных компромиссов по производительности. Для SFF-сборок смотреть Ryzen 7 9700X (65W) или Ryzen 9 7900 (65W Eco Mode).

## Характеристики

- Архитектура: Zen 5 (Granite Ridge), dual-CCD (2×8 ядер)
- Техпроцесс: TSMC 4nm (2× CCD) + 6nm (IOD)
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 16C/32T (2× CCD по 8 ядер)
- Базовая частота: 4.3 GHz
- Boost: 5.7 GHz (на 1–2 ядрах)
- All-core нагрузка: ~5.0–5.2 GHz (зависит от охлаждения)
- L2-кэш: 16 MB (1 MB × 16)
- L3-кэш: 64 MB (32 MB × 2 CCD)
- TDP / PPT: 170W / 230W; измеренный средний: 148W
- TJmax: 95°C — процессор намеренно работает на этом пределе для максимальной частоты
- iGPU: RDNA 2, 2 CU, 2200 MHz — базовый вывод
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel, native DDR5-5600 (против 5200 у Zen 4)
- PCIe: 5.0, 28 линий (24 usable)
- Поддержка AVX-512: да (полноценная, не dual-pumped как у Zen 4)
- Разблокированный множитель: да

## Производительность

### DAWBench DSP (Reaper, 96 kHz, 64-sample buffer)

- 9950X: ~520 RXC instances — **абсолютный рекорд среди потребительских CPU**
- Core Ultra 9 285K: ~440 RXC (9950X **+18%**)
- 7950X: ~470 RXC (9950X **+11%**)
- i9-14900K: ~430 RXC (+21%)

### Cinebench R23

- Single-core: ~2 150 баллов
- Multi-core (stock 170W): ~42 000 баллов
- Multi-core (PBO): ~44 000–46 000 баллов

### Cinebench 2024

- Single-core: ~135 баллов
- Multi-core (stock): ~2 300 баллов

### Рабочие нагрузки

- Blender Classroom: ~220 секунд (7950X: ~250 сек, **+12%**)
- 7-Zip Compression: ~195 000 MIPS
- V-Ray Benchmark: ~28 000 баллов
- Компиляция Linux Kernel (defconfig): ~28 секунд
- AI Inference (LLaMA 7B Q4_K_M, CPU-only): ~18 t/s (AVX-512)

### Игры (1440p)

В играх 9950X уступает однокристальным процессорам и X3D-моделям из-за dual-CCD latency:

- Cyberpunk 2077: ~140 fps (9800X3D: ~175 fps, −20%)
- CS2: ~520 fps (9800X3D: ~720 fps, −28%)
- Baldur's Gate 3: ~170 fps (9800X3D: ~210 fps, −19%)

**Для игр 9950X избыточен.** Если нужен компромисс «игры + работа» — 9950X3D.

## Сравнение с Ryzen 9 7950X

- Ядра/потоки: 16C/32T vs 16C/32T — одинаковое количество, +16% IPC у 9950X
- Техпроцесс: TSMC 4nm vs 5nm — лучше эффективность
- R23 multi: ~42 000 vs ~37 500 (+12% благодаря Zen 5 IPC)
- R23 single: ~2 150 vs ~2 000 (+7.5%)
- DAWBench DSP: +11% (преимущество Zen 5 IPC)
- Память: DDR5-5600 native vs DDR5-5200
- AVX-512: полноценный vs dual-pumped (на ~56% выше пропускная способность)
- Потребление: 148W средний vs 170W+ (холоднее и эффективнее)
- **Вывод:** 9950X выигрывает в многопотоке за счёт Zen 5 IPC и более высоких частот. Для любых задач — рендеринга, DAW, компиляции — 9950X быстрее и холоднее. 7950X остаётся актуальным только при ограниченном бюджете на вторичном рынке.

## Сравнение с Intel Core i9-14900K

- Ядра/потоки: 16C/32T Zen 5 vs 24C/32T (8P+16E) Raptor Lake
- R23 multi: ~42 000 vs ~40 000 (+5%)
- R23 single: ~2 150 vs ~2 300 (−7%)
- DAWBench DSP: +21% (преимущество Zen 5 AVX-512 и DPC latency)
- Потребление (R23 multi): 170W vs 300W+ (−43%!)
- AVX-512: есть vs нет
- Платформа: AM5 (живая до Zen 6) vs LGA1700 (тупиковая)
- Стабильность: без проблем vs известная деградация Raptor Lake

**Вывод:** 9950X быстрее в Cinebench multi при вдвое меньшем энергопотреблении и значительно превосходит в DAW. 9950X — более рациональный и холодный выбор для профессионалов на живой платформе.

## Охлаждение

170W TDP / 230W PPT — требования как у 7950X. 9950X спроектирован для работы при 95°C:

- **Минимум (будет throttling):** Arctic Liquid Freezer III 280 — температуры 90–95°C, частоты ~4.4–4.6 GHz
- **Рекомендуется:** Arctic Liquid Freezer III 360 / Deepcool LT720 — температуры 85–92°C, частоты ~4.6–4.8 GHz
- **Оптимально:** Кастомная СВО с радиатором 360+ мм — температуры 75–85°C, максимальные частоты
- **Воздух не рекомендуется:** даже NH-D15 будет на пределе с пониженными частотами

**Важно:** 95°C для 9950X — **штатный режим**, не баг. Процессор использует термобюджет полностью.

### Eco Mode

- **Eco 105W:** ~33 000 R23 multi, температуры ~65–75°C, можно воздухом
- **Eco 65W:** ~25 000 R23 multi, температуры ~55–65°C, практически бесшумен

Eco 105W сохраняет ~78% многопоточной производительности при кардинально меньших требованиях к охлаждению.

## Память

DDR5 only. Zen 5 IMC улучшен относительно Zen 4:

- **DDR5-6000 CL30** — золотой стандарт для 1:1 (гарантирован на Zen 5)
- **DDR5-6400 CL32** — доступно на многих экземплярах в 1:1
- **4 планки:** частота падает до DDR5-5200–5600. Для большого объёма лучше 2×48 GB (96 GB total) на DDR5-6000

Для DAW-станций: объём памяти критичнее частоты. 96 GB DDR5-5200 для крупных проектов > 32 GB DDR5-6000.

## Для кого

**Идеален:**
- **Профессиональная работа со звуком (DAW)** — лучший CPU для микширования 500+ треков, минимальная DPC latency, AVX-512 для DSP-плагинов
- **Рендеринг и 3D** (Blender, V-Ray, Cinema 4D) — 32 потока Zen 5 с AVX-512
- **Компиляция больших проектов** (AOSP, Chromium, Unreal Engine)
- **AI/ML инференс на CPU** — AVX-512 даёт ×1.5–2 ускорение относительно FP32
- **Data Engineering** (ETL, Spark, базы данных) — 32 потока для параллельных пайплайнов
- **Научные расчёты** (CFD, FEA, MATLAB) — полноценный AVX-512

**Не подходит:**
- **SFF-сборки** — 170W TDP несовместим с компактными корпусами без серьёзного throttling'а
- **Тихие сборки** — 170W требует активного охлаждения с неизбежным шумом
- **Игровые сборки** — берите 9800X3D. 9950X медленнее в играх и значительно горячее
- **Бюджетные сборки** — высокая цена CPU + дорогая материнская плата + дорогое охлаждение
- **Домашний сервер 24/7** — 170W TDP в простое неоправдан; лучше 7900 (65W) или 9700X (65W)

## Связки

**Профессиональная DAW-станция:**
- MB: ASRock X670E Taichi / GIGABYTE X670E AORUS Master (стабильный VRM, минимум DPC latency)
- Кулер: Arctic Liquid Freezer III 360
- RAM: 64–96 GB DDR5-5600 (стабильность > частота)
- GPU: RTX 4060 (пассивный режим при низкой нагрузке — тишина в студии)
- Блок питания: 850W+ (с запасом для transient)
- Корпус: Fractal Design Define 7 (шумоподавление)

**Рабочая станция (рендеринг/компиляция):**
- MB: GIGABYTE X670E AORUS Master
- Кулер: Arctic Liquid Freezer III 360 / Deepcool LT720
- RAM: 64–128 GB DDR5-5600
- GPU: RTX 4090/5090 (для GPU-рендеринга)
- Блок питания: 1000W+

**Компромиссная (Eco Mode 105W):**
- MB: MSI B650 Tomahawk Wi-Fi
- Кулер: Thermalright Peerless Assassin 120
- RAM: 64 GB DDR5-6000 CL30
- Производительность: ~78% от стока, тихо и холодно

## Российский рынок

- Статус: **draft** — цены актуализированы 2026-06-07
- Доступность: стабильная (3+ магазинов на price.ru)
- Диапазон цен: 36 750 – 43 650 ₽ (медиана 40 425 ₽)
- Конкуренты: Intel Core i9-14900K (LGA1700), Core Ultra 9 285K (LGA1851)

## Источники

1. AMD Zen 5 Product Specifications (amd.com)
2. Puget Systems — Ryzen 9 9950X for Content Creation (2024)
3. Scan Pro Audio — DAWBench DSP Results (2025)
4. Gamers Nexus — Ryzen 9 9950X Review & Benchmarks (2024)
5. TechPowerUp — Ryzen 9 9950X Review (2024)
6. price.ru — мониторинг цен (2026-06-07)
