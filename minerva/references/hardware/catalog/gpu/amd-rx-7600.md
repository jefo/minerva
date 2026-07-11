---
id: "amd-rx-7600"
type: "gpu"
title: "AMD Radeon RX 7600 8GB"
vendor: "amd"
status: "verified"
price_ru:
  min: 25011
  median: 27500
  max: 29873
  source: "price.ru"
  date: "2026-06-03"
tags: ["amd", "rdna3", "navi33", "monolithic-die", "tsmc-n6", "128bit-narrow-bus", "8gb-vram-critical", "infinity-cache-32mb", "pcie4.0-x8", "raster-optimized", "rt-weak", "165w-tbp", "1x8pin-power", "amf-encoder", "1080p-only"]
last_updated: "2026-06-03"
links:
  competitor_nvidia: "catalog/gpu/nvidia-rtx-4060.md"
  predecessor: "catalog/gpu/amd-rx-6600.md"
  architecture: "catalog/gpu/amd-rx-7000.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "Navi 33 XL (RDNA 3)"
  lithography: "TSMC N6 (6nm)"
  stream_processors: 2048
  compute_units: 32
  ray_accelerators: 32
  ai_accelerators: 64
  boost_clock: "2.625 GHz (Game Clock ~2.25 GHz)"
  vram: "8 GB GDDR6 (128-bit)"
  vram_bandwidth: "288 GB/s"
  infinity_cache: "32 MB"
  tbp: "165W"
  power_connector: "1× 8-pin"
  pcie: "PCIe 4.0 x8"
  display_outputs: "3× DP 2.1, 1× HDMI 2.1"
  msrp_usd: "$269"
  engineering_notes: "Navi 33 — монолитный RDNA 3 на TSMC N6. 32 CU на 128-bit — сбалансировано под 1080p (32MB Infinity Cache даёт hit rate ~50%). На 1440p hit rate падает до 30%, bandwidth 288 GB/s — bottleneck. 8GB через 4×2GB — потолок 128-bit шины без clamshell. Карта спроектирована умереть в 1080p ровно когда 8GB перестанут быть достаточными."
