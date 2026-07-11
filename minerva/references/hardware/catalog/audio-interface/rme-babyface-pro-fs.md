---
id: "rme-babyface-pro-fs"
type: "audio_interface"
title: "RME Babyface Pro FS"
vendor: "RME"
status: "draft"
tags: ["rme", "audio-interface", "usb", "tier-0", "studio", "low-latency"]
last_updated: "2026-06-07"
links:
  driver_taxonomy: "concepts/audio-interface-drivers.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  driver_tier: "T0_Reference"
  connection: "USB 3.1 Type-C"
  inputs: 12
  outputs: 14
  preamps: 2
  adat_io: "1x ADAT I/O (8ch)"
  midi_io: true
  max_sample_rate_khz: 192
  rtt_ms_at_32: 1.2
  rtt_ms_at_64: 2.5
  min_stable_buffer: 32
  bus_powered: true
  dsp_mixer: "TotalMix FX"
  headphone_outputs: 2
  phantom_power: "+48V"
profiles:
  reference_driver_quality:
    capability_level: 3
    steel_man_desc: "Эталонные драйверы. 32 сэмпла стабильно. RTT ~1.2 мс на 32 сэмплах. TotalMix FX."
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 94449
  median: 105000
  max: 121220
  source: "price.ru, 2026-06-07"
  stores: 5

# RME Babyface Pro FS

## Позиционирование
Эталонный аудиоинтерфейс Tier 0. Ручная сборка драйверов, TotalMix FX, 32 сэмпла стабильно.

## Характеристики
| Параметр | Значение |
|---|---|
| Driver Tier | T0_Reference |
| Подключение | USB 3.1 Type-C |
| Входы | 12 (2 XLR/TRS + ADAT 8ch) |
| Выходы | 14 |
| Преампы | 2 (SteadyClock FS) |
| RTT @ 32 | ~1.2 ms |
| RTT @ 64 | ~2.5 ms |
| Питание | USB Bus Power |
| DSP | TotalMix FX |
| Наушники | 2 независимых |

## Для кого
- Профессиональная DAW: запись на 32 сэмплах без дропаутов
- Мобильная студия (bus-powered)

## НЕ подходит
- Бюджетная студия (70 000 ₽)
- Многоканальная запись (2 преампа → Fireface UFX II)

## Источники
- RME specs, Gearspace RTL Database, VI-Control
