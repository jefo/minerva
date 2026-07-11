---
id: "epistemological-profiles"
type: "concept"
title: "PCBO Epistemological Profiles Dictionary v3.3"
status: "verified"
last_updated: "2026-06-03"
generation: "Blackwell / RDNA 4 / Battlemage / Zen 5 / Arrow Lake (2025–2026)"
---

# PCBO Epistemological Profiles Dictionary v3.3

## Принципиальные изменения относительно v3.2

1. **MECE power envelopes** — exhaustive разбиение TGP/TDP, исключающее «провалы»
   между категориями. Пороги — не магические числа, а **reference points**,
   привязанные к характеристикам текущего поколения.
2. **Reference points** — документированные точки отсчёта. Каждый порог
   обоснован конкретным компонентом из актуальной линейки.
3. **Normative profiles** — профили для «архитектурной нормы» (компонентов без
   экстремальных характеристик). Закрывают пробел «здоровый человек без
   диагноза».
4. **failure_type** — LINEAR_DEGRADATION (допустимый TradeOff) vs CLIFF_DROP
   (жёсткий BLOCK независимо от веса интента).

---

## Reference Points (точки отсчёта)

Каждый порог power envelope привязан к конкретному компоненту текущего поколения.
При смене поколения reference points обновляются — пороги двигаются автоматически.

### GPU Reference Points (Blackwell / RDNA 4 / Battlemage, 2025–2026)

```yaml
gpu_reference_points:
  low_tdp_boundary:
    value: 150W
    anchor: "RTX 5060 (GB206) — самая холодная карта Blackwell. 150W TBP."
    note: "Карты на этом уровне и ниже: пассивное охлаждение достаточно, БП 450W."
  high_tdp_boundary:
    value: 280W
    anchor: "RTX 5070 Ti (GB205) / RX 9070 XT (Navi 48 XT) — вход в энтузиаст-класс. 280W."
    note: "Карты от этого уровня: 12V-2×6 или 2×8-pin, БП 750W+, активный продув корпуса."
  generation: "Blackwell / RDNA 4 / Battlemage (2025–2026)"
```

### CPU Reference Points (Zen 4/5 / Arrow Lake, 2025–2026)

```yaml
cpu_reference_points:
  low_tdp_boundary:
    value: 65W
    anchor: "Ryzen 5 7500F / Ryzen 7 7700 / Core Ultra 5 225F — стандартный TDP 65W."
    note: "65W и ниже: любая башня за $40, пассивный режим вентиляторов корпуса."
  high_tdp_boundary:
    value: 120W
    anchor: "Ryzen 7 7800X3D (120W) / Core Ultra 9 285K (125W) — верхняя граница 'потребительского' TDP."
    note: "120W+: СЖО или двухбашенный кулер, активный airflow. Выше 170W — HEDT-территория."
  generation: "Zen 4/5 / Arrow Lake (2025–2026)"
```

---

## Power Envelopes (MECE-разбиение)

Исчерпывающее разбиение TGP/TDP на три класса. Гарантия: любой компонент с
известным TDP попадает ровно в один envelope. Без дырок.

### GPU Power Envelopes

```yaml
gpu_power_envelope_low:
  criteria: "TGP < 150W"
  description: "Низкое энергопотребление. Пассивное охлаждение достаточно, БП 450W+."

gpu_power_envelope_mid:
  criteria: "150W ≤ TGP < 280W"
  description: "Среднее энергопотребление. Стандартные сборки ATX, БП 550–750W."

gpu_power_envelope_high:
  criteria: "TGP ≥ 280W"
  description: "Высокое энергопотребление. 12V-2×6 или 2×8-pin, БП 750W+, активный продув."
```

### CPU Power Envelopes

```yaml
cpu_power_envelope_low:
  criteria: "TDP < 65W"
  description: "Сверхнизкое. Пассивное охлаждение, no-fan режим."

cpu_power_envelope_mid:
  criteria: "65W ≤ TDP < 120W"
  description: "Стандартное. Любая башня за $40, тихая работа."

cpu_power_envelope_high:
  criteria: "TDP ≥ 120W"
  description: "Высокое. СЖО или двухбашенный кулер, активный airflow."
```

