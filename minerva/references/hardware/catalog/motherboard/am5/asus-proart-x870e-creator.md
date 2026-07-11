---
id: "asus-proart-x870e-creator"
type: "motherboard"
title: "ASUS ProArt X870E-Creator WiFi"
vendor: "asus"
status: "draft"
tags: ["asus", "proart", "x870e", "am5", "thunderbolt", "creator", "tb4", "usb4", "dual-lan", "dpc-risk"]
last_updated: "2026-06-07"
links:
  platform_cpu: "catalog/cpu/amd-ryzen-9-9950x.md"
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  chipset_concept: "../../concepts/pcie-lanes.md"
  concept_vrm: "../../concepts/vrm-phases.md"
specs:
  socket: "AM5"
  chipset: "X870E"
  form_factor: "ATX"
  vrm: "18+2+2 (110A SPS)"
  memory: "4× DDR5, до 8000+ MT/s (EXPO)"
  pcie_slots: "1× PCIe 5.0 x16, 1× PCIe 4.0 x4 (chipset)"
  m2_slots: "4× M.2 (1× PCIe 5.0 x4 от CPU, 3× PCIe 4.0 x4 от чипсета)"
  sata_ports: 4
  lan: "Dual 5 GbE: Intel I226-V + Realtek RTL8126"
  wifi: "WiFi 7 (MediaTek MT7927) — **отключить для DPC-безопасности**"
  bluetooth: "5.4"
  usb4: "2 порта (USB4 40 Гбит/с, совместимы с TB4)"
  thunderbolt4: "2 порта (Intel JHL9040R контроллер)"
  audio: "Realtek ALC1220P (DAC: ESS SABRE 9118)"
  # 3D Envelope (keep-out zones)
  vrm_heatsink_height_max_mm: 38
  ram_slot_offset_x_mm: 52
  flashback: true
  bifurcation_risk: false
price_ru:
  low: 41490
  median: 55000
  high: 68332
  source: "price.ru"
  date: "2026-06-07"
  stores:
    - name: "Гипер Трейд"
      price: 41490
    - name: "Funny Play"
      price: 45639
    - name: "Регард"
      price: 48410
verdict: "Профессиональная creator-плата на X870E с Thunderbolt 4, USB4 и Dual 5GbE. 18+2+2 фазы 110A — запас для любого Ryzen 9. Четыре M.2 без отъёма линий GPU. Идеальна для DAW при отключении WiFi/BT (MediaTek MT7927 — источник DPC-задержек). Единственный недостаток — цена от 41 500 ₽."

profiles:
  creator_workstation:
    capability_level: 3
    steel_man_desc: "X870E с 18+2+2 фазами (110A SPS), Dual 5GbE, Thunderbolt 4/USB4 (2 порта Intel JHL9040R), 4× M.2. Профессиональный аудиокодек ALC1220P + ESS SABRE 9118 DAC. Создана для видеомонтажёров, 3D-художников и музыкантов."
    failure_mode_desc: "Избыточна для игровых сборок. WiFi-чип MediaTek MT7927 создаёт DPC-задержки (~500 мкс при включённом адаптере) — критично для DAW и real-time аудио. Цена значительно выше конкурентов без TB4."
    optimal_for_intents: ["video_editing_8k", "daw_zero_dpc_latency", "virtualization", "data_engineering", "scientific_computing", "llm_training_lora"]
    failure_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "daw_zero_dpc_latency"]
    failure_severity: "WARN"
    failure_type: "CONDITIONAL"
    failure_condition: "Для DAW — обязательно отключить WiFi/BT в BIOS и удалить драйвер MediaTek MT7927. После отключения плата пригодна для профессиональной аудиоработы."

  thunderbolt4_equipped:
    capability_level: 3
    steel_man_desc: "Два порта Thunderbolt 4 (Intel JHL9040R) + два порта USB4 (40 Гбит/с) на задней панели. Полноценная поддержка TB4-доков, внешних NVMe-массивов и аудиоинтерфейсов UAD Apollo."
    failure_mode_desc: "Не все USB4-устройства корректно работают через чипсет X870E — проверять совместимость с конкретным TB-оборудованием."
    optimal_for_intents: ["daw_zero_dpc_latency", "video_editing_8k"]
    failure_for_intents: []
