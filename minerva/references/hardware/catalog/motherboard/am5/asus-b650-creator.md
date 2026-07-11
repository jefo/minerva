---
id: "asus-b650-creator"
type: "motherboard"
title: "ASUS B650 Creator"
vendor: "ASUS"
status: "draft"
tags: ["asus", "b650", "am5", "creator", "usb4", "budget"]
last_updated: "2026-06-07"
links:
  up_variant_proart: "catalog/motherboard/am5/asus-b650e-proart.md"
  platform_cpu: "catalog/cpu/amd-ryzen-7-7700.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "AM5"
  chipset: "B650"
  form_factor: "ATX"
  memory: "4× DDR5, до 192GB, 6400+ MT/s (OC)"
  lan_chip: "Realtek RTL8125BG 2.5GbE"
  wifi: true
  wifi_chip: "WiFi 6 (MediaTek MT7921)"
  bluetooth: true
  bluetooth_version: "5.2"
  usb4: "1 порт (Intel JHL8540)"
  m2_slots: 3
  m2_gen5: 0
  m2_gen4: 3
  m2_topology: "M2_1: CPU PCIe 4.0 x4, M2_2: PCH PCIe 4.0 x4, M2_3: PCH PCIe 4.0 x4"
  pcie_5_x16: false
  pcie_4_x16: true
  vrm: "12+2 фазы, 60A DrMOS"
  audio: "Realtek ALC1220P"
  usb_ports_back: 8
  vrm_heatsink_height_max_mm: 32
  ram_slot_offset_x_mm: 54
profiles:
  creator_budget:
    capability_level: 2
    steel_man_desc: "Единственная B650 с USB4. 1× TB4/USB4 порт за ~18 000 ₽ — вход в экосистему Thunderbolt-аудиоинтерфейсов."
    failure_mode_desc: "WiFi/BT присутствуют — нужно отключать. B650 (не E) — нет PCIe 5.0. 12 фаз 60A — не для 170W CPU."
    optimal_for_intents: ["daw_zero_dpc_latency"]
    failure_for_intents: ["ai_inference_base"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 16000
  median: 18000
  max: 22000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# ASUS B650 Creator

## Позиционирование

Бюджетная creator-плата с USB4. Самый доступный вход в Thunderbolt-экосистему на AM5: 1× USB4 (Intel JHL8540) для профессиональных аудиоинтерфейсов. WiFi/BT — отключить в UEFI.

**Отличие от B650E-ProArt:** B650 (не E) — нет PCIe 5.0 на x16, только PCIe 4.0. USB4 только 1 порт (vs 1 на ProArt). VRM слабее (12 фаз vs 12+2+2). Цена на 7 000 ₽ ниже.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | AM5 |
| Чипсет | B650 |
| Сеть | Realtek RTL8125BG 2.5GbE |
| USB4 | 1× (Intel JHL8540) |
| WiFi/BT | WiFi 6 + BT 5.2 (**отключить**) |
| M.2 | 3× (все Gen4) |
| PCIe | 4.0 x16 (нет 5.0) |
| VRM | 12+2 (60A) |

## DPC Latency

| Компонент | Риск | Mitigation |
|---|---|---|
| Realtek 2.5GbE | Низкий | Стабилен для аудио |
| WiFi 6 | Средний | **Отключить в UEFI** |
| BT 5.2 | Низкий | **Отключить в UEFI** |

## Для кого

- **Бюджетная DAW с TB-интерфейсом:** USB4 за 18 000 ₽
- **Ryzen 7 7700 / 9700X (65-105W):** VRM достаточно
- **Сборки без PCIe 5.0-потребностей:** аудио не требует Gen5 GPU

## НЕ подходит

- **PCIe 5.0 GPU/NVMe:** только PCIe 4.0. Брать B650E-ProArt
- **170W CPU:** 12 фаз 60A — слабо. Брать X670E/X870E
