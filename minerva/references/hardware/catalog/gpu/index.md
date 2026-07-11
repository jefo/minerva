---
id: "gpu-index"
type: "index"
title: "Видеокарты"
status: "verified"
last_updated: "2026-07-09"
---

# Видеокарты (GPU)

NVIDIA Blackwell (RTX 50) и Ada Lovelace (RTX 40) · AMD RDNA 4 (RX 9000) и RDNA 3 (RX 7000) · Intel Battlemage (Arc B).

Всего: **15 карт** (7 verified, 8 draft). Данные структурированы по GPU Entity Type v1.0.

## NVIDIA GeForce RTX 50 (Blackwell)
_GDDR7, PCIe 5.0, DLSS 4 + MFG_

| Модель | VRAM | TBP | Цена (₽) | Апскейлер | RT | Статус |
|---|---|---|---|---|---|---|
| [RTX 5060](nvidia-rtx-5060.md) | 8 GB GDDR7 | 145W | 35 000 | DLSS 4 | Gen 4 | ✅ verified |
| [RTX 5060 Ti](nvidia-rtx-5060-ti.md) | 16 GB GDDR7 | 180W | 52 000 | DLSS 4 | Gen 4 | ✅ verified |
| [RTX 5070](nvidia-rtx-5070.md) | 12 GB GDDR7 | 250W | 72 000 | DLSS 4 | Gen 4 | ✅ verified |
| [RTX 5070 Ti](nvidia-rtx-5070-ti.md) | 16 GB GDDR7 | 300W | 98 000 | DLSS 4 | Gen 4 | 📝 draft |
| [RTX 5080](nvidia-rtx-5080.md) | 16 GB GDDR7 | 320W | 125 000 | DLSS 4 | Gen 4 | 📝 draft |
| [RTX 5090](nvidia-rtx-5090.md) | 32 GB GDDR7 | 500W | 260 000 | DLSS 4 | Gen 4 | 📝 draft |

## NVIDIA GeForce RTX 40 (Ada Lovelace)
_GDDR6/GDDR6X, PCIe 4.0 — сняты с производства_

| Модель | VRAM | TBP | Цена (₽) | Апскейлер | RT | Статус |
|---|---|---|---|---|---|---|
| [RTX 4060](nvidia-rtx-4060.md) | 8 GB GDDR6 | 115W | 32 000 | DLSS 3.5 | Gen 3 | ✅ verified |
| [RTX 4060 Ti](nvidia-rtx-4060-ti.md) | 16 GB GDDR6 | 165W | 46 500 | DLSS 3 | Gen 3 | ✅ verified |
| [RTX 4070](nvidia-rtx-4070.md) | 12 GB GDDR6X | 200W | 45 000 | DLSS 3 | Gen 3 | ✅ verified |

## AMD Radeon RX 9000 (RDNA 4)
_GDDR6, PCIe 5.0, FSR 4_

| Модель | VRAM | TBP | Цена (₽) | Апскейлер | RT | Статус |
|---|---|---|---|---|---|---|
| [RX 9060 XT](amd-rx-9060-xt.md) | 16 GB GDDR6 | 200W | 48 000 | FSR 4 | Gen 3 | 📝 draft |
| [RX 9070](amd-rx-9070.md) | 16 GB GDDR6 | 240W | 64 000 | FSR 4 | Gen 3 | 📝 draft |
| [RX 9070 XT](amd-rx-9070-xt.md) | 16 GB GDDR6 | 280W | 75 000 | FSR 4 | Gen 3 | 📝 draft |

## AMD Radeon RX 7000 (RDNA 3)
_GDDR6, PCIe 4.0 — бюджетный сегмент_

| Модель | VRAM | TBP | Цена (₽) | Апскейлер | RT | Статус |
|---|---|---|---|---|---|---|
| [RX 7600](amd-rx-7600.md) | 8 GB GDDR6 | 165W | 28 000 | FSR 3 | Gen 2 | ✅ verified |

## Intel Arc B (Battlemage)
_GDDR6, PCIe 4.0/5.0, XeSS 3 + MFG_

| Модель | VRAM | TBP | Цена (₽) | Апскейлер | RT | Статус |
|---|---|---|---|---|---|---|
| [Arc B570](intel-arc-b570.md) | 10 GB GDDR6 | 170W | 29 000 | XeSS 3 | Gen 2 | 📝 draft |
| [Arc B580](intel-arc-b580.md) | 12 GB GDDR6 | 190W | 28 000 | XeSS 3 | Gen 2 | 📝 draft |

---

## Структура каталога

- **Каждая страница GPU** — полные характеристики, software-стек, observations из тестов, editorial verdict
- **Данные структурированы** — VRAM, compute (RT/ML-ядра), software — в машиночитаемом виде (GPU Entity Type v1.0)
- **Аналитический слой** (`/gpu`) — сравнения, Envelope Map, Fit Classes — см. [GPU Analytics](/gpu)
- **Цены:** price.ru / DNS / Ozon, ориентировочные на момент обновления
- **Связанные концепты:** [PCIe-версия](../concepts/pcie-lanes.md) · [Бюджет мощности](../concepts/power-budget.md)
