---
id: "motu-ultralite-mk5"
type: "audio_interface"
title: "MOTU UltraLite Mk5"
vendor: "MOTU"
status: "draft"
tags: ["motu", "audio-interface", "usb", "tier-1", "professional", "avb"]
last_updated: "2026-06-07"
links:
  up_variant: "catalog/audio-interface/motu-828es.md"
specs:
  driver_tier: "T1_Professional"
  connection: "USB-C (USB 3.0)"
  inputs: 18
  outputs: 14
  preamps: 2
  adat_io: "1x ADAT (8ch)"
  avb: true
  midi_io: true
  max_sample_rate_khz: 192
  rtt_ms_at_64: 3.0
  min_stable_buffer: 64
  bus_powered: false
  dsp_mixer: "48-channel DSP"
  phantom_power: "+48V"
profiles:
  professional_driver_quality:
    capability_level: 2
    steel_man_desc: "Tier 1 драйверы. Стабильно на 64 сэмплах. 18 входов, AVB."
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 45000
  median: 50000
  max: 58000
  source: "DAW reference, June 2026"
---

# MOTU UltraLite Mk5

## Позиционирование
Tier 1 в компактном корпусе. 18 входов, AVB, DSP-микшер. Оптимально когда RME не по бюджету.

## Характеристики
| Параметр | Значение |
|---|---|
| Driver Tier | T1_Professional |
| Входы | 18 (2 XLR + 8 line + ADAT 8ch) |
| Выходы | 14 |
| AVB | Да |
| RTT @ 64 | ~3.0 ms |
| DSP | 48-channel mixer |

## Для кого
- Профессиональная DAW на 64 сэмплах
- AVB-студии

## НЕ подходит
- 32 сэмпла (RME Tier 0)
- Много преампов (828es)
