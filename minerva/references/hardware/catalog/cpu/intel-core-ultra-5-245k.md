---
id: "intel-core-ultra-5-245k"
type: "cpu"
title: "Intel Core Ultra 5 245K (125W)"
vendor: "intel"
status: "draft"
tags: ["intel", "arrow-lake", "lga1851", "ddr5", "125w", "14-core", "quicksync"]
last_updated: "2026-06-03"
external_audit_verification: passed
links:
  platform: "catalog/motherboard/lga1851/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/intel-core-ultra.md"
  up_variant: "catalog/cpu/intel-core-ultra-7-265k.md"
  competitor_amd: "catalog/cpu/amd-ryzen-7-9700x.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "LGA1851"
  architecture: "Arrow Lake (Lion Cove P-cores + Skymont E-cores)"
  lithography: "TSMC N3B (Compute tile) + TSMC N5 (GPU tile) + TSMC N6 (SoC tile) + TSMC N6 (I/O tile) + Intel 22FFL (Base tile)"
  cores: 14
  threads: 14
  p_cores: 6
  e_cores: 8
  base_clock_p: "4.2 GHz"
  base_clock_e: "3.6 GHz"
  boost_clock_p: "5.2 GHz"
  boost_clock_e: "4.6 GHz"
  l2_cache: "26 MB (3 MB × 6 P-core + 4 MB × 2 clusters E-core)"
  l3_cache: "24 MB"
  tdp: "125W"
  tdp_pl2: "159W"
  tjmax: "105°C"
  pcie_lanes: "24 CPU (16× PCIe 5.0 + 4× PCIe 5.0 + 4× PCIe 4.0), конфигурации: 1×16+2×4 / 2×8+2×4 / 1×8+4×4"
  pcie_version: "5.0"
  memory: "DDR5 only, dual-channel, до 6400 JEDEC / 8000+ XMP (CUDIMM)"
  max_memory: "192 GB официально (4×48 GB), практический лимит на валидированных платах — 256 GB (4×64 GB)"
  igpu: "Intel Graphics (4 Xe-LPG cores, до 1.9 GHz, QuickSync)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "Q4 2024"
  multiplier: "unlocked"
  multiplier_source: "https://www.intel.com/content/www/us/en/products/sku/241067/intel-core-ultra-5-processor-245k-24m-cache-up-to-5-20-ghz/specifications.html"
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
  note: "Цены в РФ завышены из-за санкций"
binning:
  full_die: "Arrow Lake-S (8P+16E, tile-based)"
  active_config: "6P+8E (отключены 2 P-cores + 2 E-core кластера)"
  disabled: "2 P-cores + 8 E-cores — продуктовая сегментация"
  percent_active: 58
platform_req:
  motherboard_min: "Z890 / B860 (LGA1851)"
  motherboard_opt: "B860"
  cooler_min: "Однобашенный воздух"
  cooler_opt: "Однобашенный воздух (Thermalright Assassin X120 / Deepcool AK400)"
  memory_sweet_spot: "DDR5-6400"
  psu_min_cpu: "600W"
  psu_min_system: "750W"
engineering_notes: "PL2 всего 159W — холодный Arrow Lake. Undervolting-friendly. K-series unlocked но разгон ограничен 6 P-cores. Встроенный Intel Arc Graphics (Xe-LPG)."
verdict: "Младший K-процессор Arrow Lake. 14 ядер, 125W, QuickSync и Intel Arc iGPU. Хороший вход в LGA1851 для создателей контента с ограниченным бюджетом. В играх уступает Ryzen 5 9600X, но в продуктивности — силён благодаря E-ядрам."
---

# Intel Core Ultra 5 245K (125W)

## Позиционирование

Core Ultra 5 245K — младший разблокированный процессор Arrow Lake с TDP 125W. Конфигурация: 6 P-cores Lion Cove + 8 E-cores Skymont (14 ядер / 14 потоков, без Hyper-Threading). По позиционированию — наследник Core i5-14600K, но с радикально лучшей энергоэффективностью и новым сокетом.

По сути — это процессор для создателей контента начального уровня: QuickSync для видеомонтажа, Intel Arc iGPU для аппаратного кодирования, 14 ядер для многозадачности. В играх — не рекордсмен, но достаточен для любого гейминга на 1440p и 4K.

Ключевое преимущество перед предшественником (i5-14600K): 125W TDP против 181W Turbo — процессор **холоднее и тише** при сопоставимой производительности.

## Характеристики

### Архитектура

Arrow Lake, чиплетная компоновка:

- **Compute tile (TSMC N3B):** 6 P-cores + 8 E-cores
- **SoC tile (TSMC N6):** DDR5-контроллер, PCIe 5.0
- **GPU tile (TSMC N5):** Intel Graphics Xe-LPG (4 Xe-ядра, до 1.9 GHz)
- **Base tile:** Intel 22FFL, Foveros-интерконнект

