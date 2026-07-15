# CPU Benchmark — Business Roadmap

Запрос контент-отдела: каталог CPU, бенчмарки, Gaming Index, Relative Metrics.

План разбит на Deliverables. Каждый этап описывает: что контент-отдел сможет
производить, какой инженерный фундамент для этого строится, зависимости между
этапами.

---

## Deliverable 0: CPU Catalog

**Контент-отдел получает:** справочник процессоров. Страницы с характеристиками
(архитектура, ядра, частоты, кэш, TDP, сокет, поддерживаемая память) и связями
(CPU → Socket → Chipset, CPU → Architecture).

**Тип контента:** обзорная карточка процессора, spec-сравнение, «что нового
в поколении».

**Инженерный фундамент:** dimensions (реестр сущностей с атрибутами). CPU, Socket,
Architecture, Chipset как dimension types. Bus matrix как контракт.

**Зависимость:** ни от чего. Dimensions — автономный слой.

---

## Deliverable 1: CPU Evidence Model + Бенчмарки

### Что контент-отдел получает

**Цифры, не только спецификации.** Возможность писать обзор процессора с
реальными игровыми замерами: «7800X3D: 142 fps в Counter-Strike 2 (1080p Low),
frametime 6.2ms, GPU utilisation 97%».

**Single-CPU обзор** — жанр, который до этого этапа невозможен: нет данных.
После этапа — возможен для каждого процессора в каталоге.

### Какой инженерный фундамент строится

**Новый fact type `cpu_observation`** — потому что grain CPU-бенчмарка
отличается от GPU-бенчмарка:

| | GPU observation (существующий) | CPU observation (новый) |
|---|---|---|
| Grain | GPU × игра × разрешение × пресет × драйвер | CPU × игра × разрешение × пресет × **сценарий** × драйвер |
| Ключевая мера | fps_avg | fps_avg, frametime, gpu_utilization |
| Сценарий | Всегда GPU-bound (1440p Ultra) | CPU-bound (1080p Low), ST, MT |

**Новый dimension type `benchmark_scenario`** — потому что CPU ведёт себя
принципиально по-разному в разных сценариях. 7800X3D может доминировать в
1080p_low gaming, но проигрывать 245K в synthetic_mt. Без разделения по
сценариям сравнение CPU бессмысленно.

**Новые resolution dimensions** — 1080p, 720p. Сейчас есть только 1440p
(достаточно для GPU). CPU требует низких разрешений чтобы снять GPU-bound.

**Новые definitions** — frametime_ms_p99, gpu_utilization_pct, cpu_utilization_pct.
Меры, специфичные для CPU-бенчмаркинга.

**Наполнение данными** — 50-100 observation. Расчёт: 6 CPU × 10 игр × сценарий
1080p_low = 60 observation. Плюс выборочно synthetic и другие сценарии.
Источники: YouTube TechTubers, собственные замеры, TechPowerUp.

### Зависимости

- **От Deliverable 0:** dimensions для CPU должны существовать. CPU, Socket,
  Architecture — созданы. Игры — переиспользуем существующие, но список нужно
  расширить под CPU-bound тайтлы (CS2, Factorio, Stellaris, Cities Skylines 2,
  Baldur's Gate 3).
- **От внешних данных:** источники бенчмарков. Без них — архитектура готова,
  данных нет.

### Что НЕ входит в этот этап

- **Сравнение CPU друг с другом** — сравнение строит Deliverable 2 поверх данных
  этого этапа.
- **Gaming Index** — единая метрика требует semantic layer. Deliverable 3.
- **Цены и FPS/рубль** — нет источника цен. Deliverable 4.

---

## Deliverable 2: CPU Comparison

**Контент-отдел получает:** автоматизированные сравнительные таблицы.
«7800X3D vs 9800X3D vs 13400F в 1080p Low: кто быстрее по fps_avg и
frametime». Comparison без ручной работы редактора.

**Тип контента:** comparison articles, «какой CPU для 1440p», «поколение Zen 4
vs Zen 5».

**Инженерный фундамент:** расширение comparison capability — поддержка
dimension type `cpu`, фильтрация по `benchmark_scenario`.

**Зависимость:** Deliverable 1 (cpu_observation).

---

## Deliverable 3: Gaming Index

**Контент-отдел получает:** единую метрику для рейтингов. «7800X3D: Gaming
Index 178 (база 7600X = 100)». Контент-отдел оперирует индексом, не сырыми FPS.

**Тип контента:** рейтинги, «топ-5 игровых процессоров», «Gaming Index:
AMD vs Intel».

**Инженерный фундамент:** semantic layer. Definition `gaming-index.yaml` +
capability, вычисляющая индекс из cpu_observation по формуле:
`mean(fps_avg) по всем играм в 1080p_low, нормализация к baseline`.
Не хранится в данных — вычисляется late-binding при изменении выборки игр.

**Зависимость:** Deliverable 2 (comparison — для валидации индекса).

---

## Deliverable 4: FPS/Рубль + Рекомендации

**Контент-отдел получает:** ответ на главный читательский вопрос. «Лучший
игровой процессор до 30K — 7600X. При бюджете 40K — 7800X3D (+25% fps,
+30% цены)».

**Тип контента:** рекомендации, «сборка за N рублей», upgrade path.

**Инженерный фундамент:** price data (внешний источник), fps_per_ruble
definition, сравнение с price-фильтром.

**Зависимость:** Deliverable 3 (Gaming Index) + source цен (отсутствует).

---

## Карта зависимостей

```
Deliverable 0 (Catalog)
    ↓
Deliverable 1 (Evidence + Бенчмарки)  ← ближайший
    ↓
Deliverable 2 (Comparison)
    ↓
Deliverable 3 (Gaming Index)
    ↓
Deliverable 4 (FPS/Рубль)
```

Каждый этап — самостоятельный продукт для контент-отдела. Не требуется
завершения следующего этапа чтобы текущий давал результат.

---

## Ближайшее действие: Deliverable 1 kickoff

**Архитектура (зона minerva):**
- benchmark_scenario dimension type + bus matrix registration
- 1080p, 720p resolution dimensions
- cpu_observation fact type: grain, mandatory_dimensions, allowed_measures
- cpu-специфичные definitions (frametime, gpu_utilization)
- measure_definitions в bus matrix

**Данные (зона acquisition):**
- Список CPU сверх 5 (какие модели в приоритете)
- Источники бенчмарков: YouTube-каналы, платформы
- Приоритетные игры для 1080p_low (CPU-bound")
