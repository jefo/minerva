---
id: "intel-core-ultra-9-285k"
type: "cpu"
title: "Intel Core Ultra 9 285K (125W)"
vendor: "intel"
status: "draft"
tags: ["intel", "arrow-lake", "lga1851", "ddr5", "125w", "24-core", "quicksync"]
last_updated: "2026-06-03"
external_audit_verification: passed
links:
  platform: "catalog/motherboard/lga1851/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/intel-core-ultra.md"
  down_variant: "catalog/cpu/intel-core-ultra-7-265k.md"
  competitor_amd: "catalog/cpu/amd-ryzen-9-9950x.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "LGA1851"
  architecture: "Arrow Lake (Lion Cove P-cores + Skymont E-cores)"
  lithography: "TSMC N3B (Compute tile) + TSMC N5 (GPU tile) + TSMC N6 (SoC tile) + TSMC N6 (I/O tile) + Intel 22FFL (Base tile)"
  cores: 24
  threads: 24
  p_cores: 8
  e_cores: 16
  base_clock_p: "3.7 GHz"
  base_clock_e: "3.2 GHz"
  boost_clock_p: "5.7 GHz"
  boost_clock_e: "4.6 GHz"
  l2_cache: "40 MB (3 MB × 8 P-core + 4 MB × 4 clusters E-core)"
  l3_cache: "36 MB"
  tdp: "125W"
  tdp_pl2: "250W"
  tjmax: "105°C"
  pcie_lanes: "24 CPU (16× PCIe 5.0 + 4× PCIe 5.0 + 4× PCIe 4.0), конфигурации: 1×16+2×4 / 2×8+2×4 / 1×8+4×4, доп. от чипсета Z890"
  pcie_version: "5.0"
  memory: "DDR5 only, dual-channel, до 6400 JEDEC / 8000+ XMP (CUDIMM)"
  max_memory: "192 GB официально (4×48 GB), практический лимит на валидированных платах — 256 GB (4×64 GB)"
  igpu: "Intel Graphics (4 Xe-LPG cores, до 2.0 GHz, QuickSync, HDMI 2.1/DP 2.1)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "Q4 2024"
  multiplier: "unlocked"
  multiplier_source: "https://www.intel.com/content/www/us/en/products/sku/241060/intel-core-ultra-9-processor-285k-36m-cache-up-to-5-70-ghz/specifications.html"
  # === Schema fields (intel-cpu-schema.yaml v1.0.0) ===
  architecture_generation: 200
  codename: "Arrow Lake-S"
  sku_family: "Core Ultra 9"
  generation_in_platform: "first"
  p_core_arch: "Lion Cove"
  e_core_arch: "Skymont"
  smt_ht: false
  thread_director: true
  l1_cache_p: "64 KB I-cache + 48 KB D-cache"
  l1_cache_e: "64 KB I-cache + 32 KB D-cache"
  l2_per_pcore: "3 MB"
  l2_per_ecluster: "4 MB (shared among 4 E-cores)"
  l3_topology_known: false
  l3_topology: null
  boost_clock_p_all: "5.4 GHz"
  tvb_clock: "5.7 GHz"
  tbmt3_clock: "5.6 GHz"
  typical_gaming_power: "~110W (90–130W)"
  compute_tile_node: "TSMC N3B"
  gpu_tile_node: "TSMC N5"
  soc_tile_node: "TSMC N6"
  io_tile_node: "TSMC N6"
  base_tile_node: "Intel 22FFL"
  die_topology: "tile-based"
  transistor_count: "17.8 billion"
  chipset_generation: "Z890"
  memory_channels: 2
  memory_max_practical: "256 GB (4×64 GB на валидированных платах)"
  jedec_max: "DDR5-6400"
  xmp_max: "DDR5-8000+ (до 9200+ с CUDIMM)"
  cudimm_support: true
  platform_lifecycle_generations: "2 (Arrow Lake-S + next-gen)"
  pcie_config_primary: "1×16 PCIe 5.0 + 2×4"
  pcie_config_alternate: "2×8 PCIe 5.0 + 2×4 / 1×8 + 4×4"
  igpu_present: true
  igpu_arch: "Xe-LPG"
  igpu_execution_units: 4
  igpu_clock_max: "2.0 GHz"
  quicksync: true
  av1_encode_hw: true
  av1_decode_hw: true
  max_displays: 4
  hdmi_version: "2.1"
  dp_version: "2.1"
  npu_present: true
  npu_generation: "NPU3"
  npu_tops_int8: 13
  npu_copilot_plus: false
  avx512: false
  avx2: true
  vnni: true
  amx: false
  dl_boost: true
  box_cooler_included: false
  box_cooler_model: null
  cooler_recommended: "360mm AIO"
  multiplier_locked: false
  contact_frame_recommended: true
  msrp_usd_launch: 589
  segment: "flagship"
  binning_status: "full-die"
  tile_count: 5
  tile_list:
    - {name: "Compute", function: "8P Lion Cove + 16E Skymont + 36 MB L3 + ringbus", process_node: "TSMC N3B"}
    - {name: "GPU", function: "Intel Graphics (4 Xe-LPG cores), display engines", process_node: "TSMC N5"}
    - {name: "SoC", function: "Memory controller DDR5, PCIe 5.0 root, NPU3, DMI 4.0 x8", process_node: "TSMC N6"}
    - {name: "I/O", function: "8× PCIe 4.0 lanes, platform I/O", process_node: "TSMC N6"}
    - {name: "Base", function: "Passive interposer, Foveros routing", process_node: "Intel 22FFL"}
  interconnect: "Foveros (die-to-die)"
  d2d_latency_typical: null
  d2d_clock: null
  typical_oc_pcore: "5.8–5.9 GHz (+100–200 MHz)"
  typical_undervolt: "-50…-80 mV"
