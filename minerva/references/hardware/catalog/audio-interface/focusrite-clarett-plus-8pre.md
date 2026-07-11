---
id: "focusrite-clarett-plus-8pre"
type: "audio_interface"
title: "Focusrite Clarett+ 8Pre"
vendor: "Focusrite"
status: "draft"
tags: ["focusrite", "clarett", "audio-interface", "usb", "tier-2"]
last_updated: "2026-06-07"
links:
  driver_taxonomy: "concepts/audio-interface-drivers.md"
  down_variant: "catalog/audio-interface/focusrite-scarlett-2i2.md"
specs:
  driver_tier: "T2_Prosumer"
  connection: "USB-C (USB 3.0)"
  inputs: 18
  outputs: 8
  preamps: 8
  adat_io: "1x ADAT I/O (8ch)"
  midi_io: true
  max_sample_rate_khz: 192
  rtt_ms_at_128: 4.0
  min_stable_buffer: 128
  bus_powered: false
  air_mode: true
  phantom_power: "+48V"
  rack_unit: "1U"
profiles:
  prosumer_driver_quality:
    capability_level: 2
    steel_man_desc: "Tier 2. 8 преампов с Air Mode, хорошее качество предусилителей. Стабилен на 128 сэмплах."
    failure_mode_desc: "При больших проектах (100+ треков) и буфере 64 — возможны дропауты. Не для критичных к latency задач."
    optimal_for_intents: []
    failure_for_intents: ["daw_zero_dpc_latency"]
    failure_type: "LINEAR_DEGRADATION"
    failure_severity: "WARN"
price_ru:
  min: 50000
  median: 55000
  max: 65000
  source: "DAW reference, June 2026"
---

# Focusrite Clarett+ 8Pre

## Позиционирование
Tier 2. 8 преампов с Air Mode (эмуляция ISA transformer), хорошее качество звука. Стабилен на 128+ сэмплах. Для домашней студии и подкастов.

## Характеристики
| Параметр | Значение |
|---|---|
| Driver Tier | T2_Prosumer |
| Входы | 18 (8 XLR + ADAT 8ch) |
| Выходы | 8 |
| Преампы | 8 (Air Mode) |
| RTT @ 128 | ~4.0 ms |
| Мин. буфер | 128 сэмплов |

## Для кого
- Домашняя студия с приоритетом качества преампов
- Подкасты / стриминг

## НЕ подходит
- DAW_zero_dpc_latency: Tier 2 (128+ сэмплов). Предпочесть MOTU (Tier 1) или RME (Tier 0)