### Базовые параметры

- Сокет: LGA1851, чипсеты Z890 / B860 / H810
- Ядер / потоков: 14C/14T (6P + 8E)
- Техпроцесс: TSMC N3B (Compute tile)
- P-cores: база 4.2 GHz, boost до 5.2 GHz
- E-cores: база 3.6 GHz, boost до 4.6 GHz
- L2-кэш: 26 MB (18 MB P-core + 8 MB E-core)
- L3-кэш: 24 MB Smart Cache
- TDP (PL1 / PL2): 125W / 159W
- TJmax: 105°C
- iGPU: Intel Graphics (4 Xe-LPG, 1.9 GHz) — QuickSync, аппаратное AV1-кодирование
- Кулер в коробке: нет

### Память и PCIe

- DDR5 only, dual-channel
- JEDEC: до DDR5-6400
- XMP: до DDR5-8000+ (CUDIMM)
- Макс. объём: 192 GB
- PCIe: 24 линии CPU (16× 5.0 + 4× 5.0 + 4× 4.0)

## Производительность

### Синтетика

**Cinebench R23:**
- Single-core: ~2 180 баллов
- Multi-core (stock 125W): ~22 000 баллов
- Multi-core (PL2 159W): ~24 500 баллов
- Для сравнения — i5-14600K (181W): ~24 000 multi при 181W. 245K догоняет при **на 22W меньшем** PL2
- Для сравнения — Ryzen 5 9600X (6C/12T, 65W): ~16 500 multi. 245K впереди на 33%+ в многопотоке

**Cinebench 2024:**
- Single-core: ~136 баллов
- Multi-core: ~1 350 баллов

**Blender Benchmark:**
- Classroom: ~10:00 (265K: ~6:30; Ryzen 5 9600X: ~11:30)

### Игры (1440p, RTX 4070 Ti)

Как и все Arrow Lake, в играх 245K не блещет:

- Cyberpunk 2077: ~135 fps (Ryzen 5 9600X: ~148 fps; разница ~9%)
- Baldur's Gate 3: ~148 fps (9600X: ~172 fps; разница ~14%)
- CS2: ~410 fps (9600X: ~520 fps; разница ~21%)
- Call of Duty Warzone: ~220 fps (9600X: ~240 fps; разница ~8%)

Для 1440p с видеокартами уровня RTX 4070 Ti и ниже — 245K **не является узким местом**. На 4K разница с Ryzen 9600X сокращается до 3–5%. Процессор достаточен для подавляющего большинства геймеров.

### Продуктивность

- **Premiere Pro:** QuickSync даёт +10–15% к скорости экспорта относительно Ryzen 5 9600X (у которого аппаратного энкодера нет). Для бюджетного видеомонтажа — отличный выбор.
- **7-Zip компрессия:** 14 ядер обходят 6-ядерный 9600X на 30–40%.
- **Photoshop / Lightroom:** паритет с 9600X, разница в пределах 3%.
- **Стриминг (OBS + игра):** E-cores берут на себя фоновые задачи + QuickSync кодирует стрим — нагрузка на P-cores минимальна.

**Ключевой вывод:** 245K — процессор для «играю и работаю». Если вы иногда монтируете видео, стримите или компилируете код — E-cores и QuickSync дают преимущество над чисто игровыми 6-ядерными Ryzen.

## Память: практические рекомендации

- **DDR5-6400 CL32** — оптимально для 245K. JEDEC-максимум без лишних затрат.
- **DDR5-7200 CL34** — имеет смысл, если планируете апгрейд на 265K/285K в будущем. Прирост над 6400 — 3–5%.
- **DDR5-8000+ (CUDIMM):** неоправданно дорого для процессора этого класса.
- **DDR5-5600 CL40:** приемлемый бюджетный минимум. Потеря 6–10% относительно 6400.

**Рекомендация:** 32 GB (2×16) DDR5-6400 CL32 — золотая середина. Не переплачивайте за сверхскоростную память — 245K не настолько чувствителен к частоте, как флагманы.

## Охлаждение и энергопотребление

### Реальное потребление

- **Idle:** 45–60W (чиплетная архитектура повышает потребление в простое)
- **Игры:** 65–90W (обычно 70–80W)
- **Cinebench R23 multi (PL1=125W):** 125W
- **Cinebench R23 multi (PL2=159W):** 155–160W

Для сравнения: i5-14600K в играх потреблял 100–140W. 245K экономит 30–50W — огромная разница.

### Температуры

- **Башенный кулер (Peerless Assassin 120, AK400):** stock 125W — 60–70°C в Cinebench; игры — 50–62°C. Идеально тихо.
- **Бюджетный кулер (ID-COOLING SE-224-XTS):** stock 125W — 70–78°C. Вполне достаточно.
- **AIO 240mm:** избыточно для стока, но полезно при разблокировке PL2.

