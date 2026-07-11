---
id: "asrock-h610m-hdv-m2"
type: "motherboard"
title: "ASRock H610M-HDV/M.2"
vendor: "ASRock"
chipset: "H610"
socket: "LGA1700"
form_factor: "Micro-ATX"
memory_type: "DDR4"
status: "draft"
tags: ["lga1700", "h610", "ddr4", "budget", "micro-atx", "no-wifi", "realtek-lan"]
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-12400f.md"
specs:
  socket: "LGA1700"
  chipset: "Intel H610"
  form_factor: "Micro-ATX (226×188 mm)"
  memory:
    type: "DDR4"
    slots: 2
    max_capacity_gb: 64
    max_speed_mt: 3200
    dual_channel: true
  pcie_slots:
    primary_x16:
      version: "4.0"
      lanes: 16
      from: "CPU"
      notes: "H610 ограничивает слот до PCIe 4.0 даже при CPU с PCIe 5.0"
    secondary_x1:
      version: "3.0"
      lanes: 1
      from: "Chipset"
  m2_slots:
    - version: "3.0"
      lanes: 4
      type: "NVMe"
      max_length: "2280"
      from: "Chipset"
      notes: "Единственный M.2. Gen3 — узкое место для NVMe Gen4 дисков."
  sata_ports: 4
  vrm:
    phases: "5+1+1"
    drmos: false
    heatsink: false
    notes: "Без радиатора. Достаточно для i3/i5 non-K. 117W PL2 i5-12400F — на пределе без обдува."
  rear_io:
    usb_3_2_gen1: 4
    usb_2_0: 2
    hdmi: "1.4"
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
  sfx_form_factor_locked: false
  pcb_layers: 4
price_ru:
  min: 5200
  median: 6000
  max: 7000
  source: "price.ru / DNS"
  date: "2026-07-06"
  status: "verified"
platform_req:
  cpu_tdp_max_w: 125
  notes: "VRM без радиатора — не рекомендуется для i7/i9 K-серии."
engineering_notes:
  - "H610 чипсет обрезает PCIe CPU-линии до 4.0 — даже с CPU, поддерживающим 5.0."
  - "1×M.2 Gen3 — узкое место для NVMe Gen4. Разница в играх незаметна."
  - "2 слота DDR4 — апгрейд RAM требует замены планок, а не добавления."
  - "VRM без радиатора: i5-12400F 117W PL2 вывезет при хорошем airflow корпуса. Без airflow — throttling."
verdict: "Абсолютный минимум для i5-12400F. VRM без радиатора — риск троттлинга в плохо вентилируемом корпусе. Брать только если каждый рубль на счету."
---

# ASRock H610M-HDV/M.2

## Позиционирование

Самая дешёвая плата на LGA1700, которая ещё имеет M.2 слот. H610 — младший чипсет: PCIe 4.0 (не 5.0), 1× M.2 Gen3, 2 слота DDR4. Минимально достаточная обвязка для i3/i5 non-K.

## Ключевые ограничения

- **PCIe 4.0 x16** — RTX 5070 работает без потери FPS, но технически не «родной» PCIe 5.0
- **1× M.2 Gen3** — один NVMe, скорость до 3500 MB/s
- **VRM без радиатора** — нужен airflow от корпусных вентиляторов
- **2 слота RAM** — максимум 64GB, без возможности докупить
