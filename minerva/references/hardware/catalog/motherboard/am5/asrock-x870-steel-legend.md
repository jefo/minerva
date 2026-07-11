---
id: "asrock-x870-steel-legend"
type: "motherboard"
title: "ASRock X870 Steel Legend"
vendor: "asrock"
status: "draft"
tags: ["am5", "x870", "atx", "ddr5", "pcie-5.0", "wifi-7", "high-end", "no-bifurcation"]
last_updated: "2026-06-03"
links:
  platform: "catalog/cpu/amd-ryzen-9000.md"
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  concept_pcie: "../../concepts/pcie-lanes.md"
  concept_vrm: "../../concepts/vrm-phases.md"
specs:
  socket: "AM5"
  chipset: "X870"
  form_factor: "ATX"
  vrm: "16+2+1 (80A SPS)"
  memory: "4× DDR5, до 8200+ MT/s"
  pcie_slots: "1× PCIe 5.0 x16 (электрически x16 всегда)"
  m2_slots: "1× PCIe 5.0 x4, 3× PCIe 4.0 x4"
  sata_ports: 4
  network: "Realtek RTL8125BG 2.5GbE, Wi-Fi 7"
  # 3D Envelope (v1.4 — keep-out zones)
  vrm_heatsink_height_max_mm: 45
  ram_slot_offset_x_mm: 55
  audio: "Realtek ALC4080"
  flashback: true
  bifurcation_risk: false
price_ru:
  median: 28000
  source: "price.ru (оценка)"
  date: "2026-06-03"
verdict: "Флагманская плата на X870 под Zen 5. 16+2+1 фаз на 80A SPS, PCIe 5.0 x16 без отъёма линий при любом заполнении M.2. 5GbE + Wi-Fi 7. Идеальна для Ryzen 9 с множеством NVMe-накопителей."

profiles:
  enthusiast_platform:
    capability_level: 3
    capability_level: 3
    steel_man_desc: "X870 с 16+2+1 фазами (80A SPS) и нефлагманским ценником. Все 16 линий PCIe 5.0 у GPU всегда — без бифуркации. 4× M.2 (1× Gen5), Wi-Fi 7, 5GbE LAN."
    failure_mode_desc: "Избыточен для игровых сборок с одной видеокартой и одним NVMe. Разница с B850 Riptide в CPU-рендеринге и играх — в пределах погрешности. Переплата за неиспользуемые линии."
    optimal_for_intents: ["video_editing_8k", "data_engineering", "virtualization", "scientific_computing", "llm_training_lora"]
    failure_for_intents: ["aaa_1080p_ultra", "esports_1080p_240hz"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# ASRock X870 Steel Legend

## Позиционирование

ASRock X870 Steel Legend — флагманская плата на чипсете X870 для процессоров AMD Ryzen 9000 (Granite Ridge). В отличие от B850, X870 **не отнимает линии PCIe у GPU** при использовании дополнительных M.2-слотов — все 16 линий PCIe 5.0 у видеокарты сохраняются всегда.

## VRM: 16+2+1 фаз, 80A SPS

| Параметр | Значение |
|---|---|
| Фазы | 16+2+1 |
| MOSFET | 80A Smart Power Stage |
| Суммарный ток (расчётный) | 16 × 80 = 1280A |
| Охлаждение | Массивные радиаторы с теплотрубкой |

VRM с тройным запасом даже для Ryzen 9 9950X под разгоном. X870 Steel Legend — одна из немногих плат, где подсистема питания не является узким местом ни при каких сценариях.

## Слоты: без компромиссов

| Слот | Источник | Версия PCIe | Примечание |
|---|---|---|---|
| PCIe_x16 | CPU | 5.0 x16 | **Всегда x16**, не делится |
| M2_1 (верхний) | CPU | 5.0 x4 | Без конфликтов |
| M2_2 | Chipset | 4.0 x4 | Без влияния на GPU |
| M2_3 | Chipset | 4.0 x4 | Без влияния на GPU |
| M2_4 | Chipset | 4.0 x4 | Без влияния на GPU |

**Главное преимущество X870 над B850**: можно заполнить все 4 M.2-слота, и GPU останется на PCIe 5.0 x16. Чипсет X870 предоставляет достаточно линий, чтобы не трогать линии CPU.

## Память DDR5

- 4 слота DIMM, до 256 ГБ
- Поддержка XMP 3.0 и AMD EXPO
- DDR5-6000 — sweet spot (MCLK:UCLK = 1:1)
- DDR5-8200+ на Hynix A-die при ручном разгоне
- Улучшенная трассировка под высокие частоты (8-слойный PCB)

## Сеть и аудио

- **LAN**: Realtek 5GbE — пропускная способность ~625 МБ/с. Идеально для NAS и рабочих станций с сетевыми хранилищами.
- **Wi-Fi**: 7 (802.11be, 320 МГц каналы, 4K QAM) — теоретически до 46 Гбит/с. Практический потолок ~5 Гбит/с.
- **Аудио**: Realtek ALC4080 (SNR 120 дБ, 32-bit/192 кГц) — флагманский кодек, достаточен для большинства аудиофилов. Дискретная карта нужна только для студийной работы.

## BIOS: USB BIOS Flashback

Обновление BIOS без процессора через USB-флешку и выделенную кнопку на задней панели.

## Сравнение с B850 Riptide

| Параметр | X870 Steel Legend | B850 Riptide |
|---|---|---|
| VRM | 16+2+1 (80A) | 14+2+1 (80A) |
| M.2 Gen5 | 1× | 1× |
| M.2 Gen4 | 3× | 2× |
| GPU x16 при всех M.2 | ✅ Да | ❌ Падает до x8 |
| LAN | 5GbE | 2.5GbE |
| Wi-Fi | 7 | 6E |
| Аудио | ALC4080 (120dB) | ALC897 (97dB) |
| Цена | ~28 000 ₽ | ~18 000 ₽ |

Разница в ~10 000 ₽ оправдана, если нужны: 3+ NVMe без потери линий GPU, 5GbE, Wi-Fi 7 и качественный аудиокодек.

## Для кого

**Идеальна:**
- Сборки на Ryzen 9 9900X/9950X
- Рабочие станции с 2+ NVMe-накопителями
- Системы с RTX 4090/5090 (нужны полные x16 линий)
- Сборки с 5GbE-сетью (NAS, видеомонтаж по сети)
- Максимальный разгон DDR5 (8-слойный PCB)

**Избыточна:**
- Бюджетные сборки на Ryzen 5 (переплата за VRM и 5GbE)
- Системы с одним NVMe и одной видеокартой (B850 Riptide справится)
- Игровые ПК без сетевых хранилищ