---

## Схема профиля (YAML Schema v4.0 — ISO 15288 / SysML Satisfy)

```yaml
profiles:
  profile_name:
    criteria_met: true|false           # per-component
    power_envelope: "low"|"mid"|"high" # ссылка на MECE-envelope
    capability_level: 1|2|3            # уровень способности (DoDAF CV-2)
    # --- LLM layer ---
    steel_man_desc: "..."              # что компонент делает лучше всех
    failure_mode_desc: "..."           # чем жертвует
    # --- Python layer ---
    optimal_for_intents: ["intent_a"]
    failure_for_intents: ["intent_x"]
    failure_severity: "WARN"|"BLOCK"
    failure_type: "LINEAR_DEGRADATION"|"CLIFF_DROP"
```

### Requirement Satisfaction with Margin Analysis (v4.0)

**Основание:** ISO/IEC/IEEE 15288:2023 §6.4.3 (System Requirements Definition),
§6.4.9 (Verification); SysML Clause 16 «satisfy» relationship;
NASA SE Handbook §4.2.1.6 (Gold Plating).

**Модель:**

Интент определяет **minimum capability requirement** — минимальный уровень
способности, необходимый для выполнения задачи. Компонент либо **satisfies**
требование, либо нет. Это бинарное отношение (SysML `«satisfy»`).

```
Компонент:
  capability_level = N (tier из профиля)

Интент:
  min_capability = M (минимально допустимый уровень)

Оценка (Verification per ISO 15288 §6.4.9):
  margin = N − M

  margin < 0  → FAIL (BLOCK): компонент недостаточен
  margin = 0  → SATISFIES (optimal): точно соответствует требованию
  margin > 0  → SATISFIES WITH EXCESS MARGIN (WARN):
                 gold plating risk (NASA §4.2.1.6).
                 Компонент функционально подходит, но имеет избыточный запас —
                 переплата, излишний нагрев, сложность.
                 MAUT оценит, оправдан ли избыток.

  Satisficing (Simon, 1956): поиск останавливается на первом
  компоненте с margin ≥ 0. Дальнейшее увеличение margin не повышает
  utility (Keeney & Raiffa, 1976: ∂U/∂x ≈ 0 за пределами satisficing threshold).
```

**Пример для AAA-гейминга:**
- 1080p: min_capability = `mainstream_efficiency_gpu` (level 1)
  → RTX 5060 (L1): margin=0 → SATISFIES ✅
  → RTX 5070 (L2): margin=+1 → SATISFIES WITH EXCESS MARGIN ⚠️ (gold plating: overkill для 1080p)
- 1440p: min_capability = `balanced_performance_gpu` (level 2)
  → RX 9070 (L2): margin=0 → SATISFIES ✅
  → RTX 5070 Ti (L3): margin=+1 → SATISFIES WITH EXCESS MARGIN ⚠️ (избыточен, но допустим)
- 4K: min_capability = `enthusiast_unrestricted_gpu` (level 3)
  → RTX 5080 (L3): margin=0 → SATISFIES ✅
  → RTX 5090 (L3): margin=0 → SATISFIES ✅
  → Примечание: RTX 5090 имеет тот же capability level что 5080, но MAUT
    выявит переплату через вес цены/TGP в функции полезности —
    не через margin analysis.

### Capability Levels (DoDAF CV-2 taxonomy)

```yaml
gpu_capability_levels:
  1: "mainstream_efficiency_gpu"       # TGP < 150W, 1080p
  2: "balanced_performance_gpu"        # TGP 150-280W, 1440p
  3: "enthusiast_unrestricted_gpu"     # TGP ≥ 280W, 4K
```

### Отличие от v3.4 (profile_range — удалён)

| v3.4 (ad-hoc) | v4.0 (ISO 15288 / SysML) |
|---|---|
| `profile_range: {min, max}` — два порога | `min_capability` — один порог (satisficing threshold) |
| «Выше max» = WARN (второй порог) | margin > 0 = WARN (gold plating) — без второго порога |
| RTX 5090 для 4K: WARN (max=enthusiast) | RTX 5090 для 4K: margin=0 → SATISFIES, MAUT оценит цену |
| Ad-hoc изобретение | Стандартная модель SysML/ISO 15288 |

