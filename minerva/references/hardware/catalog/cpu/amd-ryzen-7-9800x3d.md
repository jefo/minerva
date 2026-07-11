---
id: amd-ryzen-7-9800x3d
type: cpu
title: AMD Ryzen 7 9800X3D (Zen 5, 3D V-Cache 2G, 120W)
vendor: amd
status: draft
tags:
- amd
- zen5
- am5
- ddr5
- 3d-v-cache
- 120w
- 8-core
- x3d
last_updated: '2026-06-03'
external_audit_verification: planned
links:
  platform: catalog/motherboard/am5/index.md
  memory_type: catalog/memory/ddr5.md
  family: catalog/cpu/amd-ryzen-9000.md
  prev_gen: catalog/cpu/amd-ryzen-7-7800x3d.md
  competitor_intel: catalog/cpu/intel-core-ultra-9-285k.md
  concepts:
  - concepts/power-budget.md
  - concepts/3d-v-cache.md
specs:
  socket: AM5 (LGA1718)
  architecture: Zen 5 (Granite Ridge) + 3D V-Cache 2-го поколения
  lithography: TSMC 4nm (CCD) + 6nm (IOD), 3D V-Cache 2G
  cores: 8
  threads: 16
  base_clock: 4.7 GHz
  boost_clock: 5.2 GHz
  l2_cache: 8 MB (1 MB × 8)
  l3_cache: 96 MB (32 MB on-die + 64 MB 3D V-Cache 2G)
  tdp: 120W
  ppt: 162W (default)
  tjmax: "95°C (равен non-X3D Zen 5)"
  pcie_lanes: 28 (24 usable), PCIe 5.0
  memory: DDR5 only, dual-channel, до 5600 JEDEC / 6000+ EXPO
  max_memory: 128 GB (4×32 GB или 2×48 GB)
  igpu: RDNA 2 (2 CUs, 2200 MHz, базовый вывод)
  box_cooler: null
  package: Retail (BOX, без кулера)
  release_date: Q4 2024
  multiplier: "unlocked"
  multiplier_source: "https://www.amd.com/en/products/processors/desktops/ryzen.html"
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
verdict: 'Абсолютный игровой бог. Zen 5 + 3D V-Cache 2-го поколения: 96 MB L3 + повышенные
  частоты (5.2 GHz против 5.0 у 7800X3D). Лучший игровой процессор на планете. Прямой
  наследник легендарного 7800X3D — быстрее, холоднее (3D V-Cache под CCD!), без частотных
  компромиссов. Цена высокая — это флагманский геймерский CPU, и он этого стоит.'
price_ru:
  min: 55000
  median: 62000
  max: 70000
  source: price.ru
  date: '2026-06-04'
---

# AMD Ryzen 7 9800X3D (Zen 5, 3D V-Cache 2G, 120W)

## Позиционирование

Ryzen 7 9800X3D — это то, чего ждали все. Второе поколение 3D V-Cache на архитектуре Zen 5. AMD исправила главный недостаток 7800X3D: **кэш-кристалл теперь расположен ПОД CCD**, а не над ним. Это означает:

- **Лучший теплоотвод** — тепло от CCD напрямую уходит в крышку, не проходя через кэш-кристалл
- **Повышенные частоты** — 4.7/5.2 GHz против 4.2/5.0 GHz у 7800X3D
- **TJmax 95°C** — равен non-X3D Zen 5, инвертированный стек 2G снял ограничение первого поколения

9800X3D — **лучший игровой процессор на планете** по состоянию на 2024–2025 гг. Zen 5 даёт +15% IPC над Zen 4, 3D V-Cache добавляет 64 MB L3, а новое расположение кристаллов убирает частотный штраф. Результат: 7800X3D был королём, 9800X3D — бог.

Единственный недостаток — цена. Это флагманский продукт для энтузиастов, готовых платить за лучший игровой опыт.

## Характеристики

