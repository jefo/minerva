---
id: "asrock-b850-riptide"
type: "motherboard"
title: "ASRock B850 Riptide"
vendor: "asrock"
status: "draft"
tags: ["am5", "b850", "atx", "ddr5", "pcie-5.0", "wifi-6e", "mid-range"]
last_updated: "2026-06-03"
links:
  platform: "catalog/cpu/amd-ryzen-9000.md"
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "../../concepts/pcie-lanes.md"
  concept_vrm: "../../concepts/vrm-phases.md"
specs:
  socket: "AM5"
  chipset: "B850"
  form_factor: "ATX"
  vrm: "14+2+1 (80A SPS)"
  memory: "4× DDR5, до 8000+ MT/s"
  pcie_slots: "1× PCIe 5.0 x16, 1× PCIe 4.0 x4"
  m2_slots: "1× PCIe 5.0 x4, 2× PCIe 4.0 x4"
  sata_ports: 4
  network: "Realtek RTL8125BG 2.5GbE, Wi-Fi 6E"
  # 3D Envelope (v1.4 — keep-out zones)
  vrm_heatsink_height_max_mm: 44
  ram_slot_offset_x_mm: 55
  audio: "Realtek ALC897"
  flashback: true
  bifurcation_risk: true
price_ru:
  median: 18000
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  bifurcation_shared_lanes:
    steel_man_desc: "B850 Riptide предлагает PCIe 5.0 x16 для GPU и три M.2-слота (1× Gen5 + 2× Gen4). При использовании только M2_1 (Gen5) конфликтов нет — GPU получает полные 16 линий."
    capability_level: 2
    failure_mode_desc: "При задействовании M2_2 или M2_3 линии могут отбираться у основного PCIe-слота через бифуркацию. Это типично для B850: чипсет имеет ограниченное количество линий, и вендор вынужден делить линии CPU между GPU и дополнительными M.2."
    optimal_for_intents: ["video_editing_4k", "data_engineering", "virtualization"]
    failure_for_intents: ["llm_inference_13b", "llm_inference_20b", "llm_training_lora"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
verdict: "Обновлённый средний сегмент AM5. 14+2+1 фаз на 80A SPS — с запасом для Ryzen 7 и Ryzen 9. Главный компромисс: PCIe-бифуркация при использовании 2+ M.2. Wi-Fi 6E и 2.5GbE — стандарт для 2025–2026."
---

# ASRock B850 Riptide

## Позиционирование

ASRock B850 Riptide — обновлённая среднебюджетная плата на чипсете B850 для AM5. Замена B650 Riptide с улучшенной поддержкой DDR5 (8000+ MT/s) и сохранением силовой части 14+2+1 на 80A SPS. Нацелена на сборки с Ryzen 7 и Ryzen 9, где не требуется более 1-2 NVMe-накопителей.

## VRM: 14+2+1 фаз, 80A SPS

| Параметр | Значение |
|---|---|
| Фазы | 14+2+1 |
| MOSFET | 80A Smart Power Stage |
| Суммарный ток (расчётный) | 14 × 80 = 1120A |
| Охлаждение | Радиаторы на VRM-зоне |

**Запаса хватает для любого Ryzen 9 на стоке.** Даже 7950X (170W TDP) не упрётся в лимит VRM при адекватном обдуве.

## Слоты и конфликты

| Слот | Источник | Версия PCIe | Примечание |
|---|---|---|---|
| PCIe_x16_1 | CPU | 5.0 x16 | Может снизиться до x8 |
| PCIe_x4 | Chipset | 4.0 x4 | — |
| M2_1 (верхний) | CPU | 5.0 x4 | Без конфликтов |
| M2_2 | Chipset/CPU | 4.0 x4 | Может отбирать линии у GPU |
| M2_3 | Chipset | 4.0 x4 | Может отбирать линии у GPU |

**Ключевой конфликт B850**: при использовании M2_2 и/или M2_3 основной PCIe-слот GPU переключается в режим x8. Для большинства современных видеокарт это ~1-3% потери производительности, но для RTX 4090 и будущих флагманов — до 5%.

## Память DDR5

- 4 слота DIMM
- Поддержка XMP 3.0 и AMD EXPO
- **DDR5-6000 — sweet spot** (MCLK:UCLK = 1:1)
- DDR5-8000+ достижим при ручном разгоне (Hynix A-die)

## Сеть и аудио

- **LAN**: Realtek RTL8125BG 2.5GbE — стабильный контроллер, без проблем с разрывами (в отличие от Intel i225/i226)
- **Wi-Fi**: 6E (2.4/5/6 ГГц, 2×2 MIMO)
- **Аудио**: Realtek ALC897 — бюджетный кодек (SNR ~97 дБ). Достаточен для игр и потокового аудио. Аудиофилам — дискретная карта.

## BIOS: USB BIOS Flashback

Поддерживает обновление BIOS без установленного процессора — критично для совместимости с Ryzen 9000 «из коробки».

## Для кого

**Подходит:**
- Сборки на Ryzen 7 7700X/7800X3D/9700X
- Конфигурации с одним NVMe Gen5 + одним SATA SSD
- Игровые ПК с мощной видеокартой (один GPU)
- Сборки с расчётом на DDR5-8000+

**Не подходит:**
- Сборки с 2+ NVMe-накопителями (падение GPU до x8)
- Серверы/рабочие станции с RAID NVMe
- Системы с несколькими GPU
- Аудиофилы (ALC897 — слабый кодек)