### Capability Levels — все типы компонентов (v4.1)

```yaml
gpu_capability_levels:
  1: "mainstream_efficiency_gpu"       # TGP < 150W, 1080p
  2: "balanced_performance_gpu"        # TGP 150-280W, 1440p
  3: "enthusiast_unrestricted_gpu"     # TGP ≥ 280W, 4K

cpu_capability_levels:
  1: "budget_efficiency_cpu"           # 6 ядер, 65W (Ryzen 5 7500F / Core Ultra 5 225F)
  2: "balanced_multicore_cpu"          # 8 ядер, 65-105W (Ryzen 7 7700 / Core Ultra 7 265K)
  3: "high_core_count_cpu"             # 12-16 ядер, 120W+ (Ryzen 9 7950X / Core Ultra 9 285K)

ram_capability_levels:
  1: "jedec_native_safe"               # JEDEC 5200, базовые тайминги — стабильность > скорость
  2: "standard_ddr5_xmp"               # XMP/EXPO 6000 CL30 — стандарт для игр и работы
  3: "high_frequency_low_latency"      # 6400+ CL32 — overclocking, esports, scientific

storage_capability_levels:
  1: "dram_less_hmb_cached"            # Клиентский SSD без sustained write
  2: "standard_tlc_dram_ssd"           # TLC + DRAM — sustained write ≥ 1.5 GB/s
  3: "gen5_high_bandwidth"             # PCIe 5.0, >10 GB/s — video_editing_8k

mb_capability_levels:
  1: "budget_platform"                 # mATX, базовый VRM, 1-2 M.2 (B650M)
  2: "mainstream_platform"             # ATX, хороший VRM, 2-3 M.2, ECC (B850)
  3: "enthusiast_platform"             # ATX, флагманский VRM, 4 M.2, no bifurcation (X870/X670E)

psu_capability_levels:
  1: "atx_2x_budget_reliable"          # 650W, без ATX 3.0 — офис, бюджетные сборки
  2: "atx_3x_transient_capable"        # 750W+, ATX 3.0/3.1 — стандарт для GPU ≥ 200W
  3: "high_wattage_enthusiast"         # 1000W+, ATX 3.1 — multi-GPU, экстремальный разгон

cooling_capability_levels:
  1: "air_tower_standard"              # Башенный кулер, до 150W TDP
  2: "air_tower_high_tdp"              # Двухбашенный, до 250W TDP
  3: "aio_liquid_standard"             # 240-280mm AIO, до 300W TDP
  4: "aio_liquid_high_tdp"             # 360mm+, >300W — HEDT, разгон

case_capability_levels:
  1: "budget_mesh"                     # Mesh-панель, 4 вентилятора — достаточный airflow
  2: "sound_dampened_thermal_trap"     # Шумоподавление, ограниченный airflow
  3: "premium_airflow"                 # Mesh + фильтры + тихие вентиляторы — silent build
```

---

## Профили GPU

### НОРМА: balanced_performance_gpu
**Назначение:** стандартная видеокарта без экстремальных характеристик.
Архитектурная норма для power_envelope_mid (150–280W).

