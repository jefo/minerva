---
name: build-economics
description: "Экономика сборки — стоимость владения инженерной стратегией. 9-section анализ: входной билет, структура бюджета, игровое ядро, визуальный слой, потенциал платформы, следующий апгрейд, ликвидность, риск устаревания, экономический диагноз."
type: capability
triggers:
  - "экономика сборки"
  - "стоимость владения"
  - "бюджет сборки"
  - "стоимость апгрейда"
  - "цена платформы"
  - "TCO сборки"
  - "экономический диагноз"
  - "стоимость игрового ПК"
  - "финансовая стратегия сборки"
---

# Build Economics — Capability

Оценивает не производительность ПК, а **стоимость владения выбранной инженерной стратегией**.

Ответ не «покупать или нет». Ответ — «какую финансовую стратегию реализует эта сборка».

## Три слоя движка

**Compute Layer** (детерминированный): цены из источников, совместимость, стоимость апгрейда. Данные: Minerva dim/ + pricing warehouse.
**Classification Layer** (model-based): gaming core vs visual layer, категории бюджета. Model training data.
**Strategic Layer** (pure reasoning): ликвидность, риск устаревания, экономический диагноз. Интеграция с forecast-lifecycle.

## Price Source Strategy

Трёхуровневый фолбэк:
- Tier 1: `warehouse-pricing` (retail, confidence 0.90+) — когда наполнен
- Tier 2: Model MSRP (training data, confidence 0.70) — текущий режим
- Tier 3: User input (`custom_prices`, confidence 1.00)

## Process

### 1. Anchor: Minerva
Загрузить `dim/cpu/{id}.yaml`, `dim/gpu/{id}.yaml`, `dim/socket/{id}.yaml`.

### 2. Разрешить конфигурацию
Если пользователь не указал MB, RAM, cooler, PSU, storage — подобрать разумные default'ы под платформу.

### 3. Compute Layer (§1, §5, §6)
- §1: `platform_cost = cpu + mb + ram + cooler` (без GPU — платформа определяет апгрейды)
- §5: max CPU на сокете, next-gen support, нужно ли менять память/плату
- §6: что менять через 2-3 года, стоимость апгрейда

### 4. Classification Layer (§2, §3, §4)
- §2: разложить бюджет по подсистемам, найти перекосы
- §3: gaming_core = CPU + GPU + RAM. Стоимость FPS-влияющих компонентов.
- §4: visual_layer = ARGB, AIO vs air, glass case, etc. «Сколько ушло на внешний вид». Model-based классификация с rationale.

### 5. Strategic Layer (§7, §8, §9)
- §7: ликвидность — model-based. Факторы: популярность сокета, lifecycle, тип памяти, бренд.
- §8: риск устаревания — что bottleneck первым. Интеграция с forecast-lifecycle.
- §9: экономический диагноз — synthesis. «Эта сборка реализует стратегию X». Не «покупать/не покупать».

### 6. Price provenance
Каждая цена маркируется: `pricing_warehouse | model_msrp | user_input`. Без provenance — ошибка.

## Output

Полный контракт: `references/build-economics-contract.yaml`. 9 секций.

## Pitfalls

1. Все цены — с provenance. Не выдумывать.
2. Platform lifecycle критичен. LGA1700 legacy → стоимость апгрейда = CPU + MB + RAM.
3. Классификация visual layer требует rationale — показать что именно и почему не влияет на FPS.
4. Экономический диагноз ≠ «покупайте». Описывает стратегию.
5. Model MSRP ±20% от street price. Дисклеймер обязателен.
