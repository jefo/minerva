---
id: "nvidia-rtx-4070"
type: "gpu"
title: "NVIDIA GeForce RTX 4070 12GB"
vendor: "nvidia"
status: "verified"
tags: ["nvidia", "ada-lovelace", "ad104-cut", "tsmc-4n", "192bit-mid-bus", "12gb-vram", "gddr6x", "pcie4.0-x16", "dlss3-fg", "rt-3rd-gen", "200w-tbp", "12vhpwr-power", "nvenc-8th-gen", "cuda-ecosystem", "1440p-rt", "4k-vram-limited", "energy-efficiency-leader", "itx-friendly", "samsung-8nm-to-tsmc-4n-jump"]
last_updated: "2026-06-18"
links:
  bigger_brother: "catalog/gpu/nvidia-rtx-4070-super.md"
  smaller_brother: "catalog/gpu/nvidia-rtx-4060-ti.md"
  competitor_amd: "catalog/gpu/amd-rx-7800-xt.md"
  predecessor: "catalog/gpu/nvidia-rtx-3070.md"
specs:
  gpu: "AD104-250-A1 (Ada Lovelace)"
  lithography: "TSMC 4N (5nm)"
  die_size: "294.5 mm²"
  transistors: "35.8 млрд"
  cuda_cores: 5888
  sm_count: 46
  sm_count_full_die: 60
  sm_utilisation: "76.7%"
  tensor_cores: "184 (4-е поколение)"
  rt_cores: "46 (3-е поколение)"
  tmus: 184
  rops: 64
  base_clock: "1920 MHz"
  boost_clock: "2475 MHz"
  vram: "12 GB GDDR6X (192-bit)"
  vram_speed: "21 Gbps"
  vram_bandwidth: "504 GB/s"
  vram_variant_gddr6: "12 GB GDDR6, 20 Gbps, 480 GB/s (с августа 2024)"
  l2_cache: "36 MB (из 48 MB на полном AD104)"
  tbp: "200W"
  avg_gaming_power: "~186W"
  power_connector: "1× 12VHPWR (12-pin) или 1× 8-pin на ряде AIB-моделей"
  pcie: "PCIe 4.0 x16"
  display_outputs: "1× HDMI 2.1a, 3× DP 1.4a"
  msrp_usd: "$599 (старт, апр. 2023); $549 (после выхода Super, янв. 2024)"
  launch_date: "12 апреля 2023"
  engineering_notes: "AD104-250 — третий по размеру кристалл Ada Lovelace (294.5 мм², 35.8 млрд транзисторов). Включено 46 из 60 SM — 76.7% кристалла. Три из четырёх 64-битных контроллеров памяти активны (192-bit), поэтому L2-кэш урезан до 36 MB (3×12 MB) против 48 MB на полном кристалле. Главный козырь карты — энергоэффективность: +20–25% FPS над RTX 3070 Ti при -31% TDP (200W vs 290W). Поколенческий скачок Samsung 8nm → TSMC 4N дал колоссальный прирост эффективности. 12GB VRAM — шаг вперёд над 8GB у 3070/3070 Ti, но 192-битная шина душит карту в 4K (504 GB/s vs 760 GB/s у RTX 3080). GDDR6-вариант (август 2024) снижает пропускную способность до 480 GB/s с минимальной потерей производительности (~1%)."
