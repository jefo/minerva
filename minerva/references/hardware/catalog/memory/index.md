---
id: "memory-index"
type: "index"
title: "Оперативная память"
status: "verified"
last_updated: "2026-06-03"
---

# Оперативная память (RAM)

Актуальные стандарты — DDR5 (AM5/LGA1851) и DDR4 (бюджетные LGA1700). DDR4 сохраняет релевантность для бюджетных сборок на Alder Lake/Raptor Lake — разница <3% FPS при +65% цены DDR5.

## Карта

### DDR5

| Файл | Тип | Частота | Тайминги | Объём | Цена (₽) |
|---|---|---|---|---|---|
| `ddr5.md` | DDR5-обзор | — | — | — | Обзор стандарта |
| `ddr5-6400-cl32.md` | DDR5 | 6400 MT/s | CL32 | 2×16 GB | ~12 500 |
| `gskill-ripjaws-s5-ddr5-6000-32gb.md` | DDR5 | 6000 MT/s | CL30 | 2×16 GB | ~10 200 |
| `ddr5-5600-cl36.md` | DDR5 | 5600 MT/s | CL36 | 2×16 GB | ~7 000 |
| `ddr5-5200-jedec.md` | DDR5 | 5200 MT/s | CL40 | 2×16 GB | ~7 500 |
| `apacer-nox-ddr5-5200-32gb.md` | DDR5 | 5200 MT/s | CL40 | 1×32 GB | ~35 000 |

### DDR4

| Файл | Тип | Частота | Тайминги | Объём | Цена (₽) |
|---|---|---|---|---|---|
| `ddr4-3200-cl16-32gb.md` | DDR4 | 3200 MT/s | CL16 | 2×16 GB | ~5 800 |
| `ddr4-3600-cl18-32gb.md` | DDR4 | 3600 MT/s | CL18 | 2×16 GB | ~6 500 |

## Sweet spots

- **AM5 гейминг** → DDR5-6000 CL30 (1:1 Infinity Fabric)
- **LGA1700 бюджет** → DDR4-3200 CL16 (sweet spot Alder Lake, <3% FPS loss vs DDR5)
- **LGA1700 DDR5** → DDR5-5600 CL36 (JEDEC-стабильность)

## Связи

- Совместимость с CPU → `../cpu/`
- Совместимость с MB → `../motherboard/`
- Тайминги и ранги → `../../concepts/memory-timings.md`
