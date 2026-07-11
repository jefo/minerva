---
id: "msi-pro-b860-p"
type: "motherboard"
title: "MSI PRO B860-P WIFI"
vendor: "MSI"
chipset: "B860"
socket: "LGA1851"
form_factor: "ATX"
memory_type: "DDR5"
status: "draft"
tags: ["lga1851", "b860", "ddr5", "pcie5", "wifi6e", "atx"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-ultra-5-225f.md"
specs:
  socket: "LGA1851"
  chipset: "Intel B860"
  form_factor: "ATX (305×244 mm)"
  memory:
    type: "DDR5"
    slots: 4
    max_capacity_gb: 256
    max_speed_mt: 7200
    dual_channel: true
  pcie_slots:
    primary_x16:
      version: "5.0"
      lanes: 16
      from: "CPU"
    secondary_x16:
      version: "4.0"
      lanes: 4
      from: "Chipset"
  m2_slots:
    - version: "5.0"
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
  sata_ports: 4
  vrm:
    phases: "12+1+1 Duet Rail"
    drmos: true
    heatsink: true
  rear_io:
    usb_3_2_gen2_type_c: 1
    usb_3_2_gen1: 4
    usb_2_0: 2
    hdmi: "2.1"
    displayport: "1.4"
    lan: "Realtek 2.5GbE"
    audio: "Realtek ALC897 (7.1)"
  wifi: "Wi-Fi 6E"
  bluetooth: "5.3"
  bios_flashback: true
physical_stereotypes:
  atx_form_factor: true
  itx_form_factor: false
  pcb_layers: 6
price_ru:
  min: 11000
  median: 12000
  max: 13500
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 250
engineering_notes:
  - "PCIe 5.0 x16 от CPU — родной интерфейс для RTX 5070. B860 не обрезает до 4.0."
  - "M.2 Gen5 x4 от CPU — будущее-proof для NVMe Gen5."
  - "3× M.2: один Gen5 + два Gen4. Для dev-сборки — запас."
  - "LGA1851 — минимум 2 поколения CPU. Не тупик как LGA1700."
verdict: "Бюджетный вход в LGA1851 с PCIe 5.0 x16. Для Ultra 5 225F с апгрейд-путём до старших Arrow Lake — идеально."
---

# MSI PRO B860-P WIFI

Бюджетная ATX плата на B860 для LGA1851. PCIe 5.0 x16, M.2 Gen5, Wi-Fi 6E, 3× M.2. Всё что нужно для старта на Arrow Lake с заделом на апгрейд.
