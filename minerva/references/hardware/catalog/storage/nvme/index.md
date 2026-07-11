---
id: "nvme-index"
type: "index"
title: "NVMe SSD"
status: "draft"
last_updated: "2026-06-07"
---

# NVMe SSD

Твердотельные накопители с NVMe через PCIe. Только M.2 2280 — актуальный форм-фактор.

## Карта

| Файл | Модель | Поколение PCIe | Объём | Тип NAND | Цена (₽) |
|---|---|---|---|---|---|
| `kingston-nv3-1tb.md` | Kingston NV3 | 4.0 x4 | 1 TB | TLC (DRAM-less) | ~5 500 |
| `kingston-kc3000-1tb.md` | Kingston KC3000 | 4.0 x4 | 1 TB | TLC (DRAM) | ~6 000 |
| `samsung-990-pro-2tb.md` | Samsung 990 Pro | 4.0 x4 | 2 TB | TLC (DRAM) | ~14 000 |
| `wd-black-sn850x-2tb.md` | WD Black SN850X | 4.0 x4 | 2 TB | TLC (DRAM, Game Mode 2.0) | ~13 000 |
| `crucial-t700-1tb.md` | Crucial T700 | 5.0 x4 | 1 TB | TLC (DRAM, радиатор обязателен) | ~16 000 |
| `corsair-mp700-1tb.md` | Corsair MP700 | 5.0 x4 | 1 TB | TLC (DRAM, радиатор обязателен) | ~8 000 |
| `crucial-t700-2tb.md` | Crucial T700 | 5.0 x4 | 2 TB | TLC (DRAM, радиатор обязателен) | ~25 000 |

## Что ещё нужно заполнить

- **PCIe 4.0**: Kingston Fury Renegade — DRAM-кэш, для OS
- **PCIe 5.0**: Samsung 9100 Pro — более эффективный контроллер, холоднее T700
- **Бюджетный**: Kingston NV3 2TB (DRAM-less, но HMB компенсирует)

## Связи

- Требования к охлаждению (Gen5 греется) → `../../cooling/`
- Бюджет линий PCIe → `../../../concepts/pcie-lanes.md`
