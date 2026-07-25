---
name: build-economics
description: "Экономика сборки — стоимость владения инженерной стратегией. 9-section анализ: входной билет, структура бюджета, игровое ядро, визуальный слой, потенциал платформы, следующий апгрейд, ликвидность, риск устаревания, экономический диагноз."
type: capability
capability:
  input:
    cpu_id: "string — Minerva dim ID (обязательный)"
    gpu_id: "string — Minerva dim ID (обязательный)"
    motherboard_chipset: "string — e.g. 'B760', 'X670E'. Default: inferred from socket + reasonable mid-range"
    ram_spec: "string — e.g. '32GB DDR5-6000'. Default: 2×16GB DDR5-6000"
    cooler_type: "string — 'air'|'aio-240'|'aio-360'|'custom'. Default: 'air'"
    case_form_factor: "string — 'atx'|'matx'|'itx'. Default: 'atx'"
    case_aesthetic: "string — 'functional'|'glass'|'premium'. Default: 'functional'"
    aesthetic_choices: "list — ['argb-fans', 'argb-ram', 'aio-upgrade', 'glass-case', 'cable-mod', 'rgb-strips']"
    psu_wattage: "integer — Default: computed from CPU+GPU TDP with headroom"
    storage_spec: "string — e.g. '1TB NVMe'. Default: '1TB NVMe Gen4'"
    custom_prices: "map — user price overrides: {cpu: N, gpu: N, motherboard: N, ram: N, cooler: N, case: N, psu: N, storage: N}"
    target_currency: "string — 'rub'|'usd'. Default: 'rub'"
  output: "BuildEconomics (YAML) — 9-section economic profile"
  invariants:
    - "Цены всегда имеют provenance: pricing_warehouse | model_msrp | user_input"
    - "Классификация gaming_core vs visual_layer — model-based, с explicit rationale"
    - "Platform data из Minerva dim/socket — не выдумывать совместимость"
    - "Если pricing warehouse пуст — model MSRP с confidence 0.70 и явным дисклеймером"
    - "§8 (obsolescence risk) интегрируется с forecast-lifecycle для CPU/GPU bottleneck prediction"
    - "§9 (economic diagnosis) — не «покупать/не покупать», а «какую стратегию реализует сборка»"
  pitfalls:
    - "Не выдумывать цены без provenance. Если данных нет — model_estimate + confidence."
    - "Не игнорировать platform lifecycle. LGA1700 = legacy → стоимость следующего апгрейда выше."
    - "Не путать «цена покупки» и «цена владения». TCO включает апгрейды."
    - "Не давать вердикта «хорошая/плохая сборка». Экономический диагноз описывает стратегию."
    - "Не забывать про совместимость памяти. DDR4 vs DDR5 на LGA1700 — разная стоимость."
  triggers:
    - "экономика сборки"
    - "стоимость владения"
    - "бюджет сборки"
    - "стоимость апгрейда"
    - "цена платформы"
    - "TCO"
    - "экономический диагноз"
    - "стоимость игрового ПК"
    - "финансовая стратегия сборки"
---

# Build Economics — Capability

Оценивает не производительность ПК, а **стоимость владения выбранной инженерной стратегией**.

Ответ не «покупать или нет». Ответ — «какую финансовую стратегию реализует эта сборка».

## Model

### Core concept

Сборка ПК — это не набор компонентов, а **инженерно-финансовая стратегия**. Каждая стратегия имеет:
- Стоимость входа (entry ticket)
- Структуру капитала (куда ушли деньги)
- Потенциал (что можно сделать на этой платформе)
- Обязательства (сколько будет стоить следующий шаг)
- Риски (что устареет первым, сколько потеряет в цене)

Финансовая стратегия ≠ «бюджетная/дорогая». Это:
- «Максимальный FPS на рубль сейчас — апгрейд через 3 года» (AMD AM5, воздух, functional case)
- «Премиум-платформа с запасом на 5-7 лет без замен» (high-end CPU, DDR5-6000+, AIO)
- «Минимальный вход сейчас — полная замена платформы потом» (LGA1700, DDR4, stock cooler)

### Три слоя движка

```
                    ┌──────────────────────────────┐
Minerva dim/        │  COMPUTE LAYER               │
  cpu, gpu, socket  │  - Цены из источников        │
Minerva pricing     │  - Совместимость              │  → Секции 1, 5, 6
  warehouse (TBD)   │  - Стоимость апгрейда         │
                    └──────────────────────────────┘
                                      │
                    ┌──────────────────────────────┐
Model training      │  CLASSIFICATION LAYER        │
  data              │  - gaming_core vs visual      │  → Секции 2, 3, 4
                    │  - Категории бюджета          │
                    │  - Model-based с rationale    │
                    └──────────────────────────────┘
                                      │
                    ┌──────────────────────────────┐
Model reasoning     │  STRATEGIC LAYER             │
  + forecast-       │  - Ликвидность               │
  lifecycle         │  - Риск устаревания           │  → Секции 7, 8, 9
                    │  - Экономический диагноз      │
                    └──────────────────────────────┘
```

## Price Source Strategy

Трёхуровневый фолбэк:

| Tier | Источник | Confidence | Когда |
|---|---|---|---|
| 1 | `warehouse-pricing` (retail) | 0.90+ | Когда склад наполнен |
| 2 | Model MSRP (training data) | 0.70 | Текущий режим |
| 3 | User input (`custom_prices`) | 1.00 | Когда пользователь указал |

