---
id: "asus-proart-z790-e"
type: "motherboard"
title: "ASUS ProArt Z790-E Creator WiFi"
vendor: "ASUS"
status: "draft"
tags: ["asus", "proart", "z790", "lga1700", "creator", "thunderbolt", "ddr5"]
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/intel-core-i9-14900k.md"
  competitor_am5: "catalog/motherboard/am5/asus-proart-x870e-creator.md"
  chipset_concept: "concepts/pcie-lanes.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "LGA1700"
  chipset: "Z790"
  form_factor: "ATX"
  memory: "4× DDR5, до 192GB, 7200+ MT/s (OC)"
  lan_chip: "Intel I226-V 2.5GbE + Marvell AQtion 10GbE"
  wifi: true
  wifi_chip: "WiFi 6E (Intel AX211)"
  bluetooth: true
  bluetooth_version: "5.3"
  thunderbolt4: "2 порта (Intel JHL8540)"
  m2_slots: 4
  m2_gen5: 1
  m2_gen4: 3
  pcie_5_x16: true
  pcie_slots: "1× PCIe 5.0 x16, 1× PCIe 4.0 x16 (x4), 1× PCIe 3.0 x1"
  sata_ports: 8
  vrm: "16+1 фаза, 70A DrMOS"
  audio: "Realtek ALC1220P"
  usb_ports_back: 10
  vrm_heatsink_height_max_mm: 35
  ram_slot_offset_x_mm: 53
profiles:
  creator_workstation:
    capability_level: 3
    steel_man_desc: "Z790 Creator: 10GbE + 2.5GbE + TB4 + 4× M.2. Полный набор для профессиональной DAW на LGA1700."
    failure_mode_desc: "Intel I226-V 2.5GbE — риск DPC-спайков на старых ревизиях. WiFi/BT обязательно отключить в UEFI."
    optimal_for_intents: ["daw_zero_dpc_latency", "video_editing_4k"]
  thunderbolt4_equipped:
    capability_level: 3
    steel_man_desc: "2× TB4 (Intel JHL8540) — прямое подключение UAD Apollo, RME Fireface"
    optimal_for_intents: ["daw_zero_dpc_latency"]
price_ru:
  min: 38000
  median: 42000
  max: 48000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# ASUS ProArt Z790-E Creator WiFi

## Позиционирование

Флагманская creator-плата для LGA1700. 10GbE + 2.5GbE, 2× Thunderbolt 4, 4× M.2 (1× Gen5). Для DAW на Intel 14-го поколения: i9-14900K / i7-14700K / i5-14600K.

**DPC-профиль:** Intel I226-V (2.5GbE) — проверить ревизию (v3 предпочтительна). Marvell AQtion 10GbE — стабилен, но драйвер обновлять. WiFi/BT — обязательно отключить в UEFI.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | LGA1700 |
| Чипсет | Z790 |
| Память | 4× DDR5, до 192GB, 7200+ MT/s |
| VRM | 16+1 (70A DrMOS) |
| Сеть | Intel I226-V 2.5GbE + Marvell AQtion 10GbE |
| WiFi/BT | Intel AX211 WiFi 6E + BT 5.3 (**отключить**) |
| Thunderbolt | 2× TB4 (Intel JHL8540) |
| M.2 | 4× (1× Gen5 + 3× Gen4) |
| Аудио | Realtek ALC1220P |
| USB (задняя) | 10 портов |

## DPC Latency

| Компонент | Риск | Mitigation |
|---|---|---|
| Intel I226-V | Средний | Проверить ревизию, обновить драйвер |
| Marvell 10GbE | Низкий | Обновить драйвер |
| WiFi 6E | Высокий | **Отключить в UEFI** |
| BT 5.3 | Средний | **Отключить в UEFI** |

## Для кого

- **DAW-станция на Intel 14th Gen:** лучшая LGA1700 плата для аудио
- **TB4-аудиоинтерфейсы (UA Apollo, RME через TB-адаптер)**
- **Сборки с приоритетом networking + expandability**

## НЕ подходит

- **Бюджетные сборки:** 42 000 ₽ за плату
- **SFF:** ATX
