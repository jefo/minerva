---
id: "amd-rx-9060-xt"
type: "gpu"
title: "AMD Radeon RX 9060 XT 16GB"
vendor: "amd"
status: "draft"
tags: ["amd", "rdna4", "navi44", "tsmc-n5", "128bit-narrow-bus", "16gb-vram-safe", "infinity-cache-48mb", "pcie5.0-x8", "fsr4-ml-based", "rt-3rd-gen", "200w-tbp", "1x8pin-power", "dp2.1-uhbr13.5", "raster-optimized", "rt-mid", "local-llm-viable", "cache-dependent"]
last_updated: "2026-06-03"
links:
  competitor_nvidia: "catalog/gpu/nvidia-rtx-5060-ti.md"
  competitor_nvidia_budget: "catalog/gpu/nvidia-rtx-5060.md"
  bigger_brother: "catalog/gpu/amd-rx-9070.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "Navi 44 (RDNA 4)"
  lithography: "TSMC N5 (5nm)"
  stream_processors: 4096
  compute_units: 64
  ray_accelerators: 64 (3-е поколение)
  ai_accelerators: 128
  boost_clock: "2.85 GHz (Game Clock ~2.5 GHz)"
  vram: "16 GB GDDR6 (128-bit)"
  vram_bandwidth: "384 GB/s"
  infinity_cache: "48 MB"
  tbp: "200W"
  power_connector: "1× 8-pin"
  pcie: "PCIe 5.0 x8"
  display_outputs: "3× DP 2.1 UHBR 13.5, 1× HDMI 2.1b"
  msrp_usd: "$379"
  engineering_notes: "Navi 44 — младший RDNA 4 на TSMC N5. 64 CU на 128-bit с 48MB Infinity Cache 3-го поколения: эффективный bandwidth ~500-550 GB/s при кэш-хитах, при промахах падает до 384 GB/s. 16GB через 4×4GB модулей. FSR 4 на 128 AI-акселераторах — паритет с DLSS 4 CNN. RT 3-го поколения — +80% к RDNA 3, но всё ещё позади Blackwell. Поведение cache-dependent: в одних играх обгоняет 5060 Ti, в других проигрывает B580."
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
  bandwidth_constrained_vram_rich:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Локальный инференс LLM (7B–13B Q4_K_M). Карта позволяет загрузить модель полностью в VRAM без offload."
    failure_mode_desc: "Нативный 4K-гейминг на ультра. Узкая 128-bit шина становится bottleneck."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b"]
    failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu"]
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
  min: 41990
  median: 48000
  max: 56000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 16
  type: "GDDR6"
  bus_width_bit: 128
  bandwidth_gb_s: 384
clock_structured:
  boost_ghz: 2.85
  game_ghz: 2.5
cache:
  size_mb: 48
  type: "Infinity Cache"
compute:
  unit:
    type: "Stream Processor"
    count: 4096
  rt:
    type: "Ray Accelerator"
    count: 64
    generation: 3
  ml:
    type: "AI Accelerator"
    count: 128
    generation: 2
software:
  upscaler: "FSR 4"
  frame_gen: "AFMF 2"
  encoder: "AMF/VCE"
  compute_api: "ROCm"
  driver_features: ["SAM", "HYPR-RX"]

observations:
  - id: "obs-ag-rx9060xt-26"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Forza Horizon 5"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 168
    notes: "Ancient Gameplays YT (2026). 32GB DDR5 6400MHz."
  - id: "obs-ag-rx9060xt-27"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Ghost of Yōtei"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 115
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-28"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "God of War"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 123
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-29"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Hogwarts Legacy"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 104
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-30"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Kingdom Come: Deliverance II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 132
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-31"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "The Last of Us Part II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 135
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-32"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Black Myth: Wukong"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 131
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rx9060xt-33"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "amd-rx-9060-xt"
    cpu: "intel-core-ultra-7-2700k"
    game: "Cyberpunk 2077"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "FSR 4.1 Quality"
      framegen: false
    avg_fps: 112
    notes: "Ancient Gameplays YT (2026)."

