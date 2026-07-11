---
id: "be-quiet-pure-base-500dx"
type: "case"
title: "be quiet! Pure Base 500DX"
vendor: "be-quiet"
status: "draft"
tags: ["mesh", "atx", "mid-tower", "rgb", "airflow", "3x140mm"]
last_updated: "2026-07-06"
links:
  silent_variant: "catalog/case/be-quiet-pure-base-500.md"
specs:
  form_factor: "Mid-Tower"
  mb_support: ["ATX", "Micro-ATX", "Mini-ITX"]
  dimensions_mm: "450×232×463"
  material: "Steel + tempered glass side panel"
  front_panel: "Mesh (перфорированная сетка)"
  fans_included:
    - size: 140
      model: "Pure Wings 2 140mm"
      position: "front"
      count: 2
      max_rpm: 900
    - size: 140
      model: "Pure Wings 2 140mm"
      position: "rear"
      count: 1
      max_rpm: 900
  fan_support:
    front: "3×120mm / 2×140mm"
    top: "2×120mm / 2×140mm"
    rear: "1×120mm / 1×140mm"
  radiator_support:
    front: "360mm"
    top: "240mm"
    rear: "140mm"
  clearance:
    gpu_max_length_mm: 369
    cooler_max_height_mm: 190
    psu_max_length_mm: 258
  drive_bays:
    internal_3_5: 2
    internal_2_5: 5
  front_io:
    usb_3_2_gen2_type_c: 1
    usb_3_2_gen1_type_a: 2
    audio: "HD Audio (mic + headphone)"
  psu_shroud: true
  cable_management: true
  dust_filters: ["front", "top", "bottom"]
  rgb: "Front + internal ARGB strip (контроллер встроен)"
physical_stereotypes:
  atx_form_factor: true
  sfx_form_factor_locked: false
  itx_form_factor: false
  airflow_class: "high"
price_ru:
  min: 8000
  median: 8800
  max: 9500
  source: "price.ru / DNS / Яндекс.Маркет"
  date: "2026-07-06"
  status: "verified"
engineering_notes:
  - "Mesh-фронтал — низкое сопротивление airflow. GPU получает холодный воздух напрямую."
  - "3× Pure Wings 2 140mm на 900 RPM — бесшумны. Не требуют замены."
  - "Акустический парадокс: mesh-корпус тише звукоизолированного при мощном GPU. Причина: низкая температура GPU → низкие обороты вентиляторов."
  - "Зазор GPU 369mm — любой RTX 5070 влезает с запасом."
  - "Зазор кулера 190mm — даже NH-D15 (165mm) влезает."
verdict: "Mesh-корпус для тихих мощных сборок. 3×140mm из коробки — не нужно докупать вентиляторы. Лучше звукоизолированного Pure Base 500 для GPU >200W."
---

# be quiet! Pure Base 500DX

## Позиционирование

Mesh-версия Pure Base 500. Сохраняет чистый дизайн, но заменяет глухую переднюю панель на перфорированную сетку. 3×140mm Pure Wings 2 на низких оборотах — бесшумный airflow.

## Ключевое отличие от Pure Base 500

| | Pure Base 500 | Pure Base 500DX |
|---|---|---|
| Передняя панель | Глухая (звукоизоляция) | Mesh (сетка) |
| Вентиляторы | 2×140mm | 3×140mm |
| Airflow | Низкий | Высокий |
| Для GPU до | ~150W | ~350W |
| Шум под нагрузкой | Выше (GPU кричит) | Ниже (GPU холодный) |

Парадокс: mesh-корпус тише звукоизолированного при мощном GPU. Причина: холодный GPU крутит вентиляторы на 40% вместо 80%.
