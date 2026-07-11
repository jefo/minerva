---
id: "nvidia-rtx-5070"
type: "gpu"
title: "NVIDIA GeForce RTX 5070 12GB"
vendor: "nvidia"
status: "verified"
tags: ["nvidia", "blackwell", "gb205-cut", "tsmc-4n", "192bit-mid-bus", "12gb-vram-critical", "gddr7", "pcie5.0-x16", "dlss4-mfg", "rt-4th-gen-leader", "250w-tbp", "12v-2x6-power", "nvenc-9th-gen", "cuda-ecosystem", "1440p-rt", "4k-vram-limited", "frametime-gaming-1440p", "vram-artificial-segmentation"]
last_updated: "2026-06-03"
last_audit: "2026-07-02"
external_audit_verification: passed
links:
  bigger_brother: "catalog/gpu/nvidia-rtx-5070-ti.md"
  smaller_brother: "catalog/gpu/nvidia-rtx-5060-ti.md"
  competitor_amd: "catalog/gpu/amd-rx-9070.md"
  predecessor: "catalog/gpu/nvidia-rtx-4070.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "GB205 (Blackwell)"
  lithography: "TSMC 4N (5nm)"
  cuda_cores: 6144
  tensor_cores: "192 (5th gen)"
  rt_cores: "48 (4th gen)"
  boost_clock: "2.51 GHz"
  vram: "12 GB GDDR7 (192-bit)"
  vram_bandwidth: "672 GB/s"
  tbp: "250W"
  power_connector: "12V-2×6 (16-pin)"
  pcie: "PCIe 5.0 x16"
  display_outputs: "3× DP 2.1b, 1× HDMI 2.1b"
  msrp_usd: "$549"
  engineering_notes: "GB205: 6144 CUDA, 192-bit шина, 12GB GDDR7 (6×16Gb чипов), 672 GB/s. Физический максимум GB205 на 192-bit шине: 18GB с чипами GDDR7 24Gb (доступны на рынке), 24GB теоретически с 32Gb чипами (не существуют в GDDR7). Соотношение bandwidth/VRAM = 56 GB/s на 1GB. RTX 5070: 12GB, 192-bit, MSRP $549. RTX 5070 Ti: 16GB, 256-bit, MSRP $749. Разница: +4GB VRAM (+33%), +224 GB/s bandwidth (+33%), +$200 цена (+36%). Тренд VRAM-потребления AAA-игр: 2020 — 6-8GB, 2023 — 10-12GB, 2025 — 12-16GB для максимальных текстур (Digital Foundry, Hardware Unboxed historical data). При сохранении тренда 12GB может ограничить максимальные настройки текстур в 1440p к 2027-2028."
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
  min: 62990
  median: 72000
  max: 85000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 12
  type: "GDDR7"
  bus_width_bit: 192
  bandwidth_gb_s: 672
clock_structured:
  boost_ghz: 2.51
  game_ghz: null
cache:
  size_mb: null
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 6144
  rt:
    type: "RT Core"
    count: 48
    generation: 4
  ml:
    type: "Tensor Core"
    count: 192
    generation: 5
software:
  upscaler: "DLSS 4"
  frame_gen: "MFG"
  encoder: "NVENC 9th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

verdict: "RTX 5070: 1440p производительность на уровне RTX 4070 Ti в растре (+15-20% над RTX 4070). 12GB VRAM при MSRP $549. Конкуренты: RX 9070 (16GB, MSRP $549) — на 8-12% быстрее в чистом растре 1440p, +4GB VRAM при той же цене. RTX 5070: +41% в RT-производительности над RX 9070 (Cyberpunk 2077 RT Ultra 1440p), CUDA-экосистема (Blender ~3800 vs ~2100 points), DLSS 4 + MFG. MFG генерирует до 3 промежуточных кадров; FSR 4 FG — 1 промежуточный кадр. 250W TBP, 16-pin питание."
---

# NVIDIA GeForce RTX 5070

## Архитектура и позиционирование

RTX 5070 построена на GPU GB205 — чипе среднего звена архитектуры Blackwell. Это не урезанный флагманский кристалл (в отличие от RTX 4070, который использовал урезанный AD104 — чип среднего звена Ada Lovelace, урезанный с 7680 до 5888 ядер; флагманом Ada был AD102 в RTX 4090), а собственный дизайн, оптимизированный под 192-битную шину. Техпроцесс TSMC 4N — тот же что у всей 50-й серии.

Позиционируется как карта для 1440p-гейминга с трассировкой лучей. NVIDIA позиционирует DLSS 4 как ключевую фичу поколения Blackwell (пресс-релиз CES 2025). NVIDIA заявила: "RTX 5070 = 4090 performance at $549". Согласно тестам Gamers Nexus (март 2025): с MFG x4 и DLSS 4 в отдельных играх RTX 5070 достигает FPS, сопоставимого с RTX 4090 без MFG. Без MFG: RTX 5070 в среднем на 40-50% медленнее RTX 4090.

**Главная претензия сообщества:** 12GB VRAM в 2026 году за $549. Конкуренты (RX 9070) предлагают 16GB за те же деньги.

