---
id: "amd-ryzen-7000"
type: "cpu"
title: "AMD Ryzen 7000 Series (Zen 4)"
vendor: "amd"
status: "verified"
tags: ["amd", "zen4", "am5", "ddr5", "5nm"]
last_updated: "2025-06-03"
external_audit_verification: planned
links:
  socket: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  predecessor: null
  successor: "amd-ryzen-9000.md"
specs:
  socket: "AM5 (LGA1718)"
  lithography: "TSMC 5nm (CCD) + 6nm (IOD)"
  max_cores: 16
  max_threads: 32
  pcie_lanes: "28 (24 usable)"
  pcie_version: "5.0"
  memory: "DDR5 only, dual-channel"
  tdp_range: "65W – 170W"
  igpu: "RDNA 2 (2 CUs, базовый вывод)"
---

# AMD Ryzen 7000 (Zen 4)

## Архитектура

Zen 4 — первое поколение AMD на сокете AM5, переход на DDR5 и PCIe 5.0. Чиплетная компоновка: одно или два ядра CCD (5nm TSMC) + кристалл ввода-вывода IOD (6nm).

Ключевые изменения относительно Zen 3 (AM4):
- **+13% IPC** за счёт удвоенного L2-кэша (1MB на ядро) и улучшенного предсказателя ветвлений
- **AVX-512** — аппаратная поддержка (через два 256-bit пути)
- **Встроенная графика RDNA 2** на всех моделях (2 CU, только для вывода)
- **DDR5-only** — обратной совместимости с DDR4 нет

## Линейка

| Модель | Ядер/Потоков | Базовая | Boost | TDP | Целевая аудитория |
|---|---|---|---|---|---|
| Ryzen 5 7600X | 6/12 | 4.7 | 5.3 | 105W | Игры, мейнстрим |
| Ryzen 7 7700X | 8/16 | 4.5 | 5.4 | 105W | Игры + стриминг |
| Ryzen 7 7800X3D | 8/16 | 4.2 | 5.0 | 120W | Игровой флагман (3D V-Cache) |
| Ryzen 9 7900X | 12/24 | 4.7 | 5.6 | 170W | Рабочие станции |
| Ryzen 9 7950X | 16/32 | 4.5 | 5.7 | 170W | Профессиональный флагман |
| Ryzen 9 7950X3D | 16/32 | 4.2 | 5.7 | 120W | Игры + работа (dual CCD) |

## 3D V-Cache

X3D-модели (7800X3D, 7950X3D) добавляют 64MB L3-кэша поверх одного CCD. Эффект: +15–25% в играх, чувствительных к latency (Factorio, WoW, MS Flight Simulator). Плата: сниженный тепловой порог (89°C throttle вместо 95°C) и ограниченный разгон.

## Memory Sweet Spot

Оптимальная частота DDR5 для Zen 4 — **DDR5-6000** при соотношении MCLK:UCLK = 1:1. Выше 6000 контроллер переходит в режим 1:2, что увеличивает latency. См. `../../concepts/memory-timings.md`.

## Источники

- AMD Zen 4 Architecture Deep Dive (Chips and Cheese, 2022)
- AMD Ryzen 7000 Reviewer's Guide
- Собственное тестирование лаборатории: 7800X3D в Cinebench R23 / игровых сценариях
