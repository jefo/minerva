---
id: "intel-core-ultra-7-265k"
type: "cpu"
title: "Intel Core Ultra 7 265K (125W)"
vendor: "intel"
status: "draft"
tags: ["intel", "arrow-lake", "lga1851", "ddr5", "125w", "20-core", "quicksync"]
last_updated: "2026-06-03"
external_audit_verification: passed
links:
  platform: "catalog/motherboard/lga1851/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/intel-core-ultra.md"
  up_variant: "catalog/cpu/intel-core-ultra-9-285k.md"
  down_variant: "catalog/cpu/intel-core-ultra-5-245k.md"
  competitor_amd: "catalog/cpu/amd-ryzen-9-9900x.md"
  concepts:
    - "concepts/power-budget.md"
specs:
  socket: "LGA1851"
  architecture: "Arrow Lake (Lion Cove P-cores + Skymont E-cores)"
  lithography: "TSMC N3B (Compute tile) + TSMC N5 (GPU tile) + TSMC N6 (SoC tile) + TSMC N6 (I/O tile) + Intel 22FFL (Base tile)"
  cores: 20
  threads: 20
  p_cores: 8
  e_cores: 12
  base_clock_p: "3.9 GHz"
  base_clock_e: "3.3 GHz"
  boost_clock_p: "5.5 GHz"
  boost_clock_e: "4.6 GHz"
  l2_cache: "36 MB (3 MB × 8 P-core + 4 MB × 3 clusters E-core)"
  l3_cache: "30 MB (два кластера по 15 MB, физически меньше чем 36 MB у 285K — не просто отключённые слайсы)"
  tdp: "125W"
  tdp_pl2: "250W"
  tjmax: "105°C"
  pcie_lanes: "24 CPU (16× PCIe 5.0 + 4× PCIe 5.0 + 4× PCIe 4.0), конфигурации: 1×16+2×4 / 2×8+2×4 / 1×8+4×4"
  pcie_version: "5.0"
  memory: "DDR5 only, dual-channel, до 6400 JEDEC / 8000+ XMP (CUDIMM)"
  max_memory: "192 GB официально (4×48 GB), практический лимит на валидированных платах — 256 GB (4×64 GB)"
  igpu: "Intel Graphics (4 Xe-LPG cores, до 2.0 GHz, QuickSync)"
  box_cooler: null
  package: "Retail (BOX, без кулера)"
  release_date: "Q4 2024"
  multiplier: "unlocked"
  multiplier_source: "https://www.intel.com/content/www/us/en/products/sku/241063/intel-core-ultra-7-processor-265k-30m-cache-up-to-5-50-ghz/specifications.html"
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
  note: "Цены в РФ завышены из-за санкций и параллельного импорта"
binning:
  full_die: "Arrow Lake-S (8P+16E, tile-based)"
  active_config: "8P+12E (отключён 1 E-core кластер)"
  disabled: "4 E-cores (1 кластер) — продуктовая сегментация"
  percent_active: 83
platform_req:
  motherboard_min: "Z890 (LGA1851)"
  motherboard_opt: "Z890"
  cooler_min: "280mm AIO / двухбашенный воздух"
  cooler_opt: "280mm AIO / Noctua NH-D15 G2"
  memory_sweet_spot: "DDR5-8000 CUDIMM"
  psu_min_cpu: "750W"
  psu_min_system: "900W"
engineering_notes: "То же что 285K но без 4 E-cores. В играх идентичен 285K. Встроенный Intel Arc Graphics (Xe-LPG) с аппаратным AV1 encode. CUDIMM выгода — до +5-8% в latency-sensitive нагрузках vs стандартной DDR5."
verdict: "Золотая середина Arrow Lake: 8 P-cores + 12 E-cores за 125W. Отличный выбор для создателей контента, кому не нужен флагманский 285K. QuickSync, Intel Arc iGPU и эффективность — сильные стороны. В играх уступает X3D, но для продуктивности — один из лучших в классе."
---

# Intel Core Ultra 7 265K (125W)

## Позиционирование

Core Ultra 7 265K — «серебряный» процессор Arrow Lake: те же 8 P-cores, что у флагмана 285K, но 12 E-cores вместо 16 и чуть ниже частоты. По сути — 285K с урезанной многопоточной производительностью, но с идентичной однопоточной в лёгких нагрузках.

Позиционируется Intel против AMD Ryzen 9 9900X (12C/24T, 120W). В многопотоке 265K выигрывает за счёт большего количества ядер (20 против 12), в играх — проигрывает из-за архитектурных особенностей Arrow Lake. QuickSync и Intel Arc iGPU — сильные дифференциаторы, которых у AMD нет.

Для видеомонтажёра или стримера с ограниченным бюджетом — вероятно, **оптимальный процессор Arrow Lake**: почти флагманская производительность за меньшие деньги. Разница с 285K в реальных сценариях — 10–15%, что редко оправдывает переплату.

## Характеристики

### Архитектура

