---
id: "msi-pro-b760m-p-ddr4"
type: "motherboard"
title: "MSI PRO B760M-P DDR4"
vendor: "MSI"
chipset: "B760"
socket: "LGA1700"
form_factor: "Micro-ATX"
memory_type: "DDR4"
status: "draft"
tags: ["lga1700", "b760", "ddr4", "budget", "micro-atx", "no-wifi", "realtek-lan"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-12400f.md"
specs:
  socket: "LGA1700"
  chipset: "Intel B760"
  form_factor: "Micro-ATX (220×243 mm)"
  memory:
    type: "DDR4"
    slots: 2
    max_capacity_gb: 64
    max_speed_mt: 4800
    dual_channel: true
  pcie_slots:
    primary_x16:
      version: "4.0"
      lanes: 16
      from: "CPU"
    secondary_x1:
      version: "3.0"
      lanes: 1
      from: "Chipset"
  m2_slots:
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "CPU"
  sata_ports: 4
  vrm:
    phases: "6+1+1"
    drmos: false
    heatsink: true
    notes: "Радиатор есть. 6 фаз — достаточно для i5-12400F."
  rear_io:
    usb_3_2_gen1: 4
    usb_2_0: 2
    hdmi: "2.1"
    displayport: "1.4"
    lan: "Realtek RTL8111H (1GbE)"
    audio: "Realtek ALC897 (7.1)"
    ps2: true
  internal_headers:
    usb_3_2_gen1: 1
    usb_2_0: 2
  wifi: false
  bluetooth: false
  bios_flashback: false
  pcie_slot_reinforcement: false
physical_stereotypes:
  atx_form_factor: false
  itx_form_factor: false
  pcb_layers: 4
price_ru:
  min: 7500
  median: 8300
  max: 9000
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 150
  notes: "Бюджетная B760. 2 слота RAM — ограничение для апгрейда."
engineering_notes:
  - "Самая дешёвая B760 с радиатором VRM."
  - "1× M.2 Gen4 — компромисс. Лучше чем H610 Gen3, хуже чем DS3H 2×Gen4."
  - "2 слота DDR4 — нельзя докупить, только заменить."
  - "1GbE LAN — устаревший стандарт, но для игр достаточно."
verdict: "Компромиссная B760: дешевле DS3H, но 2 слота RAM и 1×M.2. Брать если уверен что 32GB хватит и второй диск не нужен."
---

# MSI PRO B760M-P DDR4

## Позиционирование

Бюджетная B760 от MSI. Радиатор VRM есть, но урезаны слоты RAM (2) и M.2 (1). Промежуточный вариант между H610 и полноценной B760.

## Ключевые ограничения

- **2 слота DDR4** — 32GB потолок без замены планок
- **1× M.2 Gen4** — только системный диск NVMe
- **1GbE LAN** — медленнее конкурентов
