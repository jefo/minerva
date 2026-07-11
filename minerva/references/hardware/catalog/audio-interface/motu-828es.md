---
id: "motu-828es"
type: "audio_interface"
title: "MOTU 828es"
vendor: "MOTU"
status: "draft"
tags: ["motu", "audio-interface", "thunderbolt", "tier-1", "professional"]
last_updated: "2026-06-07"
links:
  down_variant: "catalog/audio-interface/motu-ultralite-mk5.md"
specs:
  driver_tier: "T1_Professional"
  connection: "USB 2.0 + Thunderbolt 2"
  inputs: 28
  outputs: 32
  preamps: 8
  adat_io: "2x ADAT (16ch)"
  avb: true
  midi_io: true
  max_sample_rate_khz: 192
  rtt_ms_at_64: 2.8
  min_stable_buffer: 64
  bus_powered: false
  dsp_mixer: "Встроенный DSP"
  headphone_outputs: 2
  phantom_power: "+48V"
  rack_unit: "1U"
profiles:
  professional_driver_quality:
    capability_level: 3
    steel_man_desc: "28 in, 8 преампов, TB + USB, AVB. Конкурент Fireface UFX II по числу каналов."
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 65000
  median: 70000
  max: 80000
  source: "DAW reference, June 2026"
---

# MOTU 828es

## Позиционирование
Многоканальный Tier 1. 28 in, 8 преампов, Thunderbolt + USB, AVB. Конкурент RME Fireface UFX II.

## Характеристики
| Параметр | Значение |
|---|---|
| Driver Tier | T1_Professional |
| Входы/Выходы | 28 / 32 |
| Преампы | 8 (+48V) |
| Цифровые I/O | 2x ADAT (16ch) |
| AVB | Да |
| RTT @ 64 | ~2.8 ms |
| Форм-фактор | 1U Rack |

## Для кого
- Многоканальная запись (8 преампов)
- AVB-студии с большим числом каналов
- Профессиональная DAW без RME-бюджета