**Model MSRP coverage (training data):**
- CPU: MSRP at launch — высокая точность (±$10-15)
- GPU: MSRP at launch — средняя (±$30-50, зависит от AIB)
- MB: Typical price by chipset tier (H610 ~$80, B760 ~$130, Z790 ~$200) — средняя
- RAM: Market price by type/capacity/speed — средняя (±$15-30)
- Cooler: Air ($30-50), AIO-240 ($80-120), AIO-360 ($130-180) — средняя
- Case: Functional ($50-70), Glass ($80-120), Premium ($150+) — средняя
- PSU: By wattage and tier — средняя (±$20-40)
- Storage: 1TB NVMe Gen4 ~$60-80 — средняя

Все model MSRP цены маркируются `price_source: model_msrp` и `confidence: 0.70`.

## Process

### 1. Anchor: загрузить Minerva

```
dim/cpu/{id}.yaml → архитектура, сокет, ядра, частоты, TDP, MSRP, release
dim/gpu/{id}.yaml → архитектура, VRAM, TDP, DLSS gen, MSRP, release
dim/socket/{id}.yaml → lifecycle, max CPU, upgrade_note, compatible_memory
```

### 2. Разрешить конфигурацию

Если пользователь не указал MB, RAM, cooler, PSU, storage — подобрать разумные default'ы:
- **MB:** чипсет среднего сегмента под сокет (B760 для LGA1700, B650 для AM5)
- **RAM:** 2×16GB, DDR5 для AM5/LGA1851, DDR5 для LGA1700 (новые сборки)
- **Cooler:** air для CPU ≤105W TDP, AIO-240 для >105W
- **PSU:** CPU TDP + GPU TDP + 100W headroom, bronze/gold
- **Case:** functional ATX
- **Storage:** 1TB NVMe Gen4

### 3. Compute Layer

**§1 — Entry Ticket (стоимость платформы без GPU):**
```
platform_cost = cpu_price + mb_price + ram_price + cooler_price
```
Почему без GPU: платформа определяет апгрейды. GPU меняется независимо.

**§5 — Platform Potential:**
```
max_cpu = dim/socket.lifecycle.supported_cpu_generations → best CPU
next_gen_support = socket successor exists? → yes/no
memory_change_needed = current RAM type compatible with next socket?
```

**§6 — Next Upgrade:**
Для каждого компонента: нужно ли менять при апгрейде через 2-3 года?
```
cpu → менять? да (если хотим CPU-апгрейд на этом сокете — но legacy платформы dead end)
mb → менять? да (если новый сокет)
ram → менять? зависит от перехода DDR4→DDR5
gpu → менять? опционально (GPU независим)
cost = сумма заменяемых компонентов
```

### 4. Classification Layer

**§2 — Budget Structure:**
Разложить все компоненты по подсистемам: CPU, GPU, платформа, хранение, корпус+охлаждение, питание.

**§3 — Gaming Core:**
Компоненты влияющие на FPS: CPU + GPU + RAM. Их суммарная стоимость.
Сравнивает «чистые» игровые стратегии — сколько ушло на fps, а не на антураж.

**§4 — Visual Layer:**
Компоненты НЕ влияющие на FPS. Model-based classification:
- `argb-fans` → доплата $30-50 vs non-RGB
- `aio-upgrade` → доплата $50-80 vs air (при air-достаточности)
- `glass-case` → доплата $30-50 vs closed
- `rgb-ram` → доплата $10-20 vs non-RGB
- `custom-cables` → доплата $30-60

Вывод: «N рублей ушло не на FPS, а на внешний вид».

### 5. Strategic Layer

**§7 — Liquidity:**
Model-based assessment. Факторы:
- Популярность платформы на вторичке
- Сокет lifecycle (active > legacy > eol)
- Тип памяти (DDR5 ликвиднее DDR4 в 2026+)
- Бренд CPU (AMD X3D → высокая ликвидность)
- Класс GPU (mid-range ликвиднее high-end)

**§8 — Obsolescence Risk:**
Интеграция с forecast-lifecycle:
- Что станет bottleneck первым? CPU или GPU?
- Per-genre: где CPU умрёт раньше?
- Упрощённая версия lifecycle forecast (без полного Monte Carlo)

**§9 — Economic Diagnosis:**
Pure reasoning. Не verdict, а стратегия:
- «Эта сборка реализует стратегию "минимальный вход сейчас — полная замена через 3 года"»
- «Стратегия "платформа с запасом на 5+ лет, GPU-апгрейд через 2-3 года"»
- «Высокая стоимость визуального слоя (N%) снижает FPS/₽, но реализует стратегию "покупка для души"»

## Output Contract

См. `references/build-economics-contract.yaml`.

## Integration Points

| Capability | Что даёт |
|---|---|
| Minerva dim/ | CPU/GPU/socket спецификации, lifecycle, MSRP |
| warehouse-pricing | Реальные розничные цены (Tier 1) |
| forecast-lifecycle | Per-genre bottleneck prediction для §8 |
| pc-parts-price-check | Актуальные розничные цены (внешний запрос) |

## Pitfalls

1. **Цены без provenance — красный флаг.** Всегда маркировать источник цены.
2. **Не путать MSRP и street price.** MSRP at launch — база. Реальная цена — ±20% для GPU.
3. **Platform lifecycle критичен для TCO.** LGA1700 legacy → стоимость следующего шага = CPU + MB + возможно RAM. AM5 active → может быть только CPU.
4. **Классификация visual layer требует rationale.** Просто сказать «доплата X» недостаточно — нужно показать что именно и почему не влияет на FPS.
5. **Экономический диагноз ≠ рекомендация.** «Стратегия максимального FPS/₽» — описание. «Покупайте эту сборку» — нарушение контракта.
