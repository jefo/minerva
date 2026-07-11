---
id: "seasonic-focus-gx-750"
type: "psu"
title: "Seasonic Focus GX-750 750W 80+ Gold"
vendor: "seasonic"
status: "draft"
tags: ["atx3.0", "750w", "gold", "fully-modular", "semi-passive", "japanese-caps"]
last_updated: "2026-06-05"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 750
  standard: "ATX 3.0 / PCIe 5.0"
  certification: "80 Plus Gold"
  cabling: "полностью модульные"
  fan: "135mm Fluid Dynamic Bearing (FDB)"
  acoustic_profile: "semi_passive"  # Hybrid Silent Mode: fan stop до ~30% нагрузки (~225W)
  protections: ["OCP", "OVP", "UVP", "OPP", "OTP", "SCP"]
  12v_2x6: true
  12v_2x6_power: "600W (native кабель)"
  12v_2x6_count: 1
  pcie_8pin_count: 5
  topology: "LLC + DC-DC"
  capacitors: "японские (Nippon Chemi-Con, 105°C)"
  warranty: "10 лет"
  mtbf: "100 000 часов"
price_ru:
  median: 12000
  source: "price.ru (оценка, параллельный импорт)"
  date: "2026-06-05"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "750W Gold — эталон надёжности и тишины. Японские конденсаторы (Nippon Chemi-Con), 135mm FDB-вентилятор, Hybrid Silent Mode с fan-stop. 10 лет гарантии. Собственная платформа Seasonic, не ODM-перебренд. MTBF 100 000 часов."
    capability_level: 2
    failure_mode_desc: "Дороже Pure Power 12M на 2 000 ₽ при схожих характеристиках. ATX 3.0 (не 3.1) — меньший запас по hold-up time. Для сборок без 24/7 нагрузки разница в конденсаторах не окупается."
    optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "software_development", "streaming", "workstation_rendering"]
    failure_for_intents: ["aaa_4k_path_tracing_5090_oc", "llm_training_lora_24h"]
    failure_severity: "WARN"
    failure_type: "OVERSPEND"
verdict: "Эталонный semi-passive PSU для требовательных сборок. Японские конденсаторы, FDB-вентилятор, 10 лет гарантии, собственная платформа Seasonic. Дороже Pure Power 12M на 2 000 ₽. Брать когда надёжность и долговечность важнее экономии. ~12 000 ₽."
---

# Seasonic Focus GX-750 750W 80+ Gold

## Позиционирование

Seasonic Focus GX-750 — премиальный представитель semi-passive Gold PSU. В отличие от конкурентов, Seasonic является **ODM-производителем** собственных платформ (не заказывает у сторонних фабрик). Это даёт полный контроль над качеством — от конденсаторов до топологии.

Главные козыри: **японские конденсаторы Nippon Chemi-Con** (стандарт de facto для надёжности), **135mm FDB-вентилятор** (тише и долговечнее rifle bearing), **10 лет гарантии**, MTBF 100 000 часов. Для рабочих станций с аптаймом 12–16 часов в сутки — лучший выбор в категории 750W Gold.

## Характеристики

- **Мощность:** 750W
- **Стандарт:** ATX 3.0 (PCIe 5.0)
- **Сертификат:** 80 Plus Gold
- **Кабели:** полностью модульные
- **12V-2x6:** 1× 600W (native кабель в комплекте)
- **PCIe 8-pin:** 5× (3 кабеля)
- **Вентилятор:** 135mm Fluid Dynamic Bearing (FDB)
- **Режим вентилятора:** Hybrid Silent Mode — 0 RPM до ~30% нагрузки (~225W)
- **Защиты:** OCP, OVP, UVP, OPP, OTP, SCP
- **Топология:** LLC + DC-DC
- **Конденсаторы:** японские Nippon Chemi-Con 105°C
- **Гарантия:** 10 лет
- **MTBF:** 100 000 часов (> 11 лет непрерывной работы)

## Почему Seasonic — «эталон»

**Японские конденсаторы (Nippon Chemi-Con)** — золотой стандарт индустрии. При 105°C и круглосуточной нагрузке деградация ёмкости на порядок медленнее, чем у тайваньских/китайских аналогов. Для рабочих станций с аптаймом 12+ часов в сутки это разница между «PSU жив 10 лет» и «конденсаторы высохли на 5-й год».

**135mm FDB (Fluid Dynamic Bearing)** — принципиально тише и долговечнее rifle bearing (используется в Pure Power 12M и RM750e). При одинаковых оборотах FDB производит на 3–5 dBA меньше шума. На практике: Seasonic на 800 RPM звучит как конкурент на 600 RPM.

**Собственная платформа** — Seasonic не заказывает платформы у CWT/FSP/Great Wall. Это означает: нестандартные решения (например, 5× PCIe 8-pin вместо типичных 4), оптимизированная топология, прямой контроль качества.

## Hybrid Silent Mode

Вентилятор выключен до ~30% нагрузки (~225W). В typical desktop (60–100W) и лёгкой работе — абсолютная тишина. При игровой нагрузке включается плавно, без рывка. 135mm диаметр означает: на тех же оборотах CFM выше, охлаждение эффективнее.

## Совместимость с GPU

- **RTX 5060 Ti (180W):** с огромным запасом, вентилятор даже не включится
- **RTX 5070 (250W):** порог fan-stop, вентилятор на грани включения
- **RTX 5070 Ti (300W):** уверенно, вентилятор на низких оборотах
- **RTX 5080 (360W):** на пределе по ваттажу, но 12V-2x6 600W — хватает
- **RTX 5090 (575W):** недостаточно

## Российский рынок (июнь 2026)

**Медиана ~12 000 ₽** (параллельный импорт). Прямые конкуренты:

- be quiet! Pure Power 12M 750W (~10 000 ₽ — дешевле, ATX 3.1, rifle bearing)
- Corsair RM750e (~9 500 ₽ — дешевле, неяпонские конденсаторы)
- be quiet! Straight Power 12 750W (~16 000 ₽ — дороже, Platinum, премиум)

Focus GX-750 на 2 000 ₽ дороже Pure Power 12M. За эти деньги: японские конденсаторы, FDB вместо rifle bearing, 5× PCIe 8-pin (а не 4), репутация Seasonic. Для сборок с аптаймом 8+ часов в день — оправдано. Для вечернего гейминга — избыточно.

## Для кого

**Идеален:**
- Рабочие станции с аптаймом 8–16 часов в сутки
- Требовательные к надёжности сборки (японские конденсаторы)
- Тихие high-end ПК (FDB + 135mm + Hybrid Silent)
- Системы, где отказ PSU = простой бизнеса

**Не подходит:**
- Бюджетные сборки (переплата 2 000–5 500 ₽ относительно PN750D/PF650)
- Сборки с RTX 5080+ (брать 850W+ версию или FSP Hydro PTM)
- Если не планируется 24/7 нагрузка (конденсаторы не окупятся)

## Источники

1. Seasonic Focus GX-750 Product Page (seasonic.com)
2. Cybenetics — сертификация 80 Plus Gold и Lambda A+ (шум)
3. Nippon Chemi-Con — спецификации конденсаторов KXJ series
4. Price.ru — рыночные цены, Москва (оценка, 05.06.2026)
5. Tom's Hardware / Hardware Busters — обзоры Focus GX-750
