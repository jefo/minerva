---
id: "msi-pro-b760m-a-wifi-ddr4"
type: "motherboard"
title: "MSI PRO B760M-A WIFI DDR4"
vendor: "MSI"
chipset: "B760"
socket: "LGA1700"
form_factor: "Micro-ATX"
memory_type: "DDR4"
status: "draft"
tags: ["lga1700", "b760", "ddr4", "wifi6e", "bluetooth", "micro-atx", "2x-m2-gen4"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-13400f.md"
specs:
  socket: "LGA1700"
  chipset: "Intel B760"
  form_factor: "Micro-ATX (244×244 mm)"
  memory:
    type: "DDR4"
    slots: 4
    max_capacity_gb: 128
    max_speed_mt: 5333
    dual_channel: true
  pcie_slots:
    primary_x16:
      version: "4.0"
      lanes: 16
      from: "CPU"
    secondary_x16:
      version: "3.0"
      lanes: 4
      from: "Chipset"
  m2_slots:
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "CPU"
      heatsink: "M.2 Shield Frozr"
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "Chipset"
      notes: "Оба слота Gen4. В отличие от DS3H где нижний Gen3."
  sata_ports: 4
  vrm:
    phases: "12+1 Duet Rail (6×2 Dr.MOS)"
    drmos: true
    heatsink: true
    notes: "Расширенный радиатор. Комфортно для i5-13400F (148W PL2)."
  rear_io:
    usb_3_2_gen2_type_c: 1
    usb_3_2_gen1: 3
    usb_2_0: 2
    hdmi: "2.1"
    displayport: "1.4"
    lan: "Realtek RTL8125BG (2.5GbE)"
    audio: "Realtek ALC897 (7.1)"
  internal_headers:
    usb_3_2_gen1: 1
    usb_2_0: 2
  wifi: "Wi-Fi 6E (Intel AX211)"
  bluetooth: "5.3"
  bios_flashback: true
  pcie_slot_reinforcement: true
physical_stereotypes:
  atx_form_factor: false
  itx_form_factor: false
  pcb_layers: 6
price_ru:
  min: 9000
  median: 10000
  max: 11000
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 150
  notes: "12+1 VRM — потолок i5-13600K (181W PL2). i7 — throttling."
engineering_notes:
  - "2× M.2 Gen4 (оба!) — ключевое преимущество над DS3H (1×Gen4 + 1×Gen3)."
  - "Wi-Fi 6E + BT 5.3 — эргономика dev-среды: меньше кабелей."
  - "BIOS Flashback — можно прошить без установленного CPU."
  - "12+1 VRM Duet Rail — запас для i5-13600K. i7 — throttling."
  - "M.2 Shield Frozr — радиатор на верхнем M.2 слоте."
verdict: "Лучшая B760 DDR4 для dev-сборки. Оба M.2 Gen4, Wi-Fi 6E, усиленный VRM. На 500-1000 ₽ дороже DS3H, но закрывает все аудиторские замечания."
---

# MSI PRO B760M-A WIFI DDR4

## Позиционирование

B760 плата с полноценными 2× M.2 Gen4 и Wi-Fi 6E. Закрывает оба критических замечания аудита RATIONAL-001: честные оба M.2 Gen4 + VRM с запасом.

## Ключевые особенности

- **Оба M.2 Gen4** — CPU + чипсет, без Gen3 компромиссов
- **Wi-Fi 6E + BT 5.3** — эргономика: меньше кабелей на столе
- **12+1 Duet Rail VRM** — запас для i5-13600K (181W PL2)