## Характеристики

- **GPU:** GB205 (Blackwell)
- **Техпроцесс:** TSMC 4N (5nm)
- **CUDA-ядер:** 6144
- **Тензорных ядер:** 192 (5-е поколение)
- **RT-ядер:** 48 (4-е поколение)
- **Boost Clock:** 2.51 GHz
- **VRAM:** 12 GB GDDR7
- **Шина:** 192-bit
- **Пропускная способность:** 672 GB/s
- **TBP:** 250W
- **Питание:** 12V-2×6 (16-pin)
- **PCIe:** 5.0 x16
- **Видеовыходы:** 3× DisplayPort 2.1b, 1× HDMI 2.1b
- **MSRP (USD):** $549

## Проблема 12GB VRAM в 2026

RTX 5070 (12GB, 192-bit, $549, GB205) и RTX 5070 Ti (16GB, 256-bit, $749, GB203) — разные кристаллы, разделённые ценой в $200.

- **1440p сегодня:** В тестах Hardware Unboxed (март 2025): из 20 игр в 1440p Ultra 18 укладываются в 12GB VRAM, 2 игры (Indiana Jones Path Tracing, Flight Simulator 2024) превышают лимит.
- **1440p через 2 года:** Вычислительная мощность: ~30.8 TFLOPS FP32. VRAM: 12GB. Для сравнения: RTX 4070 (2023) — 29.1 TFLOPS, 12GB. Прирост поколения: +6% compute при том же объёме VRAM.
- **4K:** даже сегодня 12GB мало для максимальных настроек. DLSS Performance снижает нагрузку, но текстуры всё равно требуют VRAM.
- **Сравнение с RTX 4070:** RTX 4070 (2023): 12GB GDDR6X, MSRP $599. RTX 5070 (2025): 12GB GDDR7, MSRP $549. Объём не изменился, цена снижена на $50. Bandwidth: 504 → 672 GB/s (+33%).

**Итог:** GB205 (RTX 5070) имеет 192-bit шину (6 каналов по 32-bit). При чипах GDDR7 16Gb: 6 × 2GB = 12GB. При чипах 24Gb: 6 × 3GB = 18GB. NVIDIA выбрала конфигурацию 12GB (6×16Gb чипов). Конфигурация 18GB на чипах 24Gb физически возможна на GB205, но не реализована. RTX 5070 Ti использует более крупный кристалл GB203 с 256-bit шиной (8 каналов по 32-bit) и 16GB VRAM.

## Сравнение с конкурентами (Iron Man Argument)

### RTX 5070 (12GB, $549) vs RX 9070 (16GB, $549)

**Где RTX 5070 сильнее:**
- **DLSS 4 + Multi Frame Generation:** MFG (до 3 промежуточных кадров) даёт субъективно более плавную картинку чем FSR 4 FG. В Alan Wake 2 с Path Tracing: RTX 5070 с MFG ощущается как 100+ FPS, RX 9070 с FSR 4 FG — около 70.
- **Трассировка лучей:** RT-ядра Blackwell 4-го поколения держат лидерство. Cyberpunk 2077 RT Ultra 1440p: RTX 5070 ~62 FPS vs RX 9070 ~44 FPS (+41%). Path Tracing — ещё больший разрыв.
- **CUDA и профессиональные приложения:** Blender Classroom: RTX 5070 ~3800 points vs RX 9070 ~2100 (ROCm/HIP) — почти двукратное преимущество. CUDA-экосистема безальтернативна для многих рабочих процессов.
- **NVENC:** аппаратный кодировщик девятого поколения. Качество AV1-кодирования превосходит AMD AMF при одинаковом битрейте.

**Где RTX 5070 слабее:**
- **Чистый растр (без RT/апскейлеров, 1440p):** RX 9070 в среднем на 8–12% быстрее. Call of Duty BO6: RX 9070 ~155 FPS vs RTX 5070 ~140 FPS. Horizon Forbidden West: RX 9070 ~98 FPS vs RTX 5070 ~88 FPS.
- **VRAM:** 12GB vs 16GB. В 4K и тяжёлых 1440p-сценариях с текстурами высокого разрешения RX 9070 имеет ощутимый запас.
- **Энергопотребление:** 250W (RTX 5070) vs 220W (RX 9070) — RTX 5070 на 30W горячее.
- **Цена:** MSRP $549 vs $549 — одинаково. В рознице РФ цены сопоставимы: ~72 000 ₽ за обе карты.
- **FSR 4 vs DLSS 4:** FSR 4 (ML-based как DLSS) значительно сократил разрыв в качестве. Да, DLSS 4 всё ещё лидирует по стабильности картинки, но FSR 4 уже «достаточно хорош» для большинства игроков. MFG — преимущество DLSS 4, но нужна игра с поддержкой.
- **Поколенческий прирост:** RTX 5070 над RTX 4070 в чистом растре +15–20% — скромно для нового поколения. RX 9070 над RX 7800 XT даёт +25–30% — AMD сделала больший шаг.

