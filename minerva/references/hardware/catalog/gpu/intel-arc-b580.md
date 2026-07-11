---
id: "intel-arc-b580"
type: "gpu"
title: "Intel Arc B580 12GB (Battlemage)"
vendor: "intel"
status: "draft"
tags: ["intel", "battlemage", "xez-hpg", "bmg-g21", "tsmc-5nm", "192bit", "12gb-vram", "gddr6", "pcie4.0-x8", "xess2", "xmx-engine", "190w-tbp", "8pin-power", "1440p-entry"]
last_updated: "2026-07-07"
external_audit_verification: planned
links:
  smaller_brother: "catalog/gpu/intel-arc-b570.md"
  competitor_nvidia: "catalog/gpu/nvidia-rtx-4060.md"
  competitor_amd: "catalog/gpu/amd-rx-7600.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "concepts/pcie-lanes.md"
  concept_power: "concepts/power-budget.md"
specs:
  gpu: "BMG-G21 (Battlemage Xe2-HPG)"
  lithography: "TSMC 5 nm (N5 EUV)"
  die_area_mm2: 272
  transistors_billion: 19.6
  xe_cores: 20
  execution_units: 128
  unified_shaders: 2560
  xmx_engines: 160
  rt_units: 20
  boost_clock: "2670 MHz (референс) / 2740 MHz (ASRock Challenger OC)"
  fp32_tflops: "13.67 (ref) / 14.03 (OC)"
  vram: "12 GB GDDR6 (192-bit)"
  vram_bandwidth: "456 GB/s"
  tbp: "190W"
  power_connector: "1× 8-pin"
  recommended_psu_w: 600
  pcie: "PCIe 4.0 x8"
  display_outputs: "1× HDMI 2.1a, 3× DisplayPort 2.1 (UHBR 13.5)"
  msrp_usd: "$249"
  launch_date: "2024-12-13"
