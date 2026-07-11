---
id: "kingston-nv3-1tb"
type: "storage"
title: "Kingston NV3 1TB NVMe SSD"
vendor: "kingston"
status: "verified"
tags: ["nvme", "pcie-4.0", "dramless", "qlc", "budget"]
last_updated: "2026-06-03"
links:
  pcie_gen: "catalog/storage/nvme/pcie-gen4.md"
  concept_pcie: "concepts/pcie-lanes.md"
specs:
  form_factor: "M.2 2280"
  interface: "PCIe 4.0 x4 NVMe 1.4"
  controller: "Silicon Motion SM2268XT (безбуферный)"
  nand: "3D QLC NAND (144L, возможно 162L)"
  dram_cache: null
  hmb: "HMB (Host Memory Buffer, 32MB)"
  capacity: "1 TB"
  seq_read: "6000 MB/s"
  seq_write: "4000 MB/s"
  random_read: "до 600K IOPS"
  random_write: "до 800K IOPS"
  endurance: "320 TBW"
  warranty: "3 года"
price_ru:
  min: 11225
  median: 11800
  max: 13490
  source: "price.ru"
  date: "2026-06-03"
profiles:
  dram_less_hmb_cached:
    steel_man_desc: "Клиентская ОС: браузер, игры. Короткие записи до 20–30 ГБ поглощаются SLC-кэшем — скорости уровня премиум-дисков при цене на 30–40% ниже."
    capability_level: 1
    failure_mode_desc: "Непрерывная многопоточная запись (СУБД, импорт RAW). После исчерпания SLC-кэша — задержки до 40 мс, скорость ≤ 350 МБ/с (уровень SATA III)."
    optimal_for_intents: ["office_productivity", "software_development", "aaa_1080p_ultra"]
    failure_for_intents: ["video_editing_4k", "video_editing_8k", "data_engineering"]
    failure_severity: "BLOCK"
    failure_type: "CLIFF_DROP"
verdict: "Бюджетный PCIe 4.0 SSD без DRAM-буфера. QLC-память — не для интенсивной записи. Для игр и системы — отлично. Для рабочей станции с большими объёмами записи — искать TLC с DRAM."
---

# Kingston NV3 1TB NVMe SSD

## Позиционирование

Kingston NV3 — наследник популярной линейки NV2 с обновлённым контроллером Silicon Motion SM2268XT. Бюджетный PCIe 4.0 SSD без DRAM-буфера, использующий HMB (Host Memory Buffer) — забирает 32 MB системной RAM под таблицы адресации.

## Архитектура

| Параметр | NV2 | NV3 |
|---|---|---|
| Контроллер | SM2267XT | SM2268XT |
| NAND | 3D QLC (144L) | 3D QLC (144L/162L) |
| Seq Read | 3500 MB/s | 6000 MB/s |
| Seq Write | 2100 MB/s | 4000 MB/s |
| TBW (1TB) | 320 TBW | 320 TBW |

Главное улучшение — вдвое выросшая скорость чтения (с 3.5 до 6 ГБ/с) за счёт нового контроллера. Ресурс TBW не изменился — 320 TBW на 1 ТБ (0.32 DWPD, ~292 ГБ/день в течение 3 лет).

## QLC-память: что нужно знать

QLC (Quad-Level Cell) = 4 бита на ячейку. Плюсы: высокая плотность, низкая цена. Минусы:

- **SLC-кэш:** ~200 GB динамического кэша (работает как быстрый SLC, пока не заполнен)
- **После заполнения кэша:** скорость записи падает до 200–400 MB/s
- **Ресурс:** 320 TBW — вдвое меньше, чем у TLC-аналогов (Samsung 980: 600 TBW)

**Для игр и системы** — QLC не проблема (игры читают, не пишут). Для регулярной записи больших файлов (видеомонтаж, базы данных) — лучше TLC с DRAM.

## Производительность

**CrystalDiskMark (типичные результаты):**
- Seq Read: 6 000 MB/s (близко к заявленным)
- Seq Write: 3 800–4 000 MB/s (пока кэш не заполнен)
- Random 4K Read: 60–70 MB/s
- Random 4K Write: 180–200 MB/s

После заполнения SLC-кэша (200+ GB непрерывной записи) скорость падает до 200–400 MB/s. В реальном использовании (игры, установка программ, загрузка ОС) кэш почти никогда не заполняется полностью.

## Нагрев

Без DRAM-буфера и с эффективным контроллером — греется умеренно. В большинстве сценариев радиатор не требуется. Но в корпусах с плохой вентиляцией или при непрерывной нагрузке — желателен даже простой радиатор материнской платы.

## Российский рынок (июнь 2026)

**Диапазон: 11 225–13 490 ₽, медиана ~11 800 ₽.**

Прямые конкуренты:
- Samsung 980 1TB (~8 000–10 000 ₽, TLC, но PCIe 3.0)
- WD Blue SN580 1TB (~9 000–11 000 ₽, TLC, без DRAM)
- ADATA Legend 960 1TB (~12 000–14 000 ₽, TLC, с DRAM)

NV3 оправдан, если нужна скорость PCIe 4.0 за минимальные деньги. Если скорость некритична — Samsung 980 на PCIe 3.0 дешевле и с TLC.

## Для кого

**Подходит:**
- Игровые сборки (основной диск под систему + игры)
- Бюджетные рабочие станции (офис, интернет)
- Как второй диск под библиотеку игр

**Не подходит:**
- Видеомонтаж и работа с большими файлами (QLC + без DRAM)
- Серверы и NAS (ресурс 320 TBW слишком мал)
- Единственный диск в системе без резервного копирования

## Источники

1. Kingston NV3 Product Page (kingston.com)
2. TechPowerUp SSD Database (techpowerup.com)
3. Price.ru — рыночные цены, Москва (03.06.2026)
