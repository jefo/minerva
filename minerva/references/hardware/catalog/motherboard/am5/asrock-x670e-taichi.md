---
id: "asrock-x670e-taichi"
type: "motherboard"
title: "ASRock X670E Taichi"
vendor: "asrock"
status: "draft"
tags: ["am5", "x670e", "e-atx", "ddr5", "pcie-5.0", "10gbe", "usb4", "thunderbolt4", "wifi-6e", "bluetooth-5.3", "flagship", "dpca-risk-wifi-bt", "dpca-risk-marvell-lan"]
last_updated: "2026-06-07"
links:
  platform: "catalog/cpu/amd-ryzen-9000.md"
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "../../concepts/pcie-lanes.md"
  concept_vrm: "../../concepts/vrm-phases.md"
  competitor: "catalog/motherboard/am5/asus-proart-x870e-creator.md"
specs:
  socket: "AM5"
  chipset: "X670E"
  form_factor: "E-ATX"
  vrm: "24+2+1 (105A SPS)"
  vrm_mosfet: "105A Smart Power Stage"
  real_vcore_phases: 24
  doublers: false
  max_ram: "4× DDR5 · до 256 ГБ · 7800+ МГц (OC)"
  ram_slots: 4
  pcie_slots: "2× PCIe 5.0 x16 (CPU, x16/x0 или x8/x8), 1× PCIe 4.0 x1"
  m2_slots: |
    M2_1: PCIe 5.0 x4 (CPU, 2280)
    M2_2: PCIe 4.0 x4 (CPU, 2280)
    M2_3: PCIe 4.0 x4 (Chipset, 2280)
    M2_4: PCIe 4.0 x4 (Chipset, 2280)
  sata_ports: 8
  lan: "10GbE (Marvell AQC113) + 2.5GbE (Killer E3100G)"
  wifi: true
  bluetooth: true
  wifi_chip: "Killer AX1675x WiFi 6E (отключаемый в BIOS)"
  bt_chip: "Bluetooth 5.3 (отключаемый в BIOS)"
  # Thunderbolt / USB4
  thunderbolt: "2× USB4 Type-C (40 Gbps, DP Alt Mode)"
  # 3D Envelope (v1.4 — keep-out zones)
  vrm_heatsink_height_max_mm: 42
  ram_slot_offset_x_mm: 55
  audio: "Realtek ALC4082 + ESS SABRE9218 DAC + WIMA Audio Caps"
  bios: "USB BIOS Flashback (обновление без CPU)"
  flashback: true
  usb_rear: "2× USB4 Type-C (40Gbps), 1× USB 3.2 Gen2x2 Type-C (20Gbps), 4× USB 3.2 Gen2 (10Gbps), 2× USB 3.2 Gen1 (5Gbps), 2× USB 2.0"
  video_outputs: "1× HDMI 2.1"
  fan_headers: "1× CPU_FAN, 1× CPU_OPT/Water Pump, 4× CHA_FAN"
  pcb_layers: 8
  pcie_5: "x16 (2 слота, x16/x0 или x8/x8)"
  bifurcation_risk: false
price_ru:
  min: 45000
  median: 50000
  max: 55680
  source: "price.ru / KNS (агрегация: KNS, 28bit, DNS, OZON)"
  date: "2026-06-07"
  availability: "EOL/снята с производства. Ограниченные остатки в рознице."
verdict: "Флагманский X670E от ASRock с инженерным VRM 24+2+1×105A, двумя портами USB4/Thunderbolt 4 и 10GbE Marvell. Идеальна для профессиональных DAW-станций с запасом по расширению и рабочим станциям с 10GbE-сетью. Требует отключения WiFi/BT в BIOS для DPC-безопасности. Главный риск — Marvell AQC113 может добавлять DPC-задержки (характерно для контроллеров Aquantia/Marvell)."

