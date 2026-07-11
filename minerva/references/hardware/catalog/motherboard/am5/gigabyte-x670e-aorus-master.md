---
id: "gigabyte-x670e-aorus-master"
type: "motherboard"
title: "Gigabyte X670E Aorus Master"
vendor: "Gigabyte"
status: "draft"
tags: ["gigabyte", "x670e", "am5", "aorus", "enthusiast"]
last_updated: "2026-06-07"
links:
  competitor_proart: "catalog/motherboard/am5/asus-proart-x870e-creator.md"
  competitor_taichi: "catalog/motherboard/am5/asrock-x670e-taichi.md"
  platform_cpu: "catalog/cpu/amd-ryzen-9-7900.md"
  chipset_concept: "concepts/pcie-lanes.md"
  dpc_concept: "concepts/dpc-latency.md"
specs:
  socket: "AM5"
  chipset: "X670E"
  form_factor: "E-ATX"
  lan_chip: "Intel I225-V 2.5GbE"
  wifi: true
  wifi_chip: "MediaTek MT7922 WiFi 6E"
  bluetooth: true
  bluetooth_version: "5.3"
  m2_slots: 4
  m2_gen5: 1
  pcie_5_x16: true
  vrm: "16+2+2 фазы, 105A SPS"
  audio: "Realtek ALC1220-VB + ESS SABRE 9118 DAC"
  usb_ports_back: 13
  vrm_heatsink_height_max_mm: 40
  ram_slot_offset_x_mm: 53
profiles:
  enthusiast_overclocking:
    power_envelope: "high"
    capability_level: 3
    steel_man_desc: "16+2+2 фазы 105A — избыточно для любого AM5 CPU. VRM 50°C при 250W нагрузке."
    failure_mode_desc: "E-ATX — не влезает в стандартные Mid-Tower корпуса. Требует корпус с поддержкой E-ATX."
    optimal_for_intents: ["daw_zero_dpc_latency"]
    failure_for_intents: ["sff_compact_itx_portable"]
    failure_type: "CLIFF_DROP"
    failure_severity: "BLOCK"
  pcie_5_ready:
    capability_level: 3
    steel_man_desc: "PCIe 5.0 x16 + 1× M.2 Gen5 — полная готовность к будущим GPU и NVMe"
    optimal_for_intents: ["daw_zero_dpc_latency", "ai_inference_base"]
price_ru:
  min: 45000
  median: 52000
  max: 60000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Gigabyte X670E Aorus Master

## Позиционирование

Флагманская плата Gigabyte на чипсете X670E. 16+2+2 фазы 105A SPS — один из лучших VRM на AM5. 4× M.2 (1× Gen5), качественный аудиотракт (ALC1220-VB + ESS 9118 DAC). Для DAW: Intel I225-V 2.5GbE требует проверки ревизии (v3 — исправлен, v1/v2 — известные DPC-проблемы).

**Отличие от конкурентов:** уступает ASRock X670E Taichi в networking (нет 10GbE) и USB4 (только через отдельную карту). Выигрывает по VRM и качеству аудиотракта.

## Характеристики

| Параметр | Значение |
|---|---|
| Сокет | AM5 |
| Чипсет | X670E (Dual Promontory 21) |
| Форм-фактор | E-ATX (305×269 мм) |
| VRM | 16+2+2 фазы, 105A SPS |
| Память | 4× DDR5, до 192GB, 8000+ MT/s (OC) |
| PCIe 5.0 x16 | 1 слот |
| M.2 | 4 слота (1× Gen5 x4, 3× Gen4 x4) |
| Сеть | Intel I225-V 2.5GbE |
| Wi-Fi / BT | MediaTek MT7922 WiFi 6E + BT 5.3 (**отключить в UEFI для DPC**) |
| Аудио | Realtek ALC1220-VB + ESS SABRE 9118 DAC |
| USB задняя панель | 13 портов (включая 1× USB-C 20Gbps) |
| VRM heatsink | 40 мм |
| RAM offset | 53 мм |

## DPC Latency Profile

| Компонент | DPC-риск | Mitigation |
|---|---|---|
| Intel I225-V (2.5GbE) | **Средний** | Проверить ревизию (v3 предпочтительна). Отключить Energy-Efficient Ethernet, обновить драйвер до последней версии |
| MediaTek MT7922 (WiFi) | **Высокий** | Отключить в UEFI |
| Bluetooth 5.3 | **Средний** | Отключить в UEFI |
| RGB Fusion | **Низкий** | Не устанавливать RGB Fusion (фоновая активность USB) |
| ALC1220-VB | **Низкий** | Отключить в UEFI (используется внешний аудиоинтерфейс) |

## Сравнение с конкурентами

| Параметр | X670E Aorus Master | ASUS ProArt X870E | ASRock X670E Taichi |
|---|---|---|---|
| VRM | 16+2+2 (105A) | 18+2+2 (110A) | 24+2+1 (105A) |
| LAN | Intel 2.5GbE | Dual 5GbE | 10GbE + 2.5GbE |
| USB4/TB4 | Нет | 2× TB4 | 2× USB4 |
| M.2 | 4× (1× Gen5) | 4× (2× Gen5) | 4× (1× Gen5) |
| Аудио | ALC1220-VB + ESS | ALC1220P | ALC4082 |
| Цена | ~52 000 ₽ | ~55 000 ₽ | ~50 000 ₽ (EOL) |

## Для кого

- **DAW-станция с приоритетом VRM и M.2:** 4× M.2 — отлично для OS + сэмплы + бэкап + scratch disk
- **Профессиональная рабочая станция:** запас VRM для будущих Zen 6 CPU
- **Требуется E-ATX корпус** (не влезает в стандартные Mid-Tower)

## НЕ подходит

- **SFF-сборки:** E-ATX
- **DAW с приоритетом минимального DPC:** Intel I225-V хуже Realtek RTL8125BG для DPC. Предпочесть ASRock B850 Riptide или ASUS ProArt B650E
- **Бюджетные сборки:** 52 000 ₽ за плату — избыточно для домашней студии

## Источники

- Gigabyte официальные спецификации (X670E Aorus Master rev. 1.x)
- VI-Control / Gearspace — DPC-тесты AM5 материнских плат (2025)
- Форум Level1Techs — Intel I225-V latency обсуждение
