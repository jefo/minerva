---
id: amd-ryzen-7-7800x3d
type: cpu
title: AMD Ryzen 7 7800X3D (Zen 4, 3D V-Cache, 120W)
vendor: amd
status: draft
tags:
- amd
- zen4
- am5
- ddr5
- 3d-v-cache
- 120w
- 8-core
- x3d
last_updated: '2026-06-03'
external_audit_verification: passed
cpu_expert_verified: '2026-06-28'
cpu_expert_sources:
  - amd.com/en/products/processors/desktops/ryzen/7000-series/amd-ryzen-7-7800x3d
  - techpowerup.com/cpu-specs/ryzen-7-7800x3d.c3022
cpu_expert_result: 18/18 specs verified, 0 errors
links:
  platform: catalog/motherboard/am5/index.md
  memory_type: catalog/memory/ddr5.md
  family: catalog/cpu/amd-ryzen-7000.md
  down_variant: catalog/cpu/amd-ryzen-7-7700x.md
  next_gen: catalog/cpu/amd-ryzen-7-9800x3d.md
  competitor_intel: catalog/cpu/intel-core-14900k.md
  concepts:
  - concepts/power-budget.md
  - concepts/3d-v-cache.md
specs:
  socket: AM5 (LGA1718)
  architecture: Zen 4 (Raphael) + 3D V-Cache
  lithography: TSMC 5nm (CCD) + 6nm (IOD), 3D V-Cache на отдельном кристалле
  cores: 8
  threads: 16
  base_clock: 4.2 GHz
  boost_clock: 5.0 GHz
  l2_cache: 8 MB (1 MB × 8)
  l3_cache: 96 MB (32 MB on-die + 64 MB 3D V-Cache)
  tdp: 120W
  ppt: 162W (default)
  tjmax: 89°C (снижен из-за 3D V-Cache)
  pcie_lanes: 28 (24 usable), PCIe 5.0
  memory: DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO
  max_memory: 128 GB (4×32 GB или 2×48 GB)
  igpu: RDNA 2 (2 CUs, 2200 MHz, базовый вывод)
  box_cooler: null
  package: Retail (BOX, без кулера)
  release_date: Q2 2023
  multiplier: "locked"
  multiplier_source: "https://www.techpowerup.com/cpu-specs/ryzen-7-7800x3d.c3022"
profiles:
  cache_dominant_gaming:
    power_envelope: high
    capability_level: 3
    steel_man_desc: Киберспорт 1080p на низких. 3D V-Cache (L3 ≥ 96MB) — 1% Low FPS
      стабильно выше 240/360 Hz.
    failure_mode_desc: 'Тяжёлые FP32/AVX-512: рендеринг, компиляция. Тепловое сопротивление
      3D-кэша снижает частоту на 300–500 МГц. Штраф 15–20%.'
    optimal_for_intents:
    - esports_1080p_240hz
    - esports_1080p_360hz
    failure_for_intents:
    - 3d_rendering_cpu
    - heavy_compilation
    - scientific_computing
    failure_severity: WARN
    failure_type: LINEAR_DEGRADATION
  dense_thermal_concentration:
    power_envelope: high
    capability_level: 2
    steel_man_desc: 'Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту
      до того как тепло преодолеет IHS. Максимальный буст на 2–3 секунды.'
    failure_mode_desc: Длительная нагрузка. Тепловое сопротивление толстой IHS (≥
      1.7 мм, AM5) → 89°C (TJmax) даже под СЖО. Thermal throttling 5–8%.
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
verdict: Лучший игровой процессор на планете для рациональных геймеров. 96 MB L3-кэша
  через 3D V-Cache дают +15–30% FPS в играх относительно 7700X. Киберспортсмены —
  это ваш процессор. Цена высокая, но оправдана. TJmax 89°C — требуется хорошее охлаждение.
price_ru:
  min: 42000
  median: 48000
  max: 55000
  source: price.ru
  date: '2026-06-04'
---

# AMD Ryzen 7 7800X3D — КИБЕРСПОРТ КОРОЛЬ

## Позиционирование

Ryzen 7 7800X3D — уникальный процессор: 8 ядер Zen 4 с технологией 3D V-Cache, добавляющей 64 MB L3-кэша поверх стандартных 32 MB — итого 96 MB. Этот дополнительный кэш радикально снижает latency при доступе к памяти и даёт колоссальный прирост FPS в играх, особенно в киберспортивных тайтлах (CS2, Valorant, Rainbow Six Siege), стратегиях (Factorio, Stellaris, Civilization) и симуляторах (MSFS 2024, Assetto Corsa).