- Архитектура: Zen 5 (Granite Ridge) + 3D V-Cache 2-го поколения
- Техпроцесс: TSMC 4nm (CCD) + 6nm (IOD)
- **Ключевое отличие от 7800X3D:** 3D V-Cache расположен ПОД CCD (а не над ним) — прямой контакт CCD с теплораспределительной крышкой
- Сокет: AM5 (LGA1718)
- Ядер / потоков: 8C/16T
- Базовая частота: 4.7 GHz — **значительно выше** 4.2 GHz у 7800X3D (+500 MHz!)
- Boost: 5.2 GHz — выше 5.0 GHz у 7800X3D (+200 MHz)
- All-core нагрузка: ~5.0–5.1 GHz
- L2-кэш: 8 MB (1 MB × 8)
- L3-кэш: **96 MB** — 32 MB on-die + 64 MB 3D V-Cache 2G
- TDP / PPT: 120W / 162W
- TJmax: 95°C — инвертированный стек 2G позволил поднять лимит до уровня non-X3D Zen 5
- iGPU: RDNA 2, 2 CU, 2200 MHz
- Кулер в коробке: отсутствует
- Память: DDR5 only, dual-channel; JEDEC до 5600
- PCIe: 5.0 (×16 или 2×8 от CPU)

## Производительность в играх

9800X3D не просто быстрее 7800X3D — он быстрее всего, что существует на рынке. Zen 5 IPC + 3D V-Cache 2G + повышенные частоты = абсолютная гегемония в играх:

### Киберспорт (1080p, RTX 4090)
- CS2: ~750 fps (7800X3D: ~680 fps, **+10%**) — 7700X: ~535 fps
- Valorant: ~890 fps (7800X3D: ~820 fps, **+9%**)
- Rainbow Six Siege: ~800 fps (7800X3D: ~730 fps, **+10%**)
- Fortnite: ~460 fps (7800X3D: ~420 fps, **+10%**)

### AAA-игры (1440p)
- Cyberpunk 2077: ~170 fps (7800X3D: ~158 fps, +8%)
- Baldur's Gate 3: ~210 fps (7800X3D: ~195 fps, +8%)
- Hogwarts Legacy: ~142 fps (7800X3D: ~132 fps, +8%)

### Симуляторы / стратегии (колоссальный прирост)
- Factorio (мегабаза): ~210 UPS (7800X3D: ~190 UPS, +11%)
- Stellaris (late-game): ~80 fps (7800X3D: ~72 fps, +11%)
- MSFS 2024: ~98 fps (7800X3D: ~88 fps, +11%)
- Civilization VII (late-game turn): на 35–45% быстрее 7700X

### Резюме
9800X3D быстрее 7800X3D на 8–12% в играх. Быстрее Intel Core Ultra 9 285K на 15–25%. Это безоговорочно лучший игровой процессор в мире.

## Производительность в рабочих задачах

Благодаря повышенным частотам, 9800X3D сократил отставание от не-X3D процессоров в работе:

- Cinebench R23 multi: ~20 500 (7800X3D: ~18 000, **+14%**)
- Cinebench R23 single: ~2 050 (7800X3D: ~1 820, **+13%**)
- Компиляция: на 12–15% быстрее 7800X3D

Теперь 9800X3D не так сильно проигрывает в рабочих задачах. Он всё ещё уступает 9700X (non-X3D) в рендеринге на ~5–8%, но разрыв сократился вдвое относительно поколения Zen 4.

**Вывод:** 9800X3D — уже не «чисто игровой» процессор. Он вполне пригоден для рабочих нагрузок, хотя 9700X/9900X всё ещё быстрее в рендеринге.

## Охлаждение

3D V-Cache 2-го поколения — это революция в охлаждении X3D:

- Кэш-кристалл ПОД CCD: тепло от CCD идёт напрямую в крышку
- 120W TDP / 162W PPT — на бумаге как 7800X3D, но охлаждается значительно легче
- TJmax 95°C — равен 9700X, инвертированный стек снял ограничение Zen 4 X3D

Рекомендации:

- **Минимум:** Thermalright Peerless Assassin 120 — Cinebench ~72–78°C, игры ~55–65°C
- **Рекомендуется:** Arctic Liquid Freezer III 240 — Cinebench ~62–68°C, тихо
- **Оптимально:** Deepcool LT720 / Arctic Liquid Freezer III 360 — Cinebench ~55–62°C
- **В отличие от 7800X3D**, качественная башня (NH-D15) держит 9800X3D без проблем. AIO не строго обязателен.

## Память

Zen 5 + 3D V-Cache — память важна меньше, чем для обычных Zen 5, но контроллер улучшен:

- **DDR5-6000 CL30** — золотой стандарт, разницы с 6400 в играх почти нет (кэш маскирует latency)
- **DDR5-6400** — Zen 5 держит 1:1, но прирост над 6000 минимален из-за 3D V-Cache
- Не переплачивайте за память — 96 MB L3 делают latency ОЗУ практически нерелевантной

## Сравнение с 7800X3D (предыдущее поколение)

