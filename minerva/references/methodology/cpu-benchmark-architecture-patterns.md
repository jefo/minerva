# CPU Benchmark Architecture — методологические паттерны

Запрос контент-отдела: «CPU-каталог, бенчмарки, Gaming Index, Relative Metrics».
Ответ: «ничего не готово, берёмся». Под этим — строим не ad-hoc, а правильные
архитектурные решения.

Ниже — паттерны из data warehousing, которые применяются к этой задаче, как если бы
это был коммерческий production-проект.

---

## Паттерн 1: Grain Declaration First

Самая частая ошибка в DW — начать собирать данные до того как определена
гранулярность. Grain = что означает одна строка в факт-таблице. Это
фундаментальное решение Kimball: все dimensions должны быть определены на одном
уровне детализации.

**GPU benchmark grain (уже есть):**
```
Один GPU × одна игра × одно разрешение × один пресет × один драйвер
```

**CPU benchmark grain (нужно определить):**
```
Один CPU × одна игра × одно разрешение × один пресет × один сценарий × один драйвер
```

Отличие: появляется **сценарий** — новое mandatory dimension. Потому что CPU
проявляет себя по-разному в разных сценариях:

- `1080p_low` — CPU-bound gaming (снимаем GPU-bound, проявляем разницу CPU)
- `720p_low` — extreme CPU-bound (максимальная дельта между процессорами)
- `synthetic_1t` — однопоточный синтетический тест (Cinebench 1T, Geekbench ST)
- `synthetic_mt` — многопоточный синтетический тест (Cinebench nT, Geekbench MT)

**Почему это важно:** если смешать 1080p_low и 4K_ultra в одной таблице —
аналитика покажет мусор. На 4K все топ-процессоры +-5%, это GPU-bound, не CPU.

→ **Архитектурное решение:** новый fact type `cpu_observation` со своим grain и
mandatory dimensions.

---

## Паттерн 2: Conformed Dimensions

В DW dimensions переиспользуются между разными fact tables. Это называется
conformed dimensions — единый источник истины для сущности.

**Что переиспользуем из GPU-модели:**
- `game_title` — та же игра для CPU-бенчмарка
- `resolution` — 1080p, 720p (нужно добавить как dimensions)
- `graphics_preset` — Low, Medium
- `driver_version` — тот же драйвер (или для CPU — версия чипсета/AGESA/microcode)
- `cpu` — уже есть 5 процессоров

**Что добавляем нового:**
- `benchmark_scenario` — новый dimension type: 1080p_low, 720p_low, synthetic_1t,
  synthetic_mt, productivity, compilation

→ **Архитектурное решение:** не дублируем game_title, resolution. Расширяем
существующие dimensions где нужно (1080p, 720p), добавляем новый тип.

---

## Паттерн 3: Fact Table Type Selection

Kimball различает три типа факт-таблиц: transaction (каждое событие — строка),
periodic snapshot (состояние на момент времени), accumulating snapshot (процесс
с шагами).

**GPU observation → transaction grain.** Каждый замер — отдельная строка.
Агрегация (средний FPS по всем играм) — на уровне semantic layer.

**CPU observation → тот же паттерн.** Но с важным отличием: для CPU критичен
frametime consistency (1% low, 0.1% low, frame time variance), потому что CPU
определяет плавность, а не просто средний FPS. Меры для CPU шире:

```
gpu_observation: fps_avg, fps_1pct_low, fps_0_1pct_low
cpu_observation:  fps_avg, fps_1pct_low, fps_0_1pct_low,
                  frametime_ms_avg, frametime_ms_p99,
                  cpu_utilization_pct, gpu_utilization_pct
```

`gpu_utilization_pct` — ключевая CPU-метрика. Если GPU utilisation < 95% на 1080p
Low — процессор не успевает кормить карту. Это и есть CPU bottleneck.

