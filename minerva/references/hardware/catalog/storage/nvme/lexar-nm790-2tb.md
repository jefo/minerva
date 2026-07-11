---
id: "lexar-nm790-2tb"
type: "storage"
title: "Lexar NM790 2TB NVMe SSD"
vendor: "lexar"
status: "draft"
tags: ["nvme", "pcie-4.0", "tlc", "dramless", "maxio", "high-iops"]
last_updated: "2026-07-06"
links:
  competitor: "catalog/storage/nvme/kingston-nv3-2tb.md"
specs:
  form_factor: "M.2 2280"
  interface: "PCIe 4.0 x4 NVMe 2.0"
  controller: "Maxio MAP1602 (12nm, ARM R5, 4-channel, DRAM-less)"
  nand: "3D TLC NAND (YMTC 232L)"
  dram_cache: null
  hmb: "HMB (Host Memory Buffer)"
  capacity: "2 TB"
  seq_read: "7400 MB/s"
  seq_write: "6500 MB/s"
  random_read: "до 1000K IOPS"
  random_write: "до 900K IOPS"
  endurance: "1500 TBW"
  warranty: "5 лет"
price_ru:
  min: 9500
  median: 10500
  max: 11500
  source: "price.ru / DNS / Ozon"
  date: "2026-07-06"
  status: "verified"
engineering_notes:
  - "TLC NAND (не QLC) — критическое преимущество для dev-нагрузок. Нет катастрофического падения скорости после SLC-кэша."
  - "Maxio MAP1602 — один из лучших DRAM-less контроллеров. HMB компенсирует отсутствие DRAM."
  - "1500 TBW — в 2.3× больше чем NV3 (640 TBW). 820 GB/день в течение 5 лет."
  - "Random write 900K IOPS — Docker build (тысячи мелких файлов) не просаживает систему."
  - "5 лет гарантии против 3 лет у NV3."
verdict: "TLC-накопитель для dev-среды. На 500 ₽ дороже NV3, но исключает микрофризы IDE при docker build. +2.3× TBW, +2 года гарантии."
---

# Lexar NM790 2TB NVMe SSD

## Позиционирование

Бюджетный 2TB Gen4 SSD на TLC (не QLC) памяти. Для разработчика критично: случайная запись не проседает при docker build. Контроллер Maxio MAP1602 с HMB — лучший в классе DRAM-less.

## Сравнение с Kingston NV3

| Параметр | Lexar NM790 2TB | Kingston NV3 2TB |
|---|---|---|
| NAND | TLC | QLC |
| Контроллер | Maxio MAP1602 | SM2268XT |
| Seq read/write | 7400/6500 | 6000/5000 |
| Random write | 900K IOPS | 850K IOPS |
| Endurance | 1500 TBW | 640 TBW |
| Гарантия | 5 лет | 3 года |
| Цена | ~10 500 ₽ | ~10 000 ₽ |

+500 ₽ за TLC + 2.3× TBW + 2 года гарантии. Для dev-среды — однозначно.