verdict: "Лучший FPS/₽ в сегменте $350–400. 16GB VRAM — главный козырь против RTX 5060 Ti 8GB и RTX 5060 12GB. В чистом растре обходит конкурентов NVIDIA. FSR 4 сделан на ML основе и вплотную приблизился к DLSS 4 по качеству. Но RT всё ещё слабее NVIDIA, а драйверы периодически преподносят сюрпризы в DX11. Выбор рационалиста."
---

# AMD Radeon RX 9060 XT 16GB

## Архитектура и позиционирование

RX 9060 XT построена на GPU Navi 44 — младшем чипе архитектуры RDNA 4. В отличие от RDNA 3 (чиплетный дизайн на старших моделях), Navi 44 — монолитный кристалл на зрелом техпроцессе TSMC N5. AMD масштабирует RDNA 4 сверху вниз, и RX 9060 XT наследует все ключевые улучшения новой архитектуры.

Позиционируется как карта для 1440p в чистом растре и 1080p с трассировкой лучей. Главный аргумент AMD: 16GB VRAM — вдвое больше чем у RTX 5060 Ti 8GB за те же деньги.

**Ключевое улучшение RDNA 4:** RT-ускорители 3-го поколения (значительный шаг вперёд по сравнению с RDNA 3), выделенные AI-акселераторы для FSR 4 (ML-based апскейлинг), улучшенный Infinity Cache 3-го поколения.

## Характеристики

- **GPU:** Navi 44 (RDNA 4)
- **Техпроцесс:** TSMC N5 (5nm)
- **Потоковых процессоров:** 4096 (64 CU)
- **RT-ускорителей:** 64 (3-е поколение)
- **AI-ускорителей:** 128
- **Game Clock:** ~2.5 GHz
- **Boost Clock:** 2.85 GHz
- **VRAM:** 16 GB GDDR6
- **Шина:** 128-bit
- **Пропускная способность:** 384 GB/s
- **Infinity Cache:** 48 MB
- **TBP:** 200W
- **Питание:** 1× 8-pin
- **PCIe:** 5.0 x8
- **Видеовыходы:** 3× DisplayPort 2.1 UHBR 13.5, 1× HDMI 2.1b
- **MSRP (USD):** $379

## 16GB на 128-bit — честно или маркетинг?

16GB на 128-битной шине — необычная конфигурация. AMD использует 4 модуля GDDR6 по 4GB (вдвое более плотные чипы, чем у NVIDIA). Infinity Cache 48 MB компенсирует узкую шину.

- **Преимущество:** 16GB дают запас для текстур высокого разрешения, моддинга и будущих игр. В Indiana Jones 1440p Supreme текстуры — 5060 Ti 8GB упирается в VRAM, RX 9060 XT нет.
- **Недостаток:** 128-bit шина ограничивает пропускную способность — 384 GB/s. RTX 5060 Ti с GDDR7 имеет 448 GB/s на той же шине. В сценариях с высоким bandwidth (4K, RT) GDDR7 NVIDIA быстрее.
- **Реальность:** в 1080p/1440p 128-bit с 48MB кэша достаточно. В 4K — карта не позиционируется для 4K.

## Сравнение с конкурентами (Iron Man Argument)

### RX 9060 XT 16GB ($379) vs RTX 5060 Ti 8GB ($379) и 16GB ($429)

**Где RX 9060 XT сильнее:**
- **VRAM за деньги:** 16GB за $379 vs 8GB за $379 (NVIDIA). Версия RTX 5060 Ti 16GB стоит $429 — на $50 дороже. AMD предлагает вдвое больше памяти за ту же цену.
- **Чистый растр (без RT, без апскейлеров):** RX 9060 XT на 8–12% быстрее RTX 5060 Ti 8/16GB в raster-only тестах. Horizon Forbidden West 1440p: RX 9060 XT ~96 FPS vs RTX 5060 Ti ~85 FPS. Call of Duty BO6: RX 9060 XT ~130 FPS vs RTX 5060 Ti ~118 FPS.
- **DisplayPort 2.1 UHBR 13.5:** полноценная пропускная способность для 4K 240Hz / 8K 60Hz. NVIDIA в этом классе имеет DP 2.1b с ограничениями (зависит от AIB).
- **FSR 4:** ML-based апскейлинг нового поколения — качество вплотную приблизилось к DLSS 4. Артефакты минимальны, ghosting почти побеждён. Да, DLSS 4 всё ещё чуть лучше на мелких деталях, но разница перестала быть аргументом «против AMD».
- **Цена:** $379 за 16GB vs $429 за 16GB у NVIDIA. В РФ экономия ~4 000–6 000 ₽.