Та же чиплетная Arrow Lake, что у 285K:

- **Compute tile (TSMC N3B):** 8 P-cores Lion Cove + 12 E-cores Skymont. Hyper-Threading отсутствует.
- **SoC tile (TSMC N6):** контроллер DDR5, PCIe 5.0.
- **GPU tile (TSMC N5):** Intel Graphics Xe-LPG (4 Xe-ядра, до 2.0 GHz).
- **Base tile:** Intel 22FFL, Foveros-интерконнект.

### Базовые параметры

- Сокет: LGA1851, чипсеты Z890 / B860 / H810
- Ядер / потоков: 20C/20T (8P + 12E)
«Техпроцесс: TSMC N3B (Compute) + TSMC N5 (GPU) + N6 (SoC)»
- P-cores: база 3.9 GHz, boost до 5.5 GHz
- E-cores: база 3.3 GHz, boost до 4.6 GHz
- L2-кэш: 36 MB (24 MB P-core + 12 MB E-core кластеров)
- L3-кэш: 30 MB Smart Cache
- TDP (PL1 / PL2): 125W / 250W
- TJmax: 105°C
- iGPU: Intel Graphics (4 Xe-LPG, 2.0 GHz) — QuickSync, аппаратное AV1-кодирование
- Кулер в коробке: нет

### Память и PCIe

- DDR5 only, dual-channel
- JEDEC: до DDR5-6400
- XMP: до DDR5-8000+ (CUDIMM)
- Макс. объём: 192 GB официально (4×48 GB), практический лимит 256 GB (4×64 GB)
- PCIe: 24 линии от CPU (16× 5.0 + 4× 5.0 + 4× 4.0)

## Производительность

### Синтетика

**Cinebench R23:**
- Single-core: ~2 280 баллов (всего на 1% ниже 285K — идентичные P-cores)
- Multi-core (stock 125W): ~32 000 баллов
- Multi-core (PL2 без лимитов): ~36 000 баллов
- Для сравнения — 285K: ~39 000 (+22%), но и стоит значительно дороже
- Для сравнения — Ryzen 9 9900X (120W): ~33 000 — паритет

**Cinebench 2024:**
- Single-core: ~142 балла
- Multi-core: ~1 850 баллов

**Blender Benchmark:**
- Classroom: ~6:30 (285K: ~5:20; 9900X: ~6:40)

### Игры (1440p, RTX 4080)

Ситуация аналогична 285K — Arrow Lake в играх объективно уступает AMD X3D:

- Cyberpunk 2077: ~153 fps (7800X3D: ~182 fps)
- Baldur's Gate 3: ~168 fps (7800X3D: ~205 fps)
- CS2: ~470 fps (7800X3D: ~610 fps)
- Hogwarts Legacy: ~132 fps (7800X3D: ~148 fps)

Для 4K-гейминга разница сокращается до 3–7% — процессор не является узким местом с любой видеокартой.

### Видеомонтаж и продуктивность

- **Premiere Pro (экспорт H.265):** 265K с QuickSync быстрее Ryzen 9 9900X на ~15%. Аппаратный энкодер Intel всё ещё лучший в индустрии.
- **DaVinci Resolve (рендер 4K):** паритет с 9900X, но QuickSync даёт преимущество при живом превью.
- **7-Zip:** ~10% быстрее 9900X благодаря 20 ядрам.
- **Компиляция (Chromium):** паритет с 9900X.

**Ключевой вывод:** для видеомонтажа 265K — лучший процессор в ценовой категории между 9900X и 9950X. QuickSync — «секретное оружие», которого у AMD нет.

## Память: практические рекомендации

Контроллер памяти идентичен 285K:

- **DDR5-6400 CL32** — стабильный старт, JEDEC-максимум
- **DDR5-7200 CL34** — золотой стандарт для 265K. Соотношение цены и производительности оптимальное
- **DDR5-8000+ (CUDIMM):** поддерживается, но прирост над 7200 — 2–4% в играх. Для продуктивности — ещё меньше. Не всегда оправдывает переплату
- **DDR5-5600 CL40:** избегайте с 265K. Потеря 8–12% производительности относительно 7200

**Рекомендация:** 32–64 GB DDR5-7200 CL34 — идеал для 265K. Не переплачивайте за CUDIMM 8000+, если бюджет ограничен.

## Охлаждение и энергопотребление

### Реальное потребление

- **Idle:** 45–60W (чиплетная архитектура повышает потребление в простое относительно монолитных CPU)
- **Игры:** 85–120W (в среднем ~100W)
- **Cinebench R23 multi (PL1=125W):** 125W
- **Cinebench R23 multi (PL2 без лимитов):** 210–240W
- **Для сравнения — i7-14700K (253W PL2):** 200–280W в пиковых нагрузках. 265K на базовом PL1 125W потребляет существенно меньше при сопоставимой производительности; при равном PL2 (~250W) обходит 14700K по эффективности без риска деградации

### Температуры и охлаждение

