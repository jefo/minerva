---
id: "be-quiet-straight-power-12-750w"
type: "psu"
title: "be quiet! Straight Power 12 750W 80+ Platinum"
vendor: "be-quiet"
status: "draft"
tags: ["atx3.1", "750w", "platinum", "fully-modular", "12v-2x6", "semi-passive", "premium"]
last_updated: "2026-06-05"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 750
  standard: "ATX 3.1"
  certification: "80 Plus Platinum"
  cabling: "полностью модульные"
  fan: "135mm be quiet! Silent Wings 4 (FDB, 6-полюсный мотор)"
  acoustic_profile: "semi_passive"  # funnel-shaped vent + Silent Wings 4 FDB = эталон тишины
  protections: ["OCP", "OVP", "UVP", "OPP", "OTP", "SCP"]
  12v_2x6: true
  12v_2x6_power: "600W (native)"
  12v_2x6_count: 1
  pcie_8pin_count: 4
  topology: "LLC + SR + DC-DC"
  capacitors: "японские (Nippon Chemi-Con, 105°C)"
  warranty: "10 лет"
price_ru:
  median: 16000
  source: "price.ru (оценка, параллельный импорт)"
  date: "2026-06-05"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "750W Platinum — премиум-эталон тишины. Silent Wings 4 FDB-вентилятор с 6-полюсным мотором (нулевой шум коммутации). Воронкообразная решётка снижает турбулентность. Японские конденсаторы, ATX 3.1, 10 лет гарантии. Самый тихий semi-passive PSU в категории 750W."
    capability_level: 2
    failure_mode_desc: "Цена ~16 000 ₽ — вдвое дороже Pure Power 12M за те же 750W. Platinum КПД даёт экономию ~15W тепла относительно Gold — заметно только при 24/7. Избыточен для не-премиум сборок."
    optimal_for_intents: ["aaa_4k_ultra", "workstation_rendering", "software_development", "streaming"]
    failure_for_intents: ["office_productivity", "esports_1080p_240hz"]
    failure_severity: "OVERSPEND"
    failure_type: "OVERSPEND"
verdict: "Самый тихий PSU в категории 750W. Silent Wings 4 FDB + funnel vent + Platinum КПД = практически неслышим даже под нагрузкой. Для премиум-сборок, где важна абсолютная тишина. Цена ~16 000 ₽ — вдвое дороже Pure Power 12M, оправдано только для no-compromise silent builds."
---

# be quiet! Straight Power 12 750W 80+ Platinum

## Позиционирование

be quiet! Straight Power 12 — предфлагманская линейка между Pure Power 12M (mid-range Gold) и Dark Power 13 (flagship Titanium). Ключевые отличия от Pure Power 12M:

| Параметр | Pure Power 12M | Straight Power 12 |
|---|---|---|
| **Сертификат** | 80+ Gold | 80+ Platinum |
| **Вентилятор** | 120mm rifle bearing | 135mm FDB (Silent Wings 4) |
| **Мотор вентилятора** | 4-полюсный | 6-полюсный (бесшумная коммутация) |
| **Решётка** | Стандартная wire grill | Воронкообразная (funnel-shaped) |
| **Конденсаторы** | Смешанные | Японские Nippon Chemi-Con |
| **Топология** | LLC + DC-DC | LLC + SR + DC-DC (оптимиз.) |
| **Гарантия** | 10 лет | 10 лет |
| **Цена** | ~10 000 ₽ | ~16 000 ₽ |

Для кого эти +6 000 ₽: для сборок, где **абсолютная тишина — requirement, а не nice-to-have**. Звукозапись, стриминг с открытым микрофоном, ПК в спальне.

## Характеристики

- **Мощность:** 750W
- **Стандарт:** ATX 3.1
- **Сертификат:** 80 Plus Platinum (КПД ≥ 92% при 50% нагрузке)
- **Кабели:** полностью модульные (премиум-оплётка)
- **12V-2x6:** 1× 600W native
- **PCIe 8-pin:** 4×
- **Вентилятор:** 135mm be quiet! Silent Wings 4 FDB, 6-полюсный мотор
- **Решётка:** воронкообразная (funnel-shaped vent — снижает турбулентность)
- **Режим вентилятора:** semi-passive, fan stop до ~200W
- **Защиты:** OCP, OVP, UVP, OPP, OTP, SCP
- **Топология:** LLC + SR (Synchronous Rectification) + DC-DC
- **Конденсаторы:** японские (Nippon Chemi-Con, 105°C)
- **Гарантия:** 10 лет

## Инженерные решения для тишины

### Silent Wings 4 с 6-полюсным мотором

Обычные вентиляторы используют 4-полюсный мотор. При каждом переключении полюса возникает слышимый «click» — шум коммутации. 6-полюсный мотор переключается чаще, но с меньшей амплитудой — click тоньше и тише. На практике: Straight Power 12 на 600 RPM звучит как **отсутствие звука** — ниже порога восприятия в тихой комнате.

### Funnel-shaped vent

Стандартная проволочная решётка создаёт турбулентность на кромках — дополнительный шум. Воронкообразная решётка Straight Power 12 направляет поток ламинарно, убирая турбулентный шум. В комбинации с FDB-подшипником — самое тихое решение на рынке 750W PSU.

### Platinum КПД = меньше тепла

Platinum (≥ 92%) vs Gold (≥ 90%) при 750W означает:
- При 375W нагрузке: Platinum теряет ~30W тепла, Gold ~38W
- Разница 8W тепла = на 3–5°C холоднее внутри PSU
- Вентилятор раскручивается позже и медленнее

## Совместимость с GPU

- **RTX 5070 (250W):** более чем достаточно, semi-passive до 200W
- **RTX 5070 Ti (300W):** уверенно, вентилятор на минимальных оборотах
- **RTX 5080 (360W):** на пределе по ваттажу, но допустимо на стоке
- **RTX 5090 (575W):** недостаточно (нужен Straight Power 12 1000W+)

## Российский рынок (июнь 2026)

**Медиана ~16 000 ₽** (параллельный импорт). Прямые конкуренты:

- be quiet! Pure Power 12M 750W (~10 000 ₽) — тот же вендор, Gold вместо Platinum, вдвое дешевле
- Seasonic Focus GX-750 (~12 000 ₽) — Gold, но с японскими конденсаторами и FDB
- Corsair RM750x (~13 000 ₽) — Gold, японские конденсаторы, магнитная левитация
- FSP Hydro Ti Pro 750W (~18 000 ₽) — Titanium, самая высокая эффективность

Straight Power 12 занимает нишу «Platinum-тишина по цене Gold-конкурентов». Дешевле FSP Hydro Ti Pro, тише Corsair RM750x, эффективнее Seasonic GX.

## Для кого

**Идеален:**
- No-compromise silent builds (звукозапись, стриминг, спальня)
- Премиум рабочие станции (видеомонтаж, 3D-рендеринг)
- Сборки с открытым корпусом / без звукоизоляции

**Не подходит:**
- Бюджетные и среднебюджетные сборки (брать Pure Power 12M — вдвое дешевле)
- Сборки с RTX 5080+ (нужен 850W+)
- Если тишина — не requirement, а nice-to-have (Gold достаточно)

## Источники

1. be quiet! Straight Power 12 Product Page (bequiet.com)
2. Cybenetics — сертификация 80 Plus Platinum и Lambda A++ (шум)
3. Silent Wings 4 White Paper — 6-полюсный мотор, FDB, funnel vent
4. Price.ru — рыночные цены, Москва (оценка, 05.06.2026)
5. Hardware Busters / KitGuru — обзоры Straight Power 12 750W
