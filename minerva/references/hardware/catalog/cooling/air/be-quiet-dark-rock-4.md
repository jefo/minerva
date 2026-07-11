---
id: "be-quiet-dark-rock-4"
type: "cooling"
title: "be quiet! Dark Rock 4"
vendor: "be quiet!"
status: "draft"
tags: ["be-quiet", "single-tower", "135mm", "air-cooling", "silent"]
last_updated: "2026-06-07"
links:
  up_variant_tf2: "catalog/cooling/air/be-quiet-dark-rock-tf-2.md"
  competitor_nh_d15: "catalog/cooling/air/noctua-nh-d15.md"
  competitor_ak620: "catalog/cooling/air/deepcool-ak620.md"
  concept_acoustic: "concepts/daw-acoustic-class.md"
specs:
  form_factor: "tower"
  layout_type: "single_tower"
  height_mm: 159
  bottom_clearance_mm: 46
  horizontal_outlay_radius_mm: 68
  ram_clearance_mm: 40
  tdp_rating_w: 200
  fans: "1× Silent Wings 3 135mm PWM"
  fan_rpm_min: 400
  fan_rpm_max: 1400
  noise_min_dba: 12.8
  noise_max_dba: 21.4
  weight_g: 920
  heatpipes: 6
  socket: ["AM5", "AM4", "LGA1700", "LGA1200"]
profiles:
  silent_air_cooling:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "200W TDP, один 135mm Silent Wings 3 — 12.8 dBA на минимальных оборотах. Практически бесшумен на 65W CPU."
    failure_mode_desc: "Односекционная башня, 200W — уступает NH-D15 (250W) и AK620 (260W) по максимальному TDP. Не для 170W+ CPU."
    optimal_for_intents: ["daw_zero_dpc_latency", "silent_build"]
    failure_for_intents: ["data_engineering_base"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 6000
  median: 7000
  max: 8500
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# be quiet! Dark Rock 4

## Позиционирование

Односекционный башенный кулер премиум-класса. 200W TDP, один 135mm вентилятор Silent Wings 3. Отличный выбор для 65-105W CPU в тихих сборках. Для DAW: 200W на 65W CPU → 3× запас → вентилятор на 400-500 RPM → 13-15 dBA (сливается с фоном комнаты).

**Ключевое преимущество:** 159 мм высота — влезает в большинство Mid-Tower корпусов (где NH-D15 165 мм уже не помещается).

## Характеристики

| Параметр | Значение |
|---|---|
| Тип | Односекционная башня |
| TDP | 200W |
| Высота | 159 мм |
| Вентилятор | 1× Silent Wings 3 135mm PWM |
| RPM | 400-1400 |
| Шум | 12.8-21.4 dBA |
| Вес | 920 г |
| Теплотрубки | 6 |
| Сокеты | AM5, AM4, LGA1700, LGA1200 |
| RAM clearance | 40 мм |

## Сравнение с конкурентами

| Параметр | Dark Rock 4 | NH-D15 | AK620 |
|---|---|---|---|
| Тип | Односекционный | Двухбашенный | Двухбашенный |
| TDP | 200W | 250W | 260W |
| Высота | 159 мм | 165 мм | 160 мм |
| Вентиляторы | 1× 135mm | 2× 140mm | 2× 120mm |
| Шум (мин) | 12.8 dBA | 19.2 dBA | 21 dBA |
| Цена | ~7 000 ₽ | ~9 500 ₽ | ~6 000 ₽ |

## Для кого

- **DAW-станция с 65-105W CPU:** 3× запас TDP → минимальные обороты → почти бесшумен
- **Корпуса с clearance <165 мм:** 159 мм — компромисс между производительностью и совместимостью
- **Тихие сборки:** be quiet! — бренд, специализирующийся на акустике

## НЕ подходит

- **170W+ CPU (Ryzen 9 9950X, i9-14900K):** 200W TDP недостаточно. Выбирать NH-D15 или AIO
- **Глухие корпуса без dGPU:** башенный → M.2/VRM в тени. Предпочесть top-flow Dark Rock TF 2

## Источники

- be quiet! официальные спецификации (Dark Rock 4)
- Тесты KitGuru / TechPowerUp — thermal benchmarks
