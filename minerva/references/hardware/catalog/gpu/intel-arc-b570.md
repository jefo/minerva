---
id: "intel-arc-b570"
type: "gpu"
title: "Intel Arc B570 10GB"
vendor: "intel"
status: "draft"
tags: ["intel", "battlemage", "bmg-g21-cut", "xe2-hpg", "tsmc-n5", "160bit-odd-bus", "10gb-vram-nonstandard", "xmx-engines-160", "xess2-ml", "av1-encode", "pcie5.0-x8", "170w-tbp", "1x8pin-power", "rebar-mandatory", "dx12-vulkan-optimized", "dx11-penalty", "high-idle-power", "subsidized-pricing", "no-cuda"]
last_updated: "2026-06-03"
links:
  bigger_brother: "catalog/gpu/intel-arc-b580.md"
  competitor_amd: "catalog/gpu/amd-rx-9060-xt.md"
  competitor_nvidia: "catalog/gpu/nvidia-rtx-5060.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "BMG-G21 (Battlemage)"
  lithography: "TSMC N5 (5nm)"
  xe_cores: 20
  rt_units: 20
  xmx_engines: 160
  boost_clock: "2.5 GHz"
  vram: "10 GB GDDR6 (160-bit)"
  vram_bandwidth: "380 GB/s"
  l2_cache: "16 MB"
  tbp: "170W"
  power_connector: "1× 8-pin"
  pcie: "PCIe 5.0 x8"
  display_outputs: "3× DP 2.1, 1× HDMI 2.1"
  msrp_usd: "$219"
  engineering_notes: "BMG-G21 урезан (20/24 Xe-ядер) на TSMC N5. 10GB через 5×2GB модулей на 160-bit шине — нечётная конфигурация (один 32-bit контроллер отключён). XMX-движки (160) дают сильный XeSS 2 и RT для бюджета. Но драйверный overhead DX9/DX11 — 20-30% потери FPS. Intel продаёт в убыток ради доли рынка."
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
  min: 25990
  median: 29000
  max: 34000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 10
  type: "GDDR6"
  bus_width_bit: 160
  bandwidth_gb_s: 380
clock_structured:
  boost_ghz: 2.5
  game_ghz: null
cache:
  size_mb: 16
  type: "L2"
compute:
  unit:
    type: "Xe Core"
    count: 20
  rt:
    type: "RT Unit"
    count: 20
    generation: 2
  ml:
    type: "XMX Engine"
    count: 160
    generation: 2

software:
  upscaler: "XeSS 3"
  frame_gen: "XeSS MFG (3x/4x)"
  encoder: "QSV"
  compute_api: "oneAPI"
  driver_features: ["XeLL Low Latency", "Driver-level Auto FG"]

verdict: "Бюджетный герой — но только для современных игр. $219 за 10GB и приличную производительность в DX12/Vulkan. XeSS 2 — сильный козырь против FSR 3 у AMD. Но драйверы для старых DX9/11 игр всё ещё immature, энергопотребление в простое выше конкурентов, а 10GB VRAM — нечётное решение (160-bit). Если игры свежие — лучший бюджетный выбор. Если в библиотеке много классики — смотрите на AMD/NVIDIA."
---

# Intel Arc B570 10GB

## Архитектура и позиционирование

Arc B570 — младшая карта архитектуры Battlemage (Xe2 HPG) на урезанном чипе BMG-G21. Полный чип имеет 24 Xe-ядра (B580); здесь активированы 20. Производится на зрелом техпроцессе TSMC N5.

Позиционируется Intel как сверхбюджетная карта для 1080p с акцентом на современные API (DX12, Vulkan). $219 — агрессивная цена, которой Intel покупает долю рынка.

**Наследие Alchemist:** первое поколение Arc (A750/A770) страдало от сырых драйверов. Battlemage — зрелая архитектура с исправленными детскими болезнями. Но reputation восстанавливается медленно.

## Характеристики

- **GPU:** BMG-G21 (Battlemage)
- **Техпроцесс:** TSMC N5 (5nm)
- **Xe-ядер:** 20
- **RT-блоков:** 20
- **XMX-движков (Xe Matrix Extensions):** 160
- **Boost Clock:** 2.5 GHz
- **VRAM:** 10 GB GDDR6
- **Шина:** 160-bit
- **Пропускная способность:** 380 GB/s
- **L2-кэш:** 16 MB
- **TBP:** 170W
- **Питание:** 1× 8-pin
- **PCIe:** 5.0 x8
- **Видеовыходы:** 3× DisplayPort 2.1, 1× HDMI 2.1
- **MSRP (USD):** $219

## 10GB на 160-bit — странная конфигурация

10GB VRAM с 160-битной шиной — уникальная конфигурация (5 модулей по 2GB). Ни AMD ни NVIDIA не используют такие комбинации:

- **Плюс:** 10GB — лучше чем 8GB у RTX 5060 (младшей) и сопоставимо с 12GB RTX 5060 в большинстве сценариев.
- **Минус:** нестандартная конфигурация памяти может вызывать неоптимальное распределение в некоторых движках. Bandwidth 380 GB/s — ниже чем у RTX 5060 с GDDR7 (384–448 GB/s).
- **Реальность:** в 1080p 10GB достаточно. В 1440p — впритык.

## Сравнение с конкурентами (Iron Man Argument)

### Arc B570 ($219) vs RTX 5060 8GB ($299) и 12GB ($349)

**Где Arc B570 сильнее:**
- **Цена — главное оружие:** $219 vs $299 (RTX 5060 8GB) — на $80 (27%) дешевле. Против 12GB-версии ($349) — экономия $130 (37%).
- **FPS/₽ в DX12/Vulkan:** в современных играх B570 выдаёт 85–90% производительности RTX 5060 за 73% цены. Call of Duty BO6 1080p: B570 ~115 FPS vs RTX 5060 ~130 FPS. Cyberpunk 2077 1080p Ultra: B570 ~72 FPS vs RTX 5060 ~82 FPS.
- **VRAM за деньги:** 10GB за $219. RTX 5060 8GB за $299 — меньше памяти за большие деньги. 12GB за $349 — на $130 дороже.
- **XeSS 2:** качественный ML-based апскейлинг лучше чем FSR 3 у AMD и сопоставим с DLSS 3. XeSS 2 FG (Frame Generation) работает в поддерживаемых играх. Качество картинки высокое.
- **AV1-кодеки:** аппаратное кодирование AV1 — фича, которой нет у бюджетных карт прошлого поколения. Стримерам на Twitch/YouTube — приятный бонус.
- **RT-производительность:** неожиданно сильная для бюджетной карты. RT-блоки Battlemage на уровне AMD RDNA 3, но слабее NVIDIA Blackwell.

**Где Arc B570 слабее:**
- **Драйверы (DX9/DX11):** главная ахиллесова пята Intel. В старых играх (CS:GO, Skyrim, GTA V, старые MMO) производительность нестабильна. Микростаттеры, недогруз GPU, иногда артефакты. Ситуация улучшается, но до стабильности NVIDIA/AMD ещё далеко.
- **Энергопотребление в простое:** ~25–30W — значительно выше чем у NVIDIA (8W) и AMD (12W). Для включённого 24/7 ПК — ощутимо за год.
- **Производительность в DX11:** в среднем на 10–15% ниже чем могла бы быть при идеальных драйверах. Некоторые игры теряют до 30%.
- **Нет high-end моделей:** потолок Intel — B580. Апгрейд-путь ограничен.
- **CUDA-экосистема:** отсутствует. Для рабочих задач — не вариант.
- **Процессорозависимость:** Arc карты требуют Resizable BAR (SAM) для нормальной работы. Без него — значительные потери FPS (15–25%).

### Arc B570 ($219) vs RX 7600 ($269)

- **Цена/VRAM:** B570: $219/10GB. RX 7600: $269/8GB. Intel выигрывает оба параметра.
- **Растр DX12:** паритет. B570 немного медленнее (~5%) но компенсирует ценой.
- **Драйверы:** AMD стабильнее для старых игр. Intel — для новых.
- **Вердикт:** если библиотека на 80% состоит из игр 2020+ — B570. Если много классики — RX 7600.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 25 990–34 000 ₽
- **Медиана:** ~29 000 ₽
- **Типичные модели:** ASRock Challenger, Sparkle Elf, Gunnir Index

Рекомендация: ASRock Challenger (~27 000 ₽) — лучшая цена. Sparkle Elf (~29 000 ₽) — достойный кулер. Gunnir Index — редкий гость в РФ, переплата неоправдана.

## Для кого

**Подходит:**
- Бюджетные сборки до 70 000 ₽
- 1080p-гейминг в современных DX12/Vulkan-играх
- Игры с XeSS 2 (Cyberpunk 2077, Hogwarts Legacy, Call of Duty)
- Стримеры-любители (AV1-кодирование)
- Апгрейд с GTX 1650 / GTX 1060 / RX 580
- Пользователи, готовые мириться с драйверными нюансами ради экономии

**Не подходит:**
- Игры на старых API (DX9/DX11) — драйверы сырые
- Профессиональная работа (нет CUDA, слабая поддержка в про-софте)
- 1440p-гейминг (10GB и 160-bit — бутылочное горлышко)
- Системы без Resizable BAR (старые платы, некоторые OEM)
- ПК включённый 24/7 (энергопотребление в простое)
- Пользователи, не готовые к occasional troubleshooting

## Источники

1. TechPowerUp — «Intel Arc B570 Review» (2025)
2. Hardware Unboxed — «Arc B570 vs RTX 5060 vs RX 7600: Budget GPU War»
3. Gamers Nexus — «Battlemage B570: $219 GPU Analysis»
4. Digital Foundry — «XeSS 2 vs DLSS 4 vs FSR 4: Quality Comparison»
5. Intel Arc — Battlemage Architecture Overview
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
