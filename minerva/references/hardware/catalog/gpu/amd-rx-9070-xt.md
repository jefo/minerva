---
id: "amd-rx-9070-xt"
type: "gpu"
title: "AMD Radeon RX 9070 XT 16GB"
vendor: "amd"
status: "draft"
tags: ["amd", "rdna4", "navi48-xt", "full-die", "tsmc-n5", "256bit-honest-bus", "16gb-vram-safe", "infinity-cache-64mb", "pcie5.0-x16", "fsr4-ml-based", "rt-3rd-gen-improved", "280w-tbp", "2x8pin-power", "dp2.1-uhbr13.5", "4k-capable", "raster-leader", "rt-upper-mid", "local-llm-viable", "frametime-gaming-1440p", "best-fps-per-dollar-high-end"]
last_updated: "2026-06-03"
links:
  smaller_brother: "catalog/gpu/amd-rx-9070.md"
  competitor_nvidia: "catalog/gpu/nvidia-rtx-5070-ti.md"
  competitor_nvidia_high: "catalog/gpu/nvidia-rtx-5080.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "Navi 48 XT (RDNA 4, полный чип)"
  lithography: "TSMC N5 (5nm)"
  stream_processors: 6144
  compute_units: 96
  ray_accelerators: 96 (3-е поколение)
  ai_accelerators: 192
  boost_clock: "2.9 GHz (Game Clock ~2.55 GHz)"
  vram: "16 GB GDDR6 (256-bit)"
  vram_bandwidth: "640 GB/s"
  infinity_cache: "64 MB"
  tbp: "280W"
  power_connector: "2× 8-pin"
  pcie: "PCIe 5.0 x16"
  display_outputs: "3× DP 2.1 UHBR 13.5, 1× HDMI 2.1b"
  msrp_usd: "$599"
  engineering_notes: "Navi 48 XT — полный чип RDNA 4: 96 CU, 256-bit шина, 64MB Infinity Cache. 640 GB/s raw + кэш = эффективно 800-900 GB/s. Без узких мест для 4K. FSR 4 на 192 AI-акселераторах. Стратегия AMD: выиграть raster war и VRAM war — 16GB на 256-bit против 12GB на 192-bit у RTX 5070. RT улучшен на 80%, но Blackwell RT-ядра всё ещё на 40-50% быстрее в Path Tracing."
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
  min: 65990
  median: 75000
  max: 90000
  source: "price.ru (оценка)"
  date: "2026-06-03"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 16
  type: "GDDR6"
  bus_width_bit: 256
  bandwidth_gb_s: 640
clock_structured:
  boost_ghz: 2.9
  game_ghz: 2.55
cache:
  size_mb: 64
  type: "Infinity Cache"
compute:
  unit:
    type: "Stream Processor"
    count: 6144
  rt:
    type: "Ray Accelerator"
    count: 96
    generation: 3
  ml:
    type: "AI Accelerator"
    count: 192
    generation: 2
software:
  upscaler: "FSR 4"
  frame_gen: "AFMF 2"
  encoder: "AMF/VCE"
  compute_api: "ROCm"
  driver_features: ["SAM", "HYPR-RX"]

verdict: "Лучший FPS/₽ в high-end сегменте. 16GB и 256-bit — без компромиссов. В чистом растре дышит в спину RTX 5080 за $599 против $999. RT улучшен значительно (RDNA 4), но NVIDIA всё ещё впереди в Path Tracing. FSR 4 отличный, но DLSS 4 MFG — уникальное преимущество NVIDIA. Если RT не главный приоритет — лучшая покупка в $600-сегменте."
---

# AMD Radeon RX 9070 XT 16GB

## Архитектура и позиционирование

RX 9070 XT — флагман архитектуры RDNA 4 на полном чипе Navi 48 XT. Все 96 вычислительных блоков активированы, частоты максимальные, 256-битная шина с 16GB GDDR6. AMD не стала делать карту уровня RTX 5090 — RDNA 4 сфокусирована на сегменте до $600.

Позиционируется как карта для 4K-гейминга в чистом растре и 1440p с трассировкой лучей. Прямой вызов RTX 5070 Ti ($749) с аргументом «на $150 дешевле, а в растре быстрее».

**Стратегия AMD в RDNA 4:** не гнаться за флагманом NVIDIA, а выигрывать в сегментах $300–600 за счёт лучшего соотношения цены и производительности.

## Характеристики

- **GPU:** Navi 48 XT (RDNA 4, полный чип)
- **Техпроцесс:** TSMC N5 (5nm)
- **Потоковых процессоров:** 6144 (96 CU)
- **RT-ускорителей:** 96 (3-е поколение)
- **AI-ускорителей:** 192
- **Game Clock:** ~2.55 GHz
- **Boost Clock:** 2.9 GHz
- **VRAM:** 16 GB GDDR6
- **Шина:** 256-bit
- **Пропускная способность:** 640 GB/s
- **Infinity Cache:** 64 MB
- **TBP:** 280W
- **Питание:** 2× 8-pin
- **PCIe:** 5.0 x16
- **Видеовыходы:** 3× DisplayPort 2.1 UHBR 13.5, 1× HDMI 2.1b
- **MSRP (USD):** $599

## RDNA 4 — что реально улучшилось

- **RT 3-го поколения:** пропускная способность RT-блоков выросла в 1.8 раза. Cyberpunk 2077 RT Ultra 4K: RX 9070 XT ~32 FPS vs RX 7900 XT ~22 FPS — почти +50% в RT.
- **AI-ускорители:** выделенные блоки для FSR 4 (ML-based). Без них ML-апскейлинг был бы невозможен на уровне качества близком к DLSS.
- **Infinity Cache:** 64 MB кэша снижают зависимость от пропускной способности VRAM — эффективная пропускная способность ближе к 800–900 GB/s.
- **Энергоэффективность:** RDNA 4 на 25% эффективнее RDNA 3 на ватт в игровых нагрузках.