---

# ASUS ProArt X870E-Creator WiFi

## Позиционирование

ASUS ProArt X870E-Creator — профессиональная плата для создателей контента на чипсете X870E (двойной Promontory 21). В отличие от игровых линеек ROG/Strix, ProArt ориентирована на монтажёров, 3D-художников и музыкантов: Thunderbolt 4, Dual 5GbE, аппаратный мониторинг и минималистичный дизайн.

## Ключевые особенности

- **Thunderbolt 4 / USB4**: 2 порта TB4 (Intel JHL9040R) + 2 порта USB4 40 Гбит/с — прямое подключение профессиональных аудиоинтерфейсов (UAD Apollo, RME), TB-доков, внешних NVMe-массивов.
- **Dual 5 GbE**: Intel I226-V (2.5GbE) + Realtek RTL8126 (5GbE) — два независимых сетевых порта, агрегация каналов, прямое подключение к NAS по выделенной линии.
- **VRM 18+2+2 (110A)**: 18 фаз на Vcore по 110A Smart Power Stage — суммарно 1980A. Запас даже для будущих 16-ядерных Ryzen под экстремальным разгоном.

## DPC-анализ: WiFi/BT — критическая проблема для DAW

**Главная слабость платы для аудиоработы — чип MediaTek MT7927 (WiFi 7 + BT 5.4).**

| Параметр | Состояние WiFi/BT | DPC Latency (LatencyMon) |
|---|---|---|
| WiFi + BT включены | ВКЛ | ~400–800 мкс (пики до 1200 мкс) |
| WiFi/BT отключены в BIOS | ВЫКЛ | ~20–50 мкс |

MediaTek MT7927 известен высокими DPC-задержками из-за драйвера `mtkwl6ex.sys`. Для профессиональной аудиоработы с низкой задержкой (буфер 32–64 сэмпла на частоте 96 кГц) это неприемлемо.

**Решение:**
1. Отключить WiFi и Bluetooth в BIOS (Advanced → Onboard Devices → WiFi/BT Controller = Disabled)
2. Удалить драйвер MediaTek из Windows (Device Manager → удалить устройство с галочкой «удалить драйвер»)
3. Использовать проводное подключение (Dual 5GbE) или отдельный USB/WiFi-адаптер на чипе Intel/Qualcomm

> ⚠️ **Важно**: после отключения WiFi/BT плата пригодна для профессиональной аудиоработы и получает профиль `daw_zero_dpc_latency`.

## VRM: 18+2+2 фазы, 110A SPS

| Параметр | Значение |
|---|---|
| Фазы Vcore | 18 |
| Фазы SOC | 2 |
| Фазы MISC | 2 |
| MOSFET | 110A Smart Power Stage (Vishay SIC850) |
| ШИМ-контроллер | Infineon XDPE192C3B |
| Суммарный ток (расчётный) | 18 × 110 = 1980A |

VRM с колоссальным запасом. Даже Ryzen 9 9950X под PBO (~250 Вт) использует лишь ~13% возможностей подсистемы питания. Радиаторы с теплотрубкой обеспечивают температуру VRM не выше 55°C под полной нагрузкой.

## Слоты: PCIe и M.2

| Слот | Источник | Версия PCIe | Примечание |
|---|---|---|---|
| PCIe_x16_1 | CPU | 5.0 x16 | Всегда x16, не делится |
| PCIe_x4_2 | Chipset | 4.0 x4 | Нижний слот |
| M2_1 (верхний) | CPU | 5.0 x4 | Под радиатором |
| M2_2 | Chipset | 4.0 x4 | Без конфликтов |
| M2_3 | Chipset | 4.0 x4 | Без конфликтов |
| M2_4 | Chipset | 4.0 x4 | Без конфликтов |

