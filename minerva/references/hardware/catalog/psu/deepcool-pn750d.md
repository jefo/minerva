---
id: "deepcool-pn750d"
type: "psu"
title: "Deepcool PN750D 750W 80+ Gold"
vendor: "deepcool"
status: "verified"
tags: ["atx", "750w", "gold", "atx3", "budget"]
last_updated: "2026-06-03"
links:
  concept_power: "concepts/power-budget.md"
  replaced_model: null
  gpu_compatible: "catalog/gpu/nvidia-rtx-5060-ti.md"
specs:
  wattage: "750W"
  certification: "80+ Gold"
  form_factor: "ATX"
  modular: false
  atx_version: "ATX 3.1"
  pcie_5_connector: "12V-2×6 (1 шт.)"
  pcie_8pin: "4× 8-pin (2 кабеля)"
  fan_size: "120 мм"
  fan_bearing: "Hydro Bearing"
  acoustic_profile: "active_low_noise"  # Hydro Bearing, без fan-stop, всегда вращается. Тихий (~22 dBA) но не 0 RPM
  pfc: "Активный"
  topology: "DC-DC"
  protections: "OVP, UVP, OPP, OTP, SCP"
  warranty: "5 лет"
  weight: "2.5 кг"
price_ru:
  min: 6620
  median: 6950
  max: 7282
  source: "price.ru"
  date: "2026-06-03"
verdict: "Прямой наследник PK750D. 750W Gold за 7 000 ₽ — отличный бюджетный БП для сборок с RTX 5070 и ниже. ATX 3.1 с 12V-2×6. Не модульный. Рейтинг 4.8."

profiles:
  atx_3x_transient_capable:
    capability_level: 2
    steel_man_desc: "750W Gold с ATX 3.1 и родным 12V-2x6. Достаточен для RTX 5070 Ti / RX 9070 XT. DC-DC топология, полный набор защит. 5 лет гарантии."
    failure_mode_desc: "Немодульный — все кабели жёстко выведены, избыточные кабели занимают место. Для RTX 5080 — на пределе по ваттажу при sustained load. Нет 80+ Platinum эффективности."
    optimal_for_intents: ["aaa_1440p_high", "esports_1080p_240hz", "software_development", "streaming"]
    failure_for_intents: ["aaa_4k_path_tracing_5090_oc", "llm_training_lora_24h"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# Deepcool PN750D 750W 80+ Gold

## Позиционирование

Deepcool PN750D — наследник популярного PK750D (снят с продажи). Переход с Bronze на **Gold** при той же цене. Главное обновление — поддержка ATX 3.1 и разъём 12V-2×6 (исправленная версия 12VHPWR без проблемы оплавления).

**Рейтинг на Price.ru: 4.8★** — рынок принял хорошо.

## Характеристики

| Параметр | PK750D (снят) | PN750D |
|---|---|---|
| Сертификат | 80+ Bronze | 80+ Gold |
| ATX-версия | ATX 2.x | ATX 3.1 |
| 12VHPWR | Нет | 12V-2×6 |
| Модульность | Нет | Нет |
| Вентилятор | 120 мм | 120 мм (Hydro Bearing) |
| Вес | 1.2 кг | 2.5 кг |
| Гарантия | 3 года | 5 лет |
| Цена | ~7 300 ₽ | ~7 000 ₽ |

Утяжеление с 1.2 до 2.5 кг — косвенный признак более качественной элементной базы (радиаторы, дроссели, конденсаторы).

## Совместимость с GPU

- **RTX 5060 Ti (180W):** с запасом, 1× 8-pin
- **RTX 5070 (250W):** достаточно, 12V-2×6
- **RTX 5080 (360W):** на пределе, но возможно (12V-2×6, 600W макс.)
- **RTX 5090 (575W):** недостаточно

Для сборок до RTX 5070 Ti включительно — отличный выбор. Для RTX 5080 и выше — 850W минимум.

## Немодульная конструкция

**PN750D — не модульный.** Все кабели жёстко закреплены. В компактных корпусах (mATX, Mini-ITX) избыток кабелей может быть проблемой. Если нужна модульность — смотреть Deepcool PN750M (модульная версия, +1 500–2 000 ₽).

## Российский рынок (июнь 2026)

**Диапазон: 6 620–7 282 ₽, медиана ~6 950 ₽.**

Прямые конкуренты в бюджете 6 000–8 000 ₽ (750W):
- Cooler Master MWE 750 Gold (~7 500 ₽, модульный)
- be quiet! System Power 10 750W (~8 000 ₽, Bronze)
- Deepcool PL750D (~6 200 ₽, Bronze — младшая модель)

PN750D выигрывает у конкурентов по соотношению Gold/цена. Главный компромисс — отсутствие модульности.

## Для кого

**Идеален:**
- Бюджетные и среднебюджетные сборки (до RTX 5070 Ti)
- Замена снятому PK750D
- Корпуса ATX с местом для кабель-менеджмента

**Не подходит:**
- Компактные корпуса (немодульный — много лишних кабелей)
- Сборки с RTX 5080/5090
- Кастомные кабели (только перепайка)

## Источники

1. Deepcool PN750D Product Page (deepcool.com)
2. Price.ru — рыночные цены и рейтинг, Москва (03.06.2026)
3. Cybenetics — сертификация 80+ Gold
