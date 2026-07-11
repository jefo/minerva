---
id: "case-index"
type: "index"
title: "Корпуса"
status: "verified"
last_updated: "2026-06-04"
---

# Корпуса

## Карта

| Файл | Форм-фактор | Airflow | Цена | Ключевая особенность |
|---|---|---|---|---|
| `deepcool-cc560.md` | Mid Tower ATX | Высокий (mesh) | ~3 000 ₽ | 4 вентилятора в комплекте, клиренс кулера 155 мм ⚠️ |
| `be-quiet-pure-base-500.md` | Mid Tower ATX | Ограниченный (глухая) | ~7 500 ₽ | Битумная шумоизоляция, виброразвязка PSU |
| `fractal-define-7.md` | Mid Tower ATX | Ограниченный (глухая + ModuVent) | ~14 000 ₽ | Битумные маты все панели, 185 мм cooler |
| `be-quiet-dark-base-701.md` | Full Tower ATX | Высокий (mesh) + звукоизоляция | ~16 000 ₽ | 3× Silent Wings 4 140mm, mesh-перед |

## Параметры выбора

- **Форм-фактор MB** — ATX, MicroATX, Mini-ITX
- **Клиренс кулера** — высота (мм) для воздушного охлаждения (CC560: 155 мм — ограничение!)
- **Поддержка радиаторов** — сверху / спереди, размеры (оба: front 360, top 240)
- **Макс. длина GPU** — критично для RTX 4090 (340+ мм; CC560: 370 мм, PB500: 369 мм)
- **Airflow** — mesh-перед (CC560) vs глухая панель с шумопоглощением (Pure Base 500)
- **Профиль `sound_dampened_thermal_trap`** — Pure Base 500 (criteria_met: true), CC560 (criteria_met: false)
