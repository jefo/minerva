---
id: "focusrite-scarlett-2i2"
type: "audio_interface"
title: "Focusrite Scarlett 2i2 (4th Gen)"
vendor: "Focusrite"
status: "draft"
tags: ["focusrite", "scarlett", "audio-interface", "usb", "tier-3", "budget"]
last_updated: "2026-06-07"
links:
  driver_taxonomy: "concepts/audio-interface-drivers.md"
  up_variant: "catalog/audio-interface/focusrite-clarett-plus-8pre.md"
specs:
  driver_tier: "T3_Consumer"
  connection: "USB 2.0 Type-C"
  inputs: 2
  outputs: 2
  preamps: 2
  midi_io: false
  max_sample_rate_khz: 192
  rtt_ms_at_128: 5.5
  min_stable_buffer: 128
  bus_powered: true
  air_mode: true
  phantom_power: "+48V"
profiles:
  consumer_driver_quality:
    capability_level: 1
    steel_man_desc: "Tier 3. Бюджетный, bus-powered, 2 преампа. Достаточно для домашней студии на 128+ сэмплах."
    failure_mode_desc: "При снижении буфера до 64/32 — риск дропаутов растёт экспоненциально. Не для профессиональной работы."
    optimal_for_intents: []
    failure_for_intents: ["daw_zero_dpc_latency"]
    failure_type: "CLIFF_DROP"
    failure_severity: "BLOCK"
price_ru:
  min: 12000
  median: 15000
  max: 18000
  source: "DAW reference, June 2026"
---

# Focusrite Scarlett 2i2

## Позиционирование
Бюджетный интерфейс Tier 3. 2 преампа с Air Mode, bus-powered. Стандартный выбор для начинающих. Стабилен на 128+ сэмплах.

## Характеристики
| Параметр | Значение |
|---|---|
| Driver Tier | T3_Consumer |
| Входы | 2 (XLR/TRS) |
| Выходы | 2 |
| Преампы | 2 (Air Mode) |
| RTT @ 128 | ~5.5 ms |
| Мин. буфер | 128 сэмплов |
| Питание | USB Bus Power |

## Для кого
- Начинающие музыканты / подкастеры
- Домашняя студия на 128 сэмплах

## НЕ подходит
- DAW_zero_dpc_latency: BLOCK. Tier 3, 128+ сэмплов, дропауты на 64/32