- **AIO 360mm:** stock — 62–72°C; PL2 без лимитов — 80–90°C
- **AIO 240mm:** stock — 70–80°C; PL2 — на грани (88–98°C)
- **Воздушная башня (NH-D15, Peerless Assassin 120):** stock — 75–85°C; PL2 — throttling при 240W

**Рекомендация:** AIO 240mm — минимально достаточное охлаждение для стокового режима. Для разблокировки PL2 берите AIO 360mm. Но в отличие от Raptor Lake — даже воздух справляется в стоке.

### Разгон и undervolt

- P-cores: +100–200 MHz заводского разгона — и всё. TSMC N3B чипы уже на пределе.
- E-cores: можно поднять до ~4.8 GHz на все ядра
- Undervolt: −50…−70 mV стабильно снижает температуры на 8–10°C. Рекомендуется всем.
- D2D частота: +200 MHz снижает игровую latency на 3–5 ns

## Сравнение с AMD аналогами

### Против Ryzen 9 9900X (12C/24T, 120W, Zen 5)

- Ядра/потоки: 20C/20T vs 12C/24T — больше физических ядер у Intel
- TDP: 125W vs 120W — паритет
- Cinebench R23 multi: ~32 000 vs ~33 000 — паритет (±3%)
- Cinebench R23 single: ~2 280 vs ~2 320 — AMD чуть впереди (~2%)
- Игры: 9900X быстрее на 5–12% (особенно в 1080p)
- Видеомонтаж (QuickSync): 265K быстрее на 10–15% при аппаратном энкодинге
- Сокет: LGA1851 (2 gen) vs AM5 (до 2027+)

**Вывод:** 265K и 9900X — прямые конкуренты. Intel выигрывает в видеомонтаже (QuickSync). AMD — в играх и долговечности платформы. При равной цене (что редкость в РФ) — выбор за сценариями использования.

### Против Ryzen 7 7800X3D (8C/16T, 120W, Zen 4, 3D V-Cache)

- Ядра/потоки: 20/20 vs 8/16 — двукратное преимущество Intel в многопотоке
- Cinebench R23 multi: ~32 000 vs ~18 500 — Intel впереди на 73%
- Игры: 7800X3D быстрее на 15–25%
- QuickSync: у 265K есть, у 7800X3D нет

**Вывод:** чистым геймерам — берите 7800X3D/9800X3D не думая. Смешанный профиль (игры + работа с видео) — 265K более универсален.

## Российский рынок

Из-за санкций Intel поставляется через параллельный импорт. Ожидаемая цена 265K в РФ: 55 000–75 000 ₽ (ориентировочно, данные уточняются).

Для сравнения: Ryzen 9 9900X в РФ стоит 48 000–58 000 ₽ — дешевле из-за меньших санкционных наценок. Это делает 9900X более привлекательным по соотношению цена/производительность, **если только вам не критичен QuickSync**.

## Для кого

### Идеален

- Видеомонтажёры и контент-креаторы: 20 ядер + QuickSync — убийственная комбинация для Premiere Pro
- Стримеры: 8 P-cores + энкодер QuickSync для кодирования стрима без потери FPS
- Сборщики, кому не нужен флагманский 285K, но нужна платформа LGA1851 с запасом на апгрейд
- Пользователи, ценящие энергоэффективность: 125W с производительностью уровня 14700K

### Не подходит

- Геймерам: Ryzen X3D быстрее и дешевле. Разница ощутима.
- Бюджетным сборкам: LGA1851 + DDR5 — дорогой вход даже с чипсетами B860
- Тем, у кого уже есть i7-14700K или i9-14900K: прирост в играх минимален, апгрейд оправдан только для продуктивности
- Желающим долгосрочную платформу: AM5 — более надёжная инвестиция

## Связки (рекомендуемые)

### Видеомонтаж (оптимальная)

- **MB:** MSI Z890 Tomahawk Wi-Fi / ASRock Z890 Pro RS
- **RAM:** 64 GB (2×32) DDR5-7200 CL34
- **Охлаждение:** Arctic Liquid Freezer III 280 или Deepcool LS720
- **GPU:** RTX 5070 Ti (NVENC + CUDA в паре с QuickSync)

### Универсальная (игры + работа)

- **MB:** GIGABYTE Z890 AORUS Elite
- **RAM:** 32 GB (2×16) DDR5-7200 CL34
- **Охлаждение:** Thermalright Peerless Assassin 120 (для стока 125W), AIO 280mm для PL2
- **GPU:** RTX 5080 / RX 9070 XT

## Источники

1. Intel Core Ultra 200S Series Product Brief (intel.com, 2024)
2. Gamers Nexus — Core Ultra 7 265K Review (October 2024)
3. Hardware Unboxed — Arrow Lake Gaming Benchmarks (November 2024)
4. Puget Systems — Premiere Pro & DaVinci Resolve with Arrow Lake (2025)
5. TechPowerUp — Core Ultra 7 265K Review (October 2024)
