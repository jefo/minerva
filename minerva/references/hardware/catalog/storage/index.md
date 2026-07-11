---
id: "storage-index"
type: "index"
title: "Накопители"
status: "draft"
last_updated: "2025-06-03"
---

# Накопители (Storage)

Актуальный стандарт — NVMe PCIe 4.0/5.0. SATA SSD — только для вторичного хранилища. HDD — не рассматриваем.

## Карта

| Файл | Тип | Интерфейс | Скорость | Цена (₽) |
|---|---|---|---|---|
| `nvme/kingston-nv3-1tb.md` | NVMe SSD | PCIe 4.0 x4 | ~6 ГБ/с read | ~5 500 |

## Что ещё нужно заполнить

- `nvme/` — NVMe Gen4 (SN850X, 990 Pro) и Gen5 (T700, 9100 Pro)
- `sata-ssd.md` — SATA SSD для массового хранилища

## Связи

- PCIe-линии → `../../concepts/pcie-lanes.md`
- Конфликты с SATA-портами → `../motherboard/`
