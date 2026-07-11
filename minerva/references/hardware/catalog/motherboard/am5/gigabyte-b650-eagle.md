---
id: "gigabyte-b650-eagle"
type: "motherboard"
title: "GIGABYTE B650 EAGLE"
vendor: "gigabyte"
status: "verified"
tags: ["am5", "b650", "atx", "ddr5", "no-wifi", "no-bluetooth", "audio-optimized", "realtek-lan", "3x-m2"]
last_updated: "2026-06-07"
links:
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  cpu_family: "catalog/cpu/amd-ryzen-9000.md"
  competitor_wifi: "catalog/motherboard/am5/asrock-b850-riptide.md"
specs:
  socket: "AM5"
  chipset: "B650"
  form_factor: "ATX"
  vrm: "12+2+2 (DrMOS)"
  vrm_mosfet: "DrMOS (50A per phase est.)"
  real_vcore_phases: 12
  doublers: false
  max_ram: "4× DDR5 · до 256 ГБ · 7600+ МГц (OC)"
  ram_slots: 4
  pcie_slots: "1× PCIe 4.0 x16 (CPU), 3× PCIe 3.0 x1 (chipset)"
  m2_slots: |
    M2_1: PCIe 5.0 x4 (CPU, 2280/2580/22110/25110)
    M2_2: PCIe 4.0 x2 (CPU, 2280/22110)
    M2_3: PCIe 4.0 x4 (Chipset, 2280/22110)
  sata_ports: 4
  lan: "Realtek RTL8111H 1GbE"
  wifi: false
  bluetooth: false
  m2_key_e_slot: false
  # 3D Envelope (v1.4 — keep-out zones)
  vrm_heatsink_height_max_mm: 38
  ram_slot_offset_x_mm: 50
  audio: "Realtek ALC897 (7.1 CH HD Audio)"
  bios: "Q-Flash Plus (обновление без CPU)"
  usb_rear: "2× USB 3.2 Gen2 (10Gbps), 2× USB 3.2 Gen1 (5Gbps), 6× USB 2.0"
  usb_rear_type_c: "1× USB 3.2 Gen2 (10Gbps)"
  video_outputs: "1× HDMI 2.1, 1× DisplayPort 1.4"
  fan_headers: "1× CPU_FAN, 1× CPU_OPT (помпа), 3× SYS_FAN"
  pcb_layers: 6
price_ru:
  min: 9101
  median: 11000
  max: 12000
  source: "price.ru (агрегация: Wildberries, torg-pc.ru, DNS)"
  date: "2026-06-07"
verdict: "Лучший выбор для аудио-станции на AM5 без WiFi/BT. 3× M.2, Realtek LAN (не Intel), полное отсутствие беспроводных чипов и M.2 Key E — нулевой DPC-риск от PCIe-перечисления WiFi/BT. Gigabyte — предпочтительный вендор для аудио (в отличие от MSI). Цена ~11 000 ₽ — на 45% ниже бюджетного лимита."