```yaml
balanced_performance_gpu:
  power_envelope: "mid"
  steel_man_desc: "Предсказуемое масштабирование производительности. Стандартные сборки ATX с БП 600–750W. Не требует специального охлаждения или инфраструктуры."
  failure_mode_desc: "Отсутствие специализации. Проигрывает enthusiast-картам в 4K, проигрывает low-power картам в SFF/тишине. Не имеет выдающихся черт — просто хорошо делает всё."
  optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "streaming"]
  failure_for_intents: ["aaa_4k_path_tracing"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: bandwidth_constrained_vram_rich
```yaml
bandwidth_constrained_vram_rich:
  power_envelope: "mid"  # обычно
  steel_man_desc: "Локальный инференс LLM (7B–13B Q4_K_M). Карта позволяет загрузить модель полностью в VRAM без offload. Интерактивная скорость > 30 t/s."
  failure_mode_desc: "Нативный 4K-гейминг на ультра. Узкая 128-bit шина становится bottleneck: fillrate падает, texture pop-in, фризы — даже при заполнении VRAM наполовину."
  optimal_for_intents: ["llm_inference_7b", "llm_inference_13b"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

### НОРМА: mainstream_efficiency_gpu
```yaml
mainstream_efficiency_gpu:
  power_envelope: "low"
  steel_man_desc: "Массовые игровые ПК: 1080p/1440p. БП 450–550W. Минимальные требования к вентиляции, низкий шум, SFF-совместимость."
  failure_mode_desc: "Нативный 4K-гейминг. Недостаток вычислительных блоков не позволяет 60 FPS — снижение до Medium/Low. AAA 1440p на ультра — на пределе."
  optimal_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "silent_build", "sff_build", "office_productivity"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing"]
  failure_severity: "BLOCK"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: enthusiast_unrestricted_gpu
```yaml
enthusiast_unrestricted_gpu:
  power_envelope: "high"
  steel_man_desc: "Нативный 4K-гейминг на максималках, профессиональный рендеринг, высокопроизводительный AI-инференс. 12V-2×6, БП 750W+."
  failure_mode_desc: "Компактные корпуса с плохой вентиляцией. 300–500W тепла → 55°C внутри → перегрев CPU и троттлинг всей системы."
  optimal_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_inference_20b", "video_editing_8k"]
  failure_for_intents: ["silent_build", "sff_build"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

### ЭКСТРЕМУМ: transient_spike_heavy
```yaml
transient_spike_heavy:
  power_envelope: "high"
  steel_man_desc: "Динамичный 3D-рендеринг и гейминг с резким изменением сложности сцены. Мгновенный переход в P-state без микрофризов."
  failure_mode_desc: "БП ATX 2.4 без ATX 3.0. Микросекундный скачок тока триггерит OCP/OPP → аварийное выключение (чёрный экран). Требуется БП с ATX 3.0/3.1."
  optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "3d_rendering_gpu"]
  failure_for_intents: ["sff_build"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

### ЭКСТРЕМУМ: sub_75w_slot_powered
```yaml
sub_75w_slot_powered:
  power_envelope: "low"
  steel_man_desc: "Апгрейд офисных ПК (Dell, HP) с проприетарными БП ≤ 240W без кабелей GPU. 1U-серверы."
  failure_mode_desc: "Гейминг ≥ 1080p с DX12. Лимит 75W заставляет сбрасывать частоты до минимума — FPS падает до неиграбельных."
  optimal_for_intents: ["office_productivity", "home_server_24_7"]
  failure_for_intents: ["aaa_1080p_ultra", "aaa_1440p_high", "esports_1080p_240hz"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

### УНИВЕРСАЛЬНЫЕ (не привязаны к power envelope)
```yaml
hardware_rt_accelerated_gen_3:
  steel_man_desc: "Path Tracing в реальном времени, архитектурная визуализация (Octane/Cycles). ×4–5 ускорение vs растеризация."
  failure_mode_desc: "DX11/OpenGL игры. RT-блоки простаивают — dark silicon, за который уплачено."
  optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"

tensor_matrix_accelerated:
  steel_man_desc: "Локальное обучение/инференс, Stable Diffusion, DLSS/XeSS. Матричное перемножение на тензорных ядрах в разы быстрее FP32."
  failure_mode_desc: "Традиционные FP32-вычисления без матричной математики. Тензорные блоки простаивают — паразитный нагрев."
  optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"

hbm_stacked_bus:
  steel_man_desc: "Сверхтяжёлые параллельные вычисления: обучение нейросетей, научные HPC. Объём данных/сек важнее объёма памяти."
  failure_mode_desc: "Коммерческий гейминг. Экстремальная стоимость интерпозера + риск термического повреждения. Экономически нецелесообразно."
  optimal_for_intents: ["llm_training_lora", "scientific_computing"]
  failure_for_intents: ["aaa_4k_ultra", "esports_1080p_240hz", "office_productivity"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"

multi_gpu_interconnect_capable:
  steel_man_desc: "Локальное обучение LLM >70B. Объединение VRAM 2+ карт в единый пул (NVLink ≥ 112 ГБ/с)."
  failure_mode_desc: "Потребительский гейминг. SLI/Multi-GPU удалены из игровых движков. Вторая карта простаивает, перекрывая airflow."
  optimal_for_intents: ["llm_training_lora", "llm_inference_20b"]
  failure_for_intents: ["aaa_4k_ultra", "esports_1080p_240hz", "aaa_1440p_high"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

---

## Профили CPU

### НОРМА: balanced_monolithic_norm
```yaml
balanced_monolithic_norm:
  power_envelope: "mid"
  steel_man_desc: "Универсальный процессор: 6–8 ядер, единый кристалл (1 CCD), TDP 65–105W. Игры, разработка, офис — всё на хорошем уровне без специализации."
  failure_mode_desc: "Отсутствие 3D V-Cache — проигрыш X3D в киберспорте на 15–25% по 1% Low. Отсутствие E-ядер — фоновая многозадачность менее эффективна."
  optimal_for_intents: ["software_development", "office_productivity", "aaa_1080p_ultra", "aaa_1440p_high", "streaming"]
  failure_for_intents: ["esports_1080p_360hz"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: cache_dominant_gaming
```yaml
cache_dominant_gaming:
  power_envelope: "high"
  steel_man_desc: "Киберспорт 1080p на низких настройках. 3D V-Cache (L3 ≥ 96MB) минимизирует CPU frame time — 1% Low FPS стабильно выше 240/360 Hz."
  failure_mode_desc: "Тяжёлые многопоточные FP32/AVX-512: 3D-рендеринг, компиляция. Тепловое сопротивление bonding layer 3D-кэша снижает частоту на 300–500 МГц. Штраф 15–20%."
  optimal_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz"]
  failure_for_intents: ["3d_rendering_cpu", "heavy_compilation", "scientific_computing"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: multi_ccd_disaggregated
```yaml
multi_ccd_disaggregated:
  power_envelope: "high"
  steel_man_desc: "Параллельные многопоточные вычисления: 3D-рендеринг, компиляция больших проектов. 12–16 ядер на потребительской платформе без HEDT-тарифа."
  failure_mode_desc: "Игры и реалтайм-задачи. Межчиплетная задержка (≥ 70 нс inter-CCD) вызывает frametime spike при перебросе потока между CCD."
  optimal_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: dense_thermal_concentration
```yaml
dense_thermal_concentration:
  power_envelope: "mid"
  steel_man_desc: "Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту до того как тепло преодолеет сопротивление IHS — максимальный буст на 2–3 секунды."
  failure_mode_desc: "Длительная нагрузка (рендеринг, компиляция). Тепловое сопротивление толстой IHS (≥ 1.7 мм) → температура мгновенно 89–95°C даже под СЖО 360мм. Thermal throttling 5–8%."
  optimal_for_intents: ["office_productivity", "software_development"]
  failure_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation", "silent_build"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: hybrid_asymmetric_efficiency
```yaml
hybrid_asymmetric_efficiency:
  power_envelope: "mid"  # или high — зависит от модели
  steel_man_desc: "Стриминг + фоновая многозадачность. E-ядра разгружают P-ядра: OBS/Discord на E-ядрах, игра на P-ядрах. Стабильный frametime."
  failure_mode_desc: "Среды без аппаратного планировщика (старые ОС, Linux без Intel Thread Director). Потоки реального времени могут попасть на слабые E-ядра — падение ×2–3."
  optimal_for_intents: ["streaming", "software_development", "video_editing_4k"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: hedt_multi_channel
```yaml
hedt_multi_channel:
  power_envelope: "high"
  steel_man_desc: "ML-станции с 3–4 GPU, серверы виртуализации, CFD/FEA. Дополнительные каналы памяти снимают bandwidth bottleneck."
  failure_mode_desc: "Потребительские нагрузки. Высокий idle power (≥ 90W платформа), NUMA-латентность снижает FPS в играх."
  optimal_for_intents: ["llm_training_lora", "scientific_computing", "virtualization", "llm_inference_20b"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz", "office_productivity", "silent_build"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

### УНИВЕРСАЛЬНЫЙ: sub_5nm_lithography
```yaml
sub_5nm_lithography:
  steel_man_desc: "Компактные ITX-сборки с жёстким лимитом энергопотребления. Максимальная производительность на ватт."
  failure_mode_desc: "Повышенная чувствительность к деградации кремния при статическом напряжении. Разгон с V > 1.35 В → ускоренная электромиграция."
  optimal_for_intents: ["sff_build", "silent_build"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

---

## Профили Storage

### НОРМА: standard_tlc_dram_ssd
```yaml
standard_tlc_dram_ssd:
  steel_man_desc: "Стандартный NVMe SSD с DRAM-кэшем. Предсказуемая производительность под любой нагрузкой: игры, ОС, разработка."
  failure_mode_desc: "Цена на 20–30% выше DRAM-less аналогов при сравнимых скоростях в клиентских сценариях."
  optimal_for_intents: ["software_development", "video_editing_4k", "data_engineering", "office_productivity"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: dram_less_hmb_cached
```yaml
dram_less_hmb_cached:
  steel_man_desc: "Клиентская ОС: браузер, игры. Короткие записи до 20–30 ГБ поглощаются SLC-кэшем — скорости уровня премиум-дисков при цене на 30–40% ниже."
  failure_mode_desc: >
    Два механизма отказа под sustained нагрузкой:
    (1) Производительность: после исчерпания SLC-кэша — задержки до 40 мс,
    скорость ≤ 350 МБ/с (уровень SATA III). Непрерывная многопоточная запись
    (СУБД, Spark shuffle) — критическое падение.
    (2) Ресурс (HIGH WRITE AMPLIFICATION): контроллер без DRAM не держит
    таблицу FTL в быстрой памяти → постоянная перезапись служебных блоков
    NAND при каждом мелком IO. Фактический TBW исчерпывается в 3–5 раз
    быстрее паспортного. Под системными логами СУБД — деградация и выход
    из строя через 6–12 месяцев.
  optimal_for_intents: ["office_productivity", "software_development", "aaa_1080p_ultra"]
  failure_for_intents: ["video_editing_4k", "video_editing_8k", "data_engineering"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

---

## Профили Motherboard

```yaml
bifurcation_shared_lanes:
  steel_man_desc: "Высокоплотные дисковые хранилища: 3–4 диска Gen4 NVMe в RAID-0. Скорость дисковой подсистемы важнее bandwidth GPU."
  failure_mode_desc: "Локальные AI-вычисления с RAM offload. Падение слота x16 → x8 урезает bandwidth PCIe с 32 до 16 ГБ/с — инференс в 2 раза медленнее."
  optimal_for_intents: ["video_editing_4k", "data_engineering", "virtualization"]
  failure_for_intents: ["llm_inference_13b", "llm_inference_20b", "llm_training_lora"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

---

## Профили RAM

### НОРМА: standard_ddr5_xmp
```yaml
standard_ddr5_xmp:
  steel_man_desc: "DDR5 с XMP/EXPO-профилем (5600–6000 MT/s). Оптимальный баланс цены и производительности для игр и рабочих станций."
  failure_mode_desc: "JEDEC-совместимость не гарантирована на всех платах. При сбросе BIOS память уходит на 4800 MT/s — потеря 10–15% FPS до повторной активации XMP."
  optimal_for_intents: ["aaa_1440p_high", "esports_1080p_240hz", "software_development"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: jedec_native_safe
```yaml
jedec_native_safe:
  steel_man_desc: "Серверы, рабочие станции 24/7. Базовые спецификации JEDEC (DDR5-4800/5200, 1.1V, CL40). Стабильность — приоритет №1. Нулевой уровень soft-bit errors."
  failure_mode_desc: "Киберспорт с FPS > 200. Latency > 85 нс ограничивает 1% Low — GPU простаивает на 20–30% в ожидании данных."
  optimal_for_intents: ["home_server_24_7", "scientific_computing", "virtualization", "data_engineering"]
  failure_for_intents: ["esports_1080p_240hz", "esports_1080p_360hz", "aaa_1440p_high"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"

### ЭКСТРЕМУМ: ddr5_6400_uclk_instability
```yaml
ddr5_6400_uclk_instability:
  steel_man_desc: "DDR5-6400 на Hynix A-die — максимальная пропускная способность на AM5. В играх с высокими требованиями к bandwidth (MSFS 2024, Star Citizen) даёт +5-7% FPS при ручном тюнинге."
  failure_mode_desc: "AMD AM5: контроллер памяти (UCLK) нестабилен в синхронном режиме 1:1 выше 6000 MT/s. Принудительный переход в режим 1:2 (UCLK=MCLK/2) после 6200 MT/s — латентность возрастает на 12-15 нс, прирост bandwidth нивелируется. Intel: стабильный Gear 2, но выигрыш над 6000 CL30 минимален."
  optimal_for_intents: ["esports_1080p_360hz", "scientific_computing"]
  failure_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "software_development"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

---

## Профили Case

```yaml
sound_dampened_thermal_trap:
  steel_man_desc: "Сборки средней мощности (TDP ≤ 200W). Полное поглощение писка дросселей и шелеста вентиляторов. Абсолютная тишина в простое."
  failure_mode_desc: "Системы > 400W. Узкие воздухозаборники → 50–55°C внутри → вентиляторы на 80% PWM → шум превышает открытый mesh-корпус."
  optimal_for_intents: ["silent_build", "office_productivity", "home_server_24_7"]
  failure_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_training_lora"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

---

## Контролируемый словарь интентов

| Intent ID | Категория | Описание |
|---|---|---|
| `esports_1080p_240hz` | Гейминг | Киберспорт 240Hz+, низкие настройки |
| `esports_1080p_360hz` | Гейминг | Киберспорт 360Hz+, минимизация frametime |
| `aaa_1080p_ultra` | Гейминг | AAA, 1080p, ультра |
| `aaa_1440p_high` | Гейминг | AAA, 1440p, высокие/ультра |
| `aaa_4k_ultra` | Гейминг | AAA, 4K, ультра, без RT |
| `aaa_4k_path_tracing` | Гейминг | AAA, 4K, Path Tracing |
| `llm_inference_7b` | AI/ML | Инференс LLM 7B (Q4_K_M) |
| `llm_inference_13b` | AI/ML | Инференс LLM 13B (Q4_K_M) |
| `llm_inference_20b` | AI/ML | Инференс LLM 20B+ |
| `llm_training_lora` | AI/ML | Файнтюнинг LoRA |
| `stable_diffusion` | AI/ML | Генерация изображений |
| `ai_upscaling` | AI/ML | DLSS / XeSS / FSR |
| `heavy_compilation` | Продуктивность | Компиляция крупных проектов |
| `3d_rendering_cpu` | Продуктивность | CPU-рендеринг (Blender, V-Ray) |
| `3d_rendering_gpu` | Продуктивность | GPU-рендеринг (Octane, Redshift) |
| `video_editing_4k` | Продуктивность | Видеомонтаж 4K |
| `video_editing_8k` | Продуктивность | Видеомонтаж 8K / RAW |
| `scientific_computing` | Продуктивность | CFD, FEA, симуляции |
| `data_engineering` | Продуктивность | ETL, базы данных |
| `software_development` | Продуктивность | IDE, Docker, компиляция |
| `office_productivity` | Продуктивность | Офис: браузер, документы |
| `silent_build` | Операции | Бесшумная работа: < 30 dBA |
| `sff_build` | Операции | Компактная сборка: ITX |
| `home_server_24_7` | Операции | Сервер 24/7 |
| `streaming` | Операции | Стриминг: OBS, NVENC |
| `virtualization` | Операции | Виртуализация: Proxmox, ESXi |

---

## Профили PSU

### НОРМА: atx_3x_transient_capable
```yaml
atx_3x_transient_capable:
  steel_man_desc: "Блок питания ATX 3.0/3.1 с поддержкой пиковых нагрузок до 200% номинала. Выдерживает transient spike современных GPU без аварийного отключения."
  failure_mode_desc: "Высокая цена относительно ATX 2.4 аналогов (+20–40%). Избыточен для систем без мощных GPU (TGP < 200W)."
  optimal_for_intents: ["aaa_4k_ultra", "aaa_4k_path_tracing", "3d_rendering_gpu", "llm_training_lora"]
  failure_for_intents: []
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### НОРМА: atx_2x_budget_reliable
```yaml
atx_2x_budget_reliable:
  steel_man_desc: "Блок питания ATX 2.4, проверенный временем стандарт. Достаточен для систем без мощных GPU (TGP < 200W). Лучшая цена/ватт."
  failure_mode_desc: "Не рассчитан на пиковые нагрузки современных GPU (RTX 5080/5090). Transient spike > 150% TGP может триггерить OCP — аварийное выключение."
  optimal_for_intents: ["aaa_1080p_ultra", "aaa_1440p_high", "esports_1080p_240hz", "office_productivity", "software_development"]
  failure_for_intents: ["aaa_4k_path_tracing", "llm_training_lora"]
  failure_severity: "BLOCK"
  failure_type: "CLIFF_DROP"
```

---

## Профили Cooling

### НОРМА: air_tower_standard
```yaml
air_tower_standard:
  steel_man_desc: "Одно/двухбашенный воздушный кулер с TDP-рейтингом 150–250W. Достаточен для большинства потребительских CPU. Нулевой риск протечки, не требует обслуживания."
  failure_mode_desc: "Процессоры с TDP > 150W под длительной нагрузкой. Температура уходит в зону T_Hot (85°C+), возможен лёгкий throttling."
  optimal_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "office_productivity", "silent_build"]
  failure_for_intents: ["heavy_compilation", "3d_rendering_cpu"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: air_tower_high_tdp
```yaml
air_tower_high_tdp:
  steel_man_desc: "Двухбашенный воздушный кулер с TDP-рейтингом 250W+. Справляется с разогнанными и high-TDP процессорами. Надёжнее AIO (нет помпы)."
  failure_mode_desc: "Габариты — высота 155–165мм, ширина до 140мм. Блокирует доступ к слотам RAM на некоторых платах. Требует корпус с запасом по высоте кулера."
  optimal_for_intents: ["heavy_compilation", "3d_rendering_cpu", "scientific_computing"]
  failure_for_intents: ["sff_build"]
  failure_severity: "BLOCK"
  failure_type: "LINEAR_DEGRADATION"
```

### НОРМА: aio_liquid_standard
```yaml
aio_liquid_standard:
  steel_man_desc: "AIO 240–280мм. Лучше воздушных кулеров для импульсных нагрузок (burst) за счёт теплоёмкости жидкости. Эстетика, доступ к RAM."
  failure_mode_desc: "Риск протечки (низкий, но не нулевой). Помпа — дополнительная точка отказа. Срок службы 5–7 лет (против 15+ у воздуха)."
  optimal_for_intents: ["aaa_4k_ultra", "video_editing_4k", "streaming", "silent_build"]
  failure_for_intents: ["home_server_24_7"]
  failure_severity: "WARN"
  failure_type: "LINEAR_DEGRADATION"
```

### ЭКСТРЕМУМ: aio_liquid_high_tdp
```yaml
aio_liquid_high_tdp:
  steel_man_desc: "AIO 360мм+. Единственный способ охлаждать CPU с TDP > 200W без троттлинга под sustained нагрузкой."
  failure_mode_desc: "Требует корпус с поддержкой 360мм радиатора. Помпа + 3 вентилятора = дополнительные точки отказа. Цена выше воздушных кулеров в 2–3 раза."
  optimal_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation", "video_editing_8k"]
  failure_for_intents: ["sff_build", "office_productivity"]
  failure_severity: "BLOCK"
  failure_type: "LINEAR_DEGRADATION"
```

---

## Сводка: что изменилось с v3.2

| Изменение | v3.2 | v3.3 |
|---|---|---|
| Power-профили | Жёсткие пороги (100–180W, ≥280W) с дырой 180–280W | MECE envelope (low/mid/high) с reference points. Без дырок |
| Нормативные профили | Отсутствовали | 4 профиля: balanced_performance_gpu, balanced_monolithic_norm, standard_tlc_dram_ssd, standard_ddr5_xmp |
| failure_type | Отсутствовал | LINEAR_DEGRADATION vs CLIFF_DROP |
| Обоснование порогов | Магические числа | Reference points с документированными anchors |
| exhaustiveness | Частичная | MECE-гарантия для power envelope |