profiles:
  balanced_performance_gpu:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Предсказуемое масштабирование производительности. Стандартные сборки ATX с БП 600-750W."
    failure_mode_desc: "Отсутствие специализации. Проигрывает enthusiast-картам в 4K, проигрывает low-power картам в SFF/тишине."
    optimal_for_intents: ["aaa_1440p_high", "aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "streaming"]
    failure_for_intents: ["aaa_4k_path_tracing"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  hardware_rt_accelerated_gen_3:
    steel_man_desc: "Path Tracing в реальном времени. Аппаратное ускорение ×4-5 vs растеризация."
    failure_mode_desc: "DX11/OpenGL игры. RT-блоки простаивают — dark silicon."
    optimal_for_intents: ["aaa_4k_path_tracing", "3d_rendering_gpu"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  tensor_matrix_accelerated:
    steel_man_desc: "Локальное обучение/инференс нейросетей, Stable Diffusion, DLSS."
    failure_mode_desc: "Традиционные FP32-вычисления. Тензорные блоки простаивают — паразитный нагрев."
    optimal_for_intents: ["llm_inference_7b", "llm_inference_13b", "stable_diffusion", "ai_upscaling", "llm_training_lora"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 38000
  median: 45000
  max: 65000
  source: "оценка рынка (июнь 2026) — вторичный рынок 38-50k, остатки розницы 55-65k"
  date: "2026-06-18"
  note: "Карта снята с розничных продаж (EOL). Price.ru показывает только 4070 Ti/Super. Цены — рыночная оценка по вторичному рынку."

# === Structured data (GPU Entity Type v1.0) ===
vram_structured:
  size_gb: 12
  type: "GDDR6X"
  bus_width_bit: 192
  bandwidth_gb_s: 504
clock_structured:
  boost_ghz: 2.475
  game_ghz: null
cache:
  size_mb: 36
  type: "L2"
compute:
  unit:
    type: "CUDA Core"
    count: 5888
  rt:
    type: "RT Core"
    count: 46
    generation: 3
  ml:
    type: "Tensor Core"
    count: 184
    generation: 4
software:
  upscaler: "DLSS 3"
  frame_gen: "FG"
  encoder: "NVENC 8th gen"
  compute_api: "CUDA"
  driver_features: ["Game Ready"]

verdict: "RTX 4070 — карта-водораздел поколения Ada Lovelace: образцовая энергоэффективность (200W), DLSS 3 Frame Generation и достаточная для 1440p производительность. Но 12GB VRAM и урезанный на 23.3% кристалл AD104 ставят под вопрос долгосрочную перспективу. RTX 4070 Super за $599 (та же стартовая цена!) даёт +15–20% FPS и полные 48MB L2 — объективно лучший выбор, если бюджет позволяет. RX 7800 XT предлагает 16GB VRAM и конкурентоспособный растр. Берите 4070 ради энергоэффективности, DLSS 3 FG, CUDA-экосистемы или ITX-сборки — в этих нишах она всё ещё блестяща."
---

# NVIDIA GeForce RTX 4070 12GB

## Архитектура и позиционирование

RTX 4070 построена на GPU AD104-250 — урезанной версии кристалла AD104 архитектуры Ada Lovelace. Это третий по размеру чип линейки Ada (после AD102 и AD103): 294.5 мм², 35.8 млрд транзисторов на техпроцессе TSMC 4N (оптимизированный 5nm).

NVIDIA активировала 46 из 60 Streaming Multiprocessors (76.7% кристалла) и 3 из 4 контроллеров памяти, получив 192-битную шину. Это классический подход NVIDIA к сегментации: отключение блоков для создания продукта с более низкой себестоимостью.

Карта вышла 12 апреля 2023 года по цене $599. После анонса RTX 4070 Super (январь 2024, те же $599) официальная цена снижена до $549. В августе 2024 появился вариант с обычной GDDR6 (20 Gbps, 480 GB/s) вместо GDDR6X (21 Gbps, 504 GB/s) — производительность отличается на ~1%.

**Позиционирование:** NVIDIA подаёт RTX 4070 как карту для 1440p-гейминга с трассировкой лучей. Маркетинговый тезис «RTX 3080 performance at half the power» близок к истине: в растре 4070 действительно на уровне 3080, потребляя при этом 200W против 320W.

**Главная претензия сообщества при запуске:** $599 за карту с 192-битной шиной, когда RTX 3080 10GB за $699 годом ранее имела 320-битную шину. NVIDIA сделала ставку на кэш (36MB L2), который частично компенсирует узкую шину, но не полностью.

## Характеристики

- **GPU:** AD104-250-A1 (Ada Lovelace)
- **Техпроцесс:** TSMC 4N (5nm)
- **Кристалл:** 294.5 мм², 35.8 млрд транзисторов
- **CUDA-ядер:** 5888 (из 7680 на полном AD104)
- **SM:** 46 из 60 (76.7% кристалла)
- **Тензорных ядер:** 184 (4-е поколение)
- **RT-ядер:** 46 (3-е поколение)
- **TMU:** 184
- **ROP:** 64
- **Base Clock:** 1920 MHz
- **Boost Clock:** 2475 MHz (Founders Edition)
- **VRAM:** 12 GB GDDR6X
- **Шина памяти:** 192-bit
- **Скорость памяти:** 21 Gbps
- **Пропускная способность:** 504 GB/s
- **GDDR6-вариант (с авг. 2024):** 20 Gbps, 480 GB/s (−4.8%)
- **L2-кэш:** 36 MB (3×12 MB; полный AD104 — 48 MB, 4×12 MB)
- **TBP:** 200W
- **Среднее энергопотребление в играх:** ~186W
- **Питание:** 1× 12VHPWR (12-pin) или 1× 8-pin на AIB-моделях
- **PCIe:** 4.0 x16
- **Видеовыходы:** 1× HDMI 2.1a, 3× DisplayPort 1.4a
- **NVENC:** 8-е поколение (два кодировщика, аппаратный AV1)
- **MSRP (USD):** $599 (старт, апрель 2023); $549 (после января 2024)
- **Дата выхода:** 12 апреля 2023

## Ключевые инженерные особенности

### AD104-250: урезанный кристалл с умным кэшированием

AD104 — это 294.5 мм² кристалл на TSMC 4N. Полный чип содержит 60 SM (7680 CUDA-ядер) и четыре 64-битных контроллера памяти (256-bit). В RTX 4070:

- **46 SM активно** (76.7%) — 5888 CUDA-ядер, 184 Tensor-ядра, 46 RT-ядер
- **3 из 4 контроллеров памяти активно** — 192-битная шина, 3×12 MB = 36 MB L2
- Отключённый контроллер памяти уносит с собой 12 MB L2-кэша — поэтому 36 MB, а не 48 MB
- 64 ROP — это аппаратный лимит 192-битной конфигурации (16 ROP на 64-битный контроллер)

36 MB L2-кэша Ada значительно снижают зависимость от пропускной способности памяти. По данным NVIDIA, эффективная пропускная способность с учётом кэша эквивалентна ~900+ GB/s в типичных игровых нагрузках, что объясняет, как 192-битная шина справляется с 1440p несмотря на «всего» 504 GB/s физической пропускной способности.

### Поколенческий скачок: Samsung 8nm → TSMC 4N

Переход с Samsung 8nm (Ampere, RTX 30) на TSMC 4N (Ada Lovelace, RTX 40) — самый значительный техпроцессный скачок NVIDIA за десятилетие. Конкретно для RTX 4070 против RTX 3070 Ti:

- **Производительность:** +20–25% FPS в 1440p-растре (данные TPU, GN, HUB — валидировано)
- **Энергопотребление:** 200W TBP vs 290W TBP (−31%)
- **Эффективность (FPS/Вт):** почти двукратный прирост
- **VRAM:** 12GB vs 8GB — критическое преимущество в современных AAA
- **Температуры/шум:** 200W легко охлаждаются двухвентиляторными кулерами; многие карты полупассивны в простое

### DLSS 3 Frame Generation

Эксклюзив 40-й серии. Оптический Flow Accelerator (OFA) на кристалле генерирует промежуточные кадры, удваивая воспринимаемую частоту кадров. В Cyberpunk 2077 с RT Overdrive: с DLSS 3 FG 4070 выдаёт играбельные 60+ FPS там, где 3070 Ti с DLSS 2 едва держит 35–40 FPS. Это не «фейковые кадры» для динамичных шутеров (задержка), но для сюжетных AAA — трансформирующая технология.

### AV1 и NVENC 8-го поколения

Два аппаратных кодировщика NVENC 8-го поколения с поддержкой AV1. Для стримеров: качество AV1 при 6 Мбит/с сопоставимо с H.264 при 10–12 Мбит/с. DaVinci Resolve, Premiere Pro, OBS — все используют NVENC.

## Сравнение с конкурентами (Iron Man Argument)

### RTX 4070 (12GB, $549) vs RTX 3070 Ti (8GB, $599 MSRP 2021)

**Где RTX 4070 сильнее:**
- **Производительность:** +20–25% FPS в 1440p-растре; в RT-сценариях разрыв ещё больше (3-е поколение RT-ядер эффективнее 2-го)
- **Энергоэффективность:** 200W vs 290W — карта на 100W холоднее. Работает на качественном 550W БП; 3070 Ti требовала 650W+
- **VRAM:** 12GB vs 8GB — в 2023+ году 8GB уже не хватает для ультра-текстур в ряде AAA (The Last of Us Part I, Hogwarts Legacy, Resident Evil 4)
- **DLSS 3 Frame Generation:** отсутствует на 30-й серии
- **AV1-кодирование:** отсутствует на 30-й серии
- **Шум/температуры:** 200W охлаждаются тихо; 290W GA104 — горячий чип

**Где RTX 4070 слабее:**
- **Пропускная способность памяти:** 504 GB/s vs 608 GB/s (3070 Ti, 256-bit) — в 4K 4070 теряет часть преимущества из-за narrower bus. На 1080p/1440p 36MB L2-кэша компенсируют.
- **Поколенческий прирост для владельцев 3070 Ti:** +20–25% за $549 — недостаточно для оправдания апгрейда. NVIDIA ориентировала карту на владельцев 2070/2060 и старше.

### RTX 4070 (12GB, $549) vs RX 7800 XT (16GB, ~$499)

**Где RTX 4070 сильнее:**
- **Трассировка лучей:** 3-е поколение RT-ядер vs 2-е у RDNA 3. Cyberpunk 2077 RT Ultra 1440p: 4070 ~55 FPS vs 7800 XT ~40 FPS (+37%). Path Tracing — преимущество NVIDIA подавляющее.
- **DLSS 3 FG vs FSR 3 FG:** DLSS даёт более стабильную картинку (меньше ghosting, артефактов на тонких элементах). FSR 3 улучшился, но всё ещё отстаёт.
- **Энергоэффективность:** 200W vs 263W — 4070 на ~24% эффективнее
- **CUDA/профессиональные приложения:** Blender, V-Ray, Octane — RTX 4070 примерно вдвое быстрее в рендеринге через OptiX vs HIP/ROCm на RX 7800 XT
- **ITX/SFF:** множество двухвентиляторных моделей 4070; RX 7800 XT преимущественно 2.5–3-слотовые карты
- **NVENC vs AMF:** качество аппаратного кодирования NVIDIA стабильно выше при равном битрейте

**Где RTX 4070 слабее:**
- **Чистый растр (1440p):** RX 7800 XT на 5–10% быстрее. В Call of Duty, Apex Legends, Horizon Forbidden West AMD впереди.
- **VRAM:** 12GB vs 16GB — для 4K и игр с HD-текстурами запас AMD ощутим
- **Цена:** $549 vs ~$499 — AMD дешевле при равном или лучшем растре
- **FSR 3 доступен на большем числе игр:** кроссплатформенность FSR означает поддержку в консольных портах «из коробки»
- **Драйверы AMD Adrenalin:** более функциональный софт (встроенный оверлей с метриками, запись, стриминг) без обязательной регистрации

### RTX 4070 vs RTX 4070 Super (+$50)

RTX 4070 Super (январь 2024) — прямой наследник по той же цене $599, что и стартовый 4070:

- **CUDA-ядер:** 7168 (+21.7%)
- **SM:** 56 из 60 (93.3% кристалла)
- **L2-кэш:** 48 MB (+33%)
- **Производительность:** +15–20% FPS
- **TBP:** 220W (+10%)

Если разница в цене между 4070 и 4070 Super составляет ≤$50 — Super объективно лучший выбор. При разнице $80–100 можно аргументировать в пользу 4070 для бюджетно-ограниченных сборок.

### Итоговый вердикт

- **RT + DLSS 3 — приоритет → RTX 4070 (или 4070 Super).** Frame Generation и RT-производительность NVIDIA — ключевые аргументы. CUDA обязательна для работы? Берите 4070 не думая.
- **Чистый растр, FPS/₽, запас VRAM → RX 7800 XT.** 16GB за меньшие деньги. Если не пользуетесь RT и не привязаны к CUDA — AMD рациональнее.
- **Компактная/тихая сборка → RTX 4070.** 200W = двухвентиляторные карты, которые поместятся в ITX-корпус и не будут выть.
- **Долгосрочная инвестиция (4+ года) → RTX 4070 Super или RX 7800 XT.** 12GB non-Super рискуют стать ограничением раньше, чем GPU-производительность.

## Российский рынок

> *Раздел будет заполнен после мониторинга цен. Ориентировочно: RTX 4070 занимает нишу 55 000–70 000 ₽ на вторичном рынке (июнь 2026), уступая место RTX 4070 Super и RTX 5070 в рознице.*

## Для кого

**Подходит:**
- 1440p-гейминг в AAA с высокими настройками и трассировкой лучей (Cyberpunk 2077, Alan Wake 2, Black Myth: Wukong)
- Апгрейд с GTX 1070/1080, RTX 2060/2070, RTX 3060 — прирост в 2–3 раза
- Стримеры и контент-мейкеры: NVENC (AV1) + CUDA
- Сборки с ограничениями по БП (качественный 550W), шуму или размеру (ITX/SFF)
- Работа в Blender, DaVinci Resolve, Adobe Suite, CAD (CUDA/OptiX)
- Энтузиасты энергоэффективности: лучшая FPS/Вт среди карт своего класса на момент выхода

**Не подходит:**
- 4K-гейминг на ультра-настройках (192-bit шина + 12GB — узко)
- Апгрейд с RTX 3070 Ti / 3080 — прирост недостаточен для оправдания затрат
- Игры с активным моддингом (Skyrim Nolvus, Cities Skylines 2 с ассетами) — 12GB VRAM под вопросом
- Чистый растр без RT/DLSS — RX 7800 XT быстрее и дешевле с 16GB
- Планирование на 4+ года без промежуточного апгрейда — 12GB VRAM станут bottleneck
- Покупка новой в 2025–2026 при наличии RTX 4070 Super или RTX 5070 в доступе

## Источники

1. TechPowerUp — GPU Database: «NVIDIA GeForce RTX 4070 Specifications» (2023)
2. TechPowerUp — «NVIDIA AD104 GPU Specs» (die size, transistor count, full configuration)
3. TechPowerUp — «NVIDIA GeForce RTX 4070 Founders Edition Review» by W1zzard (April 2023)
4. Gamers Nexus — «NVIDIA RTX 4070 Review & Benchmarks» (April 2023)
5. Hardware Unboxed — «RTX 4070 vs RX 7800 XT: Full Benchmark Suite» (2023)
6. Tom's Hardware — «Nvidia officially announces new RTX 4070 with slower GDDR6 memory» (August 2024)
7. Tom's Hardware — «Nvidia Reveals Ada Lovelace GPU Secrets: Transistor Counts, Die Sizes» (September 2022)
8. NVIDIA — «GeForce RTX 40 SUPER Series Graphics Cards Launching This January» (January 2024)
9. Wikipedia — «GeForce RTX 40 series» и «Ada Lovelace (microarchitecture)»
10. Собственное тестирование лаборатории (раздел будет дополнен)
