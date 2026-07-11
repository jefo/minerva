---
id: "asrock-z890-pro-rs"
type: "motherboard"
title: "ASRock Z890 Pro RS"
vendor: "asrock"
status: "draft"
tags: ["lga1851", "z890", "atx", "ddr5", "pcie-5.0", "wifi-6e", "mid-range", "arrow-lake"]
last_updated: "2026-06-03"
links:
  platform: "catalog/cpu/intel-core-ultra-200.md"
  socket: "catalog/motherboard/lga1851/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "../../concepts/pcie-lanes.md"
  concept_vrm: "../../concepts/vrm-phases.md"
specs:
  socket: "LGA1851"
  chipset: "Z890"
  form_factor: "ATX"
  vrm: "16+1+1 (DrMOS)"
  memory: "4× DDR5, до 8667+ MT/s"
  pcie_slots: "1× PCIe 5.0 x16, 1× PCIe 4.0 x4"
  m2_slots: "1× PCIe 5.0 x4, 3× PCIe 4.0 x4"
  sata_ports: 4
  network: "Realtek 2.5GbE, Wi-Fi 6E"
  audio: "Realtek ALC897"
  flashback: true
  bifurcation_risk: false
price_ru:
  median: 22000
  source: "price.ru (оценка)"
  date: "2026-06-03"
verdict: "Вход в LGA1851 на Z890. 16+1+1 DrMOS, 4 M.2 без отъёма линий у GPU. Хороший баланс цены и возможностей для Arrow Lake. Главный компромисс: бюджетный аудиокодек ALC897."

profiles:
  mainstream_platform:
    capability_level: 2
    capability_level: 2
    steel_man_desc: "Z890 с 16+1+1 фазами — достаточный VRM для любого Arrow Lake на стоке. 4× M.2 (1× Gen5), Wi-Fi 6E, BIOS Flashback. Хороший баланс цены и возможностей."
    failure_mode_desc: "ALC897 аудиокодек — экономия на звуке. Realtek 2.5GbE вместо Intel — выше загрузка CPU при сетевых операциях. Нет Thunderbolt 4 на плате."
    optimal_for_intents: ["aaa_1440p_high", "software_development", "streaming", "video_editing_4k"]
    failure_for_intents: ["video_editing_8k"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# ASRock Z890 Pro RS

## Позиционирование

ASRock Z890 Pro RS — среднебюджетная плата на чипсете Z890 для процессоров Intel Core Ultra 200 (Arrow Lake, сокет LGA1851). В линейке ASRock это «рабочая лошадка»: достаточно VRM для любого Arrow Lake на стоке, 4 M.2-слота без конфликтов с GPU, но с экономией на аудиокодеке.

## LGA1851: новый сокет Intel

LGA1851 пришёл на смену LGA1700 вместе с процессорами Arrow Lake (Core Ultra 200). Ключевые отличия:

- **Больше контактов**: 1851 против 1700 — задел на будущие поколения
- **PCIe 5.0**: нативное у CPU (20 линий: x16 GPU + x4 M.2)
- **DDR5-only**: поддержка DDR4 отсутствует
- **Чипсет Z890**: до 24 линий PCIe 4.0, до 8 SATA, Wi-Fi 7 опционально

> LGA1851 — новый долгоживущий сокет (как минимум 2 поколения CPU).

## VRM: 16+1+1 фаз, DrMOS

| Параметр | Значение |
|---|---|
| Фазы | 16+1+1 |
| MOSFET | DrMOS (интегрированный драйвер + MOSFET) |
| Охлаждение | Радиаторы на VRM-зоне |

Производитель не раскрывает точную модель DrMOS и силу тока, но 16 фаз на Vcore с запасом хватает для Core Ultra 9 285K (125W база / 250W turbo). Разгон CPU ограничен не VRM, а тепловым пакетом Arrow Lake.

## Слоты: без компромиссов по линиям

| Слот | Источник | Версия PCIe | Примечание |
|---|---|---|---|
| PCIe_x16 | CPU | 5.0 x16 | Всегда x16 |
| PCIe_x4 | Chipset | 4.0 x4 | Открытый слот |
| M2_1 (верхний) | CPU | 5.0 x4 | Без конфликтов |
| M2_2 | Chipset | 4.0 x4 | Без влияния на GPU |
| M2_3 | Chipset | 4.0 x4 | Без влияния на GPU |
| M2_4 | Chipset | 4.0 x4 | Без влияния на GPU |

В отличие от B850 на AMD, Z890 не имеет проблемы бифуркации линий CPU. Все 4 M.2 можно заполнить одновременно, и GPU останется на PCIe 5.0 x16.

## Память DDR5

- 4 слота DIMM, до 256 ГБ
- Поддержка XMP 3.0
- Базово до 8667+ MT/s (зависит от IMC процессора)
- **DDR5-6400 — sweet spot** для Arrow Lake (Gear 2)

## Сеть и аудио

- **LAN**: Realtek 2.5GbE — стандартный контроллер среднего сегмента
- **Wi-Fi**: 6E (6 ГГц, 2×2 MIMO)
- **Аудио**: Realtek ALC897 — бюджетный кодек (SNR ~97 дБ). Главный компромисс платы. Для качественного аудио — дискретная звуковая карта или внешний USB-ЦАП.

## BIOS: USB BIOS Flashback

Обновление BIOS без процессора через USB-флешку — критично для будущих поколений CPU на LGA1851.

## Сравнение с аналогами

| Параметр | Z890 Pro RS | MSI Z890 Tomahawk (ожид.) | Gigabyte Z890 Aorus Elite (ожид.) |
|---|---|---|---|
| VRM | 16+1+1 DrMOS | 16+1+1+1 (90A) | 16+1+2 (80A) |
| M.2 Gen5 | 1× | 1× | 1× |
| M.2 Gen4 | 3× | 4× | 3× |
| LAN | 2.5GbE | 5GbE | 2.5GbE |
| Wi-Fi | 6E | 7 | 7 |
| Аудио | ALC897 | ALC4080 | ALC1220 |
| Цена (оценка) | ~22 000 ₽ | ~30 000 ₽ | ~28 000 ₽ |

Z890 Pro RS выигрывает по цене, но проигрывает по аудиокодеку и беспроводной сети.

## Для кого

**Подходит:**
- Сборки на Core Ultra 5 245K / Ultra 7 265K
- Системы с 2+ NVMe-накопителями без потери линий GPU
- Игровые ПК (GPU всегда на x16)
- Первый вход в LGA1851 с прицелом на будущий апгрейд CPU

**Не подходит:**
- Аудиофилы (ALC897 — нужен внешний ЦАП)
- Экстремальный разгон CPU (нужен Z890 Apex/Taichi)
- Сборки с 5GbE-сетью (только 2.5GbE)
- Бюджетные сборки на Core Ultra 3 (лучше подождать B860)
