---
id: "gigabyte-b650m-s2h"
type: "motherboard"
title: "GIGABYTE B650M S2H"
vendor: "gigabyte"
status: "verified"
tags: ["am5", "b650", "ddr5", "matx", "budget", "no-wifi"]
last_updated: "2026-06-03"
links:
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  cpu_recommended: "catalog/cpu/amd-ryzen-5-7500f.md"
  cpu_family: "catalog/cpu/amd-ryzen-7000.md"
  chipset_compare: "catalog/motherboard/am5/msi-b650-tomahawk.md"
specs:
  socket: "AM5"
  chipset: "B650"
  form_factor: "mATX"
  vrm: "6+2+1 Phases (без удвоителей)"
  vrm_mosfet: "50A DrMOS (Vishay SiC651A)"
  real_vcore_phases: 6
  doublers: false
  max_ram: "2× DDR5 · до 96 ГБ · 6400+ МГц (OC)"
  ram_slots: 2
  pcie_slots: "1× PCIe 4.0 x16 (CPU), 1× PCIe 3.0 x1 (chipset)"
  m2_slots: "1× M.2 PCIe 5.0 x4 (CPU)"
  sata_ports: 4
  lan: "1G Realtek RTL8111H"
  # 3D Envelope (v1.4 — keep-out zones)
  vrm_heatsink_height_max_mm: 35
  ram_slot_offset_x_mm: 50
  wifi: null
  bluetooth: null
  audio: "Realtek ALC897 (старый бюджетный кодек)"
  bios: "Q-Flash Plus (обновление без CPU)"
  usb_rear: "4× USB 3.2 Gen1 (5Gbps), 4× USB 2.0"
  video_outputs: "1× HDMI 2.1, 1× DP 1.4"
  fan_headers: "1× CPU_FAN, 2× SYS_FAN"
price_ru:
  min: 6652
  median: 7800
  max: 8520
  source: "price.ru"
  date: "2026-06-03"
verdict: "Бюджетный вход в AM5. Достаточна для Ryzen 5 7500F/7600. Всего 2 слота RAM — не для 4-канальных конфигураций. Не для Ryzen 9."

profiles:
  budget_platform:
    capability_level: 1
    capability_level: 1
    steel_man_desc: "B650M с 6+2+1 фазами (50A DrMOS) — минимальный достаточный вход в AM5. 2 слота DDR5 без penalty по частоте (daisy chain на 2 слота стабильнее 4). Q-Flash Plus позволяет обновить BIOS без CPU."
    failure_mode_desc: "Всего 2 слота DDR5 — невозможен апгрейд памяти добавлением планок, только полная замена. 1× M.2 слот — недостаточен для сборок с разделением ОС/данные. ALC897 — устаревший аудиокодек без оптического выхода."
    optimal_for_intents: ["aaa_1080p_ultra", "office_productivity", "home_server_24_7"]
    failure_for_intents: ["video_editing_4k", "data_engineering", "virtualization"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# GIGABYTE B650M S2H

## Позиционирование

B650M S2H — самый доступный вход в платформу AM5 от Gigabyte. Микро-ATX плата с минимальным, но достаточным для бюджетных сборок набором функций. Главный компромисс — **всего 2 слота DDR5** (большинство B650-плат имеют 4).

## VRM: 6+2+1 фаз, 50A DrMOS

| Параметр | Значение |
|---|---|
| Фазы Vcore | 6 (реальных, без удвоителей) |
| MOSFET | Vishay SiC651A (50A DrMOS) |
| PWM-контроллер | Richtek RT3678BE |
| Суммарный ток (расчётный) | 6 × 50 = 300A |
| Охлаждение VRM | Скромный радиатор без теплотрубки |

**Для Ryzen 5 7500F/7600 (65W) — с огромным запасом.** Для Ryzen 7 7700X (105W) — достаточно, но без разгона. Для Ryzen 9 7900X/7950X — **не рекомендуется**: VRM будет работать на пределе, возможен троттлинг при длительной нагрузке.

## Слоты: минимализм

| Слот | Источник | Линий | Версия PCIe |
|---|---|---|---|
| PCIe_x16 | CPU | 16 | 4.0 |
| M.2 (единственный) | CPU | 4 | **5.0** |
| PCIe_x1 | Chipset | 1 | 3.0 |

**Всего 1 слот M.2** — это главное ограничение. Если в будущем понадобится второй NVMe-накопитель — только через PCIe-адаптер в слот x1 (медленно) или замена единственного SSD на более ёмкий.

## Память: 2 слота — нюанс

В отличие от большинства B650-плат, здесь **только 2 слота DIMM**. Это означает:

- **Плюс:** лучший разгон памяти (2-слотовые платы стабильнее на высоких частотах)
- **Минус:** нельзя докупить ещё 2 планки позже — только замена комплекта
- **Максимум:** 96 ГБ (2× 48 ГБ)

Для бюджетной сборки с 32GB (2×16) — не проблема. Если в перспективе нужно 64GB — берите сразу комплект 2×32.

## Сеть и аудио — бюджетный минимум

- **LAN:** 1G Realtek RTL8111H — старый контроллер, но надёжный
- **Wi-Fi:** нет (можно добавить карту в слот PCIe x1)
- **Аудио:** Realtek ALC897 — бюджетный кодек, SNR 97 дБ. Для игр и музыки в наушниках до 5 000 ₽ — достаточно. Для серьёзного аудио — дискретная звуковая карта.

## BIOS: Q-Flash Plus

Несмотря на бюджетность, плата имеет **Q-Flash Plus** — обновление BIOS без процессора. Критично важно, поскольку B650-платы могут поставляться с BIOS, не поддерживающим Ryzen 9000 (Granite Ridge). Обновление через USB-флешку и кнопку на плате решает проблему.

## Российский рынок (июнь 2026)

**Диапазон: 6 652–8 520 ₽, медиана ~7 800 ₽.**

Прямые конкуренты:
- ASRock B650M-HDV/M.2 — 7 500–9 000 ₽ (2 RAM-слота, но есть радиатор M.2)
- MSI PRO B650M-P — 8 000–9 500 ₽ (4 RAM-слота, слабее VRM)

## Для кого

**Идеальна:**
- Бюджетные сборки с Ryzen 5 7500F/7600/7600X
- mATX-корпуса (Zalman i3, Deepcool MATREXX 30)
- Сборки где не планируется более 1 NVMe-накопителя
- Системы с одним комплектом RAM 2×16/2×32 ГБ

**Не подходит:**
- Ryzen 9 (VRM не справится)
- Сборки с 2+ NVMe-накопителями
- 4-канальные конфигурации памяти
- Системы без дискретной GPU (CPU с iGPU нужен, но есть видеовыходы на плате)
- Аудиофилы (ALC897 — слабый кодек)
