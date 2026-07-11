---
id: "cooling-index"
type: "index"
title: "Охлаждение"
status: "draft"
last_updated: "2025-06-03"
---

# Охлаждение

## Типы

| Директория | Тип | Принцип | Целевые CPU |
|---|---|---|---|
| `air/` | Воздушное | Теплотрубки + радиатор + вентилятор(ы) | До 200W TDP |
| `liquid/` | Жидкостное (AIO) | Помпа + радиатор + вентиляторы | 150W+ TDP, эстетика |

## Готовые entry

### Air
- `air/deepcool-ak400.md` — бюджетная башня, 4×6mm, 220W TDP, ~3 000 ₽
- `air/deepcool-ak620.md` — двухбашенный флагман, 6×6mm, 260W TDP, ~6 000 ₽

### Liquid
- `liquid/arctic-liquid-freezer-iii-240.md` — AIO 240мм, помпа в радиаторе, VRM-вентилятор, ~8 500 ₽
- `liquid/arctic-liquid-freezer-iii-360.md` — AIO 360мм, до 350W TDP, ~12 000 ₽

## Что ещё нужно заполнить

- **Air**: Thermalright Peerless Assassin, Noctua NH-D15 — топ-башни
- **Liquid**: Deepcool LT/LS — AIO-конкуренты

## Связи

- Тепловые пакеты CPU → `../cpu/`
- Требования к корпусу (клиренс, поддержка радиаторов) → `../case/`
- Бюджет мощности (помпа AIO) → `../../concepts/power-budget.md`
