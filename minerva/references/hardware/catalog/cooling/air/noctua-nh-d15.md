---
id: "noctua-nh-d15"
type: "cooling"
title: "Noctua NH-D15"
vendor: "Noctua"
status: "draft"
tags: ["noctua", "dual-tower", "140mm", "air-cooling", "high-tdp"]
last_updated: "2026-06-07"
links:
  competitor_ak620: "catalog/cooling/air/deepcool-ak620.md"
  competitor_dark_rock: "catalog/cooling/air/be-quiet-dark-rock-tf-2.md"
  concept_thermal: "concepts/power-budget.md"
  concept_acoustic: "concepts/daw-acoustic-class.md"
specs:
  form_factor: "tower"
  layout_type: "dual_tower"
  height_mm: 165
  bottom_clearance_mm: 67
  horizontal_outlay_radius_mm: 75
  ram_clearance_mm: 32
  tdp_rating_w: 250
  fans: "2× NF-A15 PWM 140mm"
  fan_rpm_min: 300
  fan_rpm_max: 1500
  noise_min_dba: 19.2
  noise_max_dba: 24.6
  weight_g: 1320
  heatpipes: 6
  socket: ["AM5", "AM4", "LGA1700", "LGA1200"]
profiles:
  silent_air_cooling:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "250W TDP на 65W CPU → 4× запас → вентиляторы 300-400 RPM = 19 dBA — не слышно с 1 метра"
    failure_mode_desc: "165 мм высота — не влезает в корпуса с clearance <165 мм (DeepCool CC560: 155 мм). Башенный — M.2/VRM в аэродинамической тени без dGPU."
    optimal_for_intents: ["daw_zero_dpc_latency", "silent_build"]
    failure_for_intents: ["sff_compact_itx_portable"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
  high_tdp_air:
    capability_level: 3
    steel_man_desc: "250W sustained — один из немногих воздушных кулеров, способных охлаждать i9-14900K без троттлинга"
    optimal_for_intents: ["data_engineering_base", "ai_inference_base"]
price_ru:
  min: 8500
  median: 9500
  max: 11000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Noctua NH-D15

## Позиционирование

Эталонный двухбашенный воздушный кулер. 250W TDP, два 140mm вентилятора NF-A15, легендарная надёжность и 6-летняя гарантия. Для DAW: с 4× запасом по TDP на 65W CPU вентиляторы работают на 300-400 RPM — практически бесшумно (19 dBA).

**Ключевое ограничение:** 165 мм высота. Не влезает в корпуса с clearance <165 мм (DeepCool CC560: 155 мм). Башенный дизайн: в глухом корпусе без dGPU зона M.2/чипсета оказывается в аэродинамической тени — требуется направленный корпусной вентилятор или top-flow кулер.

## Характеристики

| Параметр | Значение |
|---|---|
| Тип | Двухбашенный воздушный |
| TDP | 250W (Noctua NSPR 183) |
| Высота | 165 мм (с вентиляторами) |
| Вентиляторы | 2× NF-A15 PWM 140mm |
| RPM | 300-1500 (с L.N.A.: 300-1200) |
| Шум | 19.2-24.6 dBA |
| Вес | 1320 г |
| Теплотрубки | 6 |
| Сокеты | AM5, AM4, LGA1700, LGA1200 |
| RAM clearance | 32 мм (передний вентилятор можно поднять, если корпус позволяет) |
| Bottom clearance | 67 мм |

## Сравнение с конкурентами

| Параметр | NH-D15 | AK620 | Dark Rock TF 2 |
|---|---|---|---|
| Тип | Двухбашенный | Двухбашенный | Top-flow |
| TDP | 250W | 260W | 230W |
| Высота | 165 мм | 160 мм | 134 мм |
| Вентиляторы | 2× 140mm | 2× 120mm | 2× 135mm |
| Шум (мин) | 19.2 dBA | 21 dBA | 12 dBA |
| M.2/VRM охлаждение | Тень (башня) | Тень (башня) | ✅ Downdraft |
| Цена | ~9 500 ₽ | ~6 000 ₽ | ~7 600 ₽ |

## Для кого

- **DAW-станция с 65-105W CPU:** огромный запас TDP → вентиляторы на минимальных оборотах → тишина
- **Сборки без dGPU в корпусах с хорошим airflow:** при направленном корпусном вентиляторе на зону VRM/M.2
- **Профессиональные рабочие станции:** надёжность Noctua + долгий срок службы

## НЕ подходит

- **Глухие корпуса без airflow:** M.2 в тепловой ловушке. Предпочесть top-flow (NH-C14S, Dark Rock TF 2)
- **SFF / корпуса с clearance <165 мм:** физически не влезает
- **Бюджетные сборки:** 9 500 ₽ — дорого. AK620 за 6 000 ₽ почти не уступает

## Источники

- Noctua официальные спецификации (NH-D15)
- Gamers Nexus / Hardware Canucks — thermal benchmarks
- Опыт сборщиков (VI-Control audio forum)