**Где RX 9060 XT слабее:**
- **Трассировка лучей:** RT-ускорители RDNA 4 улучшены, но Blackwell RT-ядра 4-го поколения всё ещё впереди. Cyberpunk 2077 RT Ultra 1440p: RX 9060 XT ~42 FPS vs RTX 5060 Ti ~55 FPS (−24%). Path Tracing — разрыв больше (NVIDIA ~35 FPS vs AMD ~22 FPS).
- **DLSS 4 MFG vs FSR 4 FG:** NVIDIA генерирует до 3 промежуточных кадров, AMD — один. В играх с поддержкой MFG (Cyberpunk, Alan Wake 2) NVIDIA обеспечивает субъективно более плавную картинку.
- **CUDA-экосистема:** отсутствует. Blender, Adobe Premiere (CUDA-ускорение), AI-фреймворки — работают хуже или не работают вовсе. ROCm/HIP — прогресс есть, но «просто работает» пока не про AMD.
- **Энергоэффективность:** 200W (AMD) vs 180W (NVIDIA) — NVIDIA экономичнее.
- **Драйверы:** Adrenalin 2026 стабилен, но occasional микростаттеры в старых DX11-играх случаются. NVIDIA Game Ready — эталон.

### Вердикт

- **Чистый растр, 16GB VRAM, бюджет → RX 9060 XT.** Больше FPS, больше памяти, меньше денег. FSR 4 закрывает главную историческую претензию к AMD.
- **RT-игры, CUDA, стриминг NVENC → RTX 5060 Ti 16GB.** Переплата $50 окупается DLSS 4 MFG и RT-лидерством.
- **Никогда не берите 8GB-версию RTX 5060 Ti.** За $379 получаете карту, которая устареет по VRAM раньше чем по производительности чипа.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 41 990–56 000 ₽
- **Медиана:** ~48 000 ₽
- **Типичные модели:** Sapphire Pulse, PowerColor Fighter, XFX Speedster QICK, ASRock Challenger

Рекомендация: Sapphire Pulse или PowerColor Fighter по 45 000–48 000 ₽ — лучшие варианты. XFX Speedster QICK с заводским разгоном оправдан только при цене до 50 000 ₽.

## Для кого

**Подходит:**
- 1440p-гейминг в чистом растре (Horizon, God of War, Call of Duty, Assassin's Creed)
- 1080p с максимальными текстурами и запасом VRAM на 3+ года
- Сборки с акцентом на FPS/₽
- Апгрейд с RX 5700 XT / RX 6600 XT / RTX 2060 Super
- Пользователи, которым не нужны CUDA и RT как приоритет

**Не подходит:**
- Игры с трассировкой лучей как основным приоритетом (Path Tracing — особенно)
- Профессиональная работа с CUDA (Blender, AI/ML, Adobe Suite) — только NVIDIA
- 4K-гейминг (нужна RX 9070 XT минимум)
- Стриминг с кодированием на GPU (NVENC предпочтительнее)
- Владельцы RX 7700 XT / RTX 4060 Ti 16GB — прирост недостаточен

## Источники

1. TechPowerUp — «AMD Radeon RX 9060 XT Review» (2025)
2. Hardware Unboxed — «RX 9060 XT vs RTX 5060 Ti: 40 Game Benchmark»
3. Gamers Nexus — «RDNA 4: RX 9060 XT Deep Dive»
4. Digital Foundry — «FSR 4 vs DLSS 4: Image Quality Face-Off»
5. AMD GPUOpen — RDNA 4 Architectural Overview
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
