---
id: "msi-meg-z790-ace"
type: "motherboard"
title: "MSI MEG Z790 Ace"
vendor: "MSI"
status: "draft"
tags: ["msi", "meg", "z790", "lga1700", "premium", "usb4", "ddr5"]
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/intel-core-i9-14900k.md"
  competitor_proart: "catalog/motherboard/lga1700/asus-proart-z790-e.md"
  competitor_taichi: "catalog/motherboard/lga1700/asrock-z790-taichi.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "LGA1700"
  chipset: "Z790"
  form_factor: "E-ATX"
  memory: "4× DDR5, до 192GB, 7800+ MT/s (OC)"
  lan_chip: "Intel I226-V 2.5GbE"
  wifi: true
  wifi_chip: "WiFi 6E (Intel AX211)"
  bluetooth: true
  bluetooth_version: "5.3"
  usb4: "2 порта (Intel JHL8540)"
  m2_slots: 5
  m2_gen5: 2
  pcie_5_x16: true
  vrm: "24+1+2 фазы, 105A"
  audio: "Realtek ALC4082 + ESS SABRE9218 DAC"
  usb_ports_back: 10
  vrm_heatsink_height_max_mm: 38
  ram_slot_offset_x_mm: 54
profiles:
  premium_workstation:
    capability_level: 3
    steel_man_desc: "5× M.2 (2× Gen5) — максимум storage. 24+1+2 VRM. USB4."
    optimal_for_intents: ["daw_zero_dpc_latency"]
  usb4_equipped:
    capability_level: 3
    steel_man_desc: "2× USB4 (Intel JHL8540) — совместимость с TB3/TB4 аудиоинтерфейсами"
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 42000
  median: 48000
  max: 55000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# MSI MEG Z790 Ace

## Позиционирование

Premium Z790 от MSI. 5× M.2 (2× Gen5), USB4, 24+1+2 VRM. Максимальный storage expansion на LGA1700. Для DAW с большими сэмпловыми библиотеками.

**DPC:** Intel I226-V 2.5GbE — проверка ревизии обязательна. WiFi/BT отключить.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Чипсет | Z790 |
| Форм-фактор | E-ATX |
| VRM | 24+1+2 (105A) |
| Сеть | Intel I226-V 2.5GbE |
| USB4 | 2× (Intel JHL8540) |
| M.2 | **5×** (2× Gen5 + 3× Gen4) |
| Аудио | ALC4082 + ESS SABRE9218 |
| WiFi/BT | Intel AX211 + BT 5.3 (**отключить**) |

## DPC Latency

| Компонент | Риск | Mitigation |
|---|---|---|
| Intel I226-V | Средний | Обновить драйвер, отключить EEE |
| WiFi 6E | Высокий | **Отключить в UEFI** |
| BT 5.3 | Средний | **Отключить в UEFI** |

## Для кого

- **DAW с 5× M.2:** OS + проекты + 2× сэмплы + бэкап на отдельных дисках
- **i9-14900K:** 24 фазы держат 253W
- **Premium Intel-сборки**

## НЕ подходит

- **Бюджет:** 48 000 ₽ за плату
- **Стандартные ATX-корпуса:** E-ATX
