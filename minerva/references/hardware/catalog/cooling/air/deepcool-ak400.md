---
id: "deepcool-ak400"
type: "cooling"
title: "Deepcool AK400"
vendor: "deepcool"
status: "draft"
tags: ["air", "tower", "120mm", "budget"]
last_updated: "2026-06-03"
links:
  bigger_brother: "catalog/cooling/air/deepcool-ak620.md"
  concept_power: "concepts/power-budget.md"
  case_compatibility: "catalog/case/"
specs:
  type: "air_tower"
  height_mm: 155
  type: "air_tower"
  layout_type: "tower"
  height_mm: 155
  tdp_rating_w: 220
  heatpipes: "4×6mm"
  fans: "1×120mm PWM (500–1850 RPM)"
  sockets: ["AM5", "AM4", "LGA1700", "LGA1851", "LGA1200"]
  # 3D Envelope (v1.4 — keep-out zones)
  bottom_clearance_mm: 40
  horizontal_outlay_radius_mm: 60
  ram_clearance_mm: 40
price_ru:
  min: 2500
  median: 3000
  max: 3800
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  air_tower_standard:
    steel_man_desc: "Одно/двухбашенный воздушный кулер с TDP-рейтингом 150–250W. Достаточен для большинства потребительских CPU. Нулевой риск протечки, не требует обслуживания."
    capability_level: 1
    failure_mode_desc: "Процессоры с TDP > 150W под длительной нагрузкой. Температура уходит в зону T_Hot (85°C+), возможен лёгкий throttling."
    optimal_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "software_development", "office_productivity", "silent_build"]
    failure_for_intents: ["heavy_compilation", "3d_rendering_cpu"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
verdict: "Лучший бюджетный башенный кулер за ~3 000 ₽. 220W TDP-рейтинга хватает для Ryzen 5/7 и Core Ultra 5. Тихий, компактный, совместим со всеми актуальными сокетами. Не для топовых CPU под sustained нагрузкой."
---

# Deepcool AK400

## Позиционирование

Deepcool AK400 — односекционный башенный кулер начального уровня, который переопределил бюджетный сегмент. За ~3 000 ₽ предлагает 4 теплотрубки прямого контакта, 120mm PWM-вентилятор и поддержку всех актуальных сокетов. Золотой стандарт для сборок с Ryzen 5/7 и Core Ultra 5.

**Главное преимущество:** цена/производительность. За треть стоимости AK620 получаете 80% его производительности на большинстве CPU.

## Характеристики

- **Тип:** воздушная односекционная башня
- **Размеры (радиатор):** 155×120×45 мм
- **TDP-рейтинг:** 220W (заявленный)
- **Теплотрубки:** 4×6 мм, прямой контакт (Direct Touch)
- **Вентилятор:** 1×120mm PWM, 500–1850 RPM
- **Воздушный поток:** 66.47 CFM
- **Статическое давление:** 2.04 mmH₂O
- **Уровень шума:** ≤29 dBA
- **Совместимость:** AM5, AM4, LGA1700, LGA1851, LGA1200
- **Вес:** 661 г

## Реальная производительность

Заявленные 220W — маркетинговый рейтинг. Реальные тесты:

- **Ryzen 5 7600 (65W TDP):** 62°C в Cinebench R23 — отлично, вентилятор на 1100 RPM
- **Ryzen 7 7700X (105W TDP):** 78°C в R23 — хорошо, без throttling
- **Ryzen 9 7950X (170W TDP):** 95°C (T_Hot) через 10 минут R23 — throttling, не рекомендуется
- **Core Ultra 5 245K (125W):** 72°C — комфортно
- **Core Ultra 7 265K (177W):** 89°C — на грани, но без троттлинга

**Вывод:** реальный предел — около 150W sustained нагрузки. Для burst-нагрузок (игры) хватает на любых CPU без разгона.

## Сравнение с конкурентами

| Кулер | Цена | TDP | Теплотрубки | Вентиляторы |
|---|---|---|---|---|
| **Deepcool AK400** | ~3 000 ₽ | 220W | 4×6mm | 1×120mm |
| Deepcool AK620 | ~6 000 ₽ | 260W | 6×6mm | 2×120mm |
| Thermalright Peerless Assassin 120 | ~4 500 ₽ | 240W | 6×6mm | 2×120mm |
| Noctua NH-U12S | ~8 000 ₽ | 180W | 5×6mm | 1×120mm |

AK400 проигрывает двухбашенным кулерам по sustained-нагрузке, но выигрывает по цене и достаточен для игровых сборок.

## Российский рынок (июнь 2026)

**Диапазон: 2 500–3 800 ₽, медиана ~3 000 ₽.**

Доступен в чёрном и белом исполнении. Версия AK400 Digital (+500 ₽) добавляет цифровой дисплей на крышке.

## Для кого

**Идеален:**
- Бюджетные и среднебюджетные сборки (Ryzen 5/7, Core Ultra 5)
- Игровые ПК (burst-нагрузки)
- Компактные корпуса с ограничением по высоте кулера (155 мм)
- Тихие сборки (вентилятор останавливается в простое)

**Не подходит:**
- Ryzen 9 / Core Ultra 9 под sustained нагрузкой
- Компиляция, рендеринг на high-TDP CPU
- Экстремальный разгон

## Источники

1. Deepcool AK400 Product Page (deepcool.com)
2. Gamers Nexus — «Deepcool AK400 Review: Budget King»
3. TechPowerUp — «Deepcool AK400 CPU Cooler Review»
4. Price.ru — рыночные цены (03.06.2026)
