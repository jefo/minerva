---
id: "samsung-990-pro-2tb"
type: "storage"
title: "Samsung 990 Pro 2TB"
vendor: "samsung"
status: "draft"
tags: ["nvme", "pcie-gen4", "dram", "tlc", "high-end"]
last_updated: "2026-06-03"
links:
  concept_pcie: "../../concepts/pcie-lanes.md"
specs:
  interface: "PCIe 4.0 x4"
  form_factor: "M.2 2280"
  controller: "Samsung Pascal"
  nand: "V-NAND V8 TLC"
  dram_cache: "2GB LPDDR4"
  seq_read: "7450 MB/s"
  seq_write: "6900 MB/s"
  random_read_iops: "1400K"
  random_write_iops: "1550K"
  slc_cache: "динамический, до ~200GB"
  tbw: "1200 TB"
  warranty: "5 лет"
  requires_heatsink: false
price_ru:
  median: 14000
  source: "price.ru (оценка)"
  date: "2026-06-03"
profiles:
  standard_tlc_dram_ssd:
    steel_man_desc: "Стандартный NVMe SSD с DRAM-кэшем. Предсказуемая производительность под любой нагрузкой: игры, ОС, разработка."
    capability_level: 2
    failure_mode_desc: "Цена на 20–30% выше DRAM-less аналогов при сравнимых скоростях в клиентских сценариях."
    optimal_for_intents: ["software_development", "video_editing_4k", "data_engineering", "office_productivity"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
---

# Samsung 990 Pro 2TB

## Позиционирование

Samsung 990 Pro — флагманский NVMe SSD на PCIe 4.0, наследник легендарного 980 Pro. Построен на новом контроллере Samsung Pascal (8nm) и памяти V-NAND V8 TLC. Заявлен как «самый быстрый PCIe 4.0 SSD на рынке» — и по цифрам это действительно так: 7450 MB/s чтения и 6900 MB/s записи вплотную приближаются к пределу пропускной способности PCIe 4.0 x4 (~8000 MB/s).

## Архитектура

| Параметр | 980 Pro | 990 Pro |
|---|---|---|
| Контроллер | Samsung Elpis (8nm) | Samsung Pascal (8nm) |
| NAND | V-NAND V6 TLC | V-NAND V8 TLC |
| DRAM | 2GB LPDDR4 | 2GB LPDDR4 |
| Seq Read | 7000 MB/s | 7450 MB/s |
| Seq Write | 5100 MB/s | 6900 MB/s |
| Random Read | 1000K IOPS | 1400K IOPS |
| Random Write | 1000K IOPS | 1550K IOPS |
| TBW (2TB) | 1200 TB | 1200 TB |

Главное улучшение относительно 980 Pro — скачок скорости записи (с 5100 до 6900 MB/s) и значительно выросшие случайные IOPS (+40–55%). Ресурс TBW остался прежним — 1200 TB на 2 ТБ (~0.33 DWPD, ~660 ГБ/день в течение 5 лет).

## SLC-кэш и реальная производительность

990 Pro использует динамический SLC-кэш: до ~200 GB на версии 2TB. Пока кэш не заполнен — запись на максимальной скорости 6900 MB/s. После заполнения кэша скорость записи падает до ~1500–2000 MB/s (native TLC), что всё ещё очень достойно для TLC-памяти.

В реальных сценариях (игры, ОС, разработка) кэш заполняется редко — 200 GB непрерывной записи это очень много. Для видеомонтажа 4K с большими проектами стоит учитывать этот порог.

## Нагрев

Контроллер Samsung Pascal на 8nm техпроцессе эффективнее предшественника. В типичной нагрузке температуры держатся в пределах 55–65°C. При интенсивной непрерывной записи может достигать 75–80°C без радиатора. Радиатор материнской платы или корпусной airflow — желательны, но не строго обязательны (в отличие от Gen5).

## Российский рынок (июнь 2026)

**Медиана: ~14 000 ₽.**

Прямые конкуренты:
- WD Black SN850X 2TB (~13 000 ₽, чуть медленнее, но Game Mode 2.0)
- Kingston Fury Renegade 2TB (~12 000–14 000 ₽, схожие характеристики)
- Crucial T700 1TB (~16 000 ₽, PCIe 5.0, быстрее, но вдвое меньше ёмкость и требуется радиатор)

990 Pro — лучший выбор, если нужна максимальная производительность на PCIe 4.0 без компромиссов. SN850X — разумная альтернатива с экономией ~1000 ₽ при сравнимых характеристиках.

## Для кого

**Подходит:**
- Игровые сборки топ-уровня (ОС + библиотека игр)
- Видеомонтаж 4K/8K (быстрая работа с большими проектами)
- Разработка ПО с интенсивным I/O (Docker, компиляция, базы данных)
- Рабочие станции с требованием к надёжности и предсказуемости

**Не подходит:**
- Бюджетные сборки (DRAM-less аналоги стоят на 20–30% дешевле)
- Экстремальные серверные нагрузки (ресурс 1200 TBW — клиентский, не датацентрный)
- Если нужна скорость PCIe 5.0 любой ценой (смотреть T700/Samsung 9100 Pro)

## Источники

1. Samsung 990 Pro Product Page (samsung.com/semiconductor)
2. TechPowerUp SSD Database (techpowerup.com)
3. Tom's Hardware — Samsung 990 Pro Review
4. Price.ru — рыночные цены, Москва (03.06.2026)
