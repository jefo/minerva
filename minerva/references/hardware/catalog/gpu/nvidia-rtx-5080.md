---
id: "nvidia-rtx-5080"
type: "gpu"
title: "NVIDIA GeForce RTX 5080 16GB"
vendor: "nvidia"
status: "draft"
tags: ["nvidia", "blackwell", "gb203", "tsmc-4np", "256bit-honest-bus", "16gb-vram-critical-for-price", "gddr7", "pcie5.0-x16", "dlss4-mfg", "rt-4th-gen-leader", "320w-tbp", "12v-2x6-power", "nvenc-9th-gen-dual", "cuda-ecosystem", "4k-ultra-rt", "productivity-workhorse", "local-llm-viable", "vram-artificial-segmentation"]
last_updated: "2026-06-03"
links:
  bigger_brother: "catalog/gpu/nvidia-rtx-5090.md"
  smaller_brother: "catalog/gpu/nvidia-rtx-5070-ti.md"
  competitor_amd: "catalog/gpu/amd-rx-9070-xt.md"
  predecessor: "catalog/gpu/nvidia-rtx-4080.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "GB203 (Blackwell)"
  lithography: "TSMC 4NP (5nm)"
  cuda_cores: 9728
  boost_clock: "2.65 GHz"
  vram: "16 GB GDDR7 (256-bit)"
  vram_bandwidth: "960 GB/s"
  tbp: "320W"
  power_connector: "12V-2×6"
  pcie: "PCIe 5.0 x16"
  display_outputs: "3× DP 2.1b, 1× HDMI 2.1b"
  msrp_usd: "$999"
  engineering_notes: "GB203 — урезанный от GB202: 9728 CUDA, 256-bit, 16GB, 960 GB/s. Инженерная драма: 16GB при $999 — повторение ошибки RTX 3080 10GB. Через 2 года 16GB станет bottleneck для карты за $1000. GB203 физически поддерживает до 32GB через clamshell — маркетинг ограничил чтобы RTX 5090 выглядела necessary. Прирост +20-25% над 4080 Super — хорошо, но не революционно. Не превосходит RTX 4090 (24GB) в VRAM-тяжёлых нагрузках."
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
  min: 109990
  median: 125000
  max: 155000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 16
  type: "GDDR7"
  bus_width_bit: 256
  bandwidth_gb_s: 960
clock_structured:
  boost_ghz: 2.65
  game_ghz: null
cache:
  size_mb: null
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 9728
  rt:
    type: "RT Core"
    count: 76
    generation: 4
  ml:
    type: "Tensor Core"
    count: 304
    generation: 5
software:
  upscaler: "DLSS 4"
  frame_gen: "MFG"
  encoder: "NVENC 9th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

verdict: "Флагман для смертных. 4K-гейминг без компромиссов в растре и с RT. Но 16GB VRAM при $999 — спорно: RTX 4090 имела 24GB за $1599, а RTX 5080 просит $999 за 16GB. Поколенческий прирост над RTX 4080 Super ~20–25% — хорошо, но не революция. RX 9070 XT с 16GB за $599 отъедает аудиторию снизу. Берите, если 4K RT — цель и бюджет позволяет."
---

# NVIDIA GeForce RTX 5080

## Архитектура и позиционирование

RTX 5080 построена на GPU GB203 — втором по старшинству чипе архитектуры Blackwell. Это урезанный кристалл от GB202 (RTX 5090), но с сохранением 256-битной шины — NVIDIA решила не давать 5080 более широкую шину, чем у предшественника.

Позиционируется как карта для бескомпромиссного 4K-гейминга с трассировкой лучей, но без запредельной цены RTX 5090. Главный вопрос: почему не 20/24GB VRAM?

**Отличие от RTX 4080 Super:** +20% CUDA-ядер, переход на GDDR7 (+30% пропускной способности), DLSS 4 с MFG, новый дизайн RT-ядер.

## Характеристики

- **GPU:** GB203 (Blackwell)
- **Техпроцесс:** TSMC 4NP (5nm)
- **CUDA-ядер:** 9728
- **Тензорных ядер:** 304 (5-е поколение)
- **RT-ядер:** 76 (4-е поколение)
- **Boost Clock:** 2.65 GHz
- **VRAM:** 16 GB GDDR7
- **Шина:** 256-bit
- **Пропускная способность:** 960 GB/s
- **TBP:** 320W
- **Питание:** 12V-2×6
- **PCIe:** 5.0 x16
- **Видеовыходы:** 3× DisplayPort 2.1b, 1× HDMI 2.1b
- **MSRP (USD):** $999

## Почему 16GB при $999 — больной вопрос

