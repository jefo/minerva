---
id: "be-quiet-dark-base-701"
type: "case"
title: "be quiet! Dark Base 701"
vendor: "be quiet!"
status: "draft"
tags: ["be-quiet", "dark-base", "full-tower", "sound-dampened", "atx", "silent", "mesh"]
last_updated: "2026-06-07"
links:
  sibling_pure_base: "catalog/case/be-quiet-pure-base-500.md"
  competitor_define7: "catalog/case/fractal-define-7.md"
specs:
  form_factor: "Full Tower ATX"
  motherboard_support: ["E-ATX", "ATX", "mATX", "ITX"]
  max_cooler_height_mm: 185
  max_gpu_length_mm: 415
  max_psu_length_mm: 250
  radiator_support: ["front: 420", "top: 360", "rear: 140"]
  fans_included: "3× Silent Wings 4 140mm PWM"
  fan_slots: 8
  front_io: ["USB-C 3.2 Gen2", "2× USB-A 3.2", "Audio"]
  sound_dampened: true
  sound_dampening_material: "Битумные маты (перед + боковые) + mesh-перед с пылевым фильтром"
  weight_kg: 14.5
  dimensions_mm: "565×249×544"
profiles:
  sound_dampened_thermal_trap:
    steel_man_desc: "Full Tower с mesh-передом и звукоизоляцией. 3× Silent Wings 4 140mm в комплекте (high-end вентиляторы). 185 мм клиренс кулера."
    failure_mode_desc: "Mesh-перед лучше Define 7 по airflow, но хуже по звукоизоляции на высоких оборотах."
    criteria_met: true
    optimal_for_intents: ["daw_zero_dpc_latency", "silent_build"]
price_ru:
  min: 14000
  median: 16000
  max: 19000
  source: "DAW reference, June 2026"
---

# be quiet! Dark Base 701

## Позиционирование

Full Tower корпус с гибридной акустикой: mesh-перед для airflow + битумные маты для звукоизоляции. 3× Silent Wings 4 140mm PWM в комплекте — вентиляторы премиум-класса (отдельно стоят ~6 000 ₽ за комплект). 

**Для DAW:** 185 мм клиренс кулера, mesh-перед решает проблему airflow в глухих корпусах (M.2/VRM получают достаточно воздуха даже без dGPU), звукоизоляция снижает широкополосный шум.

## Характеристики

| Параметр | Значение |
|---|---|
| Тип | Full Tower ATX |
| MB поддержка | E-ATX, ATX, mATX, ITX |
| Max высота кулера | 185 мм |
| Max длина GPU | 415 мм |
| Вентиляторов | 3× Silent Wings 4 140mm PWM |
| Слотов под вентиляторы | 8 |
| Радиаторы | Front 420, Top 360 |
| Front I/O | USB-C 3.2 Gen2, 2× USB-A |
| Звукоизоляция | Битумные маты + mesh-перед |
| Вес | 14.5 кг |

## Сравнение

| Параметр | Dark Base 701 | Define 7 | Pure Base 500 |
|---|---|---|---|
| Тип | Full Tower | Mid Tower | Mid Tower |
| Вентиляторов | 3× SW4 140mm | 2× GP-14 140mm | 2× PW3 140mm |
| Airflow | Mesh (отличный) | Глухой (ограничен) | Глухой (ограничен) |
| Цена | ~16 000 ₽ | ~14 000 ₽ | ~7 500 ₽ |

## Для кого

- **DAW-станция с горячим CPU (170W+) в тихом корпусе:** mesh-перед даёт airflow, звукоизоляция снижает шум
- **E-ATX платы** — Full Tower гарантирует совместимость
- **Сборки без dGPU:** mesh-перед + 3 вентилятора создают сквозной airflow даже без GPU

## НЕ подходит

- **Бюджетные сборки:** 16 000 ₽ + стоимость корпуса. Pure Base 500 за 7 500 ₽ — разумная альтернатива
- **SFF:** Full Tower, 14.5 кг
