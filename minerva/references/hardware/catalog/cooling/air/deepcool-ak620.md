---
id: "deepcool-ak620"
type: "cooling"
title: "Deepcool AK620"
vendor: "deepcool"
status: "draft"
tags: ["air", "dual-tower", "120mm", "high-tdp"]
last_updated: "2026-06-03"
links:
  smaller_brother: "catalog/cooling/air/deepcool-ak400.md"
  concept_power: "concepts/power-budget.md"
  case_compatibility: "catalog/case/"
specs:
  type: "air_dual_tower"
  layout_type: "tower"
  height_mm: 160
  width_mm: 138
  depth_mm: 110
  tdp_rating_w: 260
  heatpipes: "6×6mm"
  fans: "2×120mm PWM (500–1850 RPM)"
  sockets: ["AM5", "AM4", "LGA1700", "LGA1851", "LGA1200"]
  # 3D Envelope (v1.4 — keep-out zones)
  bottom_clearance_mm: 40
  horizontal_outlay_radius_mm: 69
  ram_clearance_mm: 40
price_ru:
  min: 5200
  median: 6000
  max: 7500
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  air_tower_high_tdp:
    steel_man_desc: "Двухбашенный воздушный кулер с TDP-рейтингом 250W+. Справляется с разогнанными и high-TDP процессорами. Надёжнее AIO (нет помпы)."
    capability_level: 2
    failure_mode_desc: "Габариты — высота 160 мм, ширина до 138 мм. Блокирует доступ к слотам RAM на некоторых платах. Требует корпус с запасом по высоте кулера."
    optimal_for_intents: ["heavy_compilation", "3d_rendering_cpu", "scientific_computing"]
    failure_for_intents: ["sff_build"]
    failure_severity: "BLOCK"
    failure_type: "LINEAR_DEGRADATION"
verdict: "Флагманский воздушный кулер Deepcool. 260W TDP, 6 теплотрубок, два 120mm вентилятора — конкурирует с Noctua NH-D15 за половину цены. Отличный выбор для Ryzen 9 и Core Ultra 7/9 под sustained нагрузкой без рисков AIO."
---

# Deepcool AK620

## Позиционирование

Deepcool AK620 — двухбашенный воздушный кулер флагманского уровня. С 6 теплотрубками, двумя 120mm PWM-вентиляторами и TDP-рейтингом 260W, он напрямую конкурирует с Noctua NH-D15, предлагая сопоставимую производительность за значительно меньшие деньги.

**Главное преимущество:** производительность уровня топовых AIO 240–280мм без риска протечки и с неограниченным сроком службы.

## Характеристики

- **Тип:** двухбашенный воздушный кулер
- **Размеры:** 160×138×110 мм
- **TDP-рейтинг:** 260W (заявленный)
- **Теплотрубки:** 6×6 мм, никелированные
- **Вентиляторы:** 2×120mm FK120 PWM, 500–1850 RPM
- **Воздушный поток:** 68.99 CFM (каждый)
- **Статическое давление:** 2.19 mmH₂O
- **Уровень шума:** ≤28 dBA
- **Совместимость:** AM5, AM4, LGA1700, LGA1851, LGA1200
- **Вес:** 1456 г
- **Гарантия:** 5 лет

## Реальная производительность

- **Ryzen 7 7800X3D (120W):** 68°C в R23 — играючи, вентиляторы на 1000 RPM
- **Ryzen 9 7950X (170W):** 88°C через 30 минут R23 — без throttling
- **Core Ultra 7 265K (177W):** 82°C — отлично
- **Core Ultra 9 285K (250W):** 92°C через 20 минут — на грани, лёгкий throttling на пределе

**Вывод:** реальный sustained-предел около 200–220W. Для 250W+ CPU под длительной нагрузкой — AIO 360мм, но AK620 держит всё кроме самых экстремальных сценариев.

## Ограничения по совместимости

**Высота 160 мм** — критичный параметр:
- Большинство Mid-Tower корпусов поддерживают ≤160 мм — **влезает впритык**
- Corsair 4000D (170 мм) — ок
- Fractal Design Pop Air (170 мм) — ок
- NZXT H510 (165 мм) — ок
- Некоторые бюджетные корпуса (155 мм) — **не влезает**

**Ширина 138 мм** — может перекрывать первый слот RAM. На платах с высокими радиаторами памяти (G.Skill Trident Z5, Corsair Vengeance RGB) возможен конфликт. Вентилятор можно сместить выше, но это увеличивает общую высоту до ~165 мм.

## Сравнение с конкурентами

| Кулер | Цена | TDP | Теплотрубки | Вентиляторы | Высота |
|---|---|---|---|---|---|
| **Deepcool AK620** | ~6 000 ₽ | 260W | 6×6mm | 2×120mm | 160 мм |
| Noctua NH-D15 G2 | ~15 000 ₽ | 250W | 8×6mm | 2×140mm | 168 мм |
| Thermalright PA120 | ~4 500 ₽ | 240W | 6×6mm | 2×120mm | 157 мм |
| be quiet! Dark Rock Pro 5 | ~11 000 ₽ | 270W | 7×6mm | 2×135mm | 168 мм |

AK620 предлагает 95% производительности NH-D15 G2 за 40% цены. Thermalright PA120 — единственный конкурент по FPS/₽, но AK620 тише и качественнее собран.

## Российский рынок (июнь 2026)

**Диапазон: 5 200–7 500 ₽, медиана ~6 000 ₽.**

Доступны версии: стандартная (чёрная), WH (белая), Digital (с дисплеем, +1 000–1 500 ₽), Zero Dark (полностью чёрная).

## Для кого

**Идеален:**
- Ryzen 9 / Core Ultra 7/9 под sustained нагрузкой
- Компиляция, рендеринг, научные расчёты
- Сборки, где недопустим риск протечки AIO
- Требовательные, но не экстремальные рабочие станции

**Не подходит:**
- SFF/Mini-ITX сборки (слишком высокий)
- Корпуса с лимитом ≤155 мм
- Core Ultra 9 285K на пределе 250W+ (лучше AIO 360)
- Экстремальный разгон с напряжением >1.3V

## Источники

1. Deepcool AK620 Product Page (deepcool.com)
2. Gamers Nexus — «Deepcool AK620 Review: Noctua NH-D15 Competitor»
3. TechPowerUp — «Deepcool AK620 Dual Tower CPU Cooler Review»
4. Hardware Canucks — «AK620 vs NH-D15: Budget vs Premium»
5. Price.ru — рыночные цены (03.06.2026)
