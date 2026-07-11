---
id: "asrock-b760m-pro-rs-d4"
type: "motherboard"
title: "ASRock B760M Pro RS/D4"
vendor: "ASRock"
chipset: "B760"
socket: "LGA1700"
form_factor: "Micro-ATX"
memory_type: "DDR4"
status: "draft"
tags: ["lga1700", "b760", "ddr4", "budget", "micro-atx", "no-wifi", "dragon-lan"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-12400f.md"
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
      notes: "B760: PCIe 4.0. Разница с 5.0 — 0 FPS для RTX 5070."
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
  sata_ports: 4
  vrm:
    phases: "7+1+1"
    drmos: true
    heatsink: true
    notes: "Dr.MOS + радиатор. Комфортно для i5-14600K."
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
  min: 8500
  median: 9500
  max: 10500
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 180
  notes: "Dr.MOS VRM — тянет i5-14600K без undervolt."
engineering_notes:
  - "Dr.MOS 7+1+1 — лучший VRM в бюджетном сегменте B760 DDR4."
  - "2× M.2 Gen4. Один от CPU, один от чипсета."
  - "Dragon 2.5GbE — стабильнее бюджетных Realtek."
  - "Нет PCIe 5.0. B760 чипсетное ограничение."
verdict: "Лучшая B760 DDR4 по VRM. Dr.MOS + радиатор — запас под апгрейд CPU. Брать если планируешь позже перейти на i5-14600K."
---

# ASRock B760M Pro RS/D4

## Позиционирование

B760 плата с усиленным VRM (Dr.MOS) — лучшая в DDR4-сегменте. Отличие от Gigabyte DS3H: более качественная подсистема питания, Dragon LAN вместо Realtek, Nahimic аудио-эффекты.

## Ключевые особенности

- **Dr.MOS 7+1+1 VRM** — запас под i5-14600K
- **Dragon 2.5GbE** — игровой LAN-чип с приоритезацией трафика
- **PCIe с армированием** — против провисания тяжёлой GPU
