---
id: "kingston-nv3-2tb"
type: "storage"
title: "Kingston NV3 2TB NVMe SSD"
vendor: "kingston"
status: "draft"
tags: ["nvme", "pcie-4.0", "dramless", "qlc", "budget", "2tb"]
last_updated: "2026-07-06"
links:
  smaller: "catalog/storage/nvme/kingston-nv3-1tb.md"
specs:
  form_factor: "M.2 2280"
  interface: "PCIe 4.0 x4 NVMe 1.4"
  controller: "Silicon Motion SM2268XT (безбуферный)"
  nand: "3D QLC NAND (144L)"
  dram_cache: null
  hmb: "HMB (Host Memory Buffer, 64MB)"
  capacity: "2 TB"
  seq_read: "6000 MB/s"
  seq_write: "5000 MB/s"
  random_read: "до 650K IOPS"
  random_write: "до 850K IOPS"
  endurance: "640 TBW"
  warranty: "3 года"
price_ru:
  min: 9000
  median: 10000
  max: 11500
  source: "price.ru / DNS / Ozon"
  date: "2026-07-06"
  status: "verified"
engineering_notes:
  - "QLC + HMB: для игр и разработки достаточно. Не для sustained write (видеомонтаж 4K)."
  - "2TB = двойной запас против 1TB. Контейнеры, проекты, игры не конкурируют за место."
  - "640 TBW — 350 GB/день в течение 5 лет. Для домашнего сценария — с запасом."
verdict: "Бюджетный 2TB Gen4 для 'не думать о месте'. Игры + Docker + проекты — всё на одном диске без компромиссов."
---

# Kingston NV3 2TB NVMe SSD

Бюджетный 2TB PCIe 4.0 SSD. QLC NAND с HMB — без DRAM, но для игровых/девелоперских нагрузок (burst reads, редкие записи) достаточно.
