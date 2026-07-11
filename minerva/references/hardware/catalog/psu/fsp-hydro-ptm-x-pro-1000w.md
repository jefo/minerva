---
id: "fsp-hydro-ptm-x-pro-1000w"
type: "psu"
title: "FSP Hydro PTM X Pro 1000W"
vendor: "fsp"
status: "draft"
tags: ["atx3.1", "1000w", "platinum", "fully-modular", "12v-2x6", "japanese-caps"]
last_updated: "2026-06-03"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 1000
  standard: "ATX 3.1"
  certification: "80 Plus Platinum"
  cabling: "полностью модульные"
  fan: "135mm FDB"
  acoustic_profile: "semi_passive"  # Platinum, premium — fan stop до ~300W
  protections: ["OPP", "OVP", "UVP", "SCP", "OTP", "OCP"]
  12v_2x6: true
  12v_2x6_power: "600W (native)"
  capacitors: "японские (Nippon Chemi-Con)"
price_ru:
  median: 20000
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "1000W Platinum с японскими конденсаторами. Золотой стандарт для RTX 5090. 12V-2x6 на 600W — полностью раскрывает флагманскую карту. FDB-вентилятор, полностью модульная конструкция, высочайший КПД."
    capability_level: 2
    failure_mode_desc: "Избыточен для систем без флагманского GPU. Цена ~20 000 ₽ — переплата, если не используется 600W по 12V-2x6."
    optimal_for_intents: ["aaa_4k_path_tracing", "llm_training_lora", "aaa_4k_ultra", "llm_inference", "workstation_rendering"]
    failure_for_intents: ["office_productivity", "esports_1080p_240hz"]
    failure_severity: "WARN"
    failure_type: "OVERSPEND"
verdict: "Флагманский 1000W Platinum ATX 3.1 на японских конденсаторах. Полностью модульный, 12V-2x6 600W. Идеален для RTX 5090 в стоке и с разгоном. Цена ~20 000 ₽ — оправдана для топовых сборок."
---

# FSP Hydro PTM X Pro 1000W

## Позиционирование

FSP Hydro PTM X Pro 1000W — флагманский блок питания для самых требовательных систем. 80 Plus Platinum, ATX 3.1, полностью модульная конструкция, японские конденсаторы. Создан для сборок с RTX 5090, в том числе с заводским разгоном.

FSP (Fortron Source Power) — тайваньский ODM-производитель, поставляющий платформы для многих brand-name PSU (be quiet!, Cooler Master, EVGA). Hydro PTM X Pro — собственная топовая линейка FSP.

## Характеристики

- **Мощность:** 1000W
- **Стандарт:** ATX 3.1
- **Сертификат:** 80 Plus Platinum
- **Кабели:** полностью модульные
- **12V-2x6:** есть (родной разъём, 600W)
- **Вентилятор:** 135mm FDB (Fluid Dynamic Bearing)
- **Конденсаторы:** японские (Nippon Chemi-Con)
- **Защиты:** OPP, OVP, UVP, SCP, OTP, OCP
- **PFC:** Активный
- **Топология:** DC-DC

## Почему Platinum и японские конденсаторы

**80 Plus Platinum** означает КПД ≥ 92% при 50% нагрузке (против ≥ 90% у Gold). Разница в 2–3% кажется небольшой, но при 1000W это:
- Меньше тепловыделения (10–20W разницы)
- Тише работа (вентилятор реже раскручивается)
- Меньше счёт за электричество при круглосуточной работе

**Японские конденсаторы (Nippon Chemi-Con)** — индустриальный стандарт надёжности. Рассчитаны на 105°C, минимальная деградация со временем. Критично для систем с аптаймом 24/7 (рабочие станции, серверы, фермы инференса).

## 12V-2x6 600W — полная мощность для RTX 5090

Родной 12V-2x6 на 600W полностью раскрывает возможности RTX 5090:
- **Сток (575W TGP):** с запасом
- **Заводской разгон (600W+):** на пределе, но в рамках спецификации
- **Transient spike:** ATX 3.1 требует выдерживать пики до 200% номинала в течение 100 мкс — Hydro PTM X Pro справляется

Для справки: у 850W блоков 12V-2x6 часто ограничен 450W — этого достаточно для RTX 5080 (360W), но для 5090 нужны полные 600W.

## Совместимость с GPU

- **RTX 5080 (360W):** с огромным запасом, переплата за мощность
- **RTX 5090 сток (575W):** уверенно
- **RTX 5090 OC (600W+):** в пределах спецификации
- **Multi-GPU (теоретически):** не рассчитан (нужны блоки с несколькими 12V-2x6)

## Российский рынок (июнь 2026)

**Медиана ~20 000 ₽.** Прямые конкуренты в сегменте 1000W Platinum ATX 3.x:
- be quiet! Dark Power 13 1000W (~25 000 ₽, Titanium)
- Corsair HX1000i (~23 000 ₽, Platinum, ATX 3.0)
- Thermaltake Toughpower GF3 1000W (~16 000 ₽, Gold, не Platinum)

FSP Hydro PTM X Pro занимает нишу «Platinum дешевле Corsair/be quiet!». Лучший баланс цены и качества в 1000W Platinum.

## Для кого

**Идеален:**
- Сборки с RTX 5090 (сток и разгон)
- Рабочие станции 24/7 (рендеринг, инференс)
- Энтузиасты, требующие максимального запаса и КПД
- Тихие сборки (FDB-вентилятор + Platinum = минимальный шум)

**Не подходит:**
- Бюджетные и среднебюджетные сборки (избыточен)
- Офисные ПК (переплата ~14 000 ₽ относительно того же PF650)
- Сборки без дискретного GPU

## Сравнение с другими PSU в каталоге

| Модель | Мощность | Сертификат | 12V-2x6 | Цена |
|---|---|---|---|---|
| Deepcool PF650 | 650W | Bronze | Нет | ~6 000 ₽ |
| Deepcool PN750D | 750W | Gold | 450W | ~7 000 ₽ |
| Deepcool PN850D | 850W | Gold | 450W | ~12 000 ₽ |
| **FSP Hydro PTM X Pro** | **1000W** | **Platinum** | **600W** | **~20 000 ₽** |

## Источники

1. FSP Hydro PTM X Pro Product Page (fsplifestyle.com)
2. Price.ru — рыночные цены (оценка, 03.06.2026)
3. Cybenetics — сертификация 80 Plus Platinum
4. Nippon Chemi-Con — спецификации конденсаторов серии KXJ
