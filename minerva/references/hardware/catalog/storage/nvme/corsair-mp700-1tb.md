---
id: "corsair-mp700-1tb"
type: "storage"
title: "Corsair MP700 1TB NVMe SSD (PCIe 5.0)"
vendor: "Corsair"
status: "draft"
tags: ["nvme", "pcie5", "dram", "tlc", "enthusiast"]
last_updated: "2026-06-07"
links:
  competitor_t700: "catalog/storage/nvme/crucial-t700-1tb.md"
  competitor_kc3000: "catalog/storage/nvme/kingston-kc3000-1tb.md"
specs:
  capacity_gb: 1024
  form_factor: "M.2 2280"
  interface: "PCIe 5.0 x4"
  protocol: "NVMe 2.0"
  nand_type: "TLC (Micron 232L)"
  controller: "Phison E26"
  dram_cache: true
  dram_size_mb: 2048
  seq_read_mbps: 10000
  seq_write_mbps: 9500
  random_read_iops: "1500K"
  random_write_iops: "1500K"
  endurance_tbw: 700
  warranty_years: 5
  heatsink: "Требуется (пассивный радиатор MB или активный)"
profiles:
  pcie5_enthusiast_nvme:
    capability_level: 3
    steel_man_desc: "10 GB/s read — максимальная пропускная способность для Kontakt DFD-стриминга. Phison E26 + Micron 232L — зрелая платформа."
    failure_mode_desc: "Требует охлаждения (heatsink). Без радиатора — thermal throttle при sustained load. Нагрев до 80°C."
    optimal_for_intents: ["daw_zero_dpc_latency", "video_editing_4k"]
    failure_for_intents: ["sff_compact_itx_portable"]
    failure_severity: "WARN"
price_ru:
  min: 7000
  median: 8000
  max: 10000
  source: "DAW reference, June 2026"
---

# Corsair MP700 1TB NVMe SSD (PCIe 5.0)

## Позиционирование

Флагманский PCIe 5.0 NVMe SSD. 10 GB/s sequential read, Phison E26 + Micron 232L TLC. Для DAW: максимальная пропускная способность для Kontakt DFD-стриминга (Direct From Disk) — загрузка сэмплов без задержек.

**Важно:** требует охлаждения. Пассивный радиатор материнской платы достаточен для типичной аудио-нагрузки (не continuous write).

## Характеристики

| Параметр | Значение |
|---|---|
| Ёмкость | 1 TB |
| Интерфейс | PCIe 5.0 x4, NVMe 2.0 |
| NAND | TLC (Micron 232L) |
| Контроллер | Phison E26 |
| DRAM | 2 GB DDR4 |
| Seq Read | 10 000 MB/s |
| Seq Write | 9 500 MB/s |
| Endurance | 700 TBW |
| Гарантия | 5 лет |
| Охлаждение | Требуется радиатор |

## Сравнение с Crucial T700

| Параметр | MP700 | T700 |
|---|---|---|
| Read | 10 000 MB/s | 12 400 MB/s |
| Write | 9 500 MB/s | 11 800 MB/s |
| TBW | 700 | 600 |
| Контроллер | Phison E26 | Phison E26 (full speed) |
| Цена | ~8 000 ₽ | ~9 000 ₽ |

## Для кого

- **Профессиональная DAW:** сэмпловые библиотеки на PCIe 5.0 → минимальные задержки стриминга
- **Видеомонтаж 8K:** sustained throughput

## НЕ подходит

- **Бюджетные сборки:** PCIe 4.0 (KC3000 за 6 000 ₽) достаточно для аудио
- **Платы без радиатора M.2:** thermal throttle без охлаждения
