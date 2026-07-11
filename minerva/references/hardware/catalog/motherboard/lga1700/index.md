---
id: "lga1700-index"
type: "index"
title: "Материнские платы LGA1700"
status: "draft"
last_updated: "2026-07-06"
links:
  platform_cpu: "catalog/cpu/intel-core-i5-12400f.md"
---

# Материнские платы LGA1700

Платформа Intel 12/13/14-го поколения. Карта покрывает полный спектр: от ультрабюджетной H610 до флагманских Z790.

## Карта моделей

### Бюджетный сегмент (H610, DDR4)

| Файл | Модель | Чипсет | RAM | M.2 | LAN | Цена |
|---|---|---|---|---|---|---|
| `asrock-h610m-hdv-m2.md` | ASRock H610M-HDV/M.2 | H610 | 2×DDR4 | 1× Gen3 | 1GbE | ~6 000 |
| `msi-pro-b760m-p-ddr4.md` | MSI PRO B760M-P DDR4 | B760 | 2×DDR4 | 1× Gen4 | 1GbE | ~8 300 |

### Средний сегмент (B760, DDR4)

| Файл | Модель | Чипсет | RAM | M.2 | LAN | Цена |
|---|---|---|---|---|---|---|
| `gigabyte-b760m-ds3h-ddr4.md` | Gigabyte B760M DS3H DDR4 | B760 | 4×DDR4 | 2× Gen4 | 2.5GbE | ~9 000 |
| `asrock-b760m-pro-rs-d4.md` | ASRock B760M Pro RS/D4 | B760 | 4×DDR4 | 2× Gen4 | 2.5GbE | ~9 500 |
| `msi-pro-b760m-a-wifi-ddr4.md` | MSI PRO B760M-A WIFI DDR4 | B760 | 4×DDR4 | 2× Gen4 | 2.5GbE | ~10 000 |

### Средний сегмент (B760, DDR5, PCIe 5.0)

| Файл | Модель | Чипсет | RAM | M.2 | PCIe | Цена |
|---|---|---|---|---|---|---|
| `asrock-b760m-pro-rs.md` | ASRock B760M Pro RS | B760 | 4×DDR5 | 3× Gen4 | **5.0** x16 | ~12 500 |

### Премиум сегмент (Z790)

| Файл | Модель | Чипсет | Ключевое | Цена |
|---|---|---|---|---|
| `asus-proart-z790-e.md` | ASUS ProArt Z790-E | Z790 | 10GbE + 2× TB4 | ~42 000 |
| `asrock-z790-taichi.md` | ASRock Z790 Taichi | Z790 | 24+1+2 (105A), 2× TB4 | ~40 000 |
| `msi-meg-z790-ace.md` | MSI MEG Z790 Ace | Z790 | 5× M.2, USB4 | ~48 000 |

## Как выбирать под i5-12400F

1. **Минимальный бюджет** → H610M-HDV/M.2 (~6K). Компромисс: VRM без радиатора, 1×M.2 Gen3.
2. **Разумный минимум** → MSI B760M-P (~8.3K). Радиатор VRM, но 2 слота RAM.
3. **Золотая середина** → Gigabyte B760M DS3H (~9K) или ASRock Pro RS/D4 (~9.5K). 4 слота RAM, 2×M.2 Gen4.
4. **PCIe 5.0 + DDR5** → ASRock B760M Pro RS (~12.5K). «Родной» PCIe для RTX 5070, но дороже.

## Связи

- CPU: `catalog/cpu/intel-core-i3-12100f.md`, `intel-core-i5-12400f.md`, `intel-core-i5-14600k.md`
- Память: `catalog/memory/ddr4-3200-cl16-32gb.md`, `catalog/memory/ddr5-5600-cl36.md`
