---
id: "asrock-z790-taichi"
type: "motherboard"
title: "ASRock Z790 Taichi"
vendor: "ASRock"
status: "draft"
tags: ["asrock", "taichi", "z790", "lga1700", "enthusiast", "thunderbolt", "ddr5"]
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/intel-core-i9-14900k.md"
  competitor_proart: "catalog/motherboard/lga1700/asus-proart-z790-e.md"
  sibling_am5: "catalog/motherboard/am5/asrock-x670e-taichi.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "LGA1700"
  chipset: "Z790"
  form_factor: "E-ATX"
  memory: "4× DDR5, до 192GB, 7200+ MT/s (OC)"
  lan_chip: "Killer E3100G 2.5GbE + Intel I219-V 1GbE"
  wifi: true
  wifi_chip: "WiFi 6E (Killer AX1675)"
  bluetooth: true
  bluetooth_version: "5.3"
  thunderbolt4: "2 порта (Intel JHL8540)"
  m2_slots: 4
  m2_gen5: 1
  pcie_5_x16: true
  vrm: "24+1+2 фазы, 105A SPS"
  audio: "Realtek ALC4082 + ESS SABRE9218 DAC"
  usb_ports_back: 10
  vrm_heatsink_height_max_mm: 42
  ram_slot_offset_x_mm: 55
profiles:
  enthusiast_overclocking:
    capability_level: 3
    steel_man_desc: "24+1+2 (105A) — один из лучших VRM на LGA1700. Держит i9-14900K без троттлинга."
    optimal_for_intents: ["daw_zero_dpc_latency"]
  thunderbolt4_equipped:
    capability_level: 3
    steel_man_desc: "2× TB4 — профессиональные аудиоинтерфейсы"
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 35000
  median: 40000
  max: 48000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# ASRock Z790 Taichi

## Позиционирование

Флагманский Z790 от ASRock. 24+1+2 фазы (105A SPS), TB4, Killer 2.5GbE, ALC4082 + ESS DAC. Лучший VRM на LGA1700 для i9-14900K.

**DPC:** Killer E3100G 2.5GbE — стабильнее Intel I225-V для аудио. WiFi/BT отключить в UEFI.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Чипсет | Z790 |
| Форм-фактор | E-ATX |
| VRM | 24+1+2 (105A SPS) |
| Сеть | Killer E3100G 2.5GbE + Intel I219-V 1GbE |
| TB4 | 2× (Intel JHL8540) |
| M.2 | 4× (1× Gen5) |
| Аудио | ALC4082 + ESS SABRE9218 DAC |
| WiFi/BT | Killer AX1675 WiFi 6E + BT 5.3 (**отключить**) |

## DPC Latency

| Компонент | Риск | Mitigation |
|---|---|---|
| Killer E3100G | Низкий | Стабильнее Intel для аудио |
| WiFi 6E | Высокий | **Отключить в UEFI** |
| BT 5.3 | Средний | **Отключить в UEFI** |

## Для кого

- **i9-14900K DAW-станция:** 24 фазы — запас для 253W CPU
- **TB4-аудиоинтерфейсы**
- **E-ATX корпуса** (Define 7, Dark Base 701)

## НЕ подходит

- **Стандартные ATX-корпуса:** E-ATX (305×267 мм)
