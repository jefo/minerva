---
id: "gigabyte-b760m-ds3h-ddr4"
type: "motherboard"
title: "Gigabyte B760M DS3H DDR4"
vendor: "Gigabyte"
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
  form_factor: "Micro-ATX (244×225 mm)"
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
      notes: "B760 чипсет: слот PCIe 4.0. Не поддерживает PCIe 5.0."
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
      notes: "Прямой CPU-линии M.2 Gen4 — без задержек чипсета"
    - version: "4.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "Chipset"
  sata_ports: 4
  vrm:
    phases: "6+2+1"
    drmos: false
    heatsink: true
    notes: "Радиатор на VRM. 117W PL2 i5-12400F — комфортно."
  rear_io:
    usb_3_2_gen2_type_c: 1
    usb_3_2_gen1: 3
    usb_2_0: 2
    hdmi: "2.1"
    displayport: "1.4"
    lan: "Realtek 2.5GbE"
    audio: "Realtek ALC897 (7.1)"
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
  sfx_form_factor_locked: false
  pcb_layers: 6
price_ru:
  min: 8000
  median: 9000
  max: 10000
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 150
  notes: "VRM с радиатором — уверенно держит i5-12400F и i5-14600K."
engineering_notes:
  - "B760 = обновлённый B660. Поддержка 14-го поколения из коробки."
  - "2× M.2 Gen4 — один от CPU (низкая latency), один от чипсета."
  - "4 слота DDR4 — можно стартовать с 2×8 и докупить до 32."
  - "Realtek 2.5GbE — лучше чем 1GbE на H610."
  - "Нет PCIe 5.0 — чипсетное ограничение. Для RTX 5070 разница 0 FPS."
verdict: "Золотая середина для DDR4-сборки. VRM с радиатором, 2× M.2 Gen4, 4 слота RAM. Всё что нужно для i5-12400F без компромиссов H610."
---

# Gigabyte B760M DS3H DDR4

## Позиционирование

Бюджетная B760 плата с радиатором VRM и 2× M.2 Gen4. Идеальный компаньон для i5-12400F: не переплачиваешь за Z790, получаешь всё необходимое.

## Ключевые особенности

- **VRM с радиатором** — держит i5-12400F без throttling в любом корпусе
- **2× M.2 Gen4** — системный + игровой/проектный диск
- **4 слота DDR4** — старт с 2×8, апгрейд до 32 без замены
- **2.5GbE LAN** — будущее-proof для домашней сети
