---
id: "arctic-liquid-freezer-iii-280"
type: "cooling"
title: "Arctic Liquid Freezer III 280"
vendor: "Arctic"
status: "draft"
tags: ["arctic", "aio", "280mm", "liquid-cooling", "high-tdp", "silent"]
last_updated: "2026-06-07"
links:
  sibling_240: "catalog/cooling/liquid/arctic-liquid-freezer-iii-240.md"
  sibling_360: "catalog/cooling/liquid/arctic-liquid-freezer-iii-360.md"
  competitor_air: "catalog/cooling/air/noctua-nh-d15.md"
  concept_acoustic: "concepts/daw-acoustic-class.md"
specs:
  form_factor: "aio"
  layout_type: "aio_280"
  radiator_size: "280mm (2×140mm)"
  radiator_thickness_mm: 38
  pump_rpm: 2000
  pump_noise_dba: 22
  fans: "2× Arctic P14 PWM 140mm"
  fan_rpm_min: 200
  fan_rpm_max: 1700
  noise_min_dba: 15
  noise_max_dba: 28
  tdp_rating_w: 350
  socket: ["AM5", "AM4", "LGA1700", "LGA1200"]
  vrm_fan: true
  vrm_fan_desc: "Встроенный 40mm вентилятор на помпе для охлаждения VRM"
profiles:
  aio_high_tdp:
    capability_level: 3
    steel_man_desc: "350W TDP, 280mm радиатор — больше площади чем 240, тише чем 360. Оптимальный баланс для 170W+ CPU."
    failure_mode_desc: "Помпа 2000 RPM = тональный шум ~2000 Hz. BLOCK для A0_Studio (студийная тишина). Для DAW — ТОЛЬКО если CPU >105W и воздух не справляется."
    optimal_for_intents: ["video_editing_4k", "data_engineering_base"]
    failure_for_intents: ["daw_zero_dpc_latency"]
    failure_type: "CLIFF_DROP"
    failure_severity: "BLOCK"
    note: "Помпа гудит на ~2000 Hz в слышимом спектре. Для daw_zero_dpc_latency — только если CPU 170W+ и воздушный кулер не справляется."
price_ru:
  min: 8500
  median: 9500
  max: 11000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Arctic Liquid Freezer III 280

## Позиционирование

AIO 280mm — золотая середина между 240 и 360. 350W TDP, толстый радиатор (38 мм), встроенный VRM-вентилятор на помпе. Тише 360 (2×140mm вместо 3×120mm) при почти той же площади радиатора.

**ВАЖНО ДЛЯ DAW:** помпа гудит на ~2000 Hz — тональный шум в зоне максимальной чувствительности слуха (1-4 kHz). Для студийной тишины (A0_Studio) — BLOCK. Использовать только если воздушный кулер не справляется с тепловыделением CPU.

## Характеристики

| Параметр | Значение |
|---|---|
| Тип | AIO 280mm |
| Радиатор | 280×140×38 мм |
| TDP | 350W |
| Вентиляторы | 2× P14 PWM 140mm |
| RPM (вент.) | 200-1700 |
| Помпа | 2000 RPM |
| Шум (мин.) | 15 dBA (вентиляторы) + 22 dBA (помпа) |
| VRM-вентилятор | Да (40mm) |
| Сокеты | AM5, AM4, LGA1700, LGA1200 |

## Сравнение AIO

| Параметр | LF III 240 | LF III 280 | LF III 360 |
|---|---|---|---|
| TDP | 300W | 350W | 380W |
| Вентиляторы | 2×120mm | 2×140mm | 3×120mm |
| Шум (нагрузка) | 26 dBA | 24 dBA | 28 dBA |
| Цена | ~8 000 ₽ | ~9 500 ₽ | ~11 000 ₽ |

## Для кого

- **i9-14900K / R9 9950X (170W+):** воздух не справляется — AIO необходимо
- **Сборки где акустика не критична** (видеомонтаж, рендеринг)

## НЕ подходит

- **DAW_zero_dpc_latency:** помпа 2000 Hz — тональный шум. BLOCK. Воздушный NH-D15 на 65-105W CPU
- **Студийная тишина (A0_Studio):** AIO = автоматический BLOCK по правилу DAW-AC-01
