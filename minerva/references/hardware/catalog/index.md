---
id: "catalog-root"
type: "index"
title: "Каталог компонентов"
status: "verified"
last_updated: "2026-06-03"
links:
  intents: "catalog/intents/index.md"
  profiles: "concepts/epistemological-profiles.md"
  modifiers: "concepts/modifiers.md"
  physical_stereotypes: "concepts/physical-stereotypes.md"
---

# Каталог компонентов

Корень knowledge base. Все компоненты ПК-железа, организованные по типу.
Каждый компонент — через Iron Man Argument (объективно, без хейта).

## ⚠️ ДИРЕКТИВА ДЛЯ LLM-АГЕНТА

При встрече ссылки вида **`path/to/file.md#section-name`**:
1. Загрузи файл через read_file
2. Найди секцию — извлеки конкретику
3. Не делай расчётов без загрузки данных по ссылке

## Структура

| Директория | Entry | Охват |
|---|---|---|---|
| `cpu/` | **22** | AMD Zen 4 (8) + Zen 5 (5) + Intel Arrow Lake (6) + Raptor Lake Refresh (3) |
| `gpu/` | **13** | NVIDIA 50xx (6) + 4060 + AMD RX 9000 (3) + 7600 + Intel Arc B (2) |
| `motherboard/` | **14** | AM5 (11): ProArt X870E, ProArt B650E, B650 Eagle, B650M S2H, B650 Tomahawk, B850 Riptide, B650E PG Riptide, B650 Creator, X870 Steel Legend, X670E Taichi, X670E Aorus Master. LGA1700 (3): ProArt Z790-E, Z790 Taichi, MEG Z790 Ace. | LGA1851: Z890 Pro RS |
| `memory/` | **5** | DDR5: обзор + Ripjaws S5 (6000 CL30) + 6400 CL32 + 5200 JEDEC + DDR5-5600 CL36 |
| `storage/nvme/` | **7** | NVMe: NV3 1TB, KC3000 1TB, 990 Pro 2TB, SN850X 2TB, T700 1TB, MP700 1TB, **T700 2TB** |
| `psu/` | **10** | Semi-passive (7): PP12M 750W, RM750e, Focus GX-650/750, Straight Power 12 750W, **Prime TX-850**, Hydro PTM X Pro 1000W. Active (3): PN750D, PN850D, PF650 |
| `cooling/` | **10** | Air (7): AK400, AK620, Dark Rock 4, Dark Rock TF 2, NH-C14S, NH-D15, NH-P1. Liquid (3): LF3 240, **LF3 280**, LF3 360 |
| `case/` | **4** | CC560, Pure Base 500, Define 7, Dark Base 701 |
| `audio-interface/` | **8** | RME (2), MOTU (2), Focusrite (2), UA Apollo (2) — T0-T3 |
| `intents/` | **6** | Esports 360Hz, AAA 4K, AI Inference, Data Eng, SFF Compact, **DAW Zero-DPC** |

**Всего: 94 entry + 6 интентов = 100 артефактов**

## Прогресс наполнения

- ✅ **GPU** — полная линейка NVIDIA 50xx, AMD RX 9000/7000, Intel Arc Battlemage
- ✅ **CPU** — все актуальные Zen 4, Zen 5, Arrow Lake + Raptor Lake Refresh (i5/i7/i9 14th Gen)
- ✅ **Материнские платы** — AM5 (8) + LGA1851 (1)
- ✅ **Память** — DDR5 (5) + DDR4-обзор
- ✅ **Накопители** — NVMe Gen4/Gen5 (6)
- ✅ **БП** — ATX 3.x (8) + ATX 2.x бюджет (1)
- ✅ **Охлаждение** — воздушное (7) + СЖО (3)
- ✅ **Корпуса** — бюджет mesh (1) + sound-dampened (3)
- ✅ **Аудиоинтерфейсы** — полный охват T0-T3 (8)
- ✅ **Интенты** — 6 полярных (esports, 4K, AI, data, SFF, **DAW**)

**Все категории покрыты!** DAW-домен: 33 новых entry + 3 концепта + 1 референс + 1 intent + 2 workload profiles. LGA1700 (3 MB) добавлен.

## Сквозные концепты

`../concepts/`:
- `epistemological-profiles.md` — словарь 26 поведенческих профилей v3.3
- `modifiers.md` — каталог модификаторов (+hardware_codec, +ecc, +dual_bios, +passive)
- `physical-stereotypes.md` — физические стереотипы (SFX, 8-layer PCB, ITX)
- `vrm-phases.md` — фазы питания, удвоители, real vs advertised
- `pcie-lanes.md` — линии PCIe, конфликты, sharing groups
- `memory-timings.md` — тайминги, ранги, MCLK:UCLK
- `power-budget.md` — бюджет мощности, пики потребления, ATX-спецификации
- `dpc-latency.md` — DPC Latency: классы, источники, измерение (аудио-домен)
- `audio-interface-drivers.md` — Driver Quality Taxonomy T0-T3
- `daw-acoustic-class.md` — A0_Studio: расширение акустической модели

## Скрипты

`../scripts/`:
- `query.py` — поиск по тегам, vendor, socket, price range
- `evaluate_profiles.py` — профильный движок (BLOCK/WARN/optimal)
- `validate_physical_constraints.py` — Skill 9: бинарные физические проверки
- `audit_tags.py` — проверка статических предикатов
