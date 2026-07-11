---
id: "nvidia-rtx-5090"
type: "gpu"
title: "NVIDIA GeForce RTX 5090 32GB"
vendor: "nvidia"
status: "draft"
tags: ["nvidia", "blackwell", "gb202", "full-die-flagship", "tsmc-4np", "512bit-wide-bus", "32gb-vram-workstation", "gddr7", "pcie5.0-x16", "dlss4-mfg", "rt-4th-gen-leader", "500w-tbp-extreme", "12v-2x6-power", "nvenc-9th-gen-triple", "cuda-ecosystem", "4k-path-tracing", "8k-video", "local-llm-viable", "productivity-workhorse", "no-compromises", "infrastructure-demanding"]
last_updated: "2026-06-03"
links:
  smaller_brother: "catalog/gpu/nvidia-rtx-5080.md"
  competitor_amd: "catalog/gpu/amd-rx-9070-xt.md"
  predecessor: "catalog/gpu/nvidia-rtx-4090.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "GB202 (Blackwell)"
  lithography: "TSMC 4NP (5nm)"
  cuda_cores: 20480
  boost_clock: "2.52 GHz"
  vram: "32 GB GDDR7 (512-bit)"
  vram_bandwidth: "1792 GB/s"
  tbp: "500W"
  power_connector: "12V-2×6"
  pcie: "PCIe 5.0 x16"
  display_outputs: "3× DP 2.1b, 1× HDMI 2.1b"
  msrp_usd: "$1999"
  engineering_notes: "GB202 — максимальная конфигурация: 20480 CUDA, 512-bit, 32GB, 1792 GB/s. Единственная карта для 4K Path Tracing и LLM 13B-20B. 500W TBP требует инфраструктуры (БП 1000W+ ATX 3.1). Прирост +25-30% над 4090. Карта-инструмент, а не игрушка."