profiles:
  audio_workstation:
    capability_level: 3
    steel_man_desc: "Gigabyte B650 EAGLE — единственная AM5 плата с 3× M.2, где полностью отсутствует беспроводной модуль: нет WiFi-чипа, нет Bluetooth-контроллера, нет даже пустующего M.2 Key E слота (который мог бы вызывать DPC-задержки при PCIe-перечислении). Realtek RTL8111H 1GbE — стабильный контроллер без проблем Intel i225/i226 (разрывы, DPC-спайки). 12+2+2 фазы VRM достаточно для любого Ryzen 7/9 без разгона. Gigabyte исторически показывает лучшие DPC-профили среди вендоров среднего сегмента."
    optimal_for_intents: ["audio_production", "daw_workstation", "music_production"]
    failure_for_intents: ["wifi_dependent", "bluetooth_peripherals"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  dpc_safety:
    capability_level: 3
    steel_man_desc: "Нулевой DPC-риск от беспроводных интерфейсов: WiFi=false, Bluetooth=false, M.2 Key E=false. В отличие от ASRock B650 PG Lightning и ASRock B650 Pro RS, где пустой M.2 Key E слот всё равно присутствует на шине PCIe и может вызывать периодическое enumeration при загрузке/пробуждении. Realtek LAN не имеет известных проблем с DPC в отличие от Intel i225/i226."
    optimal_for_intents: ["audio_production", "low_latency_audio", "real_time_audio"]
    failure_mode_desc: "Единственный компромисс — 1GbE вместо 2.5GbE. Для аудио-станции скорости достаточно (стриминг 32ch/96kHz RAW ≈ 25 Mbps). M.2 слоты не конфликтуют с GPU (нет бифуркации как на B850)."
    failure_for_intents: []
    failure_severity: "NONE"
    failure_type: "NONE"
---

# GIGABYTE B650 EAGLE

## Позиционирование

GIGABYTE B650 EAGLE — ATX-плата на чипсете AMD B650 без каких-либо беспроводных интерфейсов. Позиционируется как доступная база для AM5-сборок, где WiFi и Bluetooth не нужны. **Идеальный кандидат для аудио-станций**, где любые PCIe-устройства с радиомодулями создают риск DPC-задержек (Deferred Procedure Call latency spikes).

## Ключевое отличие: полное отсутствие WiFi/BT

В отличие от большинства B650-плат, где даже в non-WiFi версиях сохранён пустой M.2 Key E слот (ASRock B650 PG Lightning, ASRock B650 Pro RS), B650 EAGLE **не имеет ни WiFi-чипа, ни M.2 Key E слота на плате**:

| Параметр | Gigabyte B650 EAGLE | ASRock B650 PG Lightning | ASRock B650 Pro RS |
|---|---|---|---|
| WiFi-чип | ❌ Нет | ❌ Нет | ❌ Нет |
| Bluetooth | ❌ Нет | ❌ Нет | ❌ Нет |
| M.2 Key E (пустой слот) | ❌ Нет | ⚠️ Есть (DPC-риск) | ⚠️ Есть (DPC-риск) |
| LAN | Realtek 1GbE | Realtek 2.5GbE | Realtek 2.5GbE |
| Цена | ~11 000 ₽ | ~13 900 ₽ (нет в наличии) | ~14 400 ₽ |

**Для аудио-станции критично:** пустой M.2 Key E слот — это PCIe endpoint, который BIOS/OS всё равно опрашивает при загрузке и пробуждении. Даже без установленного модуля он может вызывать DPC-спайки до 500+ μs — фатально для real-time audio.

## VRM: 12+2+2 фаз

| Параметр | Значение |
|---|---|
| Фазы Vcore | 12 (реальных, без удвоителей) |
| MOSFET | DrMOS |
| Охлаждение VRM | Радиатор на зоне VRM |
| Разъём питания CPU | 1× 8-pin EPS |

**Достаточно для любого Ryzen 7/9 на стоке.** Для 7950X (170W TDP) — с запасом при адекватном обдуве корпуса. Разгон не рекомендуется (ограничение чипсета B650, не платы).

## Слоты M.2: три без конфликтов

| Слот | Источник | Версия PCIe | Форм-факторы | Скорость |
|---|---|---|---|---|
| M2_1 (верхний) | CPU | 5.0 x4 | 2280/2580/22110/25110 | 128 Gb/s |
| M2_2 (средний) | CPU | 4.0 x2 | 2280/22110 | 32 Gb/s |
| M2_3 (нижний) | Chipset | 4.0 x4 | 2280/22110 | 64 Gb/s |

**Важно для аудио-станции:** M2_2 работает в режиме x2 (не x4), но для аудио-сборки это не проблема — OS/DAW диск в M2_1, семплы/проекты в M2_3. M2_2 можно использовать для менее требовательного SSD.

**Нет конфликта бифуркации с GPU** — в отличие от B850-плат, где задействование 2+ M.2 отбирает линии у PCIe x16.

## Память: 4 слота DDR5

- 4× DIMM, до 256 ГБ
- Поддержка AMD EXPO и Intel XMP 3.0
- **DDR5-6000 — sweet spot** (MCLK:UCLK = 1:1 для Ryzen 7000/9000)
- DDR5-7600+ достижим при ручном разгоне на Hynix A-die
- При заполнении 4 слотов — ограничение по частоте (DDR5-5200 JEDEC)

## Сеть: Realtek 1GbE (не Intel!)

- **Чип:** Realtek RTL8111H (1 Gbps)
- **Почему Realtek, а не Intel:** у Intel i225/i226 (2.5GbE) — известные проблемы с DPC-спайками до 1000+ μs и периодическими разрывами соединения. Realtek RTL8111H — старый, но стабильный контроллер без проблем в DPC Latency Monitor.
- **1GbE достаточно для аудио-станции:** стриминг 32 каналов 96kHz/24bit RAW + Dante = ~25 Mbps. Даже с запасом на сетевые ресурсы — утыкания в 1GbE не будет.

## Аудио: встроенный кодек и расширение

- **Встроенный:** Realtek ALC897 (7.1 CH HD Audio, SNR ~97 дБ)
- **Оптический выход (S/PDIF):** отсутствует
- **Для аудио-станции:** встроенный кодек не используется — вывод через внешний USB-аудиоинтерфейс (RME, Focusrite, UAD). ALC897 достаточен для системных звуков и мониторинга.

## BIOS / UEFI

- **Q-Flash Plus:** обновление BIOS с USB-флешки без процессора (кнопка на плате)
- Критично для запуска Ryzen 9000 на старых ревизиях платы
- UEFI с поддержкой Secure Boot (требуется для Windows 11)

## DPC Latency Profile (аудио-специфичный)

Оценка DPC-профиля (теоретическая, на основе компонентов):

| Компонент | DPC-риск | Примечание |
|---|---|---|
| WiFi/BT чип | **Нет** | Полностью отсутствует |
| M.2 Key E слот | **Нет** | Слот не распаян на плате |
| LAN (Realtek RTL8111H) | Минимальный | Нет известных DPC-спайков |
| NVMe (CPU) | Минимальный | Прямые линии CPU, без коммутации чипсета |
| SATA (чипсет) | Низкий | Стандартный AHCI-драйвер |
| USB (чипсет) | Низкий | Стандартный xHCI-драйвер |
| Аудио (ALC897) | Минимальный | При отключении в BIOS — ноль |

**Вывод:** плата имеет минимально возможное количество источников DPC-задержек среди всех AM5 ATX-плат. После отключения встроенного аудио в BIOS — единственный потенциальный источник DPC: сеть (Realtek, стабилен) и USB (стандартный стек Windows).

## Российский рынок (июнь 2026)

**Диапазон: 9 101–12 000 ₽, медиана ~11 000 ₽.**

| Магазин | Цена | Наличие |
|---|---|---|
| Wildberries | 9 101 ₽ | В наличии |
| torg-pc.ru | 11 101 ₽ | В наличии |
| DNS | ~12 000 ₽ | Уточнять |

**В рамках бюджета 20 000 ₽:** остаётся ~9 000 ₽ запаса на другие компоненты.

## Сравнение с кандидатами

### ASRock B650 PG Lightning (~13 900 ₽)

- **Плюс:** Realtek 2.5GbE (Dragon RTL8125BG)
- **Минус:** M.2 Key E слот на плате (DPC-риск), цена выше на 3 000 ₽, отсутствует в наличии
- **Вердикт:** Хуже для аудио из-за M.2 Key E слота

### ASRock B650 Pro RS (~14 400 ₽)

- **Плюс:** Realtek 2.5GbE, 3× M.2 (все x4)
- **Минус:** M.2 Key E слот, дороже на 3 500 ₽
- **Вердикт:** Хуже для аудио из-за M.2 Key E слота

### Gigabyte B650 EAGLE AX (~13 000 ₽)

- **Плюс:** WiFi 6E + BT 5.3 (для обычных сборок)
- **Минус:** WiFi/BT на борту — DPC-риск, цена выше
- **Вердикт:** Не подходит для аудио-станции (требование «БЕЗ WiFi/BT»)

## Для кого

**Идеально:**
- Аудио-станции / DAW-сборки (главный use-case)
- Сборки с external USB-аудиоинтерфейсом (RME, Focusrite, UAD, MOTU)
- Любые сборки, где WiFi/BT не нужны и критичен низкий DPC
- Конфигурации с 2-3 NVMe-накопителями
- Ryzen 7 7700X/9700X, Ryzen 9 7900/7950X на стоке

**Не подходит:**
- Сборки, где нужен WiFi/BT (выбрать AX-версию)
- Сборки с 4+ NVMe-накопителями
- Экстремальный разгон CPU (ограничение B650)
- Сборки с 2.5GbE как обязательным требованием
