---
id: "nvidia-rtx-5060"
type: "gpu"
title: "NVIDIA GeForce RTX 5060 8GB"
vendor: "nvidia"
status: "verified"
tags: ["nvidia", "blackwell", "gb206-cut", "tsmc-4n", "128bit-narrow-bus-gddr7", "12gb-vram-rumored", "gddr7", "pcie5.0-x8", "dlss4-mfg", "rt-4th-gen", "145w-tbp-silent", "1x8pin-power", "nvenc-9th-gen", "cuda-ecosystem", "1080p-only", "silent-viable", "frametime-gaming-1080p"]
last_updated: "2026-06-19"
links:
  bigger_brother: "catalog/gpu/nvidia-rtx-5060-ti.md"
  competitor_amd: "catalog/gpu/amd-rx-9060-xt.md"
  competitor_intel: "catalog/gpu/intel-arc-b580.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "GB206-250-A1 (Blackwell)"
  lithography: "TSMC 4N (5nm)"
  cuda_cores: 3840
  boost_clock: "2.50 GHz"
  vram: "8 GB GDDR7 (128-bit)"
  vram_bandwidth: "448 GB/s"
  tbp: "145W"
  power_connector: "1× 8-pin"
  pcie: "PCIe 5.0 x8"
  display_outputs: "3× DP 2.1b, 1× HDMI 2.1b"
  msrp_usd: "$299 (8GB)"
  engineering_notes: "GB206-250-A1 урезан (3840/4608 CUDA, -17%) на TSMC 4N. GDDR7 28 Gbps на 128-bit даёт 448 GB/s — bandwidth как у RTX 4060 Ti 16GB (288 GDDR6). GDDR7 компенсирует узость шины в 1080p. 145W TBP — холодная и тихая. 12GB-версия ожидается в RTX 50 SUPER refresh (конец 2026), на тех же чипах bandwidth не изменится. 8GB-версия за $299 — замануха: DLSS 4 снижает разрешение рендеринга, но текстуры требуют физический VRAM."
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
  min: 31990
  median: 35000
  max: 39000
  source: "price.ru (оценка)"
  date: "2026-06-19"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 8
  type: "GDDR7"
  bus_width_bit: 128
  bandwidth_gb_s: 448
clock_structured:
  boost_ghz: 2.50
  game_ghz: null
cache:
  size_mb: 24
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 3840
  rt:
    type: "RT Core"
    count: 30
    generation: 4
  ml:
    type: "Tensor Core"
    count: 120
    generation: 5
software:
  upscaler: "DLSS 4"
  frame_gen: "MFG"
  encoder: "NVENC 9th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

observations:
  - id: "obs-ag-rtx5060-18"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Forza Horizon 5"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 151
    notes: "Ancient Gameplays YT (2026). 32GB DDR5 6400MHz."
  - id: "obs-ag-rtx5060-19"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Ghost of Yōtei"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 105
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-20"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "God of War"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 119
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-21"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Hogwarts Legacy"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 96
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-22"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Kingdom Come: Deliverance II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 125
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-23"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "The Last of Us Part II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 127
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-24"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Black Myth: Wukong"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 123
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-rtx5060-25"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "nvidia-rtx-5060"
    cpu: "intel-core-ultra-7-2700k"
    game: "Cyberpunk 2077"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "DLSS 4.5 Quality"
      framegen: false
    avg_fps: 104
    notes: "Ancient Gameplays YT (2026)."

verdict: "Самый доступный вход в экосистему Blackwell. 8GB VRAM — осознанный компромисс: DLSS 4 спасает в играх, но текстуры будущего требуют больше памяти. 12GB-версия ожидается в RTX 50 SUPER refresh (конец 2026). В чистом растре RX 9060 XT 16GB даст больше за те же деньги."
---

# NVIDIA GeForce RTX 5060

## Архитектура и позиционирование

RTX 5060 — младшая карта линейки Blackwell на урезанном чипе GB206-250-A1. Тот же кристалл что у RTX 5060 Ti, но с отключённой частью вычислительных блоков. Техпроцесс TSMC 4N — зрелый 5nm-класс, обеспечивающий хорошую энергоэффективность.

Позиционируется NVIDIA как «народная» карта для 1080p с поддержкой DLSS 4 и Multi Frame Generation. Версия с 12GB VRAM ожидается в RTX 50 SUPER refresh (конец 2026) — на старте доступна только 8GB.

**Отличие от RTX 5060 Ti:** на ~17% меньше CUDA-ядер (3840 vs 4608), чуть ниже частоты, TBP снижен до 145W. Чип тот же — GB206.

## Характеристики

- **GPU:** GB206-250-A1 (Blackwell)
- **Техпроцесс:** TSMC 4N (5nm)
- **CUDA-ядер:** 3840
- **Тензорных ядер:** 120 (5-е поколение)
- **RT-ядер:** 30 (4-е поколение)
- **Boost Clock:** 2.50 GHz
- **VRAM:** 8 GB GDDR7
- **Шина:** 128-bit
- **Пропускная способность:** 448 GB/s
- **L2-кэш:** 24 MB
- **TBP:** 145W
- **Питание:** 1× 8-pin
- **PCIe:** 5.0 x8
- **Видеовыходы:** 3× DisplayPort 2.1b, 1× HDMI 2.1b
- **MSRP (USD):** $299 (8GB)

## 8GB сейчас, 12GB в будущем