profiles:
  enthusiast_unrestricted_gpu:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "Нативный 4K-гейминг на максималках, профессиональный рендеринг, высокопроизводительный AI-инференс."
    failure_mode_desc: "Компактные корпуса с плохой вентиляцией. 300–500W тепла → 55°C внутри → перегрев CPU и троттлинг."
    optimal_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_inference_20b", "video_editing_8k"]
    failure_for_intents: ["silent_build", "sff_build"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
  transient_spike_heavy:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "Динамичный 3D-рендеринг и гейминг. Мгновенный переход в P-state без микрофризов."
    failure_mode_desc: "БП ATX 2.4 без ATX 3.0. Микросекундный скачок тока триггерит OCP → чёрный экран."
    optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "3d_rendering_gpu"]
    failure_for_intents: ["sff_build"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
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
  min: 219990
  median: 260000
  max: 320000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 32
  type: "GDDR7"
  bus_width_bit: 512
  bandwidth_gb_s: 1792
clock_structured:
  boost_ghz: 2.52
  game_ghz: null
cache:
  size_mb: null
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 20480
  rt:
    type: "RT Core"
    count: 160
    generation: 4
  ml:
    type: "Tensor Core"
    count: 640
    generation: 5
software:
  upscaler: "DLSS 4"
  frame_gen: "MFG"
  encoder: "NVENC 9th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

verdict: "Безоговорочно быстрейшая потребительская видеокарта на планете. 32GB VRAM и 512-битная шина — единственная карта, которая не боится 4K Path Tracing. Но $1999 (260 000 ₽ в РФ) и 500W TBP делают её инструментом для энтузиастов и профессионалов. Поколенческий прирост над RTX 4090 ~25–30% — солидно, но не революционно за $400 доплаты. Если вы не рендерите 8K-видео, не тренируете LLM и не играете в 4K Path Tracing — RTX 5080 хватит с запасом."
---

# NVIDIA GeForce RTX 5090

## Архитектура и позиционирование

RTX 5090 построена на GPU GB202 — самом большом потребительском чипе NVIDIA в истории. 20480 CUDA-ядер на монолитном кристалле TSMC 4NP. Это не урезанная профессиональная карта — это максимальная конфигурация, доступная в потребительском сегменте.

Позиционируется как универсальный инструмент: 4K Path Tracing без компромиссов, 8K-видеомонтаж, AI-тренировка моделей уровня 13B-20B параметров, 3D-рендеринг на уровне RTX 6000 Ada предыдущего поколения.

**Ключевое отличие от RTX 4090:** +25% ядер, 512-битная шина (вместо 384-bit), GDDR7 (вместо GDDR6X), пропускная способность памяти +78%.

## Характеристики

- **GPU:** GB202 (Blackwell)
- **Техпроцесс:** TSMC 4NP (5nm)
- **CUDA-ядер:** 20480
- **Тензорных ядер:** 640 (5-е поколение)
- **RT-ядер:** 160 (4-е поколение)
- **Boost Clock:** 2.52 GHz
- **VRAM:** 32 GB GDDR7
- **Шина:** 512-bit
- **Пропускная способность:** 1792 GB/s
- **TBP:** 500W
- **Питание:** 12V-2×6 (обязательно с новым стандартом БП)
- **PCIe:** 5.0 x16
- **Видеовыходы:** 3× DisplayPort 2.1b, 1× HDMI 2.1b
- **MSRP (USD):** $1999

## 32GB VRAM + 512-bit — когда это реально нужно

**Да, нужно:**
- **4K Path Tracing (Cyberpunk 2077, Alan Wake 2, Indiana Jones):** 16GB карты упираются в VRAM даже с DLSS. RTX 5090 — единственная карта, где Path Tracing работает без компромиссов.
- **Локальные LLM:** 32GB позволяют запускать модели 13B-20B параметров полностью в VRAM (Llama 3, Qwen, DeepSeek). RTX 4090 с 24GB тоже может, но с меньшим контекстным окном.
- **Stable Diffusion / Flux:** генерация в 4K-разрешении, обучение LoRA на больших датасетах.
- **8K-видеомонтаж (DaVinci Resolve):** 32GB — комфортный минимум для 8K-таймлайна с цветокоррекцией.
- **3D-рендеринг больших сцен (Blender, Octane, V-Ray):** сцены с 20M+ полигонов требуют >16GB.

**Нет, не нужно:**
- 4K-гейминг без Path Tracing — RTX 5080 справляется.
- 1440p-гейминг — карта дико избыточна.
- Стриминг — NVENC есть на всех RTX 50xx.

## 500W TBP — инфраструктурные требования

500W — это тепловой пакет карты, а не всей системы. Реальные требования:

- **Блок питания:** минимум 1000W качественного БП (ATX 3.1 с 12V-2×6). Corsair RM1000x / Seasonic Vertex GX-1000.
- **Охлаждение корпуса:** 500W тепла нужно выводить. Корпус с mesh-передней панелью и 3+ вентиляторами — обязательно.
- **Разъём 12V-2×6:** новый улучшенный стандарт, но требует аккуратности. Карта комплектуется переходником на 4× 8-pin (но лучше использовать нативный кабель БП).
- **Счёт за электричество:** 500W × 4 часа в день × 30 дней = 60 kWh/мес. В РФ ~300–500 ₽/мес — терпимо. В Европе ощутимо.

## Сравнение с конкурентами (Iron Man Argument)

### RTX 5090 ($1999) — сравнение не с кем

У AMD нет карты этого класса. RX 9070 XT ($599) — карта совершенно другой лиги. Сравнивать их некорректно — как сравнивать Ferrari с Toyota Camry.

**Единственный релевантный конкурент — RTX 4090 (предыдущий флагман):**

**Где RTX 5090 сильнее:**
- **Производительность в растре:** +25–30% в 4K. Cyberpunk 2077 Ultra 4K: RTX 5090 ~100 FPS vs RTX 4090 ~78 FPS.
- **Пропускная способность памяти:** 1792 GB/s vs 1008 GB/s (+78%). Критично для 4K+ и VRAM-тяжёлых рабочих нагрузок.
- **VRAM:** 32GB vs 24GB (+33%). Ощутимо для AI/ML и 8K-монтажа.
- **DLSS 4 + MFG:** эксклюзив Blackwell. RTX 4090 ограничена DLSS 3.5 FG (один промежуточный кадр).
- **RT-производительность:** RT-ядра 4-го поколения vs 3-го. Alan Wake 2 Path Tracing 4K: RTX 5090 ~65 FPS vs RTX 4090 ~48 FPS (+35%).

**Где RTX 5090 слабее:**
- **Цена:** $1999 vs $1599 (MSRP) — на $400 дороже. В реальной рознице РФ разница может достигать 80 000–100 000 ₽.
- **Энергопотребление:** 500W vs 450W (+11%). Разница в тепловыделении заметна.
- **Поколенческий прирост не революционен:** +25–30% за +$400 — дорогой апгрейд. RTX 4090 всё ещё актуальна для 99% задач.
- **Доступность:** флагманские карты NVIDIA традиционно в дефиците первые 3–6 месяцев после релиза.

### Вердикт

- **Абсолютный максимум без компромиссов → RTX 5090.** Если бюджет не ограничен — это лучшая карта.
- **С RTX 4090 → не апгрейдить.** +25% не стоят $1999 при наличии 4090. Ждите RTX 6090.
- **Профессиональная работа с AI/8K → RTX 5090.** 32GB VRAM открывают возможности, недоступные на 24GB.
- **4K-гейминг без Path Tracing → RTX 5080.** 5090 избыточна, 5080 справляется.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 219 990–320 000 ₽
- **Медиана:** ~260 000 ₽
- **Типичные модели:** ASUS ROG Astral, MSI Suprim Liquid, Gigabyte Aorus Master, Palit GameRock

Рекомендация: Palit GameRock (~230 000 ₽) — surprisingly хороший вариант для флагмана. MSI Suprim Liquid (~280 000 ₽) — если готовы к СЖО. ASUS ROG Astral (300 000+ ₽) — премиум, который не окупается производительностью.

## Для кого

**Подходит:**
- Энтузиасты с неограниченным бюджетом — лучшая карта без «но»
- 4K Path Tracing в Cyberpunk 2077, Alan Wake 2, Indiana Jones
- Профессиональный 8K-видеомонтаж (DaVinci Resolve, Premiere Pro)
- AI/ML-специалисты: тренировка и инференс моделей 13B–20B
- 3D-художники с большими сценами (Blender, Octane, V-Ray)
- Стримеры с 4K60 + запись одновременно

**Не подходит:**
- Геймеры с бюджетом < 250 000 ₽ на всю сборку — RTX 5080 / 5070 Ti
- 1440p-гейминг — карта избыточна на 300%
- Киберспорт — избыточно даже для 360Hz мониторов
- Владельцы RTX 4090 — прирост не оправдывает $1999
- Сборки без топового БП и охлаждения корпуса
- Те, кто не использует RT/AI/монтаж профессионально

## Источники

1. TechPowerUp — «NVIDIA GeForce RTX 5090 Review» (2025)
2. Gamers Nexus — «RTX 5090: $2000 GPU Benchmark & Analysis»
3. Hardware Unboxed — «RTX 5090 vs RTX 4090 — 50 Game Benchmark»
4. Digital Foundry — «RTX 5090 Path Tracing: The 4K Dream»
5. Blender Open Data — GPU Benchmark Database
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
