---
id: "nvidia-rtx-4060"
type: "gpu"
title: "NVIDIA GeForce RTX 4060 8GB"
vendor: "nvidia"
status: "verified"
price_ru:
  min: 29000
  median: 32000
  max: 36000
  source: "price.ru (оценка по рынку)"
  date: "2026-06-03"
tags: ["nvidia", "ada-lovelace", "ad107", "tsmc-4n", "128bit-narrow-bus", "8gb-vram-critical", "24mb-l2-cache", "pcie4.0-x8", "dlss3.5", "rt-3rd-gen", "115w-tgp-silent", "1x8pin-power", "nvenc-8th-gen", "cuda-ecosystem", "1080p-only", "rt-leader-budget", "silent-viable"]
last_updated: "2026-06-03"
links:
  competitor_amd: "catalog/gpu/amd-rx-7600.md"
  predecessor: "catalog/gpu/nvidia-rtx-3060.md"
  architecture: "catalog/gpu/nvidia-rtx-4000.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "AD107 (Ada Lovelace)"
  lithography: "TSMC 4N (5nm)"
  cuda_cores: 3072
  tensor_cores: "96 (4-е поколение)"
  rt_cores: "24 (3-е поколение)"
  boost_clock: "2.46 GHz"
  vram: "8 GB GDDR6 (128-bit)"
  vram_bandwidth: "272 GB/s"
  l2_cache: "24 MB"
  tgp: "115W"
  power_connector: "1× 8-pin (многие AIB — 1× 6-pin)"
  pcie: "PCIe 4.0 x8"
  display_outputs: "3× DP 1.4a, 1× HDMI 2.1"
  msrp_usd: "$299"
  engineering_notes: "AD107 на TSMC 4N. 24MB L2-кэша (8× больше RTX 3060) — компенсирует 128-bit шину через hit rate ~50% в 1080p. Работает блестяще в 1080p, на 1440p hit rate падает — 272 GB/s bottleneck. 115W TGP — архитектурный шедевр энергоэффективности. 8GB VRAM — осознанный компромисс: карта умрёт по памяти раньше чем по compute. RT-ядра 3-го поколения + DLSS 3.5 — безальтернативна для RT в бюджете."
profiles:
  mainstream_efficiency_gpu:
    power_envelope: "low"
    capability_level: 1
    steel_man_desc: "Массовые игровые ПК: 1080p/1440p. БП 450–550W. Минимальные требования к вентиляции, низкий шум, SFF-совместимость."
    failure_mode_desc: "Нативный 4K-гейминг. Недостаток вычислительных блоков не позволяет 60 FPS — снижение до Medium/Low."
    optimal_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "silent_build", "sff_build", "office_productivity"]
    failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing"]
    failure_severity: "BLOCK"
    failure_type: "LINEAR_DEGRADATION"
  hardware_rt_accelerated_gen_3:
    steel_man_desc: "Path Tracing в реальном времени. Аппаратное ускорение ×4–5 vs растеризация."
    failure_mode_desc: "DX11/OpenGL игры. RT-блоки простаивают — dark silicon."
    optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  tensor_matrix_accelerated:
    steel_man_desc: "Локальное обучение/инференс нейросетей, Stable Diffusion, DLSS/XeSS."
    failure_mode_desc: "Традиционные FP32-вычисления. Тензорные блоки простаивают — паразитный нагрев."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 29990
  median: 32000
  max: 38000
  source: "price.ru"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 8
  type: "GDDR6"
  bus_width_bit: 128
  bandwidth_gb_s: 272
clock_structured:
  boost_ghz: 2.46
  game_ghz: null
cache:
  size_mb: 24
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 3072
  rt:
    type: "RT Core"
    count: 24
    generation: 3
  ml:
    type: "Tensor Core"
    count: 96
    generation: 4
software:
  upscaler: "DLSS 3.5"
  frame_gen: "FG"
  encoder: "NVENC 8th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

verdict: "Лучшая карта в сегменте для AAA с трассировкой лучей благодаря DLSS 3.5 и энергоэффективности Ada Lovelace. Но 128-битная шина и 8GB VRAM — осознанное ограничение NVIDIA. Для чистого растра RX 7600 даёт больше FPS дешевле."
---

