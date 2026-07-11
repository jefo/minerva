---
id: "crucial-t700-2tb"
type: "storage"
title: "Crucial T700 2TB NVMe SSD (PCIe 5.0)"
vendor: "Crucial"
status: "draft"
tags: ["nvme", "pcie5", "dram", "tlc", "enthusiast", "high-capacity"]
last_updated: "2026-06-07"
links:
  sibling_1tb: "catalog/storage/nvme/crucial-t700-1tb.md"
  competitor_mp700: "catalog/storage/nvme/corsair-mp700-1tb.md"
specs:
  capacity_gb: 2048
  form_factor: "M.2 2280"
  interface: "PCIe 5.0 x4"
  protocol: "NVMe 2.0"
  nand_type: "TLC (Micron 232L)"
  controller: "Phison E26 (full speed)"
  dram_cache: true
  dram_size_mb: 4096
  seq_read_mbps: 12400
  seq_write_mbps: 11800
  random_read_iops: "1500K"
  random_write_iops: "1500K"
  endurance_tbw: 1200
  warranty_years: 5
  heatsink: "Встроенный пассивный радиатор (11.5 мм высота) или без радиатора"
profiles:
  pcie5_enthusiast_nvme:
    capability_level: 3
    steel_man_desc: "12.4 GB/s read, 2TB — максимальная скорость + ёмкость для Kontakt DFD. Phison E26 full speed, 4GB DRAM."
    failure_mode_desc: "Требует активного охлаждения при sustained write. Радиатор обязателен."
    optimal_for_intents: ["daw_zero_dpc_latency", "video_editing_8k"]
price_ru:
  min: 22000
  median: 25000
  max: 30000
  source: "DAW reference, June 2026"
  note: "estimated — цены из DAW-референса, июнь 2026"
---

# Crucial T700 2TB NVMe SSD (PCIe 5.0)

## Позиционирование

Флагманский PCIe 5.0 NVMe SSD максимальной ёмкости. 2TB + 12.4 GB/s read + 4GB DRAM. Для DAW Profi-тира: 2× T700 2TB = 4TB сверхбыстрого хранилища для оркестровых библиотек (Spitfire, Orchestral Tools).

## Характеристики

| Параметр | Значение |
|---|---|
| Ёмкость | 2 TB |
| Интерфейс | PCIe 5.0 x4, NVMe 2.0 |
| Read | 12 400 MB/s |
| Write | 11 800 MB/s |
| DRAM | 4 GB |
| Endurance | 1200 TBW |
| Охлаждение | Встроенный радиатор (опционально) |

## Сравнение T700 1TB vs 2TB

| Параметр | T700 1TB | T700 2TB |
|---|---|---|
| Read | 11 700 MB/s | 12 400 MB/s |
| Write | 9 500 MB/s | 11 800 MB/s |
| DRAM | 2 GB | 4 GB |
| TBW | 600 | 1200 |
| Цена | ~16 000 ₽ | ~25 000 ₽ |

## Для кого

- **DAW Profi-тир:** 2× T700 2TB = 4TB для оркестровых библиотек
- **Видеомонтаж 8K:** sustained throughput

## НЕ подходит

- **Бюджет:** 25 000 ₽ за один SSD. KC3000 1TB за 6 000 ₽
- **Платы без радиатора M.2 Gen5**