→ **Архитектурное решение:** новый fact type в bus matrix, расширенный набор
allowed_measures, новый measure_definition для cpu-специфичных метрик.

---

## Паттерн 4: Semantic Layer — Late-Binding

В DW метрики не хранятся в факт-таблицах. Они вычисляются в semantic layer
поверх сырых данных. Это называется late-binding: привязка бизнес-логики к
данным происходит в момент запроса, не в момент загрузки.

**Gaming Index** — это не observation. Это derived metric:

```
Gaming Index(CPU) = mean(fps_avg) по всем играм в сценарии 1080p_low,
                    нормализованное относительно baseline (например, 7600X = 100)
```

**Почему не хранить как observation:**
- Состав игр изменится → индекс пересчитывается
- Baseline изменится → пересчитывается
- Добавилась новая игра → пересчитывается

→ **Архитектурное решение:** Gaming Index = definition в `warehouse/definitions/`
+ capability, вычисляющая его из сырых cpu_observation. Не храним, вычисляем.

---

## Паттерн 5: Coverage-Driven Incremental Build

В production-DW никто не заполняет «все CPU × все игры × все сценарии». Это
комбинаторный взрыв. Вместо этого:

1. Определяется business question: «какой CPU лучше для гейминга за 30K»
2. Из вопроса выводится coverage target: 5 целевых CPU, 10 ключевых игр, сценарий 1080p_low
3. Заполняется coverage target — не больше
4. Gap analysis показывает что закрыто, что нет

Это coverage-driven approach: метрика покрытия управляет приоритетами acquisition.

**Для контент-отдела:** не «собрать все бенчмарки всех процессоров», а
«закрыть Gaming Index для топ-6 CPU в 10 играх на 1080p Low». Это achievable
за дни, не за месяцы.

→ **Архитектурное решение:** переиспользовать coverage-matrix capability,
расширив под cpu_observation.

---

## Паттерн 6: Source-System Independence

В DW данные из разных source systems нормализуются к единой модели. Source
system не диктует структуру DW.

CPU-бенчмарки приходят из разных источников:
- YouTube-видео (ручной импорт)
- TechPowerUp / Tom's Hardware (парсинг)
- Собственные замеры (manual)

Но в DW они все выглядят одинаково: `cpu_observation` с единым grain,
source_url, confidence. Разные источники → разный confidence, но одинаковая
структура.

→ **Архитектурное решение:** fact-insert как ingestion gateway. Неважно откуда
данные — контракт един.

---

## Паттерн 7: Relative Metrics = Comparison Over Baseline

Relative Performance («насколько 7800X3D быстрее 7600X») — это не новый
fact type. Это comparison capability, применённый к cpu_observation.

Но для CPU comparison сложнее чем для GPU: сценарий имеет значение. «7800X3D
быстрее 7600X» — в каком сценарии? 1080p_low gaming? synthetic_mt?
Ответ может быть противоположным для разных сценариев.

→ **Архитектурное решение:** comparison capability должен принимать filter по
dimensions. `comparison(dim_a="7800X3D", dim_b="7600X", filter={scenario: "1080p_low"})`.

---

## Порядок архитектурных решений (зависимости)

```
1. benchmark_scenario dimension    ← новый dimension type
2. 1080p, 720p resolution dims     ← расширение существующего
3. cpu_observation в bus matrix    ← новый fact type с grain, mandatory dims, allowed measures
4. cpu-специфичные definitions     ← frametime, gpu_utilization, gaming_index
5. coverage matrix для CPU         ← расширение coverage-matrix capability
6. Gaming Index definition + computation  ← semantic layer
7. Ingestion: первые 50-100 cpu_observation ← наполнение
```

Шаги 1-5 — architecture. Шаг 6 — semantic layer. Шаг 7 — data.

**Ключевое:** Gaming Index и Relative Performance — самые дальние шаги (6-7).
Нельзя начать с них. Сначала grain, dimensions, fact type, definitions.
Фундамент перед витриной.