# NVIDIA GeForce RTX 4060 8GB

## Архитектура и позиционирование

RTX 4060 построена на GPU AD107 — самом младшем чипе архитектуры Ada Lovelace. Техпроцесс TSMC 4N (оптимизированный 5nm) — тот же, что и у всей RTX 40-й серии. Это приносит карте ключевое преимущество: исключительную энергоэффективность при 115W TGP.

Позиционируется NVIDIA как карта для 1080p с RT и DLSS 3. Главный маркетинговый посыл: «RT + Frame Generation за $299». Однако инженерные решения — 128-битная шина, 8GB VRAM, x8 PCIe — вызвали критику со стороны сообщества.

**Ключевая особенность AD107:** 24 MB L2-кэша (против 3 MB у RTX 3060). Большой кэш частично компенсирует узкую шину памяти — хитрейт в Ada Lovelace достигает ~50%, тогда как у Ampere было ~30%.

## Характеристики

- **GPU:** AD107-400 (Ada Lovelace)
- **Техпроцесс:** TSMC 4N (5nm)
- **CUDA-ядер:** 3072
- **Тензорных ядер:** 96 (4-е поколение)
- **RT-ядер:** 24 (3-е поколение)
- **Boost Clock:** 2.46 GHz (реальные — 2.5–2.7 GHz)
- **VRAM:** 8 GB GDDR6
- **Шина:** 128-bit
- **Пропускная способность:** 272 GB/s
- **L2-кэш:** 24 MB
- **TGP (Total Graphics Power):** 115W
- **Питание:** 1× 8-pin (многие AIB — 1× 6-pin, потребление настолько низкое)
- **PCIe:** 4.0 x8
- **Видеовыходы:** 3× DisplayPort 1.4a, 1× HDMI 2.1
- **MSRP (USD):** $299

## Почему 128-битная шина — осознанное ограничение

NVIDIA сделала ставку на большой L2-кэш (24 MB) вместо широкой шины. Это работает при кэш-хитах, но при промахах — узкая шина становится бутылочным горлышком.

**Где ограничение проявляется:**
- **1440p:** кэш-хитрейт падает, пропускная способность 272 GB/s становится недостаточной — потери 10–15% относительно гипотетической 192-bit версии
- **Текстуры высокого разрешения + RT:** VRAM забивается быстрее, подкачка из системной памяти через PCIe 4.0 x8 — худший сценарий

**Где не проявляется:**
- 1080p в большинстве игр — кэша хватает
- DLSS с пониженным внутренним разрешением — снижает нагрузку на VRAM

## Сравнение с RX 7600 (Iron Man Argument)

### Где RTX 4060 сильнее

- **DLSS 3.5 + Frame Generation:**
  - Лучшее качество апскейлинга среди всех технологий на рынке
  - Frame Generation даёт +60–80% к плавности в поддерживаемых играх (Cyberpunk 2077, Alan Wake 2, Black Myth: Wukong)
  - DLSS Ray Reconstruction — улучшенное качество RT-эффектов (меньше шума, лучше детализация отражений)

- **Трассировка лучей:**
  - Cyberpunk 2077 RT Ultra 1080p: RTX 4060 ~48 FPS vs RX 7600 ~32 FPS (+50%)
  - RT-ядра 3-го поколения Ada Lovelace — качественный скачок над RT-ускорителями RDNA 3
  - Alan Wake 2 Path Tracing: RTX 4060 играбельно с DLSS Performance, RX 7600 — неиграбельно

- **Энергоэффективность — ключевое преимущество:**
  - RTX 4060: 115W TGP
  - RX 7600: 165W TBP (−30% больше)
  - Меньше нагрев → тише кулер → дешевле блок питания → меньше счёт за электричество при длительных сессиях
  - Карты с одним 6-pin разъёмом работают даже на старых БП без 8-pin

- **Драйверы и экосистема:**
  - NVIDIA Reflex — эталонная система снижения задержки ввода (CS2, Valorant, Apex)
  - NVENC — лучший аппаратный кодировщик для стриминга (Twitch/YouTube)
  - CUDA — совместимость с рабочими приложениями (Blender, DaVinci Resolve, Adobe Premiere)
  - Broadcast — шумоподавление, виртуальный фон без потери FPS
  - Стабильность драйверов — исторически меньше жалоб на микростаттеры в DX11

