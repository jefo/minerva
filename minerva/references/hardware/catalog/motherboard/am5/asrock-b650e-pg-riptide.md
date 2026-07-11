---
id: "asrock-b650e-pg-riptide"
type: "motherboard"
title: "ASRock B650E PG Riptide"
vendor: "ASRock"
status: "draft"
tags: ["asrock", "b650e", "am5", "daw-optimized", "minimal-controllers"]
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/amd-ryzen-7-7700.md"
  competitor_tomahawk: "catalog/motherboard/am5/msi-b650-tomahawk.md"
  up_variant_riptide: "catalog/motherboard/am5/asrock-b850-riptide.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "AM5"
  chipset: "B650E"
  form_factor: "ATX"
  memory: "4× DDR5, до 256GB, 7200+ MT/s (OC)"
  lan_chip: "Realtek RTL8125BG 2.5GbE"
  wifi: false
  bluetooth: false
  m2_slots: 3
  m2_gen5: 1
  pcie_5_x16: true
  vrm: "14+2+1 фазы, 60A DrMOS"
  audio: "Realtek ALC897"
  usb_ports_back: 8
  vrm_heatsink_height_max_mm: 30
  ram_slot_offset_x_mm: 53
profiles:
  daw_optimized_minimal:
    capability_level: 2
    steel_man_desc: "Нет WiFi, нет Bluetooth, Realtek 2.5GbE, минимум контроллеров. DPC-оптимизирована 'из коробки' — нечего отключать."
    failure_mode_desc: "ALC897 — базовый аудиокодек (не важно: внешний интерфейс). 14 фаз VRM — не для 170W CPU."
    optimal_for_intents: ["daw_zero_dpc_latency"]
    failure_for_intents: ["data_engineering_base"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 14000
  median: 16000
  max: 19000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# ASRock B650E PG Riptide

## Позиционирование

**Минималистичная DAW-плата.** Нет WiFi, нет Bluetooth, Realtek 2.5GbE, минимум дополнительных контроллеров. DPC-оптимизирована «из коробки» — нечего отключать в UEFI. Идеальна для бюджетных и средних DAW-станций.

**Ключевое отличие от B850 Riptide:** B650E вместо B850, слабее VRM (14 фаз 60A vs 16 фаз 80A), нет WiFi/BT совсем (B850 Riptide имеет, нужно отключать).

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | AM5 |
| Чипсет | B650E |
| Сеть | Realtek RTL8125BG 2.5GbE |
| WiFi/BT | **Нет** (DPC-преимущество) |
| M.2 | 3× (1× Gen5 + 2× Gen4) |
| VRM | 14+2+1 (60A) |
| Аудио | Realtek ALC897 |

## DPC Latency — преимущество

| Компонент | Статус | DPC-риск |
|---|---|---|
| Realtek 2.5GbE | Присутствует | Низкий |
| WiFi | **Отсутствует** | Нулевой |
| Bluetooth | **Отсутствует** | Нулевой |
| RGB-контроллер | Минимальный | Низкий |

## Для кого

- **Бюджетная/средняя DAW-станция:** DPC-оптимизация без ручного отключения
- **AMD Ryzen 7 7700 / 9700X (65-105W):** VRM достаточно
- **Сборки «включил и работаешь»**

## НЕ подходит

- **170W CPU (9950X):** 14 фаз 60A — предел. Брать B850 Riptide или X670E
- **Нужен WiFi:** отсутствует. B650 Tomahawk с отключением WiFi