### Вердикт

- **RT и DLSS — приоритет → RTX 5070.** DLSS 4 + MFG трансформируют опыт в сюжетных AAA. RT-производительность вне конкуренции. CUDA обязательна для работы.
- **Чистый растр и FPS/₽ → RX 9070.** 16GB памяти и +10% FPS при той же цене. FSR 4 «достаточно хорош».
- **Если планируете 4K → ни одна.** Для 4K нужна RTX 5070 Ti 16GB минимум.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 62 990–85 000 ₽
- **Медиана:** ~72 000 ₽
- **Типичные модели:** Palit GamingPro, Gigabyte Gaming OC, MSI Ventus 3X, ASUS TUF

Palit GamingPro: ~65 000 ₽ (референсные частоты). Gigabyte Gaming OC: ~73 000 ₽ (+12%, заводской разгон). MSI Ventus 3X: ~68 000 ₽. ASUS TUF: ~82 000 ₽. RTX 5070 Ti: от ~95 000 ₽. Разница между ASUS TUF 5070 и минимальной 5070 Ti: +13 000 ₽ (+16%).

## Для кого

**Подходит:**
- 1440p-гейминг с трассировкой лучей в AAA-тайтлах (Cyberpunk 2077, Alan Wake 2, Black Myth: Wukong)
- Стримеры и контент-мейкеры (NVENC + CUDA)
- Работа в Blender, DaVinci Resolve, Adobe Suite
- Апгрейд с RTX 2070/3060 Ti/3070 — ощутимый прирост

**Не подходит:**
- 4K-гейминг (нужна RTX 5070 Ti / 5080)
- Максимальные текстуры с запасом на 3+ года (12GB VRAM под вопросом)
- Игры с активным моддингом (Skyrim Nolvus, Cities Skylines 2 с ассетами)
- Покупка исключительно под чистый растр — RX 9070 быстрее при той же цене
- Долгосрочная инвестиция без апгрейда 4+ года

## Источники

1. TechPowerUp — «NVIDIA GeForce RTX 5070 Review» (2025)
2. Gamers Nexus — «RTX 5070 vs RX 9070: Full Benchmark Suite»
3. Hardware Unboxed — «RTX 5070 12GB — Enough VRAM for 1440p?» 
4. Digital Foundry — «DLSS 4 vs FSR 4: Image Quality Comparison»
5. Blender Open Data — GPU Benchmark Database
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории

observations:
  # === 1440p native raster (GPU-bound baseline) ===
  - id: "obs-5070-001"
    source_id: "agg"
    source_confidence: 0.90
    observation_quality: 0.88
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 87
    p1_fps: 62
    gpu_utilization: 98
    cpu_utilization: 40
    notes: "GPU-bound: utilisation 98%. i5-14600K не bottleneck."

  - id: "obs-5070-002"
    source_id: "agg"
    source_confidence: 0.90
    observation_quality: 0.88
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Alan Wake 2"
    game_version: "1.2.x (2025)"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 72
    p1_fps: 54
    gpu_utilization: 97
    cpu_utilization: 35

  - id: "obs-5070-003"
    source_id: "agg"
    source_confidence: 0.90
    observation_quality: 0.88
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Hogwarts Legacy"
    game_version: "2025 build"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 95
    p1_fps: 68
    gpu_utilization: 98
    cpu_utilization: 42

  # === 1440p RT Medium ===
  - id: "obs-5070-004"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "Ultra"
      rt: "Medium"
      upscaler: "None"
      framegen: false
    avg_fps: 52
    p1_fps: 38
    gpu_utilization: 99
    notes: "RT Medium без DLSS — GPU-bound даже сильнее из-за RT-нагрузки."

  # === 1080p native (CPU difference visible) ===
  - id: "obs-5070-005"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "1920x1080"
      preset: "Ultra"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 112
    p1_fps: 82
    gpu_utilization: 85
    cpu_utilization: 62
    notes: "1080p: GPU utilisation падает до 85% — CPU начинает влиять. Но FPS всё ещё высокий."

  # === 4K native ===
  - id: "obs-5070-006"
    source_id: "agg"
    source_confidence: 0.88
    observation_quality: 0.85
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "3840x2160"
      preset: "High"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 48
    p1_fps: 34
    gpu_utilization: 99
    cpu_utilization: 28
    notes: "4K: 100% GPU-bound. CPU разница исчезает полностью."

  # === Competitive 1080p (CPU-bound сценарий) ===
  - id: "obs-5070-007"
    source_id: "agg"
    source_confidence: 0.85
    observation_quality: 0.82
    gpu: "nvidia-rtx-5070"
    cpu: "intel-core-i5-14600k"
    game: "CS2"
    game_version: "2025"
    config:
      resolution: "1920x1080"
      preset: "Competitive (Low)"
      rt: "Off"
      upscaler: "None"
      framegen: false
    avg_fps: 385
    p1_fps: 210
    gpu_utilization: 60
    cpu_utilization: 75
    notes: "Competitive 1080p — CPU-bound сценарий. Здесь разница CPU видна."
