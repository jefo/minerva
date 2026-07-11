---
id: "seasonic-focus-gx-650"
type: "psu"
title: "Seasonic Focus GX-650"
vendor: "Seasonic"
status: "draft"
tags: ["seasonic", "focus", "gold", "650w", "semi-passive", "atx3"]
last_updated: "2026-06-07"
links:
  sibling_750: "catalog/psu/seasonic-focus-gx-750.md"
  competitor_bequiet: "catalog/psu/be-quiet-pure-power-12m-750w.md"
  concept_power: "concepts/power-budget.md"
  concept_acoustic: "concepts/daw-acoustic-class.md"
specs:
  wattage: 650
  efficiency: "80+ Gold"
  form_factor: "ATX"
  length_mm: 140
  fan_size_mm: 120
  fan_type: "Fluid Dynamic Bearing"
  acoustic_profile: "semi_passive"
  fan_stop_threshold_w: 200
  modular: true
  atx_version: "ATX 3.0"
  pcie_5_12vhpwr: false
  warranty_years: 10
  protections: ["OPP", "OVP", "UVP", "SCP", "OCP", "OTP"]
profiles:
  semi_passive_psu:
    capability_level: 2
    steel_man_desc: "Fan-stop до ~200W. Для 65W CPU без dGPU (система <115W) вентилятор никогда не включается. 0 dBA всегда."
    failure_mode_desc: "650W — маловато для сборок с мощной dGPU (RTX 5080+ 360W). Нет 12V-2×6 (только ATX 3.0, не 3.1)."
    optimal_for_intents: ["daw_zero_dpc_latency", "silent_build", "esports_competitive_360hz"]
    failure_for_intents: ["ai_inference_base"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
price_ru:
  min: 8000
  median: 9000
  max: 11000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Seasonic Focus GX-650

## Позиционирование

Премиальный 650W блок питания с semi-passive режимом и 10-летней гарантией. Эталонный выбор для сборок без dGPU: при системном потреблении <115W (65W CPU + NVMe + чипсет) вентилятор никогда не включается → 0 dBA от БП.

**Ключевое отличие от 750W-версии:** Focus GX-750 уже в каталоге. GX-650 — для сборок где 750W избыточно, а semi-passive порог важен.

## Характеристики

| Параметр | Значение |
|---|---|
| Мощность | 650W |
| Сертификат | 80+ Gold |
| Форм-фактор | ATX, 140 мм |
| Вентилятор | 120mm FDB |
| Акустический профиль | Semi-passive (fan-stop до ~200W) |
| Модульность | Полная |
| ATX-версия | 3.0 |
| 12V-2×6 | Нет |
| Гарантия | 10 лет |

## Сравнение с Focus GX-750

| Параметр | GX-650 | GX-750 |
|---|---|---|
| Мощность | 650W | 750W |
| Fan-stop порог | ~200W | ~225W |
| Цена | ~9 000 ₽ | ~10 500 ₽ |
| Выбор для | iGPU сборки до 150W | Сборки с dGPU до 300W |

## Для кого

- **DAW-станция без dGPU:** 650W с запасом 5.6× для системы 115W peak. Fan-stop активен всегда
- **Silent-сборки с iGPU:** 0 dBA от PSU в рабочем диапазоне
- **Бюджетные сборки с dGPU до 200W:** достаточный запас для RTX 4060 / RX 7600

## НЕ подходит

- **Сборки с мощной dGPU (RTX 5080+, 360W):** недостаточно мощности + нет 12V-2×6
- **Multi-GPU сборки**
- **Будущий апгрейд на мощную dGPU**

## Источники

- Seasonic официальные спецификации (Focus GX-650)
- Cybenetics 80+ Gold сертификация
