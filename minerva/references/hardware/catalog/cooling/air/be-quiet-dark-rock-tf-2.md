---
id: "be-quiet-dark-rock-tf-2"
type: "cooling"
title: "be quiet! Dark Rock TF 2"
vendor: "be-quiet"
status: "verified"
tags: ["air", "top-flow", "dual-heatsink", "silent-wings", "high-tdp", "am5"]
last_updated: "2026-06-06"
links:
  concept_power: "concepts/power-budget.md"
  case_compatibility: "catalog/case/"
specs:
  type: "air_tower_standard"
  layout_type: "top_flow"
  height_mm: 134
  tdp_rating_w: 230
  heatpipes: "6×6mm"
  fans: "2×Silent Wings 3 135mm PWM"
  noise_dba:
    min: 12
    max: 27.1
  sockets: ["AM5", "AM4", "LGA1700", "LGA1851", "LGA1200"]
  # 3D Envelope (v1.4 — keep-out zones)
  bottom_clearance_mm: 40
  horizontal_outlay_radius_mm: 68
  ram_clearance_mm: 45
price_ru:
  min: 7400
  median: 7600
  max: 7800
  source: "price.ru, DNS, Ozon, Wildberries"
  date: "2026-06-06"
profiles:
  air_tower_standard:
    steel_man_desc: "Топовый top-flow кулер с 230W TDP. Два вентилятора Silent Wings 3 на минимальных оборотах — мощный downdraft на VRM/M.2. Идеален для аудио-станций и silent-сборок без dGPU."
    capability_level: 1
    failure_mode_desc: "Высота 134mm — проверять совместимость с корпусом. Dual-вентилятор может перекрывать высокие модули RAM."
    optimal_for_intents: ["silent_build", "sff_build", "software_development", "office_productivity", "aaa_1080p_ultra"]
    failure_for_intents: ["heavy_compilation", "3d_rendering_cpu"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
verdict: "Флагманский top-flow кулер be quiet! с TDP 230W. Два вентилятора Silent Wings 3 обеспечивают мощный downdraft на VRM и M.2 — критично для плат без активного охлаждения VRM. Идеален для аудио-станций, compact-сборок и silent-конфигураций. На AM5 работает из коробки."
---

# be quiet! Dark Rock TF 2

## Позиционирование

be quiet! Dark Rock TF 2 — двухсекционный top-flow кулер флагманского уровня. С 6 теплотрубками, двумя вентиляторами Silent Wings 3 (135mm) и TDP-рейтингом 230W, это самый мощный top-flow кулер на рынке. В отличие от башенных кулеров, поток воздуха направлен **вниз на материнскую плату** — активное охлаждение VRM, M.2 и слотов RAM.

**Главное преимущество:** мощный downdraft на подсистему питания и NVMe-диски, плюс рекордная тишина — вентиляторы Silent Wings 3 на 600 RPM практически бесшумны. Идеален для silent-сборок без выделенного GPU-потока.

## Характеристики

- **Тип:** двухсекционный top-flow (два heatsink блока, продув сверху вниз)
- **Высота:** 134 мм (один из самых низких high-TDP кулеров)
- **TDP-рейтинг:** 230W (официальный, bequiet.com)
- **Теплотрубки:** 6×6 мм, никелированные
- **Вентилятор 1:** Silent Wings 3 135mm PWM (верхний, 1000–1400 RPM)
- **Вентилятор 2:** Silent Wings 135mm PWM (нижний, 1000–1400 RPM)
- **Уровень шума:** 12 dBA (мин) — 27.1 dBA (макс)
- **Совместимость:** AM5, AM4, LGA1700, LGA1851, LGA1200
- **Гарантия:** 3 года

## Реальная производительность

- **Ryzen 7 7800X3D (120W):** 72°C в R23 — отлично, вентиляторы на ~800 RPM
- **Ryzen 9 7950X (170W):** 90°C через 30 минут R23 — на грани, но без throttling
- **Core Ultra 7 265K (177W):** 85°C — достойно для top-flow
- **Core Ultra 9 285K (250W):** 95°C+ через 15 минут — **не рекомендуется**, лучше башенный кулер или AIO

**Вывод:** реальный sustained-предел около 170–180W. Для 230W+ CPU под длительной нагрузкой — башенный кулер или AIO. Dark Rock TF 2 берёт не абсолютной мощностью, а **направленным охлаждением зоны VRM/M.2**.

## Ограничения по совместимости

**Высота 134 мм** — важный параметр:
- Большинство Mid-Tower корпусов (≥150 мм) — **с запасом**
- Корпуса с ограничением ≤135 мм — **впритык, проверять**
- SFF/ITX корпуса (≤100 мм) — **не влезает**

**Dual-вентилятор и RAM:**
- Два вентилятора могут перекрывать слоты DIMM на некоторых платах
- Высокие модули RAM (G.Skill Trident Z5 ≥44 мм) — возможен конфликт с нижним вентилятором
- Решение: сместить или снять нижний вентилятор (потеря 5–8°C на CPU, но downdraft сохраняется)

**Top-flow преимущество:**
- Охлаждение VRM и M.2 под радиатором — **не требует отдельных вентиляторов**
- Для плат без радиаторов на VRM (бюджетные B650/B760) — критическое преимущество

## Сравнение с конкурентами

| Кулер | Тип | TDP | Высота | Вентиляторы | Шум (max) | Цена |
|---|---|---|---|---|---|---|
| **be quiet! Dark Rock TF 2** | Top-flow | 230W | 134 мм | 2×135mm | 27.1 dBA | ~7 600 ₽ |
| Noctua NH-C14S | Top-flow | ~150W | 115/82 мм | 1×140mm | 24.6 dBA | ~9 000 ₽ |
| Deepcool AK620 | Башня | 260W | 160 мм | 2×120mm | 28 dBA | ~6 000 ₽ |
| Thermalright AXP120-X67 | Low-profile | ~150W | 67 мм | 1×120mm | 30 dBA | ~4 500 ₽ |

Dark Rock TF 2 — компромисс: мощнее NH-C14S, ниже любого башенного кулера, но дороже и требует проверки совместимости с RAM.

## Российский рынок (июнь 2026)

**Диапазон: 7 400–7 800 ₽, медиана ~7 600 ₽.**

Присутствует на Ozon, Wildberries, DNS. Стабильный сток, дефицита нет. По сравнению с башенными кулерами сопоставимой мощности — переплата ~1 500 ₽ за top-flow форм-фактор и бренд be quiet!.

## Для кого

**Идеален:**
- Silent-сборки: аудио-станции, HTPC, медиасерверы
- Системы с пассивным охлаждением VRM (бюджетные платы)
- Compact ATX/mATX без выделенного airflow на зону CPU (нет верхних вентиляторов)
- Сборки с единственным корпусным вентилятором на выдув

**Не подходит:**
- Core Ultra 9 285K / Ryzen 9 7950X под sustained нагрузкой (лучше башенный кулер)
- Экстремальный разгон с напряжением >1.25V
- SFF корпуса с лимитом ≤110 мм (нужен low-profile кулер)
- Сборки с высокими модулями RAM + dual-вентилятор

## Источники

1. be quiet! Dark Rock TF 2 Product Page (bequiet.com)
2. TechPowerUp — «be quiet! Dark Rock TF 2 Review»
3. KitGuru — «be quiet! Dark Rock TF 2: Top-Flow Titan»
4. price.ru, DNS, Ozon, Wildberries — рыночные цены (06.06.2026)
5. Noctua AM5 compatibility list (noctua.at)
