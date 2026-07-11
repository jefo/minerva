---
id: "psu-index"
type: "index"
title: "Блоки питания"
status: "draft"
last_updated: "2026-06-07"
---

# Блоки питания (PSU)

Актуальный стандарт — ATX 3.1 с 12V-2x6 для NVIDIA RTX 50xx. Все современные PSU — с активным PFC и DC-DC.

## Карта каталога

### Budget / Standard (active_standard)
Вентилятор всегда вращается. Для сборок, где цена/ватт важнее тишины.

- `deepcool-pf650.md` — DeepCool PF650 — 650W — ATX 2.4 — 80+ Bronze — ~6 000 ₽

### Mid-range Quiet (active_low_noise)
Тихий вентилятор (FDB/Hydro), но без fan-stop. Всегда вращается, но на низких оборотах (~20-22 dBA).

- `deepcool-pn750d.md` — DeepCool PN750D — 750W — ATX 3.1 — 80+ Gold — ~6 950 ₽
- `deepcool-pn850d.md` — DeepCool PN850D — 850W — ATX 3.1 — 80+ Gold — ~12 000 ₽

### Silent / Semi-Passive (semi_passive)
Fan-stop при низкой нагрузке → 0 dBA в простое. Для сборок с требованием тишины.

- `seasonic-focus-gx-650.md` — Seasonic Focus GX-650 — 650W — ATX 3.0 — 80+ Gold — ~9 000 ₽
- `be-quiet-pure-power-12m-750w.md` — be quiet! Pure Power 12M — 750W — ATX 3.1 — 80+ Gold — ~10 000 ₽
- `corsair-rm750e.md` — Corsair RM750e — 750W — ATX 3.0 — 80+ Gold — ~9 500 ₽
- `seasonic-focus-gx-750.md` — Seasonic Focus GX — 750W — ATX 3.0 — 80+ Gold — ~12 000 ₽
- `be-quiet-straight-power-12-750w.md` — be quiet! Straight Power 12 — 750W — ATX 3.1 — 80+ Platinum — ~16 000 ₽

### Flagship / Workstation (semi_passive, high wattage)
Для RTX 5080/5090 и круглосуточной нагрузки.

- `seasonic-prime-tx-850.md` — Seasonic Prime TX-850 — 850W — ATX 3.0 — 80+ Titanium — ~25 000 ₽
- `fsp-hydro-ptm-x-pro-1000w.md` — FSP Hydro PTM X Pro — 1000W — ATX 3.1 — 80+ Platinum — ~20 000 ₽

## Acoustic-легенда (как читать `acoustic_profile`)

| Класс | Ранг | Поведение | Idle шум | Load шум | Пример |
|---|---|---|---|---|---|
| `semi_passive` | 1 | Fan-stop при низкой нагрузке | 0 dBA | Низкий (FDB/Platinum) | Pure Power 12M, Seasonic GX |
| `active_low_noise` | 2 | Всегда вращается, тихий подшипник | ~20-22 dBA | Средний | DeepCool PN750D/850D |
| `active_standard` | 3 | Всегда вращается, обычный подшипник | ~25-28 dBA | Заметный | DeepCool PF650 |

**Правило фильтрации:** `max_acoustic_class="X"` пропускает все PSU с рангом ≤ ранга X.
- `"semi_passive"` → только fan-stop модели
- `"active_low_noise"` → semi_passive + active_low_noise
- `None` (без фильтра) → все

## Профили PSU

- **`atx_2x_budget_reliable`** — ATX 2.4, бюджетные Bronze-блоки. Для систем без мощных GPU (TGP < 200W). Риск: transient spike → OCP → выключение.
- **`atx_3x_transient_capable`** — ATX 3.x, Gold/Platinum. Держат пиковые нагрузки современных GPU. 12V-2x6 native.

## Что ещё нужно заполнить

- SFX: компактные корпуса
- 850W+ semi-passive (для RTX 5080 в тихих сборках)
- 1000W+ Gold/Platinum от других вендоров (Corsair, Seasonic, Thermaltake)

## Связи

- Бюджет мощности → `../../concepts/power-budget.md`
- Требования GPU → `../gpu/`
- Совместимость с корпусами → `../case/`