X870E (двойной чипсет) предоставляет достаточно линий, чтобы все 4 M.2 работали одновременно без отъёма линий у GPU. GPU всегда на PCIe 5.0 x16.

## Thunderbolt 4 / USB4

| Порт | Контроллер | Скорость | DP Alt Mode |
|---|---|---|---|
| TB4 Port 1 | Intel JHL9040R | 40 Гбит/с | Да (DP 1.4 через iGPU) |
| TB4 Port 2 | Intel JHL9040R | 40 Гбит/с | Да |
| USB4 Port 1 | Чипсет X870E | 40 Гбит/с | Нет |
| USB4 Port 2 | Чипсет X870E | 40 Гбит/с | Нет |

Два полноценных порта TB4 с поддержкой Power Delivery (15 Вт на порт) и DisplayPort Alt Mode через встроенную графику Ryzen. Идеально для подключения UAD Apollo Twin X, внешних мониторов и TB-доков.

## Сеть и аудио

- **LAN 1**: Intel I226-V 2.5GbE — стабильный, низкие DPC-задержки. Рекомендуется для основного подключения.
- **LAN 2**: Realtek RTL8126 5GbE — пропускная способность до 625 МБ/с. Для NAS, сетевых хранилищ, изолированных сетей.
- **WiFi**: 7 (802.11be, MediaTek MT7927) — **отключить для DAW**. В обычных сценариях до 5.8 Гбит/с.
- **Аудио**: Realtek ALC1220P (SNR 120 дБ playback, 110 дБ recording) + ESS SABRE 9118 DAC — флагманский интегрированный аудиокодек. Дискретная звуковая карта нужна только для студийной работы высокого класса.

## Память DDR5

- 4 слота DIMM, до 256 ГБ
- Поддержка AMD EXPO и Intel XMP 3.0
- DDR5-6000 — sweet spot (MCLK:UCLK = 1:1)
- DDR5-8000+ на Hynix A-die/M-die при ручном разгоне
- 8-слойный PCB с улучшенной трассировкой

## Сравнение с ASRock X870E Taichi

| Параметр | ProArt X870E-Creator | X870E Taichi |
|---|---|---|
| VRM | 18+2+2 (110A) | 24+2+1 (110A) |
| TB4/USB4 | 2× TB4 + 2× USB4 | 2× USB4 (не TB4) |
| LAN | Dual 5GbE (Intel+Realtek) | 5GbE + 2.5GbE |
| WiFi | MediaTek MT7927 | MediaTek MT7927 |
| Аудио | ALC1220P + ESS 9118 | ALC4082 + ESS 9219 |
| M.2 | 4× (1× Gen5) | 4× (1× Gen5) |
| Цена | ~55 000 ₽ | ~60 000+ ₽ |

ProArt выигрывает по наличию полноценных TB4-портов (Intel-контроллер) и профессиональному аудиокодеку. Taichi выигрывает по числу фаз VRM (избыточно в обоих случаях).

## Цены (price.ru, июнь 2026)

| Магазин | Цена |
|---|---|
| Гипер Трейд | 41 490 ₽ |
| Funny Play | 45 639 ₽ |
| Регард | 48 410 ₽ |
| **Диапазон** | **41 490 – 68 332 ₽** |
| **Медиана** | **~55 000 ₽** |

## Для кого

**Идеальна:**
- DAW-сборки с внешними Thunderbolt-интерфейсами (UAD Apollo, RME Fireface, Apogee) — после отключения WiFi/BT
- Видеомонтаж 4K/8K с сетевым хранилищем (Dual 5GbE → агрегация каналов)
- 3D-художники и архитекторы (GPU всегда x16 + 4 NVMe под ассеты)
- Рабочие станции с несколькими NVMe-накопителями без компромиссов

**Не подходит:**
- Игровые ПК (переплата за TB4 и Dual LAN)
- DAW «из коробки» без ручной настройки (WiFi/BT — источник DPC-задержек)
- Бюджетные сборки (дешевле взять X870 Steel Legend за 28 000 ₽)