RTX 5060 на старте вышла только в конфигурации 8 GB GDDR7. NVIDIA анонсировала RTX 50 SUPER refresh на конец 2026 — в его рамках ожидается версия с 12GB. Текущая ситуация:

- **8GB в 2026:** уже недостаточно для максимальных текстур в ряде AAA-тайтлов (Indiana Jones, Hogwarts Legacy, The Last of Us Part I). Текстуры «средние» вместо «ультра» — компромисс, заметный глазу.
- **12GB (ожидается):** запас на 2–3 года вперёд. Даже в 4K с DLSS Performance карта не упрётся в VRAM (ограничителем будет производительность чипа, а не память). Цена не объявлена.
- **DLSS 4 частично маскирует проблему 8GB:** внутреннее разрешение ниже → меньше VRAM под буфер кадра. Но текстуры высокого разрешения всё равно требуют места.

**Вывод:** 8GB сегодня — компромисс для бюджетных сборок. 12GB появится в RTX 50 SUPER refresh и станет более сбалансированным вариантом.

## Энергопотребление и нагрев

- **TBP 145W** — на 35W ниже RTX 5060 Ti. Карта холодная и тихая даже с простыми кулерами.
- **Питание:** 1× 8-pin — совместимость с любым блоком питания от 450W.
- **Реальные замеры:** большинство AIB-моделей укладываются в 145–155W.
- **Простой:** ~8W — отлично.

## Сравнение с конкурентами (Iron Man Argument)

### NVIDIA RTX 5060 8GB vs AMD RX 9060 XT 16GB

**Где RTX 5060 сильнее:**
- **DLSS 4 + Multi Frame Generation:** MFG генерирует до 3 промежуточных кадров — картинка плавнее чем FSR 4 FG (1 кадр). В Cyberpunk 2077 с RT + MFG воспринимаемая плавность выше, даже при меньшем базовом FPS.
- **Трассировка лучей:** RT-ядра Blackwell 4-го поколения. В Alan Wake 2 RT Medium 1080p: RTX 5060 ~55 FPS vs RX 9060 XT ~38 FPS (+45%).
- **CUDA-экосистема:** Blender, DaVinci Resolve, Adobe Premiere — CUDA работает сразу и без проблем. ROCm у AMD улучшается, но всё ещё догоняет.
- **Энергоэффективность:** 145W vs ~200W — карта холоднее и тише.
- **Драйверы:** NVIDIA Game Ready — эталон стабильности. AMD Adrenalin improved но occasional issues в DX11.

**Где RTX 5060 слабее:**
- **Чистый растр (без RT, без апскейлеров):** RX 9060 XT с 16GB и 128-bit шиной объективно быстрее на 10–15% в raster-only сценариях. В Call of Duty, Apex Legends, Valorant — AMD впереди.
- **VRAM:** 8GB vs 16GB — RX 9060 XT имеет запас для 4K-текстур и моддинга. Разница проявится уже сейчас в тяжёлых тайтлах.
- **Цена:** RX 9060 XT 16GB ожидается по ~$349–379 — на $50–80 дороже RTX 5060 8GB, но с вдвое большей памятью.
- **DisplayPort 2.1:** у AMD полноценный UHBR 13.5; у NVIDIA — DP 2.1b с ограниченной пропускной способностью (зависит от AIB).

### NVIDIA RTX 5060 vs Intel Arc B580

- **RTX 5060 (8GB) $299 vs B580 (12GB) $249 — разница $50 (20%).**
- B580 выигрывает FPS/₽ безусловно. Но проигрывает в RT (~30% weaker), не имеет DLSS 4 (XeSS 2 хорош, но не дотягивает), драйверы слабее для DX9/11.
- Если бюджет жёсткий и игры современные (DX12/Vulkan) → B580. Если нужны RT, стриминг NVENC, работа с CUDA → RTX 5060.

## Российский рынок (июнь 2026)

- **Диапазон цен (8GB):** 32 000–39 000 ₽
- **Медиана:** ~35 000 ₽
- **Типичные модели:** Palit Dual, Gigabyte Windforce, MSI Ventus 2X, ASUS Dual

Рекомендация: Palit Dual 8GB по ~33 000 ₽ — оптимально. MSI Ventus 2X переоценён для карты такого класса.

## Для кого

**Подходит:**
- 1080p-гейминг на высоких/ультра настройках (с оговоркой на 8GB VRAM)
- Киберспорт с запасом под 144Hz мониторы
- Апгрейд с GTX 1060/1660/RTX 2060 — качественный скачок
- Бюджетные рабочие станции (CUDA для хобби-проектов)
- Сборки с ограничением по мощности БП (145W — очень низко)

**Не подходит:**
- 1440p-гейминг на ультра (нужна RTX 5060 Ti 16GB минимум)
- 4K в любом виде (RTX 5070 Ti / 5080)
- Игры с трассировкой путей (Path Tracing) — слишком слабый чип
- Профессиональный 3D-рендеринг (мало ядер, 128-bit шина)
- Долгосрочная investment (5+ лет) — лучше доплатить за 16GB

## Источники

1. TechPowerUp — спецификации NVIDIA GB206 (Blackwell)
2. Gamers Nexus — «RTX 5060 Series Review» (2025)
3. Hardware Unboxed — «RTX 5060 vs RX 9060 XT Benchmark»
4. Digital Foundry — «DLSS 4 Multi Frame Generation Analysis»
5. Price.ru — рыночные цены, Москва (19.06.2026)
6. Собственное тестирование лаборатории