## Сравнение с конкурентами (Iron Man Argument)

### RX 9070 XT 16GB ($599) vs RTX 5070 Ti 16GB ($749)

**Где RX 9070 XT сильнее:**
- **Цена:** $599 vs $749 — разница $150 (20%). В РФ: ~75 000 ₽ vs ~98 000 ₽ — экономия 23 000 ₽.
- **Чистый растр (без RT/апскейлеров):** RX 9070 XT на 5–8% быстрее. Horizon Forbidden West 4K: RX 9070 XT ~82 FPS vs RTX 5070 Ti ~76 FPS. Call of Duty BO6 4K: RX 9070 XT ~120 FPS vs RTX 5070 Ti ~112 FPS. Cyberpunk 2077 Ultra 4K no RT: паритет (~65 FPS).
- **DisplayPort 2.1 UHBR 13.5:** полноценный стандарт для 4K 240Hz без DSC. NVIDIA DP 2.1b ограничен.
- **Питание 2× 8-pin:** нет проблем с 12V-2×6. Совместимость с любым качественным БП от 750W.
- **FSR 4 апскейлинг:** ML-based, качество близко к DLSS 4. Артефактов мало. Для 90% сценариев разница неразличима без стоп-кадров.
- **FPS/₽:** абсолютно лучший в high-end сегменте.

**Где RX 9070 XT слабее:**
- **Трассировка лучей:** RT-ускорители RDNA 4 прогрессировали, но RT-ядра Blackwell 4-го поколения всё ещё на 40–50% впереди в тяжёлых RT-нагрузках. Cyberpunk 2077 RT Overdrive 4K: RX 9070 XT ~32 FPS vs RTX 5070 Ti ~48 FPS. Alan Wake 2 Path Tracing: RX 9070 XT ~28 FPS vs RTX 5070 Ti ~42 FPS.
- **DLSS 4 MFG:** Multi Frame Generation (до 3 кадров) — уникальное преимущество NVIDIA. FSR 4 FG ограничен одним промежуточным кадром. В играх с поддержкой MFG NVIDIA ощущается плавнее.
- **CUDA-экосистема:** отсутствует. Для профессионалов (Blender, DaVinci Resolve с CUDA-эффектами, AI/ML) — RTX 5070 Ti в 1.5–2 раза быстрее в рабочих задачах.
- **NVENC vs AMF:** аппаратный кодировщик NVIDIA 9-го поколения лучше при низком битрейте. Для стримеров — аргумент в пользу NVIDIA.

### RX 9070 XT ($599) vs RTX 5080 ($999)

- **Чистый растр:** RX 9070 XT на 20–25% медленнее RTX 5080. Но за $599 против $999 — FPS/₽ у AMD в 1.5 раза лучше.
- **RT:** разрыв больше — 40–50%.
- **Смысл сравнения:** RTX 5080 за $999 — карта другой лиги по производительности. Но RX 9070 XT предлагает 75% производительности за 60% цены.
- **Вывод:** если RTX 5080 — Porsche, то RX 9070 XT — BMW M3. Медленнее в абсолюте, но удовольствие за деньги максимальное.

### Вердикт

- **4K чистый растр, FPS/₽ → RX 9070 XT.** Лучшая покупка в high-end. 23 000 ₽ экономии против RTX 5070 Ti.
- **4K RT, CUDA, стриминг → RTX 5070 Ti.** DLSS 4 MFG и RT-лидерство оправдывают переплату.
- **Если есть $1000 → RTX 5080.** Быстрее во всём, но FPS/₽ хуже.

## Российский рынок (июнь 2026)

- **Диапазон цен:** 65 990–90 000 ₽
- **Медиана:** ~75 000 ₽
- **Типичные модели:** Sapphire Nitro+, PowerColor Red Devil, XFX Mercury, ASRock Taichi

Рекомендация: Sapphire Nitro+ (~72 000 ₽) — лучший воздушный кулер среди Radeon. PowerColor Red Devil (~75 000 ₽) — для максимальной тишины. ASRock Taichi (~82 000 ₽) — переоценён без ощутимого прироста. XFX Mercury (~78 000 ₽) — достойный вариант.

## Для кого

**Подходит:**
- 4K-гейминг в чистом растре на высоких/ультра настройках
- 1440p ультра + RT (RT-ускорители RDNA 4 справляются)
- Лучший FPS/₽ в high-end сегменте
- Сборки Ryzen + Radeon (SAM)
- 16GB VRAM — запас на 4+ года
- Апгрейд с RX 6800 XT / RTX 3080 / RTX 4070

**Не подходит:**
- 4K Path Tracing — нужна NVIDIA (RTX 5070 Ti / 5080)
- Профессиональная работа с CUDA (Blender, AI/ML, Adobe)
- Стриминг с кодированием на GPU (NVENC объективно лучше)
- Игры с DLSS 4 MFG как обязательным требованием
- Владельцы RX 7900 XT — прирост в растре ~15%, RT ~50% (думайте)

## Источники

1. TechPowerUp — «AMD Radeon RX 9070 XT Review» (2025)
2. Hardware Unboxed — «RX 9070 XT vs RTX 5070 Ti vs RTX 5080: Ultimate Comparison»
3. Gamers Nexus — «RDNA 4 Navi 48 XT: RX 9070 XT Full Analysis»
4. Digital Foundry — «FSR 4 Image Quality & RX 9070 XT RT Performance»
5. AMD GPUOpen — RDNA 4 Architecture Whitepaper
6. Price.ru — рыночные цены, Москва (03.06.2026)
7. Собственное тестирование лаборатории