7800X3D — **лучший игровой процессор на планете** на момент выхода (2023) среди рациональных вариантов. Он быстрее Intel Core i9-14900K в играх, потребляя при этом в 2–3 раза меньше энергии. Единственный компромисс: сниженные базовые частоты (4.2 vs 4.5 GHz у 7700X) и пониженный TJmax (89°C) из-за теплоизолирующего эффекта кэш-кристалла над CCD.

Если ваша главная задача — выжать максимум FPS без оглядки на рабочие нагрузки, 7800X3D — безальтернативный выбор на AM5 до выхода Zen 5 X3D.

## Характеристики

- Архитектура: Zen 4 (Raphael) + 3D V-Cache (дополнительный кристалл кэша поверх CCD)
- Техпроцесс: TSMC 5nm (CCD) + 6nm (IOD), кэш-кристалл — 7nm
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 8C/16T
- Базовая частота: 4.2 GHz — снижена относительно 7700X (4.5) из-за тепловых ограничений 3D V-Cache
- Boost: 5.0 GHz — снижен относительно 7700X (5.4) по той же причине
- All-core нагрузка: ~4.8–4.9 GHz
- L2-кэш: 8 MB (1 MB × 8)
- L3-кэш: **96 MB** — 32 MB on-die + 64 MB 3D V-Cache
- TDP / PPT: 120W / 162W
- TJmax: **89°C** — снижен из-за чувствительности 3D V-Cache к температуре
- iGPU: RDNA 2, 2 CU, 2200 MHz
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel
- PCIe: 5.0 (×16 или 2×8 от CPU)

## Производительность в играх

96 MB L3-кэша делают этот процессор абсолютным королём игровой производительности. Игры, чувствительные к latency памяти, получают колоссальный прирост:

### Киберспорт (1080p, RTX 4090)
- CS2: ~680 fps (7700X: ~535 fps, **+27%**)
- Valorant: ~820 fps (7700X: ~620 fps, **+32%**)
- Rainbow Six Siege: ~730 fps (7700X: ~560 fps, **+30%**)
- Fortnite: ~420 fps (7700X: ~350 fps, **+20%**)

### AAA-игры (1440p)
- Cyberpunk 2077: ~158 fps (7700X: ~144 fps, +10%)
- Baldur's Gate 3: ~195 fps (7700X: ~171 fps, +14%)
- Hogwarts Legacy: ~132 fps (7700X: ~118 fps, +12%)

### Симуляторы / стратегии (самый большой прирост)
- Factorio (мегабаза): ~190 UPS (7700X: ~130 UPS, **+46%**)
- Stellaris (late-game): ~72 fps (7700X: ~52 fps, **+38%**)
- MSFS 2024: ~88 fps (7700X: ~68 fps, **+29%**)
- Civilization VII (late-game turn): на 30–40% быстрее

## Производительность в рабочих задачах

В неигровых нагрузках 7800X3D уступает 7700X из-за сниженных частот:

- Cinebench R23 multi: ~18 000 (7700X: ~19 700, −9%)
- Cinebench R23 single: ~1 820 (7700X: ~1 960, −7%)
- Компиляция, рендеринг: на 8–10% медленнее 7700X

**Вывод:** 7800X3D — чисто игровой инструмент. Для смешанных нагрузок (игры + работа) — 7950X3D или 7700X.

## Охлаждение

3D V-Cache создаёт термическое сопротивление: кэш-кристалл находится между CCD и крышкой, затрудняя теплоотвод. Это означает:

- **TJmax снижен до 89°C** — throttling наступает раньше
- **120W TDP / 162W PPT** — на бумаге выше 7700X (105W TDP / 142W PPT), но охлаждать сложнее из-за термосопротивления
- **Требуется качественное охлаждение** — башенный кулер минимум, желательно AIO

Рекомендации:

- **Минимум (на грани):** Thermalright Peerless Assassin 120 — Cinebench ~80–85°C, близко к TJmax
- **Рекомендуется:** Deepcool AK620 / Noctua NH-D15 — Cinebench ~72–78°C
- **Оптимально:** Arctic Liquid Freezer III 240/280 — Cinebench ~62–68°C, тихо и стабильно
- **Не пытайтесь использовать Wraith Prism** — мгновенный throttling

## Память