- Архитектура: Zen 5 vs Zen 4 (+15% IPC)
- Базовая частота: 4.7 vs 4.2 GHz (+500 MHz!)
- Boost: 5.2 vs 5.0 GHz (+200 MHz)
- All-core: ~5.05 vs ~4.85 GHz (+200 MHz)
- L3-кэш: 96 MB — идентично
- TDP: 120W — идентично
- Охлаждение: значительно легче (кэш под CCD)
- Игры: +8–12%
- Работа: +13–14% (значительное улучшение!)
- Цена: выше

**Вывод:** Если у вас 7800X3D — апгрейд на 9800X3D даст 8–12% в играх. Не обязательно, но если вы гонитесь за каждым FPS — оно того стоит. Если собираете с нуля — однозначно 9800X3D.

## Сравнение с Intel Core Ultra 9 285K

9800X3D быстрее флагмана Intel Arrow Lake в играх на 15–25%. При этом:

- Потребляет 60–85W в играх против 100–150W у 285K
- Не имеет проблем с планировщиком потоков (нет P/E-ядер)
- AM5 — живая платформа (Zen 6 впереди) vs LGA1851 (будущее неизвестно)
- 3D V-Cache даёт преимущество, которое архитектурой не компенсировать

285K быстрее в многопоточных рабочих нагрузках (24 ядра против 8), но для игр 9800X3D — однозначный победитель.

## Для кого

**Идеален:**
- **Киберспортсмены и хардкорные геймеры** — лучший FPS на планете
- **Игроки в стратегии/симуляторы** — 3D V-Cache даёт +30–45% к некоторым играм
- **Владельцы топ-видеокарт** (RTX 4090/5090) на 1080p/1440p — раскрытие потенциала GPU
- **Сборка мечты** без компромиссов — лучший игровой CPU, точка
- **Апгрейд с AM4** (Ryzen 5 5600X / 5800X3D) — переход на Zen 5 + 3D V-Cache 2G

**Не подходит:**
- **Бюджетные сборки** — цена высокая, 7500F/7600 дают 80% FPS за 30% цены
- **Рабочие станции** — 9700X/9900X/7950X быстрее в рендеринге и компиляции
- **Владельцы 7800X3D с ограниченным бюджетом** — прирост 8–12% не всегда оправдывает замену
- **SFF-сборки с плохой вентиляцией** — 120W всё ещё требует внимания к температурам
- **Геймеры на 4K** — при 4K разница между 9800X3D и 7600 минимальна, всё упирается в GPU

## Цена и ценность

9800X3D — дорогой процессор, флагманская цена. Но для геймера-энтузиаста это лучшая инвестиция в FPS:

- +8–12% над 7800X3D в играх
- +13–14% в рабочих задачах
- Лучшее охлаждение, выше частоты
- AM5 с перспективой Zen 6

Если бюджет позволяет — берите не думая. Если нет — 7800X3D всё ещё великолепен (и возможно, дешевле).

## Связки

**Киберспорт (максимальный FPS):**
- MB: ASRock X870E Taichi / GIGABYTE X870E AORUS Master
- Кулер: Arctic Liquid Freezer III 360
- RAM: 32 GB DDR5-6000 CL28
- GPU: RTX 5090

**Оптимальная игровая:**
- MB: MSI B650 Tomahawk Wi-Fi (да, B650 достаточно!)
- Кулер: Arctic Liquid Freezer III 240
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5080 / RX 9070 XT

**Прагматичная:**
- MB: ASRock B650E PG Riptide
- Кулер: Thermalright Peerless Assassin 120
- RAM: 32 GB DDR5-6000 CL30
- GPU: RTX 5070 Ti

## Российский рынок

- Статус: **draft** — цены будут добавлены после мониторинга
- Доступность: стабильная, высокий спрос
- Цена высокая — флагманский продукт
- Конкуренты: Intel Core Ultra 9 285K (LGA1851, проигрывает в играх), Ryzen 7 7800X3D (Zen 4, дешевле)

## Источники

1. AMD Zen 5 + 3D V-Cache 2nd Gen Technology Brief (amd.com, 2024)
2. Gamers Nexus — Ryzen 7 9800X3D Review & Benchmarks (2024)
3. Hardware Unboxed — 9800X3D Gaming Benchmark (2024)
4. TechPowerUp — Ryzen 7 9800X3D Review (2024)
5. Der8auer — 9800X3D Thermal Analysis & Delid (2024)
6. Level1Techs — Zen 5 X3D Deep Dive (2024)
