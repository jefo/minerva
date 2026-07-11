---
id: "deepcool-pn850d"
type: "psu"
title: "Deepcool PN850D 850W 80+ Gold"
vendor: "deepcool"
status: "draft"
tags: ["atx3.1", "850w", "gold", "modular", "12v-2x6"]
last_updated: "2026-06-03"
links:
  concept_power: "../concepts/power-budget.md"
  predecessor: "deepcool-pn750d.md"
specs:
  wattage: 850
  standard: "ATX 3.1"
  certification: "80 Plus Gold"
  cabling: "модульные"
  fan: "135mm FDB"
  acoustic_profile: "active_low_noise"  # FDB подшипник, тихий (~20 dBA), но без fan-stop — всегда вращается
  protections: ["OPP", "OVP", "UVP", "SCP", "OTP"]
  12v_2x6: true
  12v_2x6_power: "450W (native)"
price_ru:
  median: 12000
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "850W Gold с ATX 3.1 и родным 12V-2x6. Уверенно держит transient spike RTX 5080/5090. Модульные кабели — чистая сборка в любом корпусе."
    capability_level: 2
    failure_mode_desc: "Для RTX 5090 с разгоном — на пределе. При sustained load > 800W в жарком корпусе может уходить в перегрев."
    optimal_for_intents: ["aaa_1440p_high", "aaa_4k_ultra", "esports_1080p_240hz", "software_development", "llm_inference"]
    failure_for_intents: ["llm_training_lora_24h", "aaa_4k_path_tracing_5090_oc"]
    failure_severity: "WARN"
    failure_type: "GRACEFUL"
verdict: "Универсальный 850W Gold ATX 3.1 с родным 12V-2x6. Модульные кабели, 135mm FDB-вентилятор. Закрывает 95% игровых и рабочих сценариев, включая RTX 5080. Цена ~12 000 ₽."
---

# Deepcool PN850D 850W 80+ Gold

## Позиционирование

Deepcool PN850D — старший брат PN750D в линейке. Те же преимущества (ATX 3.1, 12V-2x6, 80+ Gold), но **850W** и **модульные кабели**. Это ключевое отличие: PN750D немодульный, PN850D — модульный.

Предназначен для high-end сборок с RTX 5080 и ниже. Для RTX 5090 — на пределе, но возможно в стоке (без разгона).

## Характеристики

- **Мощность:** 850W
- **Стандарт:** ATX 3.1
- **Сертификат:** 80 Plus Gold
- **Кабели:** модульные
- **12V-2x6:** есть (родной разъём, 450W native)
- **Вентилятор:** 135mm FDB (Fluid Dynamic Bearing)
- **Защиты:** OPP, OVP, UVP, SCP, OTP
- **PFC:** Активный
- **Топология:** DC-DC

## 12V-2x6 — родной разъём для RTX 50xx

12V-2x6 — исправленная версия 12VHPWR. Укороченные sense-пины гарантируют, что разъём не подаст питание, если вставлен не до конца. Проблема оплавления, характерная для ранних 12VHPWR, **полностью решена**.

Родной разъём на блоке питания означает: **не нужен переходник** 3× 8-pin → 12V-2x6. Меньше точек отказа, чище кабель-менеджмент.

## Совместимость с GPU

- **RTX 5060 Ti (180W):** с огромным запасом
- **RTX 5070 (250W):** более чем достаточно
- **RTX 5080 (360W):** уверенно, с учётом transient spike
- **RTX 5090 (575W):** на пределе в стоке, нежелательно с разгоном

Для RTX 5090 с заводским разгоном (600W+) — 1000W минимум.

## Модульная конструкция

В отличие от PN750D, **PN850D полностью модульный**. Подключаете только нужные кабели. Чистый кабель-менеджмент даже в компактных корпусах. Совместим с кастомными кабелями (с оговорками — проверять pinout).

## Российский рынок (июнь 2026)

**Медиана ~12 000 ₽.** Прямые конкуренты в сегменте 850W Gold ATX 3.x:
- Cooler Master MWE Gold 850 V2 (~13 000 ₽, ATX 3.0)
- be quiet! Pure Power 12 M 850W (~14 000 ₽, ATX 3.0)
- Thermaltake Toughpower GF A3 850W (~11 500 ₽, ATX 3.0)

PN850D конкурентоспособен по цене и выигрывает наличием ATX 3.1 (не 3.0) и 135mm FDB-вентилятором.

## Для кого

**Идеален:**
- High-end игровые сборки (RTX 5070 Ti / RTX 5080)
- Рабочие станции (рендеринг, компиляция, инференс LLM)
- Сборки в любых корпусах (модульные кабели)

**Не подходит:**
- RTX 5090 с разгоном (брать 1000W+)
- Круглосуточный тренинг LLM (брать Platinum/Titanium)

## Источники

1. Deepcool PN850D Product Page (deepcool.com)
2. Price.ru — рыночные цены (оценка, 03.06.2026)
3. Cybenetics — сертификация 80 Plus Gold