DDR5 only. 7800X3D менее чувствителен к частоте памяти, чем обычные Zen 4 — огромный L3-кэш маскирует latency оперативной памяти:

- DDR5-6000 CL30 vs DDR5-5200 JEDEC: разница в играх всего 3–5% (против 8–12% у 7700X)
- Оптимально: DDR5-6000 CL30 — всё равно золотой стандарт
- Не переплачивайте за DDR5-6400+ — прирост минимален

## Сравнение с Intel Core i9-14900K

7800X3D быстрее 14900K в играх в среднем на 5–10%, при этом:

- Потребляет 60–80W в играх против 120–180W у 14900K
- Не требует AIO на 360 мм
- Не деградирует (проблемы Raptor Lake с напряжением)
- AM5 — живая платформа с апгрейдом до Zen 5/6
- LGA1700 — тупиковая

Единственное преимущество 14900K — многопоточная производительность (24 ядра vs 8).

## Для кого

**Идеален:**
- Киберспортсмены и геймеры, для которых важен каждый FPS
- Игроки в стратегии / симуляторы (Stellaris, Factorio, MSFS) — прирост до 40%+
- Сборки с топ-видеокартами (RTX 4090/5080) на 1080p/1440p
- Геймеры, которые не занимаются рабочими нагрузками на CPU
- Апгрейд с AM4 (Ryzen 5 5600X / 5800X3D): радикальный прирост FPS

**Не подходит:**
- Рабочие станции — 7700X/7900X быстрее в рендеринге и компиляции
- Бюджетные сборки — процессор дорогой, кулер тоже нужен хороший
- Тихие сборки без мощного охлаждения — 89°C TJmax требует внимания к температурам
- Смешанные сценарии (игры + стриминг + работа) — смотрите 7950X3D

## Связки

**Киберспорт (оптимально):**
- MB: MSI B650 Tomahawk Wi-Fi / ASRock B650E PG Riptide
- Кулер: Arctic Liquid Freezer III 240
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5070 Ti / RX 9070 XT

**Максимальный FPS:**
- MB: ASRock X670E Taichi / GIGABYTE X670E AORUS Master
- Кулер: Arctic Liquid Freezer III 360
- RAM: 32 GB DDR5-6000 CL28
- GPU: RTX 5090

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная, высокий спрос
- Цена высокая — сравнима с топовыми Intel Core i9
- Конкуренты: Intel Core i9-14900K (LGA1700, быстрее в работе, но горячее и тупиковая платформа)

## Цена и ценность

7800X3D — дорогой процессор. Но для геймера, который хочет лучший игровой CPU без компромиссов по энергопотреблению и нагреву, это инвестиция, которая окупается годами. AM5 будет поддерживать Zen 5 и Zen 6 — платформа не тупиковая.

## Источники

1. AMD 3D V-Cache Technology Brief (amd.com, 2023)
2. Gamers Nexus — Ryzen 7 7800X3D Review & Benchmarks (2023)
3. Hardware Unboxed — 7800X3D vs 14900K Gaming Benchmark (2024)
4. TechPowerUp — Ryzen 7 7800X3D Review (2023)
5. Der8auer — 7800X3D Delid & Thermal Analysis (2023)

observations:
  # === Сравнение с i5-14600K + RTX 5070 в 1440p ===
  - id: "obs-7800x3d-001"
    source_id: "agg"
    source_confidence: 0.90
    observation_quality: 0.88
    cpu: "amd-ryzen-7-7800x3d"
    comparison_cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 89
    p1_fps: 64
    competitor_avg_fps: 87
    competitor_p1_fps: 62
    fps_delta: "+2 FPS над i5-14600K (2.3%)"
    price_delta: "+18K₽ (40K vs 22K)"
    gpu_utilization: 98
    notes: "3D V-Cache даёт +2% в 1440p GPU-bound. Ценовая премия не окупается FPS-приростом в этом разрешении."

  # === 1080p — где 7800X3D раскрывается ===
  - id: "obs-7800x3d-002"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    cpu: "amd-ryzen-7-7800x3d"
    comparison_cpu: "intel-core-i5-14600k"
    gpu: "nvidia-rtx-5070"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "1920x1080"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 128
    p1_fps: 95
    competitor_avg_fps: 112
    competitor_p1_fps: 82
    fps_delta: "+16 FPS над i5-14600K (14.3%)"
    gpu_utilization: 85
    notes: "1080p: 3D V-Cache даёт значимое преимущество. Разница видна когда GPU не saturated."
