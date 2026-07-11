---
id: "deepcool-pf650"
type: "psu"
title: "Deepcool PF650 650W"
vendor: "deepcool"
status: "draft"
tags: ["atx2.4", "650w", "bronze", "non-modular", "budget"]
last_updated: "2026-06-03"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 650
  standard: "ATX 2.4"
  certification: "80 Plus Bronze"
  cabling: "фиксированные (non-modular)"
  fan: "120mm"
  acoustic_profile: "active_standard"  # бюджетный вентилятор, всегда audible
  protections: ["OPP", "OVP", "UVP", "SCP"]
  12v_rail_w: 588
  12v_2x6: false
price_ru:
  median: 6000
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  atx_2x_budget_reliable:
    steel_man_desc: "Блок питания ATX 2.4, проверенный временем. Достаточен для систем без мощных GPU (TGP < 200W). Лучшая цена/ватт."
    capability_level: 1
    failure_mode_desc: "Не рассчитан на пиковые нагрузки современных GPU. Transient spike > 150% TGP может триггерить OCP — аварийное выключение."
    optimal_for_intents: ["aaa_1080p_ultra", "aaa_1440p_high", "esports_1080p_240hz", "office_productivity", "software_development"]
    failure_for_intents: ["aaa_4k_path_tracing", "llm_training_lora"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
verdict: "Бюджетный 650W Bronze на проверенной платформе ATX 2.4. Достаточен для офисных и игровых сборок без мощных GPU. Не модульный. Цена ~6 000 ₽ — лучший выбор в категории «цена/ватт»."
---

# Deepcool PF650 650W

## Позиционирование

Deepcool PF650 — бюджетный блок питания на проверенной временем платформе ATX 2.4. Сертификат 80 Plus Bronze, фиксированные кабели, 120mm вентилятор. Предназначен для систем, где не требуется поддержка пиковых нагрузок современных GPU с ATX 3.x.

650W с отдачей 588W по линии 12V — достаточно для большинства среднебюджетных сборок.

## Характеристики

- **Мощность:** 650W
- **Стандарт:** ATX 2.4
- **Сертификат:** 80 Plus Bronze
- **Кабели:** фиксированные (non-modular)
- **Вентилятор:** 120mm
- **Защиты:** OPP, OVP, UVP, SCP
- **12V-линия:** 588W
- **12V-2x6:** нет
- **PFC:** Активный

## Ограничения ATX 2.4

ATX 2.4 не рассчитан на transient spike (кратковременные пиковые броски потребления) современных GPU. У RTX 30xx/40xx/50xx пиковые всплески могут в 2–2.5 раза превышать номинальный TGP. При превышении порога срабатывает OCP/OPP — ПК аварийно выключается.

**Практический потолок по GPU:** видеокарты с TGP до 180–200W (RTX 5060, RTX 4060 Ti, RX 7600 XT). Для RTX 5070 и выше — брать ATX 3.x.

## Совместимость с GPU

- **RTX 5060 (150W):** с запасом
- **RTX 5060 Ti (180W):** достаточно
- **RTX 5070 (250W):** рискованно (transient spike могут триггерить защиту)
- **RTX 5080 и выше:** не совместим

## Немодульная конструкция

Все кабели жёстко закреплены. В компактных корпусах избыток кабелей может быть проблемой. Для mATX/Mini-ITX с ограниченным местом под кабель-менеджмент лучше рассмотреть модульные аналоги.

## Российский рынок (июнь 2026)

**Медиана ~6 000 ₽.** Прямые конкуренты в бюджете 5 000–7 000 ₽ (650W):
- Deepcool PK650D (~6 500 ₽, Bronze, снят с продажи)
- Cooler Master MWE 650 Bronze (~6 500 ₽)
- be quiet! System Power 10 650W (~7 000 ₽, Bronze)

PF650 выигрывает по цене, проигрывая в отсутствии модульности и ATX 3.x.

## Для кого

**Идеален:**
- Офисные и домашние ПК
- Бюджетные игровые сборки (до RTX 5060 Ti)
- Сборки без дискретного GPU (встроенная графика)

**Не подходит:**
- Игры в 4K / с path tracing
- Сборки с RTX 5070 и выше
- Компактные корпуса (немодульный)

## Источники

1. Deepcool PF650 Product Page (deepcool.com)
2. Price.ru — рыночные цены (оценка, 03.06.2026)
3. Cybenetics — сертификация 80 Plus Bronze
