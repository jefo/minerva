---
id: "fractal-define-7"
type: "case"
title: "Fractal Design Define 7"
vendor: "Fractal Design"
status: "draft"
tags: ["fractal", "define", "mid-tower", "sound-dampened", "atx", "silent"]
last_updated: "2026-06-07"
links:
  competitor_pure_base: "catalog/case/be-quiet-pure-base-500.md"
  concept_acoustic: "concepts/daw-acoustic-class.md"
specs:
  form_factor: "Mid Tower ATX"
  motherboard_support: ["E-ATX", "ATX", "mATX", "ITX"]
  max_cooler_height_mm: 185
  max_gpu_length_mm: 470
  max_psu_length_mm: 250
  radiator_support: ["front: 360", "top: 420", "bottom: 240"]
  drive_bays: "6× 3.5/2.5 + 2× 2.5 + 2× 5.25"
  fans_included: "2× Dynamic X2 GP-14 140mm"
  fan_slots: 9
  front_io: ["USB-C 3.2 Gen2", "2× USB-A 3.0", "Audio"]
  sound_dampened: true
  sound_dampening_material: "Битумные маты (перед + боковые + верхняя панель)"
  weight_kg: 13.5
  dimensions_mm: "547×240×475"
profiles:
  sound_dampened_thermal_trap:
    steel_man_desc: "Полная звукоизоляция битумными матами на всех панелях + вентиляционные заслонки ModuVent. 185 мм клиренс кулера — совместим с NH-D15 (165 мм)."
    failure_mode_desc: "Глухой корпус без dGPU → M.2/VRM в аэродинамической тени. Требует направленного airflow (top-flow кулер или дополнительный вентилятор на чипсет)."
    criteria_met: true
    optimal_for_intents: ["daw_zero_dpc_latency", "silent_build"]
    failure_for_intents: ["sff_compact_itx_portable"]
price_ru:
  min: 12000
  median: 14000
  max: 17000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Fractal Design Define 7

## Позиционирование

Флагманский звукоизолированный корпус. Битумные маты на всех панелях, съёмные вентиляционные заслонки ModuVent, поддержка E-ATX, клиренс кулера 185 мм (влезает NH-D15 165 мм с запасом 20 мм). Индустриальный стандарт для тихих сборок.

**Для DAW:** 185 мм клиренс → совместим с любым воздушным кулером. 2× 140mm вентилятора в комплекте (можно добавить ещё). Требует направленного airflow на зону M.2/VRM при отсутствии dGPU.

## Характеристики

| Параметр | Значение |
|---|---|
| Форм-фактор | Mid Tower ATX |
| MB поддержка | E-ATX, ATX, mATX, ITX |
| Max высота кулера | 185 мм |
| Max длина GPU | 470 мм |
| Вентиляторов в комплекте | 2× 140mm |
| Слотов под вентиляторы | 9 |
| Радиаторы | Front 360, Top 420, Bottom 240 |
| Front I/O | USB-C 3.2 Gen2, 2× USB-A 3.0, Audio |
| Звукоизоляция | Битумные маты (все панели) + ModuVent |
| Вес | 13.5 кг |
| Габариты | 547×240×475 мм |

## Сравнение с Pure Base 500

| Параметр | Define 7 | Pure Base 500 |
|---|---|---|
| Клиренс кулера | 185 мм | 190 мм |
| Вентиляторов | 2× 140mm | 2× 140mm |
| Звукоизоляция | Полная + ModuVent | Битумные маты |
| Вес | 13.5 кг | 7.8 кг |
| E-ATX | Да | Нет |
| Цена | ~14 000 ₽ | ~7 500 ₽ |

## Для кого

- **Профессиональная DAW-станция:** полная звукоизоляция + совместимость с любым воздушным кулером
- **E-ATX платы** (Gigabyte X670E Aorus Master, ASRock X670E Taichi)
- **Сборки с приоритетом тишины и расширяемости**

## НЕ подходит

- **Бюджетные сборки:** 14 000 ₽ за корпус — дорого. Pure Base 500 за 7 500 ₽ покрывает 90% потребностей
- **SFF / компактные сборки:** 13.5 кг, большие габариты

## Airflow для DAW без dGPU

В Define 7 без видеокарты зона M.2/чипсета в нижней части платы получает меньше airflow. Решения:
- **Top-flow кулер** (Dark Rock TF 2, NH-C14S) — дует вниз на VRM/M.2
- **Дополнительный 140mm на нижнюю позицию** — направленный поток на чипсет
- **Top exhaust** — два 140mm на верхнюю панель (снять ModuVent)

## Источники

- Fractal Design официальные спецификации (Define 7)
- Gamers Nexus — thermal + acoustic benchmarks