engineering_notes: "BMG-G21 — монолитный чип Xe2-HPG второго поколения (Battlemage). 20 Xe2-ядер, 160 XMX Matrix Engines, 20 RT Units. Ключевые отличия от Alchemist: SIMD16 native execution (против SIMD8), выделенные RT-блоки на каждое Xe2-ядро (против общих), XeSS 2 с Frame Generation, DisplayPort 2.1 UHBR 13.5, +50-70% perf/W. PCIe 4.0 x8 — bandwidth не является bottleneck для 1440p гейминга. Известная проблема: CPU driver overhead на слабых CPU (ниже Ryzen 5 7600 / i5-13400) — падение производительности 10-20%. B580 — топовая модель B-серии; BMG-G31 (флагман) отменён. ASRock Challenger OC: заводской разгон 2740 MHz, dual-fan, 249×132×41 мм, цена РФ 28 000 ₽."
profiles:
  balanced_performance_gpu:
    power_envelope: "mid"
    capability_level: 1
    steel_man_desc: "Предсказуемое масштабирование производительности. Стандартные сборки ATX с БП 600–750W. Не требует специального охлаждения или инфраструктуры."
    failure_mode_desc: "Отсутствие специализации. Проигрывает enthusiast-картам в 4K, проигрывает low-power картам в SFF/тишине."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "streaming"]
    failure_for_intents: ["aaa_4k_path_tracing"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  tensor_matrix_accelerated:
    power_envelope: "mid"
    steel_man_desc: "XMX Matrix Engines — аппаратное ускорение INT8/FP16/BF16. XeSS (включая XeSS 2 с Frame Generation), локальный инференс небольших моделей."
    failure_mode_desc: "Традиционные FP32-вычисления без XMX. XMX-блоки простаивают — dark silicon при чистом растре."
    optimal_for_intents: ["llm_inference_7b", "ai_upscaling"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 28000
  median: 28000
  max: 32000
  source: "DNS / Ozon (ASRock Challenger OC)"
  date: "2026-07-07"

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 12
  type: "GDDR6"
  bus_width_bit: 192
  bandwidth_gb_s: 456
clock_structured:
  boost_ghz: 2.67
  game_ghz: null
cache:
  size_mb: null
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

observations:
  - id: "obs-b580-001"
    source_id: "user_verified"
    source_confidence: 0.95
    observation_quality: 0.95
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-5-225f"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 120
    notes: "Подтверждено пользователем. Паритет с RTX 5060 + DLSS 4.5 в этом сценарии."
  - id: "obs-b580-002"
    source_id: "user_verified"
    source_confidence: 0.90
    observation_quality: 0.90
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-5-225f"
    game: "Cyberpunk 2077: Phantom Liberty"
    game_version: "2.2 (2025)"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Medium"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: null
    notes: "Требует верификации. Оценка: 70-85 fps."

  - id: "obs-ag-b580-10"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Forza Horizon 5"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 163
    notes: "Ancient Gameplays YT (2026). 32GB DDR5 6400MHz. Frametime ~6.1ms."
  - id: "obs-ag-b580-11"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Ghost of Yōtei"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 112
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-12"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "God of War"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 127
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-13"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Hogwarts Legacy"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 105
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-14"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Kingdom Come: Deliverance II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 135
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-15"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "The Last of Us Part II"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 134
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-16"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Black Myth: Wukong"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 133
    notes: "Ancient Gameplays YT (2026)."
  - id: "obs-ag-b580-17"
    source_id: "ancient_gameplays"
    source_confidence: 0.85
    observation_quality: 0.85
    gpu: "intel-arc-b580"
    cpu: "intel-core-ultra-7-2700k"
    game: "Cyberpunk 2077"
    config:
      resolution: "2560x1440"
      preset: "High"
      rt: "Off"
      upscaler: "XeSS 3.0 Quality"
      framegen: false
    avg_fps: 113
    notes: "Ancient Gameplays YT (2026)."

---

# Intel Arc B580 12GB (Battlemage)

## Архитектура и позиционирование

Arc B580 — флагман B-серии на архитектуре Xe2-HPG «Battlemage». Построена на монолитном чипе BMG-G21 (TSMC 5 нм, 272 мм², 19.6 млрд транзисторов). Второе поколение дискретных GPU Intel: исправлены ключевые недостатки Alchemist — утилизация EU, RT-производительность, энергоэффективность.

Позиционируется как карта для 1440p-гейминга в сегменте $249 MSRP. Прямые конкуренты: RTX 5060 (8GB, ~$299) и RX 7600 (8GB, ~$269). Ключевое преимущество B580: **12GB VRAM** при более низкой цене. В паре с Ultra 5 225F: 1440p High + XeSS 3.0 Quality = **120 FPS в Cyberpunk 2077** — уровень RTX 5060 с DLSS 4.5.

В РФ: ASRock Challenger OC — 28 000 ₽. Вдвое дешевле RTX 5070 (65 000 ₽) при достижении целевых 120 FPS на High с XeSS. Идеальный sweet spot для 144Hz 1440p монитора: не премиум, но далеко не дно. Для архетипа «программист, который расслабляется в AAA по выходным» — находка.

**Важное ограничение:** CPU driver overhead. На процессорах слабее Ryzen 5 7600 / i5-13400 — падение производительности 10-20%. Ultra 5 225F — выше этого порога. ✓

## Характеристики

| Параметр | Arc B580 | ASRock Challenger OC |
|---|---|---|
| GPU | BMG-G21 (Xe2-HPG) | — |
| Техпроцесс | TSMC 5 нм | — |
| Xe2-ядер | 20 | — |
| XMX Engines | 160 | — |
| RT Units | 20 | — |
| Boost Clock | 2670 MHz | 2740 MHz |
| FP32 | 13.67 TFLOPS | 14.03 TFLOPS |
| VRAM | 12 GB GDDR6 | — |
| Шина | 192-bit | — |
| Пропускная способность | 456 GB/s | — |
| TBP | 190W | — |
| Питание | 1× 8-pin | — |
| PCIe | 4.0 x8 | — |
| Размеры | 272×115×45 мм (LE) | 249×132×41 мм |
| MSRP | $249 | 28 000 ₽ |

## Производительность

### 1440p Raster (без RT/апскейлеров)

| Игра | Preset | avg_fps | Источник |
|---|---|---|---|
| Cyberpunk 2077 | Ultra | **48** | Intel Media Deck |
| Alan Wake 2 | High | ~40-45* | Оценка |
| Hogwarts Legacy | Ultra | ~44* | Оценка |

*Требует верификации через TechPowerUp/GN review.

### 1440p RT + XeSS

Cyberpunk 2077 1440p Ultra RT + XeSS Performance: целевые 50-60 fps. XeSS 2 с Frame Generation дополнительно увеличивает плавность (input lag остаётся приемлемым для сюжетных AAA).

## Сравнение с конкурентами

### Arc B580 vs RTX 5070

| Параметр | Arc B580 | RTX 5070 | Разница |
|---|---|---|---|
| Цена (РФ) | 28 000 ₽ | 65 000 ₽ | **−57%** |
| VRAM | 12 GB | 12 GB | Паритет |
| TBP | 190W | 250W | −60W |
| 1440p Ultra (CP2077) | 48 fps | 87 fps | −45% |
| Питание | 1× 8-pin | 12V-2×6 | Проще |
| PCIe | 4.0 x8 | 5.0 x16 | Уже |

B580 стоит 43% цены RTX 5070 и даёт 55% её производительности. Для архетипа «достаточность > максимальность» — 48 fps native (или 60+ с XeSS) на 1440p Ultra в самой тяжёлой игре — достаточно.

### Arc B580 vs RTX 4060

| Параметр | Arc B580 | RTX 4060 |
|---|---|---|
| Цена (РФ) | 28 000 ₽ | 35 000+ ₽ |
| VRAM | **12 GB** | 8 GB |
| Шина | **192-bit** | 128-bit |
| 1440p | Комфортно | На пределе VRAM |

B580 выигрывает по VRAM и ширине шины — ключевые параметры для 1440p.

## Epistemic Notes

[^fact-1]: BMG-G21 — единственный геймерский чип Battlemage; флагман BMG-G31 отменён.
[^fact-2]: CPU driver overhead: падение 10-20% на CPU ниже Ryzen 5 7600. Ultra 5 225F — выше порога.
[^obs-1]: Наблюдения #001-003 требуют верификации через TechPowerUp/GN review.

## Источники

1. Intel ARK — Arc B580 Specifications
2. TechPowerUp GPU Database — Intel Arc B580
3. Intel Arc B580-B570 Media Deck (download.intel.com)
4. Gamers Nexus — Intel Arc B580 Battlemage GPU Review
5. TechSpot — Intel Arc B580 Re-Review (Jan 2025) — driver overhead