- **RTX 4090 (2022):** 24GB за $1599.
- **RTX 5080 (2025):** 16GB за $999.
- **На бумаге:** меньше памяти за меньшую цену — логично.
- **На практике:** 16GB в 4K с RT + текстурами ультра — впритык уже сегодня (Indiana Jones Path Tracing требует >16GB для 4K native). Через 2 года 16GB может стать узким местом для карты за $1000.
- **Позиция NVIDIA:** «DLSS 4 снижает нагрузку на VRAM через внутреннее разрешение». Это правда, но текстуры высокого разрешения всё равно требуют памяти. MFG не решает проблему нехватки VRAM.
- **Вывод:** 16GB — осознанное ограничение для сегментации (чтобы RTX 5090 с 32GB выглядела оправданно дорогой).

## Сравнение с конкурентами (Iron Man Argument)

### RTX 5080 (16GB, $999) vs RX 9070 XT (16GB, ~$599)

**Где RTX 5080 сильнее:**
- **Чистый растр в 4K:** RTX 5080 на 30–35% быстрее. Cyberpunk 2077 Ultra 4K no RT: RTX 5080 ~78 FPS vs RX 9070 XT ~58 FPS. Разрыв огромен.
- **Трассировка лучей:** пропасть. Alan Wake 2 Path Tracing 4K: RTX 5080 ~52 FPS (DLSS Performance + MFG) vs RX 9070 XT ~28 FPS. Почти двукратное преимущество.
- **DLSS 4 MFG:** 3 промежуточных кадра превращают 40 базовых FPS в субъективные 120+ FPS. FSR 4 FG с одним промежуточным кадром даёт только ~70.
- **CUDA-экосистема:** безальтернативна для AI/ML, 3D-рендеринга, видеомонтажа.
- **NVENC 9-го поколения:** два энкодерных чипа — стриминг + запись одновременно без потери качества.

**Где RTX 5080 слабее:**
- **Цена:** $999 vs $599 — разница $400 (40%). В РФ: 125 000 ₽ vs 72 000 ₽ — почти вдвое.
- **FPS/₽:** RX 9070 XT имеет значительно лучший показатель. Платите $400 за +30% FPS в растре и +80% в RT — RT-премиум становится экстремально дорогим.
- **VRAM — паритет:** у обеих карт 16GB. AMD не даёт больше (RDNA 4 ограничена 16GB), но и не просит $999.
- **Энергопотребление:** 320W (RTX 5080) vs ~280W (RX 9070 XT) — NVIDIA горячее.

### RTX 5080 vs RTX 4090 (предыдущий флагман)

- RTX 4090 (24GB, $1599) в чистом растре всё ещё на 10–15% быстрее RTX 5080. В VRAM-тяжёлых сценариях (4K текстуры + моды) 24GB дают 4090 преимущество.
- RTX 5080 выигрывает только за счёт DLSS 4 MFG — технологии, которая не работает во всех играх.
- **Парадокс:** RTX 5080 не превосходит предыдущий флагман во всех сценариях — необычно для поколения 80-го класса.

### Вердикт

- **4K RT-гейминг, работа с AI/рендерингом → RTX 5080.** Лучшая карта до $1000 для этих задач. DLSS 4 — killer feature.
- **1440p, FPS/₽, чистый растр → RTX 5070 Ti или RX 9070 XT.** RTX 5080 избыточна.
- **Если у вас RTX 4080 Super → не апгрейдите.** +20% не стоят $999.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 109 990–155 000 ₽
- **Медиана:** ~125 000 ₽
- **Типичные модели:** Palit GameRock, Gigabyte Aorus Master, MSI Suprim X, ASUS ROG Strix

Рекомендация: Palit GameRock (~115 000 ₽) — лучший вариант. ASUS ROG Strix (150 000+ ₽) — премиум за бренд без ощутимого прироста. MSI Suprim X — достойный компромисс (120 000–130 000 ₽), но проверяйте шум кулера на 320W.

## Для кого

**Подходит:**
- 4K-гейминг на ультра-настройках с трассировкой лучей
- Профессиональный 3D-рендеринг (Blender, Octane, Redshift)
- AI/ML-разработка (Stable Diffusion, LLM inference, training небольших моделей)
- Стриминг + запись 4K60 одновременно
- Апгрейд с RTX 3080 / 3080 Ti — качественный скачок

**Не подходит:**
- 1440p-гейминг — карта избыточна (RTX 5070 Ti справится)
- Экономия — RX 9070 XT в 1.7 раза дешевле
- Игры без RT и без DLSS — переплата за неиспользуемые фичи
- 4K с запасом на 4+ года — 16GB VRAM под вопросом
- Владельцы RTX 4080 Super — прирост недостаточен для апгрейда
- Сборки с БП < 850W — 320W TBP требует запаса

## Источники

1. TechPowerUp — «NVIDIA GeForce RTX 5080 Review» (2025)
2. Gamers Nexus — «RTX 5080: $999 4K GPU Analysis»
3. Hardware Unboxed — «RTX 5080 vs RTX 4090 — New vs Old Flagship»
4. Digital Foundry — «RTX 5080 DLSS 4 Multi Frame Gen Deep Dive»
5. Blender Open Data — GPU Benchmark Database
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
