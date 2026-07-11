---
id: "gskill-ripjaws-s5-ddr5-6000-32gb"
type: "memory"
title: "G.Skill Ripjaws S5 32GB DDR5-6000 CL30"
vendor: "gskill"
status: "verified"
tags: ["ddr5", "6000mhz", "cl30", "32gb", "dual-channel", "dual-rank", "expo", "xmp"]
last_updated: "2026-06-03"
links:
  memory_type: "catalog/memory/ddr5.md"
  platform_am5: "catalog/motherboard/am5/index.md"
  platform_lga1700: "catalog/motherboard/lga1700/index.md"
  cpu_recommended: "catalog/cpu/amd-ryzen-5-7500f.md"
  concept_timings: "concepts/memory-timings.md"
specs:
  capacity: "32 GB (2×16 GB)"
  speed: "DDR5-6000 MT/s"
  timings: "CL30-36-36-96"
  voltage: "1.35V"
  ranks: "Dual Rank (2× single-rank модуля)"
  profiles: "AMD EXPO + Intel XMP 3.0"
  form_factor: "288-pin DIMM"
  color: "Чёрный (матовый радиатор)"
  height: "33 мм (low-profile)"
  chips: "SK Hynix A-die"
price_ru:
  min: 44331
  median: 47000
  max: 50035
  source: "price.ru"
  date: "2026-06-03"
verdict: "Лучший выбор для AM5: DDR5-6000 CL30 попадает точно в sweet spot Zen 4/5 (MCLK:UCLK 1:1). SK Hynix A-die — разгонный потенциал до 8000+. Рыночная цена 45–50k — дорого, но стандарт качества."

profiles:
  standard_ddr5_xmp:
    capability_level: 2
    capability_level: 2
    steel_man_desc: "DDR5-6000 CL30 на Hynix A-die — золотой стандарт AM5. Синхронный режим UCLK=MCLK (1:1) без penalty по латентности. Low-profile 33 мм — совместимость с любым воздушным кулером."
    failure_mode_desc: "Цена на 20–25% выше бюджетных DDR5-5600. JEDEC-фоллбэк 4800 CL40 при сбросе BIOS — система загрузится, но FPS просядет до восстановления EXPO."
    optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "esports_1080p_240hz", "software_development"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# G.Skill Ripjaws S5 32GB DDR5-6000 CL30

## Позиционирование

Ripjaws S5 — линейка DDR5 от G.Skill без RGB-подсветки, ориентированная на производительность. Модель `F5-6000J3036F16GX2-RS5K` (CL30) — верхняя планка линейки по таймингам. SK Hynix A-die под радиаторами.

## Характеристики

| Параметр | Значение |
|---|---|
| Комплект | 2×16 GB (32 GB total) |
| Частота | DDR5-6000 MT/s |
| Тайминги | CL30-36-36-96 |
| Напряжение | 1.35V |
| Чипы | SK Hynix A-die |
| Ранги | 1R (каждый модуль — single rank) |
| Профили | AMD EXPO + Intel XMP 3.0 |
| Высота | 33 мм (low-profile) |

**33 мм высоты** — критически важно. Проходит под любой башенный кулер без смещения вентилятора (в отличие от многих RGB-комплектов с высотой 42+ мм).

## Почему DDR5-6000 CL30

Для AMD AM5:
- **DDR5-6000 = sweet spot** — контроллер памяти работает в синхронном режиме MCLK:UCLK = 1:1
- Выше 6000 → переход в 1:2 → +10–15 нс latency
- CL30 — один из лучших таймингов для 6000 MT/s

Для Intel LGA1700:
- Контроллер всегда в Gear 2 для DDR5, поэтому 6000 — нижняя планка
- Можно разогнать до 7200+ на Z790

## SK Hynix A-die

A-die — лучшие чипы DDR5 для разгона на рынке. В Ripjaws S5 они работают на консервативных CL30-36-36 (1.35V), но способны на:

- DDR5-6400 CL30 (1.40V) — на AM5 с 1:1
- DDR5-8000+ (1.45V+) — на Intel Z790 с Gear 4

Для пользователей, которые не планируют ручной разгон, XMP/EXPO-профиль CL30 даёт отличную производительность «из коробки».

## Российский рынок (июнь 2026)

**Диапазон: 44 331–50 035 ₽, медиана ~47 000 ₽.**

Конкуренты (DDR5-6000 32GB):
- Kingston FURY Beast CL30 (~42 000–47 000 ₽, Samsung/Hynix, лотерея чипов)
- ADATA XPG Lancer CL30 (~40 000–44 000 ₽, Hynix A-die)
- Patriot Viper Venom CL30 (~38 000–43 000 ₽, Hynix M-die)

Ripjaws S5 дороже конкурентов на 5–10%, но гарантированно A-die и лучшая совместимость с AM5 (G.Skill тесно работает с AMD над валидацией EXPO-профилей).

**Рост цен:** в апреле 2026 комплект стоил ~38 000 ₽ (смета EST-2026-0422-K1). К июню 2026 — 44 000–50 000 ₽. Рост ~24% за два месяца. Возможные причины: дефицит A-die, курс валют, сезонный спрос.

## Совместимость

**AMD AM5:** лучший выбор. EXPO-профиль загружается одной кнопкой в BIOS. Проверен на платах:
- MSI MAG B650 Tomahawk
- GIGABYTE B650M S2H
- ASUS TUF B650-Plus

**Intel LGA1700:** XMP 3.0 работает. На Z790 можно разогнать выше 6000.

## Для кого

**Идеален:**
- Игровые сборки AM5 (Ryzen 5 7500F / 7600 / 7700X / 7800X3D)
- Сборки где важна совместимость «воткнул и забыл»
- Корпуса с ограниченным клиренсом кулера (33 мм высота)

**Избыточен:**
- Офисные ПК (DDR5-5600 CL36 достаточно)
- Бюджетные сборки где каждая 1 000 ₽ на счету (брать ADATA/Patriot)
- Сборки без дискретной GPU (iGPU не нагружает память)

## Источники

1. G.Skill Ripjaws S5 Product Page (gskill.com)
2. Price.ru — рыночные цены, Москва (03.06.2026)
3. Собственное тестирование лаборатории в сборке EST-2026-0422-K1
4. Buildzoid / Actually Hardcore Overclocking — анализ A-die
