---
id: "ddr5"
type: "memory"
title: "DDR5 SDRAM"
vendor: null
status: "verified"
tags: ["ddr5", "jedec", "on-die-ecc", "pmic"]
last_updated: "2025-06-03"
links:
  used_by_cpu:
    - "catalog/cpu/amd-ryzen-7000.md"
    - "catalog/cpu/amd-ryzen-9000.md"
    - "catalog/cpu/intel-core-14th.md"
    - "catalog/cpu/intel-core-ultra.md"
  used_by_mb_am5: "catalog/motherboard/am5/index.md"
  used_by_mb_lga1700: "catalog/motherboard/lga1700/index.md"
  predecessor: "catalog/memory/ddr4.md"
  concept_timings: "concepts/memory-timings.md"
specs:
  standard: "JEDEC DDR5"
  voltage: "1.1V (JEDEC) / 1.25–1.45V (XMP/EXPO)"
  speeds_jedec: "4800, 5200, 5600 MT/s"
  speeds_oc: "6000–8400+ MT/s"
  max_capacity_per_dimm: "64 GB (в перспективе 128 GB)"
  channels_per_module: "2 × 32-bit (вместо 1 × 64-bit у DDR4)"
  on_die_ecc: true
  pmic: "На модуле (5V вход)"
---

# DDR5 SDRAM

## Ключевые отличия от DDR4

| Параметр | DDR4 | DDR5 |
|---|---|---|
| Напряжение | 1.2V | 1.1V |
| Каналов на модуль | 1 × 64-bit | 2 × 32-bit |
| Управление питанием | На плате | PMIC на модуле |
| On-die ECC | Нет | Да (только для ячеек, не шины) |
| Макс. ёмкость DIMM | 32 GB | 64 GB (128 GB в перспективе) |
| XMP/EXPO | XMP 2.0 | XMP 3.0 / AMD EXPO |
| Число профилей XMP | 2 | 5 (3 вендорских + 2 пользовательских) |

> **On-die ECC в DDR5** — это не ECC-память в классическом понимании. Защищает от ошибок внутри чипа (повышение плотности ячеек), но не между чипом и контроллером. Серверная DDR5 ECC (RDIMM) — отдельный класс.

## Архитектура: два 32-битных канала

Каждый модуль DDR5 разбит на два независимых 32-битных подканала (у DDR4 — один 64-битный). Это увеличивает эффективную пропускную способность при смешанных нагрузках, но каждый подканал имеет вдвое меньший burst length (BL16 → BL8 × 2).

## Sweet spot для платформ

### AMD AM5 (Zen 4/5)
- **DDR5-6000 — оптимальная точка.** Контроллер памяти работает в синхронном режиме (MCLK:UCLK = 1:1).
- Выше 6000 → переход в 1:2 → рост latency на 10–15 нс → прирост пропускной способности не компенсирует.
- AMD EXPO-профили оптимизированы под Zen 4/5 (отличаются от XMP субтаймингами).

### Intel LGA1700 (12–14 gen)
- Контроллер памяти более гибкий, работает в Gear 2 (1:2) начиная с DDR5-4400.
- DDR5-6400–7200 — практический максимум для большинства плат Z790.
- Gear 4 на экстремальных частотах (8000+) — сильный рост latency.

## Ранги и конфигурации

- **1R (Single Rank)** — 1 набор чипов на канал. Легче разгоняется. До 32 GB на DIMM.
- **2R (Dual Rank)** — 2 набора чипов на канал. +3–5% производительности за счёт чередования (rank interleaving). Труднее разгон.
- 4 планки 2R — худший сценарий для контроллера памяти. Ожидать понижения частоты.

## PMIC (Power Management IC)

В отличие от DDR4, где питание подаётся с платы, DDR5 имеет собственный PMIC на каждом модуле. Это даёт точный контроль напряжения на уровне модуля, но создаёт тепловыделение на самой планке. При напряжении выше 1.35V рекомендуется активный обдув планок.

## Ключевые производители чипов

| Производитель | Тип чипов | Особенности |
|---|---|---|
| SK Hynix | A-die, M-die | A-die — лидер по разгону (8000+) |
| Samsung | B-die DDR5 | Хороший разгон, но уступает Hynix A-die |
| Micron | Rev. A, Rev. B | Стабильны, но ограниченный разгонной потенциал |

## Источники

- JEDEC DDR5 SDRAM Standard (JESD79-5)
- Buildzoid / Actually Hardcore Overclocking — DDR5 timing deep dives
- AnandTech — DDR5 vs DDR4 scaling analysis
- Собственное тестирование лаборатории на AM5 и LGA1700
