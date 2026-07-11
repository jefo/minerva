---
id: "asrock-b760m-pro-rs"
type: "motherboard"
title: "ASRock B760M Pro RS (DDR5)"
vendor: "ASRock"
chipset: "B760"
socket: "LGA1700"
form_factor: "Micro-ATX"
memory_type: "DDR5"
status: "draft"
tags: ["lga1700", "b760", "ddr5", "pcie5", "micro-atx", "no-wifi", "dragon-lan"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-12400f.md"
specs:
  socket: "LGA1700"
  chipset: "Intel B760"
  form_factor: "Micro-ATX (244×244 mm)"
  memory:
    type: "DDR5"
    slots: 4
    max_capacity_gb: 192
    max_speed_mt: 7200
    dual_channel: true
  pcie_slots:
    primary_x16:
      version: "5.0"
      lanes: 16
      from: "CPU"
      notes: "PCIe 5.0 x16 — единственная в бюджетном сегменте. Родной интерфейс для RTX 5070."
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
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "Chipset"
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "Chipset"
      notes: "Третий M.2 — редкость в бюджетном сегменте"
  sata_ports: 4
  vrm:
    phases: "7+1+1"
    drmos: true
    heatsink: true
    notes: "Dr.MOS — как у D4-версии. Тянет i5-14600K."
  rear_io:
    usb_3_2_gen2_type_c: 1
    usb_3_2_gen1: 3
    usb_2_0: 2
    hdmi: "2.1"
    displayport: "1.4"
    lan: "Dragon RTL8125BG (2.5GbE)"
    audio: "Realtek ALC897 + Nahimic"
  internal_headers:
    usb_3_2_gen1: 1
    usb_2_0: 2
  wifi: false
  bluetooth: false
  bios_flashback: false
  pcie_slot_reinforcement: true
physical_stereotypes:
  atx_form_factor: false
  itx_form_factor: false
  pcb_layers: 6
price_ru:
  min: 11000
  median: 12500
  max: 14000
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 180
  notes: "PCIe 5.0 + 3× M.2 Gen4 + Dr.MOS — лучшая бюджетная B760."
engineering_notes:
  - "Единственная бюджетная B760 с PCIe 5.0 x16. DDR5-версия получила 5.0, DDR4 — 4.0."
  - "3× M.2 Gen4 — больше чем у многих Z790."
  - "Dr.MOS 7+1+1 — запас под апгрейд CPU."
  - "DDR5 обязателен — плата не поддерживает DDR4. +4K к бюджету за RAM."
verdict: "Если нужен PCIe 5.0 x16 'как родной' для RTX 5070 — это единственная бюджетная опция. Плата за DDR5: +3-4K против DDR4 сборки при нулевой разнице в FPS. Инженерно — избыточно, но эстетически — честно."
---

# ASRock B760M Pro RS (DDR5)

## Позиционирование

Та же плата что Pro RS/D4, но на DDR5 — и с PCIe 5.0 x16. Единственная в бюджетном сегменте с «родным» интерфейсом для RTX 5070.

## Ключевые особенности

- **PCIe 5.0 x16** — технически «родной» для RTX 5070. Разница с 4.0 — 0 FPS в играх
- **3× M.2 Gen4** — больше чем нужно для большинства сборок
- **DDR5** — обязателен, плата не поддерживает DDR4. Дороже на 3-4K против DDR4-сборки
