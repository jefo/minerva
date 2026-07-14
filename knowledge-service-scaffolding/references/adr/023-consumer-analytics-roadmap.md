---
id: adr-023
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [consumer-analytics, roadmap, comparison, recommendation, upgrade-path, bottleneck, vram-forecast]
based_on: [adr-015, adr-016, adr-019, adr-022]
---

# ADR-023: Consumer Analytics Roadmap — масштабирование аналитики для читателя

## Контекст

Инженерная аналитика (Laws, architectural tensions, design tradeoffs) закрыта предыдущим движком. Теперь задача — масштабировать аналитику для consumer-вопросов: выбор карты под бюджет, сравнение конкурентов, апгрейд, совместимость сборок.

Consumer-аналитика отличается от инженерной:
- **Инженерная:** «почему RTX 5060 такая» — одна карта, её архитектурные решения
- **Consumer:** «какую карту купить за 30K для 1440p» — выбор из десятков карт по критериям читателя

## Решение

### Семь типов consumer-аналитики

#### 1. Кросс-GPU сравнение по сценариям читателя

**Текущее состояние:** редактор вручную выбирает с чем сравнивать (предшественник, конкурент).

**Целевое:** система автоматически определяет релевантных конкурентов и строит сравнение под сценарий.

| Сценарий читателя | Какие GPU сравнивать | Метрики | Готовность |
|---|---|---|---|
| «Бюджет X, разрешение Y» | Все карты в ценовой категории ±20% | FPS, FPS/рубль, VRAM, DLSS/FSR | 70% |
| «Обновляюсь с карты Z» | Z vs текущее поколение vs прошлое поколение | Прирост FPS, цена обновления | 60% |
| «Хочу 4K за минимальные деньги» | Карты с VRAM ≥ 12GB до ценового порога | FPS в 4K, DLSS/FSR, VRAM headroom | 50% |
| «Собираю ПК за бюджет B» | Связки CPU+GPU в бюджете | FPS, GPU utilisation | 40% |

**Требует:** правила конкурентного анализа. «Конкуренты = карты в ценовом диапазоне ±20% с VRAM ≥ требованию сценария».

#### 2. FPS/рубль с поправками

**Текущее состояние:** FPS/рубль не вычисляется. Цена не в Warehouse.

**Целевое:** FPS/рубль с поправками на разрешение, VRAM pressure и DLSS availability.

**Поправки:**
- **Разрешение:** только для разрешения читателя (не средний FPS по всем)
- **VRAM pressure:** если 1% low < 30 fps из-за VRAM → карта исключена из рекомендации
- **DLSS availability:** отдельные оценки native и DLSS FPS/рубль
- **Цена в регионе:** розничная, не MSRP

**Требует:** price data source (acquisition connector). Derived Metric: `fps_per_ruble`.

#### 3. Coverage-driven recommendations

**Текущее состояние:** Coverage View (ADR-015) спроектирован, но не интегрирован в recommendations.

**Целевое:** каждая рекомендация включает coverage statement.

```
«RTX 5060: лучшая карта до 35K для 1440p.
 FPS/рубль: 3.1. Покрытие: 7/9 целевых игр.
 Нет данных: Alan Wake 2, TLOU2.
 Альтернатива: RX 9060 XT (2.9 FPS/рубль, покрытие 8/9).»
```

**Требует:** интеграция coverage-view в вывод recommendation.

#### 4. Upgrade path analysis

**Текущее состояние:** `comparison` двух GPU есть. Стоимость апгрейда — нет.

**Целевое:** прирост FPS на каждый потраченный рубль апгрейда.

| Сейчас | Апгрейд | Прирост FPS | Цена апгрейда | FPS/рубль апгрейда | Вердикт |
|---|---|---|---|---|---|
| RTX 3060 (45 fps) | RTX 5060 (68 fps) | +51% | 18K (новая − продажа старой) | 1.28 | «Стоит» |
| RTX 4060 (52 fps) | RTX 5060 (68 fps) | +30% | 17K | 0.94 | «Не стоит — подождать 5060 Super» |

**Требует:** SCD Type 1 трекинг цены. Derived Metric: `upgrade_fps_per_ruble` = (FPS_new − FPS_old) / (price_new − resale_old).

#### 5. Bottleneck detection для сборок

**Текущее состояние:** CPU+GPU Observations отсутствуют. Нет данных о GPU utilisation в паре.

**Целевое:** для пары CPU+GPU → GPU utilisation %. Если < 90% → bottleneck warning.

**Требует:** Observations с GPU utilisation метрикой. Relation: CPU → GPU pairing. Самый дорогой в сборе данных.

#### 6. VRAM adequacy forecast

**Текущее состояние:** SCD Type 2 есть (историчность). VRAM requirement trend — нет.

**Целевое:** прогноз достаточности VRAM на 1-2 года вперёд.

```
«VRAM requirements trend (2020-2026):
  2020: 4GB → 2022: 6GB → 2024: 8GB → 2026: 10GB (forecast).
  RTX 5060 (8GB): достаточно до середины 2027.»
```

**Требует:** historical VRAM requirements (SCD-tracked). Forecasting model (linear+).

#### 7. Персонализированные рекомендации

**Текущее состояние:** AI Data Analyst Agent (ADR-022) спроектирован. Не реализован.

**Целевое:** читатель → «играю в X, Y, Z на 1440p, бюджет B» → система → «твоя карта — RTX 5060. Вот почему. Вот альтернативы. Вот что потеряешь если сэкономишь.»

**Требует:** AI Data Analyst + intent routing. Комбинация всех предыдущих аналитик под конкретного читателя.

### Дорожка: приоритет по ценности для читателя

| Приоритет | Аналитика | Поисковый запрос читателя | Готовность minerva | Что достроить |
|---|---|---|---|---|
| **P1** | FPS/рубль с coverage | «лучшая карта до 35K 1440p» | 50% | Price data source. fps_per_ruble. Интеграция coverage |
| **P2** | Upgrade path | «стоит ли обновляться с RTX 3060» | 60% | SCD-трекинг цены. upgrade_fps_per_ruble |
| **P3** | Bottleneck detection | «какой CPU для RTX 5060» | 40% | CPU+GPU Observations. GPU utilisation метрика |
| **P4** | VRAM forecast | «хватит ли 8GB в 2027» | 30% | Historical VRAM requirements. Forecasting |
| **P5** | Персонализированные рекомендации | «во что играть на RTX 5060 1440p» | 20% | AI Data Analyst (ADR-022). Intent routing |

### Что дать первым

**P1: FPS/рубль с coverage** — 80% поисковых запросов. Покрывается `comparison` + Coverage View + price data. Самая высокая готовность к реализации.

**P2: Upgrade path** — второй по частоте вопрос. `comparison` + SCD-трекинг цены + derived metric. Достраивается на фундаменте P1.

**P3–P5** — требуют данных, которых ещё нет в Warehouse. Отложены до наполнения данными.

## Последствия

**Что становится проще:**
- Consumer-вопросы получают количественные ответы, не «экспертное мнение»
- Coverage прозрачен: читатель видит где данных достаточно, где нет
- Upgrade path заменяет «ну это смотря с чем сравнивать» на конкретную цифру прироста на рубль

**Что требует данных, которых пока нет:**
- Price data source (acquisition connector к ценовым агрегаторам)
- CPU+GPU pairing Observations (самый дорогой сбор данных)
- Historical VRAM requirements (5+ лет назад)
