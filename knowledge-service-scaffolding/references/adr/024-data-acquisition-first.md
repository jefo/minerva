---
id: adr-024
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [data-acquisition, etl, priority, coverage, manual-import, sources]
based_on: [adr-018, adr-023]
---

# ADR-024: Data Acquisition First — приоритет ETL над аналитикой

## Контекст

ADR-023 определил consumer-аналитику как цель. Но любой сценарий упирается в дефицит данных: покрытие 3/7 игр, exclusion карт из-за недостатка Observations.

Минимальное жизнеспособное покрытие для consumer-рекомендаций: 5 GPU × 7 игр × 1 пресет = 105 Observations. Текущее состояние: ~30 разрозненных Observations. Дефицит: ~75.

Без наполнения Warehouse аналитика бесполезна — каждый отчёт будет заканчиваться «покрытие: X/7 ⚠️».

## Решение

### Приоритет: Data Acquisition перед Consumer Analytics

```
Фаза 1: ETL Pipeline + Source Connectors   ← СЕЙЧАС
Фаза 2: Наполнение Warehouse (5 GPU × 12 obs)
Фаза 3: Consumer Analytics P1 (FPS/рубль)
Фаза 4: Consumer Analytics P2 (Upgrade path)
```

### Стратегия источников

#### Источник 1: TechPowerUp review pages (automated)

**Причина выбора:** один extraction = 12-15 структурированных Observations. Таблицы в HTML — парсинг, не transcription. Максимальная скорость наполнения.

**Source connector:** `techpowerup-review`
- URL → HTML-таблица → `acquisition/raw/techpowerup/{gpu}-review.yaml`
- Имена игр → bus-matrix resolution («CP 2077» → «cyberpunk-2077»)
- Значения FPS → unit-convert → numbers

**Охват за одну страницу:** 10-15 игр × 1-3 разрешения = 15-45 Observations.

**Приоритетные GPU для extraction:**

| Приоритет | GPU | Почему |
|---|---|---|
| 1 | RTX 5060 | Текущий фокус, флагман xx60-класса |
| 2 | RTX 4060 Ti | Прямой конкурент в бюджете до 35K |
| 3 | RX 9060 XT | AMD-конкурент, 16GB VRAM |
| 4 | RTX 4070 | Следующий класс, б/у-вариант |
| 5 | Arc B580 | Intel-альтернатива, бюджетный вариант |

После extraction: 5 GPU × 12 obs = 60 Observations → достаточное покрытие для consumer-рекомендаций.

#### Источник 2: YouTube benchmarks (manual import)

**Причина:** даёт игры, которые TechPowerUp не тестирует. Даёт 1% low (TechPowerUp часто даёт только avg). Но: видео-контент недоступен для модели. Импорт — вручную.

**YouTube-каналы и поисковые запросы:**

```
Каналы:
  - Hardware Unboxed
  - Gamers Nexus
  - Daniel Owen
  - Paul's Hardware
  - Ancient Gameplays (меньше известен, но детальные замеры)

Поисковые запросы (копировать в YouTube):
  - "RTX 5060 review benchmark"
  - "RTX 5060 vs RTX 4060 benchmark 1440p"
  - "RTX 5060 1440p gaming test"
  - "RTX 5060 frame time test"
  - "RTX 5060 1 percent low benchmark"
  - "RX 9060 XT vs RTX 5060 benchmark"
  - "Arc B580 1440p benchmark"
  - "RTX 4060 Ti 2026 benchmark update latest drivers"

Что искать в видео:
  - FPS avg + 1% low (не только avg)
  - 1440p High/Ultra (релевантное читателю разрешение)
  - Апскейлеры: DLSS on vs off (отдельные замеры)
  - VRAM usage в играх с высокими требованиями
  - Frametime графики для detection микро-статтеров

Приоритетные игры для заполнения coverage gaps:
  - Alan Wake 2 (RT + DLSS)
  - The Last of Us Part II
  - Starfield
  - Black Myth: Wukong
  - Monster Hunter Wilds
```

**Процесс manual import:**

Пользователь смотрит видео → извлекает FPS → заполняет шаблон → `manual-import` → Observation в Warehouse.

Шаблон для manual import:

```yaml
# acquisition/manual/{gpu}-{game}-{resolution}-{preset}.yaml
gpu: "nvidia-rtx-5060"
game: "cyberpunk-2077"
resolution: "1440p"
preset: "high"
source:
  type: "youtube"
  channel: "Hardware Unboxed"
  video_title: "RTX 5060 Review — 1440p Benchmarks"
  video_url: "https://youtube.com/watch?v=..."
  timestamp: "12:34"                 # где в видео показан результат
measures:
  fps_avg: 68
  fps_1pct_low: 52
  fps_0_1pct_low: null               # если не показано
conditions:
  upscaler: "DLSS 4 Quality"
  frame_gen: false
  ray_tracing: "High"
  driver_version: "572.16"           # если указано в видео
confidence: 0.85                     # 0.95 для своих замеров, 0.85 для ютуб-бенчмарков
```

#### Источник 3: Собственные замеры (manual import)

**Причина:** максимальная точность и контроль условий. Но: медленно. Один замер = 5-10 минут на игру.

**Приоритет:** только для игр с противоречиями между источниками («TechPowerUp даёт 68 fps, Hardware Unboxed — 72. Нужен третий замер»).

#### Источник 4: Ценовые данные (отдельный connector)

**Причина:** без цен consumer-аналитика невозможна. FPS/рубль, upgrade cost — все требуют актуальных цен.

**Source connector:** `price-aggregator` (DNS, Ситилинк, Яндекс.Маркет)
- Ручной ввод цен раз в неделю
- SCD Type 1 (overwrite)

### Что НЕ делаем сейчас

- **YouTube автоматический extraction.** Модель не умеет читать видео. Транскрипты дают речь, не таблицы FPS. YouTube — manual-only источник
- **Пользовательские сабмишны.** Требуют модерации и верификации. Будущее
- **API бенчмарк-сайтов.** Нет публичных API. Web scraping только

### KPI фазы 1

| Метрика | Текущее | Цель (конец фазы 1) |
|---|---|---|
| Observations в Warehouse | ~30 | 60+ |
| GPU с покрытием ≥5 игр | 2-3 | 5+ |
| Пересечение игр между GPU | 2-3 общих игры | 5+ общих игр |
| Готовность consumer-рекомендаций | ❌ exclusion для 50% карт | ✅ минимум 3 карты с полным покрытием |

## Последствия

**Что становится проще:**
- Скорость наполнения. TechPowerUp: 12 obs за extraction. Ручной ввод: 1 obs за замер
- Структура manual import: шаблон + поисковые запросы. Пользователь не гадает «что вводить» и «где искать»

**Что требует дисциплины:**
- Каждый manual import → валидация. Не «примерно 68 fps», а «68 fps, DLSS Q, драйвер 572.16»
- YouTube-замеры: confidence 0.85 (не свои данные). При противоречиях → свой замер
- Цены: еженедельное обновление. Без актуальных цен FPS/рубль — вредная цифра