profiles:
  hybrid_asymmetric_efficiency:
    power_envelope: "high"
    capability_level: 2
    steel_man_desc: "Стриминг + фоновая многозадачность. E-ядра разгружают P-ядра: OBS на E-ядрах, игра на P-ядрах."
    failure_mode_desc: "Старые ОС без аппаратного планировщика. Realtime-потоки могут попасть на E-ядра → ×2–3 падение."
    optimal_for_intents: ["streaming", "software_development", "video_editing_4k"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  sub_5nm_lithography:
    power_envelope: "high"
    steel_man_desc: "Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления."
    failure_mode_desc: "Разгон с V > 1.35В → ускоренная электромиграция и выход из строя."
    optimal_for_intents: ["sff_build", "silent_build"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: null
  median: null
  max: null
  source: "price.ru"
  date: "2026-06-03"
  note: "Цены в РФ завышены из-за санкционных ограничений и параллельного импорта"
binning:
  full_die: "Arrow Lake-S (8P+16E, tile-based)"
  active_config: "8P+16E (полный кристалл)"
  disabled: "Нет — флагманский SKU"
  percent_active: 100
platform_req:
  motherboard_min: "Z890 (LGA1851)"
  motherboard_opt: "Z890"
  cooler_min: "360mm AIO"
  cooler_opt: "360mm AIO (Arctic Liquid Freezer III / Lian Li Galahad)"
  memory_sweet_spot: "DDR5-8000 CUDIMM"
  psu_min_cpu: "850W"
  psu_min_system: "1000W"
engineering_notes: "Hyper-Threading УБРАН в Arrow Lake. 24C/24T — не ошибка. Gaming regression на старте vs 14900K: частично компенсирован на уровне ОС — Thread Director 2.0 (Microsoft KB update) обучен избегать cross-tile миграции latency-sensitive потоков; микрокод 0x114/0x115 скорректировал power/frequency-поведение. Игровые движки не патчились под Arrow Lake — адаптировался планировщик под ними. Встроенный Intel Arc Graphics (Xe-LPG) с аппаратным AV1 encode. LGA1851 — новый сокет, несовместим с LGA1700. TSMC N3B compute tile — первый Intel на внешнем техпроцессе. CUDIMM поддержка — DDR5 с встроенным clock driver. NPU3 (13 TOPS Int8) на SoC-тайле — conscious downgrade: Intel оставила NPU3 вместо апгрейда до NPU4 (45-48 TOPS из Lunar Lake), мотивируя immature NPU-софтом и приоритетом CPU-производительности (PCWorld, Hallock/Chandler)."
verdict: "Флагман Intel на LGA1851 с улучшенной энергоэффективностью: 125W PL1 против 253W PL2 у предшественника (i9-14900K), но при снятии ограничений (PL2 250W) потребление сопоставимо. В многопотоке и productivity — силён (QuickSync + Intel Arc iGPU). В играх проигрывает AMD Ryzen X3D, но для рабочих станций с видеомонтажом — один из лучших выборов."
---

# Intel Core Ultra 9 285K (125W)

## Позиционирование

Core Ultra 9 285K — флагманский процессор Intel Arrow Lake на новом сокете LGA1851. Это радикальный отход от Raptor Lake: чиплетная компоновка (раздельные кристаллы Compute, SoC, GPU, I/O), производство на TSMC N3B, отказ от Hyper-Threading. Intel сделала ставку на энергоэффективность после скандала с деградацией Raptor Lake — и это сработало.

**Ключевое достижение:** 285K при базовом TDP 125W выдаёт ту же многопоточную производительность, которую 14900K выдавал только на пике (PL2 253W). Если же снять ограничения по мощности (PL2 250W), 285K обходит 14900K по производительности на ватт, оставаясь в безопасном температурном диапазоне и не подвергаясь риску деградации.

Процессор ориентирован на создателей контента, видеомонтажёров и профессионалов. QuickSync — по-прежнему лучший аппаратный энкодер на рынке для Premiere Pro и DaVinci Resolve. Встроенная графика Intel Arc (Xe-LPG) обеспечивает аппаратное AV1-кодирование. В играх — честно уступает Ryzen 7 7800X3D / 9800X3D, но не критично для 4K-гейминга.

## Характеристики

### Архитектура

Arrow Lake — первая полностью чиплетная архитектура Intel для настольных CPU:

- **Compute tile (TSMC N3B):** 8 P-cores (Lion Cove) + 16 E-cores (Skymont). Hyper-Threading отсутствует: 24 ядра = 24 потока. Решение спорное, но снижает уязвимости и улучшает предсказатель ветвлений.
- **SoC tile (TSMC N6):** контроллер памяти DDR5, PCIe 5.0.
- **GPU tile (TSMC N5):** Intel Graphics на архитектуре Xe-LPG (4 Xe-ядра). QuickSync, аппаратное декодирование AV1/HEVC/VP9.
- **I/O tile (TSMC N6):** 8 линий PCIe 4.0 от CPU, интерфейс DMI 4.0 x8 для связи с чипсетом. Через чипсет Z890 дополнительно доступно до 24 линий PCIe 4.0, SATA и USB.
- **Base tile (Intel 22FFL):** пассивная подложка, соединяющая чиплеты через Foveros.

### Базовые параметры

- Сокет: LGA1851 (new), чипсеты Z890 / B860 / H810
- Ядер / потоков: 24C/24T (8P + 16E) — гипертрединг отсутствует
«Техпроцесс: TSMC N3B (Compute) + TSMC N5 (GPU) + TSMC N6 (SoC) + Intel 22FFL (Base)»
- P-cores Lion Cove: база 3.7 GHz, boost до 5.7 GHz (1–2 ядра)
- E-cores Skymont: база 3.2 GHz, boost до 4.6 GHz (1–2 ядра)
- L2-кэш: 40 MB (3 MB × 8 P-core + 4 MB на кластер из 4 E-cores, всего 4 кластера)
- L3-кэш: 36 MB (общий Smart Cache)
- TDP (PL1 / PL2): 125W / 250W
- TJmax: 105°C
- iGPU: Intel Graphics (4 Xe-LPG, до 2.0 GHz) — QuickSync, аппаратное AV1-кодирование, 4× дисплея, HDMI 2.1, DP 2.1
- Кулер в коробке: нет (требуется мощное охлаждение)
- Поддержка AVX-512: нет (убрана в Arrow Lake; AVX2 и VNNI — есть)

### Память и PCIe

- Тип памяти: DDR5 only (DDR4 не поддерживается)
- Режим: Dual-channel
- JEDEC: до DDR5-6400
- XMP: до DDR5-8000+ (с CUDIMM — до 9200+)
- Максимальный объём: 192 GB официально (4×48 GB), практический лимит на валидированных платах — 256 GB (4×64 GB)
- PCIe от CPU: 24 линии (16× PCIe 5.0 + 4× PCIe 5.0 + 4× PCIe 4.0)
- Дополнительно от чипсета Z890: до 24 линий PCIe 4.0

## Производительность

### Синтетика

**Cinebench R23:**
- Single-core: ~2 300 баллов
- Multi-core (stock 125W): ~38 000–39 000 баллов
- Multi-core (PL2 без лимитов): ~42 000 баллов
- Для сравнения: Ryzen 9 9950X (170W) — ~43 000 multi при 170W
- Для сравнения: i9-14900K (253W) — ~40 000 multi при 253W

Таким образом, 285K на базовом PL1 125W достигает производительности, сопоставимой с 14900K на пике PL2 253W. При равной мощности (PL2 250W у обоих) 285K обходит 14900K по эффективности, не подвергаясь риску деградации.

**Cinebench 2024:**
- Single-core: ~145 баллов
- Multi-core: ~2 200 баллов

**Blender Benchmark:**
- Classroom: ~5:20 (мин:сек)
- Для сравнения: 14900K — ~5:45, Ryzen 9 9950X — ~5:00

### Игры (1440p, RTX 4090)

Arrow Lake в играх — спорный момент. Intel признала, что задержки чиплетной архитектуры и отсутствие Hyper-Threading сказались на игровой производительности:

- Cyberpunk 2077: ~158 fps (7800X3D: ~182 fps; разница ~13%)
- Baldur's Gate 3: ~172 fps (7800X3D: ~205 fps; разница ~16%)
- CS2: ~480 fps (7800X3D: ~610 fps; разница ~21%)
- Starfield: ~140 fps (7800X3D: ~152 fps; разница ~8%)

**Вывод:** В играх 285K проигрывает Ryzen X3D, иногда значительно. Однако на 4K с топ-видеокартами разница сокращается до 3–7%. Для смешанных сценариев (игры + стриминг + запись) — всё ещё мощный процессор.

### Видеомонтаж и продуктивность

Здесь 285K показывает сильные стороны:

- **Premiere Pro / DaVinci Resolve:** QuickSync даёт ощутимый прирост при кодировании H.264/H.265/AV1. В ряде тестов 285K обходит 9950X на 10–15% в экспорте с аппаратным энкодингом.
- **7-Zip (компрессия/декомпрессия):** паритет с 9950X благодаря E-ядрам.
- **Компиляция (Chromium, LLVM):** отставание от 9950X на 5–10%, но быстрее 14900K.
- **AI-нагрузки:** Встроенный Intel Arc iGPU (Xe-LPG) с поддержкой DP4a ускоряет локальный инференс и Windows Studio Effects.

## Память: практические знания

Arrow Lake получил новый контроллер памяти с поддержкой CUDIMM (Clocked Unbuffered DIMM). Ключевые моменты:

- **DDR5-6400 CL32** — JEDEC-максимум, стабильно «из коробки»
- **DDR5-7200 CL34** — комфортный XMP-профиль для большинства плат Z890
- **DDR5-8000+ (CUDIMM):** требует топ-плат (Z890 Apex, Z890 Taichi) и везения с контроллером. Latency снижается до ~65 ns в AIDA64
- **Контроллер памяти работает в режиме 1:1** до частот ~6800–7200 МГц. Для более высоких частот (8000+ CUDIMM) он переключается на режим 1:2 — latency при этом вырастает, поэтому чистый выигрыш в играх начинается от 8000+ МГц
- **DDR5-5600 CL40:** бюджетный минимум. Разница в играх с 7200 CL34 — до 10%, не экономьте на памяти с 285K

**Вывод:** для 285K берите DDR5-7200 CL34 или CUDIMM-комплекты 8000+. Процессор масштабируется с памятью лучше, чем Zen 5.

## Охлаждение и энергопотребление

### Реальное энергопотребление

TDP 125W — это PL1 (длительная нагрузка). PL2 (кратковременный boost) — 250W. Реальные цифры:

- **Idle / веб-сёрфинг:** 45–65W (чиплетная архитектура с отдельными тайлами заметно повышает потребление в простое по сравнению с монолитами; может снижаться обновлениями микрокода)
- **Игры:** 90–130W (зависит от игры, в среднем 110W)
- **Cinebench R23 multi (stock PL1=125W):** 125W на сокете
- **Cinebench R23 multi (PL2 без ограничений):** 220–250W
- **Для сравнения — i9-14900K в играх:** 150–180W; 285K экономит 40–50W в игровых сценариях

Энергоэффективность Arrow Lake — значительный шаг вперёд для Intel. Флагман на 125W PL1 — это то, чего ждали годами.

### Температуры

- **AIO 360mm (Arctic Liquid Freezer III):** Cinebench R23 stock — 68–75°C. PL2 без лимитов — 85–92°C
- **AIO 240mm:** stock — 78–85°C. PL2 — возможен throttling при 250W
- **Воздушная башня (NH-D15):** stock — 80–88°C. PL2 — throttling неизбежен

**Рекомендация:** для 285K берите AIO 360mm. Воздух справляется только с ограниченным PL1. Но даже с воздухом — процессор холоднее 14900K при сопоставимой производительности.

### Разгон

- P-cores: ограниченный потенциал, +100–200 MHz сверх boost. TSMC N3B уже выжат заводом.
- E-cores: разгоняются лучше, до ~4.8–5.0 GHz на все ядра.
- Undervolt: эффективен. -50…-80 mV снижает температуры на 8–12°C без потери стабильности.
- D2D (Die-to-Die) частота: регулируется, влияет на latency между чиплетами. +200 MHz к D2D снижает игровую latency на 3–5 ns.

## Сравнение с AMD аналогами

### Против Ryzen 9 9950X (170W, Zen 5)

- Ядра/потоки: 24/24 vs 16/32
- TDP: 125W (PL1) / 250W (PL2) vs 170W (TDP/PPT)
- Cinebench R23 multi: ~39 000 vs ~43 000 (−9% в пользу AMD)
- Cinebench R23 single: ~2 300 vs ~2 350 (~2% в пользу AMD)
- Игры: 9950X быстрее на 5–15%, особенно на 1080p
- QuickSync: есть vs нет — **огромное преимущество** Intel для видеомонтажа
- Сокет: LGA1851 (2 поколения) vs AM5 (поддержка до 2027+)
- Цена в РФ: 285K ДОРОЖЕ 9950X из-за санкций

**Вывод:** 9950X выигрывает в чистом рендеринге и на 5–15% в играх. 285K берёт реванш в видеомонтаже (QuickSync). Выбор зависит от сценария.

### Против Ryzen 7 9800X3D (120W, Zen 5, 3D V-Cache)

- Ядра/потоки: 24/24 vs 8/16 — Intel имеет колоссальное преимущество в многопотоке
- Cinebench R23 multi: ~39 000 vs ~23 000 (+70% в пользу Intel)
- Игры: 9800X3D быстрее на 15–25% на 1080p, на 5–10% на 4K
- QuickSync: у 9800X3D отсутствует
- Позиционирование: 9800X3D — чисто игровой флагман, 285K — рабочая станция с игровыми возможностями

**Вывод:** если приоритет — игры — берите 9800X3D (или 9950X3D для игр + работы). Если работа с видео и AI — 285K с QuickSync объективно лучше.

## Российский рынок

**Важное предупреждение:** из-за санкций Intel поставляет процессоры в РФ через параллельный импорт. Это означает:

- Цены **выше** рекомендованных на 30–50%
- Гарантия — только от продавца (DNS, Citilink, Регард), не от Intel
- Доступность нестабильная: крупные партии заходят волнами
- Core Ultra 9 285K часто стоит **дороже** Ryzen 9 9950X, несмотря на формально более низкую рекомендованную цену

На момент написания (июнь 2026) — ожидается мониторинг цен. Ориентировочный диапазон: 80 000–110 000 ₽.

## Для кого

### Идеален

- Видеомонтажёры и контент-мейкеры: QuickSync + 24 ядра — топ для Premiere Pro и DaVinci Resolve
- Рабочие станции смешанного профиля: рендеринг, компиляция, AI-инференс
- Профессионалы, ценящие энергоэффективность: 125W флагман без компромиссов по охлаждению
- Пользователи, кому нужен Intel Arc iGPU для аппаратного AV1-кодирования и Windows Studio Effects
- Сборщики на новом LGA1851 с расчётом на 2 поколения апгрейда
- Те, кто принципиально предпочитает платформу Intel (совместимость с корпоративным ПО)

### Не подходит

- Чистым геймерам: Ryzen X3D объективно быстрее в играх и дешевле
- Оверклокерам-энтузиастам: Arrow Lake разгоняется хуже Raptor Lake, заводской разгон уже близок к пределу
- Бюджетным сборкам: процессор дорогой, платы Z890 — дорогие, охлаждение AIO 360mm — обязательно
- Тем, кто хочет долгосрочную платформу: AM5 поддерживается до 2027+, LGA1851 — предположительно 2 поколения
- Пользователям с DDR4: LGA1851 — только DDR5, придётся менять всю память

## Связки (рекомендуемые)

### Рабочая станция (видеомонтаж)

- **MB:** ASRock Z890 Taichi / MSI Z890 Ace — мощный VRM, Thunderbolt 4
- **RAM:** 64 GB (2×32) DDR5-7200 CL34 (G.Skill Trident Z5)
- **Охлаждение:** Arctic Liquid Freezer III 360
- **GPU:** RTX 5080 / RTX 5090 (для CUDA-ускорения)

### Профессиональная универсальная

- **MB:** ASUS ROG Strix Z890-E / GIGABYTE Z890 AORUS Elite
- **RAM:** 48 GB (2×24) DDR5-8000 CUDIMM (G.Skill или Kingston)
- **Охлаждение:** Lian Li Galahad II Trinity 360
- **GPU:** RTX 5070 Ti и выше

## Источники

1. Intel Core Ultra 200S Series Product Brief (intel.com, October 2024)
2. Gamers Nexus — Intel Core Ultra 9 285K Review & Benchmarks (October 2024)
3. Hardware Unboxed — Arrow Lake Gaming: What Went Wrong? (November 2024)
4. TechPowerUp — Core Ultra 9 285K Review (October 2024)
5. Der8auer — Arrow Lake Delid & OC Analysis (November 2024)
6. Puget Systems — Intel Core Ultra 200S for Premiere Pro & DaVinci Resolve (2025)
7. Price.ru — мониторинг российского рынка (данные ожидаются)