profiles:
  enthusiast_overclocking:
    capability_level: 3
    power_envelope: "high"
    steel_man_desc: "ASRock X670E Taichi — флагманская платформа AM5 с 24 реальными фазами Vcore на 105A SPS (без удвоителей). Суммарный ток до 2520A — абсолютный рекорд среди потребительских AM5-плат. 8-слойный PCB с низкими потерями, поддержка DDR5-7800+. Два слота PCIe 5.0 x16 с возможностью x8/x8. Идеально для экстремального разгона Ryzen 9 7950X/9950X под жидким азотом или кастомной СЖО."
    failure_mode_desc: "E-ATX форм-фактор не влезает в большинство стандартных корпусов Mid-Tower. 24 фазы × 105A — VRM никогда не будет узким местом, даже под LN2, но плата стоит соответственно. Для повседневного разгона (PBO +200 MHz) избыточна — X870 Steel Legend с 16 фазами справится за половину цены."
    optimal_for_intents: ["scientific_computing", "virtualization", "video_editing_8k", "data_engineering", "llm_training_lora"]
    failure_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz", "office_productivity", "sff_build"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  thunderbolt4_equipped:
    capability_level: 3
    power_envelope: "high"
    steel_man_desc: "Два порта USB4/Thunderbolt 4 (40 Gbps) с DP Alt Mode. Подключение профессиональных аудиоинтерфейсов (UAD Apollo TB, RME Fireface UFX+), TB-доков, 10GbE-адаптеров и NVMe-корпусов без занятия слотов PCIe. Критично для профессиональной DAW-станции с периферией по Thunderbolt."
    failure_mode_desc: "Thunderbolt-контроллер (Intel JHL8540) подключён через чипсет X670, а не напрямую к CPU — добавляет +3-5 мкс DPC latency при активном трафике TB-устройств. Для максимальной DPC-безопасности при неиспользовании TB — отключить контроллер в BIOS."
    optimal_for_intents: ["audio_production", "daw_workstation", "music_production", "video_editing_8k"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# ASRock X670E Taichi

## Позиционирование

ASRock X670E Taichi — флагманская материнская плата на чипсете AMD X670E для процессоров Ryzen 7000/9000 (AM5). Входит в топовую линейку Taichi от ASRock и выделяется **промышленным VRM (24+2+1×105A)**, двумя портами **USB4/Thunderbolt 4** и дуальной сетевой подсистемой: **10GbE (Marvell AQC113)** + **2.5GbE (Killer E3100G)**.

> **Ключевое отличие от X870-плат:** X670E использует два чипсета Promontory 21 (daisy-chain), что даёт больше линий PCIe для слотов расширения, но ценой чуть большей задержки DMI между чипсетами.

### Сравнение с ASUS ProArt X870E Creator

| Параметр | X670E Taichi | ProArt X870E Creator (ожид.) |
|---|---|---|
| VRM | 24+2+1 (105A) | 16+2+1 (80A) |
| Сеть | 10GbE + 2.5GbE | 10GbE + 2.5GbE |
| USB4/TB4 | 2 порта | 2 порта |
| M.2 | 4× (1× Gen5) | 4× (1× Gen5) |
| Чипсет | X670E (dual) | X870E (single?) |
| ECC | ✅ | ✅ |

X670E Taichi выигрывает по VRM (24×105A vs 16×80A) — критично для разгона Ryzen 9. ProArt Creator — потенциально лучший DPC-профиль (Marvell 10GbE vs Intel/Realtek).

## VRM: 24+2+1 фаз, 105A SPS — абсолютный флагман

| Параметр | Значение |
|---|---|
| Фазы Vcore | 24 (реальных, без удвоителей) |
| MOSFET | 105A Smart Power Stage |
| Суммарный ток (расчётный) | 24 × 105 = 2520A |
| Охлаждение | Массивные радиаторы с теплотрубками |
| PCB | 8 слоёв, low-loss материал |

VRM рассчитан на экстремальный разгон (LN2). Для повседневных сценариев — тройной запас даже под Ryzen 9 9950X с PBO. **24 реальные фазы без удвоителей** — это означает, что каждая фаза работает независимо, без деления ШИМ-сигнала, что даёт чистейшее напряжение с минимальными пульсациями.

## Сеть: 10GbE + 2.5GbE — профессиональный дуал

| Контроллер | Скорость | Чип | DPC-риск |
|---|---|---|---|
| **10GbE** | 10 Гбит/с | Marvell AQC113 | ⚠️ Средний (Aquantia-драйверы) |
| **2.5GbE** | 2.5 Гбит/с | Killer E3100G | Низкий |

**Marvell AQC113 (Aquantia):** 10GbE на борту без дополнительной карты. Пропускная способность ~1.25 ГБ/с — идеально для рабочих станций с сетевыми хранилищами (NAS, SAN), видеомонтажа 8K RAW по сети. **НО:** драйверы Aquantia/Marvell исторически имеют проблемы с DPC-задержками (спайки до 300-500 μs при активном трафике). Для чистой аудио-станции — либо использовать только 2.5GbE (Killer), либо отключить AQC113 в BIOS.

**Killer E3100G:** стандартный 2.5GbE-контроллер с приоритезацией трафика. Стабилен, DPC-нейтрален.

## USB4 / Thunderbolt 4: 2 порта

- 2× USB4 Type-C (40 Gbps каждый)
- DP Alt Mode (вывод видео через Type-C)
- Поддержка Thunderbolt 3/4 устройств
- Контроллер: Intel JHL8540 (через чипсет X670)

**Для аудио-станции:** прямое подключение UAD Apollo Twin X, RME Fireface UFX+ или других TB-аудиоинтерфейсов без переходников. TB-контроллер добавляет незначительную DPC-задержку (3-5 μs) — для максимальной безопасности отключается в BIOS.

## Слоты M.2 и PCIe

| Слот | Источник | Версия PCIe | Форм-факторы | Примечание |
|---|---|---|---|---|
| M2_1 (Blazing) | CPU | 5.0 x4 | 2280 | Основной Gen5 |
| M2_2 (Hyper) | CPU | 4.0 x4 | 2280 | Без конфликтов |
| M2_3 (Hyper) | Chipset | 4.0 x4 | 2280 | Без конфликтов |
| M2_4 (Hyper) | Chipset | 4.0 x4 | 2280 | Без конфликтов |
| PCIe_1 | CPU | 5.0 x16 | — | GPU |
| PCIe_2 | CPU | 5.0 x8 | — | x8 при занятом слоте |

**Без бифуркации:** при заполнении всех 4 M.2-слотов GPU остаётся на PCIe 5.0 x16. X670E (dual chipset) предоставляет достаточно линий.

**SATA:** 8 портов — рекордный показатель для AM5. Полезно для аудио-станций с большим количеством архивных HDD/SSD.

## Память DDR5

- 4 слота DIMM, до 256 ГБ
- Поддержка AMD EXPO и Intel XMP 3.0
- **DDR5-6000 — sweet spot** (MCLK:UCLK = 1:1 для Ryzen 7000/9000)
- DDR5-7800+ достижим при ручном разгоне на Hynix A-die
- 8-слойный PCB с улучшенной трассировкой под высокие частоты

## Аудио: Realtek ALC4082 + ESS SABRE9218 DAC

- **Кодек:** Realtek ALC4082 (USB-аудио, SNR 120 дБ)
- **DAC:** ESS SABRE9218 (отдельный ЦАП для фронтальных каналов)
- **Конденсаторы:** WIMA (аудиофильские, золотая серия)
- **Оптический выход (S/PDIF):** есть

Для аудио-станции встроенный аудиотракт отключается в BIOS — вывод через внешний USB/TB-интерфейс. ALC4082 + ESS 9218 достаточен для мониторинга и системных звуков, но не заменяет профессиональный аудиоинтерфейс.

## DPC Latency Profile (аудио-специфичный)

**Критически важно для DAW:** плата требует ручной настройки BIOS для минимизации DPC.

| Компонент | DPC-риск | Действие |
|---|---|---|
| **WiFi 6E** (Killer AX1675x) | ⚠️ Высокий | **Отключить в BIOS** |
| **Bluetooth 5.3** | ⚠️ Средний | **Отключить в BIOS** |
| **Marvell AQC113 10GbE** | ⚠️ Средний | Отключить в BIOS при неиспользовании |
| **Killer E3100G 2.5GbE** | ✅ Низкий | Оставить (стабилен) |
| **Intel JHL8540 TB4** | ✅ Низкий | Отключить при неиспользовании |
| **NVMe (CPU)** | ✅ Минимальный | Прямые линии CPU |
| **SATA (чипсет)** | ✅ Низкий | Стандартный AHCI |
| **USB (чипсет)** | ✅ Низкий | Стандартный xHCI |
| **Аудио ALC4082** | ✅ Низкий | Отключить в BIOS |

**Вывод:** после отключения WiFi, Bluetooth, 10GbE и TB4 в BIOS — плата становится DPC-безопасной на уровне B650 EAGLE (с учётом оставшегося Killer 2.5GbE). Однако Marvell AQC113 — известный источник DPC-спайков, и если 10GbE нужен (NAS/сеть), это **неустранимый риск** для real-time аудио.

### DPC-чеклист для аудио-станции

1. **BIOS:** отключить WiFi (Killer AX1675x)
2. **BIOS:** отключить Bluetooth
3. **BIOS:** отключить встроенный аудио (ALC4082)
4. **BIOS:** отключить Marvell AQC113 (если 10GbE не нужен)
5. **BIOS:** отключить Intel TB4 (если не используются TB-устройства)
6. **BIOS:** отключить LED-подсветку (устраняет PWM-шум подсветки)
7. **Windows:** использовать драйвер Killer E3100G без Killer Control Center (только драйвер)

## Российский рынок (июнь 2026)

**Диапазон: 45 000–55 680 ₽, медиана ~50 000 ₽.**

> ⚠️ Плата снята с производства (EOL). Доступны только остатки в рознице. При отсутствии в наличии — рассматривать X870E Taichi (10GbE Aquantia + WiFi 7) как прямую замену.

| Магазин | Цена | Наличие |
|---|---|---|
| KNS | 44 602–47 158 ₽ | Нет (EOL) |
| 28bit | 53 680 ₽ | Уточнять |
| DNS | ~55 000 ₽ | Уточнять |
| OZON | — | Нет в наличии |

**Альтернативы при отсутствии X670E Taichi:**
- **ASRock X870E Taichi** (~65 000 ₽) — 10GbE Aquantia + WiFi 7, актуальная модель
- **ASUS ProArt X870E Creator** (~60 000 ₽) — 10GbE Marvell + 2× TB4, лучший DPC-профиль (ожидается)
- **ASRock X870 Steel Legend** (~28 000 ₽) — 5GbE, без TB4, но доступна и дешевле в 2 раза

## Для кого

**Идеально:**
- Профессиональные DAW-станции с запасом по расширению (4× M.2, 8× SATA, 10GbE)
- Рабочие станции с 10GbE-сетью (видеомонтаж 8K RAW по сети, научные вычисления)
- Экстремальный разгон Ryzen 9 (24×105A — абсолютный запас по VRM)
- Сборки с Thunderbolt 4 периферией (UAD Apollo, RME Fireface, TB-доки)
- Системы с большим количеством накопителей (8 SATA + 4 M.2 = до 12 дисков)

**Не подходит:**
- Игровые ПК (избыточен: X870 Steel Legend справится за половину цены)
- Бюджетные аудио-станции (B650 EAGLE за 11 000 ₽ имеет лучший DPC-профиль)
- SFF-сборки (E-ATX — только полноразмерные корпуса)
- Сборки, где WiFi/BT нужны (для DPC-безопасности требуется отключение)
- Системы без 10GbE-сети (переплата за неиспользуемый Marvell AQC113)

**Пограничный случай — аудио-станция с 10GbE NAS:**
Если 10GbE необходим для работы с семплами/проектами на NAS — Marvell AQC113 остаётся включённым. Это создаёт риск DPC-спайков до 300-500 μs. Рекомендация: провести тест с LatencyMon в целевой конфигурации ДО покупки (если возможно), либо рассмотреть ASUS ProArt X870E Creator с альтернативным 10GbE-контроллером.