**Рекомендация:** 245K охлаждается **воздухом** без проблем. Башенный кулер за 2 500–4 000 ₽ достаточен с запасом. AIO не нужен — это приятный бонус после эпохи Raptor Lake.

### Разгон

- P-cores: потенциал ограничен. +100–200 MHz сверх boost — типичный результат.
- E-cores: можно поднять до ~4.8 GHz.
- Undervolt: −50…−80 mV снижает температуры на 8–12°C. Рекомендуется.
- PL2: на платах Z890 можно разблокировать до ~180–200W — даст +5–8% многопотока ценой нагрева.

## Сравнение с AMD аналогами

### Против Ryzen 5 9600X (6C/12T, 65W, Zen 5)

- Ядра/потоки: 14C/14T vs 6C/12T — Intel имеет подавляющее преимущество в многопотоке
- TDP: 125W vs 65W — AMD эффективнее в стоке
- Cinebench R23 multi: ~22 000 vs ~16 500 — Intel впереди на 33%
- Cinebench R23 single: ~2 180 vs ~2 200 — паритет
- Игры: 9600X быстрее на 8–15% (особенно в 1080p)
- QuickSync: есть vs нет — ключевое различие
- Цена в РФ (ориентировочно): 245K дороже на 20–30% из-за санкций

**Вывод:** 9600X — лучший чисто игровой процессор. 245K — лучший гибридный процессор (игры + работа + стриминг). Если вы ТОЛЬКО играете — берите 9600X. Если работаете с видео — 245K выигрывает.

### Против Ryzen 7 7700 (8C/16T, 65W, Zen 4)

- Ядра/потоки: 14/14 vs 8/16 — Intel выигрывает по числу физических ядер, но у AMD есть SMT
- Cinebench R23 multi: ~22 000 vs ~18 500 — Intel впереди на 19%
- Игры: примерно паритет (7700 чуть быстрее в среднем на 3–5%)
- QuickSync: у 245K есть, у 7700 iGPU — только вывод изображения

**Вывод:** 245K и 7700 — близкие конкуренты. 245K выигрывает в продуктивности, 7700 — в играх и цене (дешевле в РФ).

## Российский рынок

Санкции делают Intel менее привлекательным по цене. Ориентировочная цена 245K в РФ: 35 000–45 000 ₽. Для сравнения:

- Ryzen 5 9600X: ~26 000–32 000 ₽
- Ryzen 7 7700: ~15 000–18 000 ₽ (значительно дешевле)

При такой разнице в цене 7700 становится более рациональным выбором для большинства сборщиков в РФ, **если только вам не критичен QuickSync**. Если же видеомонтаж — важная часть рабочего процесса, переплата за 245K оправдана.

## Для кого

### Идеален

- Начинающие видеомонтажёры и стримеры: QuickSync + E-cores — мощный фундамент для старта
- Пользователи со смешанным профилем: игры + работа с фото/видео
- Сборщики, входящие в LGA1851 с прицелом на апгрейд до 285K в будущем
- Те, кто ценит тишину и холод: 125W на воздухе — идеально
- Пользователи, кому нужен Intel Arc iGPU для аппаратного кодирования AV1

### Не подходит

- Чистым геймерам: Ryzen 5 9600X или Ryzen 7 7700 (AM5) — дешевле и быстрее в играх
- Сборщикам с DDR4: новый сокет + DDR5 = замена всей платформы, дорого
- Тем, у кого уже i5-14600K: прирост минимален, апгрейд не оправдан
- Тяжёлым рабочим нагрузкам: 14 ядер для рендеринга — маловато, смотрите 265K или 285K
- Бюджетным сборкам до 80 000 ₽: AM5 с Ryzen 5 7500F или 7600 — намного дешевле

## Связки (рекомендуемые)

### Бюджетная игровая + работа

- **MB:** GIGABYTE Z890 UD / ASRock Z890 Pro RS (или B860 при выходе)
- **RAM:** 32 GB (2×16) DDR5-6400 CL32 (TeamGroup T-Create / G.Skill Ripjaws)
- **Охлаждение:** Thermalright Peerless Assassin 120 (~3 500 ₽)
- **GPU:** RTX 5070 / RX 9070

### Оптимальная для стриминга

- **MB:** MSI Z890 Tomahawk Wi-Fi
- **RAM:** 32 GB (2×16) DDR5-7200 CL34
- **Охлаждение:** Deepcool AK620 / Arctic Freezer 36
- **GPU:** RTX 5070 Ti

## Источники

1. Intel Core Ultra 200S Product Brief (intel.com, 2024)
2. Gamers Nexus — Core Ultra 5 245K Review (October 2024)
3. Hardware Unboxed — Arrow Lake Gaming Analysis (November 2024)
4. TechPowerUp — Core Ultra 5 245K Review (October 2024)
5. Puget Systems — Content Creation Benchmarks (2025)