- **RTX Video Super Resolution:** апскейлинг видео в браузере силами GPU — приятный бонус, отсутствующий у AMD

### Где RTX 4060 слабее

- **Чистый растр (без RT, без апскейлеров):**
  - CS2 (1080p competitive): RTX 4060 ~295 FPS vs RX 7600 ~320 FPS (−8%)
  - Valorant: RTX 4060 ~380 FPS vs RX 7600 ~410 FPS (−8%)
  - Cyberpunk 2077 Ultra 1080p no RT: RTX 4060 ~74 FPS vs RX 7600 ~78 FPS (−5%)

- **Цена:**
  - Медиана 32 000 ₽ vs 28 000 ₽ у RX 7600 (+14% дороже)
  - Разница 4 000 ₽ — цена за DLSS 3.5 и лучший RT

- **VRAM — общая проблема:**
  - 8GB GDDR6 на 128-bit шине — идентично RX 7600
  - В 2026 году 8GB — минимально допустимый объём даже для 1080p (Hogwarts Legacy, The Last of Us Part I, Forspoken)
  - NVIDIA не предлагает вариант 12GB в этом сегменте (в отличие от RTX 3060 12GB в прошлом поколении — шаг назад)

- **PCIe 4.0 x8 (как и у RX 7600):**
  - На PCIe 3.0 платах — потеря 2–4% FPS
  - Но: в отличие от AMD, NVIDIA использует меньше bandwidth при тех же x8 благодаря лучшей компрессии данных

### Объективный вердикт

- **AAA с RT/DLSS, стриминг, работа с CUDA → RTX 4060.** DLSS 3.5 меняет опыт. 115W — реальное преимущество.
- **Киберспорт, максимум FPS за деньги → RX 7600.** +8-10% FPS в растре за меньшие деньги. 4 000 ₽ разницы.
- **8GB VRAM — shared weakness.** Обе карты ограничены памятью. Если бюджет позволяет — прыгать на RTX 5060 Ti 16GB или RX 9060 XT 16GB.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 29 990–38 000 ₽
- **Медиана:** ~32 000 ₽
- **Типичные модели:** Palit Dual, Gigabyte Windforce, MSI Ventus 2X, ASUS Dual

Парадокс рынка: Palit Dual — одна из самых дешёвых (29 990–31 000 ₽) и при этом достаточно тихая благодаря 115W TGP (слабый нагрев прощает любой кулер). ASUS Dual переоценён для карты такого класса (35 000+ ₽).

## Для кого

**Подходит:**
- Геймеры AAA-тайтлов с трассировкой лучей в 1080p (Cyberpunk 2077, Alan Wake 2, Black Myth: Wukong)
- Стримеры — NVENC экономит ресурсы CPU/GPU на кодировании
- Пользователи, ценящие тишину и низкое энергопотребление (115W — бескомпромиссно)
- Работа с CUDA-приложениями (Blender, Adobe, DaVinci Resolve) на начальном уровне
- Апгрейд с GTX 1060 / 1650 / 1660 — качественный скачок во всём

**Не подходит:**
- Киберспортсмены с фокусом на чистый FPS/₽ (RX 7600 дешевле и быстрее в растре)
- 1440p-гейминг (8GB VRAM и 128-bit шина душат производительность)
- Игры с высокими требованиями к VRAM (моды Skyrim, Flight Simulator 2024, Cities Skylines 2)
- Максимальные настройки текстур в 2026 году (8GB упираются даже в 1080p)
- Те, кто держит карту 4+ года — лучше доплатить за 12/16GB VRAM

## Источники

1. Gamers Nexus — «NVIDIA RTX 4060 Review & Benchmarks» (июнь 2023)
2. TechSpot / Hardware Unboxed — «RTX 4060 vs RX 7600: 50 Game Benchmark» (2023–2024)
3. Digital Foundry — «RTX 4060: DLSS 3 Frame Generation Analysis»
4. TechPowerUp — «NVIDIA GeForce RTX 4060 Founders Edition Review»
5. ComputerBase.de — «GeForce RTX 4060 im Test: AD107 mit 8 GB»
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории в сборке EST-2026-0422-K1