profiles:
  balanced_performance_gpu:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Предсказуемое масштабирование производительности. Стандартные сборки ATX с БП 600–750W. Не требует специального охлаждения или инфраструктуры."
    failure_mode_desc: "Отсутствие специализации. Проигрывает enthusiast-картам в 4K, проигрывает low-power картам в SFF/тишине."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "streaming"]
    failure_for_intents: ["aaa_4k_path_tracing"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 25990
  median: 28000
  max: 32000
  source: "price.ru"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 8
  type: "GDDR6"
  bus_width_bit: 128
  bandwidth_gb_s: 288
clock_structured:
  boost_ghz: 2.625
  game_ghz: 2.25
cache:
  size_mb: 32
  type: "Infinity Cache"
compute:
  unit:
    type: "Stream Processor"
    count: 2048
  rt:
    type: "Ray Accelerator"
    count: 32
    generation: 2
  ml:
    type: "AI Accelerator"
    count: 64
    generation: 1
software:
  upscaler: "FSR 3"
  frame_gen: "AFMF"
  encoder: "AMF"
  compute_api: "ROCm"
  driver_features: ["SAM"]

verdict: "Лучший FPS/₽ в сегменте до 30k для киберспорта и нетребовательных игр на низких/средних. Проигрывает RTX 4060 в RT и DLSS, но выигрывает в чистом растре за меньшие деньги. 8GB VRAM — ахиллесова пята обеих карт."
---

# AMD Radeon RX 7600 8GB

## Архитектура и позиционирование

RX 7600 построена на GPU Navi 33 — самом младшем чипе RDNA 3, единственном в линейке на монолитной архитектуре (без чиплетов). Техпроцесс TSMC N6 (6nm) — зрелый и дешёвый, но не передовой 5nm как у старших Navi 31/32.

Позиционируется AMD как карта для 1080p-гейминга с прицелом на киберспорт и нетребовательные ААА-тайтлы. Прямой наследник RX 6600, но с заметным архитектурным скачком: RDNA 3 принёс выделенные AI-акселераторы (64 шт.) и улучшенные RT-ускорители второго поколения.

**Принципиальное отличие от старших RDNA 3:** Navi 33 — монолитный кристалл, тогда как Navi 31/32 используют чиплетную компоновку (GCD + MCD). Это исключает проблемы с latency Infinity Fabric, характерные для RX 7900-й серии.

## Характеристики

- **GPU:** Navi 33 XL (RDNA 3)
- **Техпроцесс:** TSMC N6 (6nm)
- **Потоковых процессоров:** 2048 (32 CU)
- **RT-ускорителей:** 32 (2-е поколение)
- **AI-ускорителей:** 64
- **Game Clock:** ~2.25 GHz
- **Boost Clock:** 2.625 GHz
- **VRAM:** 8 GB GDDR6
- **Шина:** 128-bit
- **Пропускная способность:** 288 GB/s
- **Infinity Cache:** 32 MB
- **TBP (Total Board Power):** 165W
- **Питание:** 1× 8-pin
- **PCIe:** 4.0 x8
- **Видеовыходы:** 3× DisplayPort 2.1, 1× HDMI 2.1
- **MSRP (USD):** $269

## PCIe 4.0 x8 — реальное влияние

RX 7600 использует только 8 линий PCIe 4.0 (как и RTX 4060). Это вызывает беспокойство у покупателей, но практическое влияние минимально:

- **На PCIe 4.0 x8:** пропускной способности 16 GB/s достаточно для 8GB VRAM — карта не упирается в лимит шины
- **На PCIe 3.0 x8 (старые платы B450/X470):** потеря 2–4% FPS — некритично
- **Реальный bottleneck:** не линии PCIe, а 8GB VRAM и 128-битная шина памяти

**Вывод:** 8 линий — маркетинговая экономия, но практического вреда при использовании карты по назначению (1080p) нет.

## Сравнение с RTX 4060 (Iron Man Argument)

### Где RX 7600 сильнее

- **Чистый растр (без RT, без апскейлеров):**
  - CS2: RX 7600 ~320 FPS vs RTX 4060 ~295 FPS (+8%)
  - Valorant: RX 7600 ~410 FPS vs RTX 4060 ~380 FPS (+8%)
  - Apex Legends: паритет (~190 FPS)
  - Cyberpunk 2077 (no RT, 1080p Ultra): RX 7600 ~78 FPS vs RTX 4060 ~74 FPS (+5%)

- **FPS/₽ для киберспорта (low/competitive settings):**
  - RX 7600 выдаёт больше кадров за меньшие деньги
  - При цене 28 000 ₽ против 32 000 ₽ у RTX 4060 — выигрыш ~14% по деньгам

- **Цена:** медиана 28 000 ₽ vs 32 000 ₽ — экономия 4 000 ₽, которые можно пустить в DDR5-6000 CL30 вместо DDR5-5600 CL36

### Где RX 7600 слабее

- **Трассировка лучей (RT):**
  - Cyberpunk 2077 RT Ultra 1080p: RX 7600 ~32 FPS vs RTX 4060 ~48 FPS (−33%)
  - RT-ускорители RDNA 3 улучшены относительно RDNA 2, но всё ещё отстают от ядер RT 3-го поколения Ada Lovelace
  - Без апскейлинга RT на RX 7600 — компромисс, а не фича

- **Апскейлинг и генерация кадров:**
  - FSR 3.1 — достойный конкурент DLSS 2, но заметно хуже DLSS 3.5 по качеству картинки (артефакты на мелких деталях, частицы, ghosting)
  - AMD Fluid Motion Frames (AFMF) — драйверный frame generation, работает в любой игре, но качество ниже аппаратного FG у NVIDIA
  - DLSS 3.5 + Frame Generation — объективно лучший стек для AAA с RT

- **Энергоэффективность:**
  - RX 7600: 165W TBP
  - RTX 4060: 115W TGP (−30%)
  - В простое разница меньше, но под нагрузкой RTX 4060 холоднее и тише

- **Драйверы:**
  - AMD Adrenalin сильно эволюционировал с 2022 года — стабильность на уровне
  - Но: occasional микростаттеры в DX11-играх (CS2 на некоторых конфигурациях, старые MMO)
  - NVIDIA Reflex — объективно лучшая система снижения задержки, прямого аналога у AMD нет (Anti-Lag 2 близок, но не идентичен)

### Объективный вердикт

- **Киберспорт, шутеры, нетребовательные игры → RX 7600.** Больше FPS, меньше денег. FSR 3.1 достаточно.
- **AAA с RT, DLSS-зависимые тайтлы, стриминг (NVENC) → RTX 4060.** DLSS 3.5, лучший RT, энергоэффективность.
- **Обе карты ограничены 8GB VRAM** — это главная проблема сегмента, а не вендор.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 25 990–32 000 ₽
- **Медиана:** ~28 000 ₽
- **Типичные модели:** Sapphire Pulse, Gigabyte Gaming OC, ASRock Challenger, PowerColor Fighter

Рекомендация: Sapphire Pulse или PowerColor Fighter по 27 000–28 000 ₽ — лучшие варианты. Gigabyte Gaming OC переоценён для карты такого класса.

## Для кого

**Подходит:**
- Киберспортсмены (CS2, Valorant, Apex, Overwatch) — максимальный FPS в 1080p на low/competitive
- Бюджетные игровые сборки до 80 000 ₽
- 1080p-гейминг на высоких настройках в большинстве ААА (без RT)
- Апгрейд с RX 580 / GTX 1060 / GTX 1660

**Не подходит:**
- Игры с трассировкой лучей как основным приоритетом (Cyberpunk RT, Alan Wake 2, Black Myth: Wukong)
- 1440p-гейминг (8GB VRAM и 128-bit шина — бутылочное горлышко)
- Стриминг с кодированием на GPU (NVENC у NVIDIA объективно лучше AMF)
- Работа с CUDA (выбор только в пользу NVIDIA)
- Сборки где важна тишина и холод (115W у RTX 4060 — преимущество)

## Источники

1. TechSpot / Hardware Unboxed — «AMD Radeon RX 7600 Review» (май 2023)
2. Gamers Nexus — «RX 7600 vs RTX 4060 Benchmark» (июнь 2023)
3. ComputerBase.de — «RX 7600 im Test: RDNA 3 für 269 Dollar»
4. Price.ru — рыночные цены, Москва (03.06.2026)
5. AMD RDNA 3 Architectural Deep Dive (GPUOpen)
6. Собственное тестирование лаборатории в сборке EST-2026-0422-K1
