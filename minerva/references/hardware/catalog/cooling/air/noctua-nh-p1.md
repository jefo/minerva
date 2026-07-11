---
id: "noctua-nh-p1"
type: "cooling"
title: "Noctua NH-P1"
vendor: "Noctua"
status: "draft"
tags: ["noctua", "passive", "fanless", "silent", "zero-rpm"]
last_updated: "2026-06-07"
links:
  concept_acoustic: "concepts/daw-acoustic-class.md"
  concept_airflow: "concepts/dpc-latency.md"
specs:
  form_factor: "passive"
  layout_type: "passive_heatsink"
  height_mm: 158
  bottom_clearance_mm: 70
  horizontal_outlay_radius_mm: 77
  ram_clearance_mm: 45
  tdp_rating_w: 65
  tdp_rating_with_fan_w: 100
  fans: 0
  noise_min_dba: 0
  noise_max_dba: 0
  weight_g: 1180
  heatpipes: 6
  fin_spacing_mm: 6.7
  socket: ["AM5", "AM4", "LGA1700", "LGA1200"]
profiles:
  passive_cooling:
    power_envelope: "low"
    capability_level: 2
    steel_man_desc: "0 dBA — абсолютная тишина. 6 теплотрубок, асимметричный дизайн, spacing 6.7 мм для естественной конвекции."
    failure_mode_desc: "CLIFF_DROP: 65W CPU в глухом корпусе без airflow → thermal soak → троттлинг. Требует сквозного airflow (mesh-перед + exhaust). НЕ для звукоизолированных корпусов."
    optimal_for_intents: ["silent_build"]
    failure_for_intents: ["daw_zero_dpc_latency"]
    failure_type: "CLIFF_DROP"
    failure_severity: "BLOCK"
    note: "В глухом корпусе Pure Base 500 — тепловая ловушка. Overrated активный кулер (260W на 65W CPU) на минимальных оборотах тише пассивного в глухом корпусе."
price_ru:
  min: 9000
  median: 10000
  max: 12000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Noctua NH-P1

## Позиционирование

Единственный массовый пассивный CPU-кулер. 0 dBA — абсолютная тишина. Асимметричный дизайн, 6 теплотрубок, широкое межрёберное расстояние (6.7 мм) для естественной конвекции.

**КЛЮЧЕВОЕ ОГРАНИЧЕНИЕ:** пассивный кулер требует сквозного airflow в корпусе. В звукоизолированном корпусе (Pure Base 500) без dGPU естественная конвекция недостаточна — 65W CPU нагревается до троттлинга. **Для DAW-станции overrated активный кулер (260W на 65W) на минимальных оборотах ТИШЕ пассивного в глухом корпусе** — активный кулер предотвращает thermal soak, пассивный не может.

## Характеристики

| Параметр | Значение |
|---|---|
| Тип | Пассивный |
| TDP (без вентилятора) | 65W (зависит от airflow корпуса) |
| TDP (с опциональным 120mm) | 100W |
| Высота | 158 мм |
| Вентиляторы | 0 (опционально: 1× 120mm) |
| Шум | 0 dBA |
| Вес | 1180 г |
| Теплотрубки | 6 |
| Межрёберное расстояние | 6.7 мм |
| Сокеты | AM5, AM4, LGA1700, LGA1200 |
| RAM clearance | 45 мм (без вентилятора) |

## Когда пассивный кулер РАБОТАЕТ

- **Mesh-корпус с хорошим airflow:** фронтальные intake + rear exhaust создают сквозной поток
- **CPU не более 65W TDP**
- **Есть dGPU:** кулер видеокарты создаёт дополнительный airflow в нижней зоне

## Когда пассивный кулер НЕ РАБОТАЕТ

- **Глухой/звукоизолированный корпус:** нет сквозного airflow → конвекции недостаточно
- **Без dGPU:** нет дополнительного потока от GPU-кулера
- **Ambient >25°C:** temperature delta слишком мала для эффективной конвекции
- **CPU с пиковым потреблением >88W (PPT для 65W TDP Ryzen):** кратковременные пики вызывают накопление тепла

## Для кого

- **Silent-сборки в mesh-корпусах с хорошим airflow**
- **Офисные / HTPC системы** с низким тепловыделением

## НЕ подходит

- **DAW-станция «студийная тишина»:** глухой корпус + пассивный кулер = thermal soak. Overrated активный кулер правильнее.
- **Любой CPU мощнее 65W без корпусных вентиляторов**
- **UAE / жаркий климат:** малый ΔT убивает конвекцию

## Источники

- Noctua официальные спецификации (NH-P1)
- Noctua NSPR compatibility guide (корпуса, CPU)
- Тесты Gamers Nexus / Optimum Tech — passive cooling viability
