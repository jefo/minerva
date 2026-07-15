---
id: adr-030
status: proposed
date: 2026-07-14
tags: [tech-debt, data-debt, lineage, catalog, capabilities, warehouse-model, semantic-layer, decision-engine]
based_on: [adr-014, adr-015, adr-016, adr-017, adr-019, adr-023, adr-025, adr-026, adr-027, adr-028, adr-029]
---

# ADR-030: Tech Debt & Data Debt Register — оценка через бизнес-ценности DW

## Контекст

R&D-сессия с консультантом по требованиям к бекенду выявила 6-слойную архитектуру:

```
5. Warehouse Model   — сущности (CPU, GPU, Socket, Architecture, Game, Price, Store)
                       и связи между ними. DW знает что существует, но не знает что лучше.
6. Semantic Layer    — вычисляемые метрики (Average FPS, Average Price, Relative Performance).
                       Объективны, определены один раз, переиспользуемы.
```

Плюс три сквозных принципа:
- **Lineage** — любой показатель можно раскрутить назад до Source (Decision → Evidence → Observation → Reviewer → Дата теста)
- **Data Catalog** — все сущности описаны: владелец, источник, версия, дата обновления
- **Evidence Warehouse vs Decision Warehouse** — Evidence (измерения) и Decision (выводы) — разные слои. Decision не хранится в Warehouse, он строится поверх него.

И Knowledge Refinement Pipeline (7 слоёв):
```
Raw Data → Canonical Facts → Evidence → Derived Metrics → Decision → Explanation → Reader Experience
```

Из этих семи слоёв в minerva реализованы только первые три (Raw Data → Canonical Facts → Evidence), и то частично.

Этот ADR фиксирует:
1. **Tech debt** — архитектурные решения, принятые в предыдущих ADR, но не реализованные (promises made, promises not kept)
2. **Data debt** — неполнота наполнения в существующих структурах (пустые слоты в контрактах)
3. **Оценку ADR-019** (Agent Query Model) — через призму бизнес-ценностей
4. **Новые архитектурные концепты** (Catalog, Decision lineage, Evidence/Decision split)

---

## Часть 1. Business Value Framework

Каждый architectural gap оценивается через бизнес-вопрос, на который система НЕ может ответить.

### Бизнес-вопросы читателя ИгроЛабы

| # | Вопрос читателя | Какой слой должен ответить | Статус |
|---|---|---|---|
| Q1 | «Какую карту купить за 30K для 1440p?» | Semantic Layer (FPS/рубль) + Decision Engine | ❌ Не отвечен |
| Q2 | «Почему вы рекомендуете именно эту карту?» | Lineage (Decision → Evidence → Source) | ❌ Не проследить |
| Q3 | «Что лучше: 5060 Ti или 4070 Super для моих игр?» | Semantic Layer (comparison) + Evidence | 🟡 Частично — данные есть, сравнения нет |
| Q4 | «Эта рекомендация ещё актуальна? Вышел новый драйвер.» | stale-check + impact-analysis | ❌ Не проверяется |
| Q5 | «Какой процессор взять под эту карту?» | Warehouse Model (CPU entities + связи) | ❌ Нет CPU в системе |
| Q6 | «Сколько стоит сборка целиком?» | Warehouse Model (CPU + Motherboard + Memory + Price) | ❌ Нет данных |

---

## Часть 2. Tech Debt Register

Tech debt = архитектурное решение в ADR принято, но не реализовано. Оценивается через бизнес-последствие.

### Слой 5 — Warehouse Model (Entities + Связи)

**Текущее состояние:** 5 типов dimensions с атрибутами (GPU, game_title, resolution, graphics_preset, driver_version). GPU-сущности имеют vendor, architecture, lithography, vram, compute, power — частично заполнены. Связей между сущностями нет (GPU не связан с Architecture как отдельной сущностью).

**Что зафиксировано в ADR, но не реализовано:**

| Архитектурный долг | ADR | Бизнес-последствие |
|---|---|---|
| CPU как entity | 027 | Нельзя ответить Q5 («какой процессор под карту»). Нельзя строить сборки. |
| Socket как entity | — | Нельзя сказать «этот CPU требует этот сокет, эти чипсеты». Невозможна проверка совместимости. |
| Architecture как entity | — | Нельзя группировать: «все GPU на RDNA 4», «все CPU на Zen 5». Architecture сейчас — атрибут, не сущность. |
| Motherboard / Chipset | — | Нельзя посчитать стоимость платформы. Сборка без материнки — не сборка. |
| Memory (RAM) | — | Нельзя сказать «этот CPU поддерживает DDR5-6000». |
| Price как dimension | 023 | Q1 не отвечен. FPS/рубль невозможен без цены. |
| Store как dimension | — | Нельзя сказать «цена в DNS vs Ситилинк». |
| Связи между сущностями | 016 | GPU не знает свой Architecture. CPU не знает свой Socket. Нет графа совместимости. |

**Бизнес-диагноз:** читатель не может получить ответ на вопрос о сборке. Система знает о видеокартах, но не знает об остальном ПК.

### Слой 6 — Semantic Layer (Вычисляемые метрики)

**Текущее состояние:** 3 definitions (average-fps, one-percent-low-fps, frame-generation). Definitions описывают *что* это, но нет capabilities, которые *вычисляют* метрики из observation.

| Архитектурный долг | ADR | Бизнес-последствие |
|---|---|---|
| Вычисление метрик | 023 | Каждый раз средний FPS вычисляется ad-hoc. Два разных запроса могут дать разные результаты. |
| avg_price definition | 023 | FPS/рубль невозможен. Q1 не отвечен. |
| relative_performance definition | 023 | Нельзя сказать «5060 Ti на 15% быстрее 4060 Ti». |
| comparison capability | 019, 023 | Q3 не отвечен. Сравнение — ручная работа редактора. |

**Бизнес-диагноз:** система хранит данные, но не умеет их интерпретировать для читателя.

### Decision Engine (Слой 3 в модели консультанта)

| Архитектурный долг | ADR | Бизнес-последствие |
|---|---|---|
| Decision-Centric ViewModel | 027 | Q1, Q3, Q5 требуют не данных, а решений. Без Decision Engine система — склад, не советчик. |
| EvidenceItem model | 027 | Выводы не привязаны к evidence. Нельзя проверить обоснованность рекомендации. |
| Decision types catalog | — | Нет перечня допустимых решений. Каждый раз решение формулируется заново. |

### Capabilities (по ADR-019)

**Текущее состояние:** реализованы dim-read, cross-reference, fact-insert, coverage-matrix (4 из ~20 зафиксированных).

| Capability | Тип | ADR | Бизнес-последствие отсутствия |
|---|---|---|---|
| **fact-read** | read | 019 | Агент не может прочитать observation и вернуть его читателю с контекстом (игра, настройки, драйвер) |
| **comparison** | read | 019 | Q3 не отвечен. Редактор сравнивает карты вручную. |
| **lineage-trace** | read | 017, 019 | Q2 не отвечен. Нельзя показать путь «рекомендация → замер → reviewer → видео». |
| **impact-analysis** | read | 017, 019 | Q4 не отвечен. Новый драйвер → неизвестно какие обзоры устарели. |
| **stale-check** | read | 019 | Читатель получает рекомендацию на устаревших данных. Молчаливая деградация качества. |
| **bus-lookup** | read | 019 | Агент ищет dimension по alias вручную. Нет единого способа резолвинга. |
| **dim-upsert** | write | 019 | Каждый dimension создаётся ручным execute_code. Нельзя программно завести CPU. |
| **pattern-promote** | write | 019 | Найденная закономерность не сохраняется для переиспользования. Инженерные инсайты теряются. |
| **artifact-compile** | write | 019 | Нельзя автоматически собрать страницу обзора. Каждая страница — ручная работа. |
| **artifact-regenerate** | write | 019 | Устаревшая страница не пересобирается. Нужно править вручную. |
| **bus-register** | write | 019 | Новый dimension может существовать без регистрации в bus matrix. Риск «потерянных» сущностей. |
| **scd-version** | read | 016 | Невозможно запросить историческую версию dimension. «Какие драйверы были в марте 2026?» |
| **minerva/SKILL.md** (оркестратор) | — | 019 | Агент не знает как комбинировать capabilities. Каждый запрос — ad-hoc навигация. |

**Бизнес-диагноз ADR-019:** capabilities — это язык, на котором агент общается со складом. 80% словаря отсутствует. Агент «немой» для большинства читательских вопросов.

### Lineage (по ADR-017)

**Текущее состояние:** ни одного lineage-поля в observation-файлах. Нет lineage-trace, impact-analysis, contradiction tracking.

| Архитектурный долг | ADR | Бизнес-последствие |
|---|---|---|
| lineage в observation | 017 | Q2 не отвечен. Любой вывод — «потому что я так сказал», без доказательств. |
| lineage-trace capability | 017, 019 | Нельзя проверить обоснованность. Эпистемическая достоверность = нулевая. |
| impact-analysis capability | 017, 019 | Данные изменились → тишина. Нет механизма узнать что сломалось. |
| contradiction tracking | 017 | Два замера FPS противоречат друг другу → система не знает об этом. Вывод может быть на противоречивых данных. |
| SCD + lineage | 017 | Lineage ссылается на конкретную версию dimension. Без lineage — SCD бесполезен. |

### Data Catalog (не зафиксирован в ADR)

Новый architectural concept. В production-DW каталог отвечает на вопросы:
- Какие сущности есть в системе?
- Кто за них отвечает?
- Когда они обновлялись?
- Какой источник данных?

| Архитектурный долг | Бизнес-последствие |
|---|---|
| Catalog сущностей | Никто не знает полный перечень dimensions. 10 GPU, 71 игра — это знание в головах, не в системе. |
| Catalog decision types | Каждое решение формулируется ad-hoc. Нет перечня допустимых вопросов к системе. |
| Метрики качества данных | Неизвестно сколько данных устарело, сколько имеет низкий confidence. |

### Acquisiton Layer (по ADR-012, 024)

| Архитектурный долг | Бизнес-последствие |
|---|---|
| ETL-коннекторы | Каждый новый GPU требует ручного поиска бенчмарков на YouTube. Не масштабируется. |
| Price connectors | Q1 не отвечен без цен. Ручной ввод цен на 10 GPU × 5 магазинов = 50 операций. |

---

## Часть 3. Data Debt Register

Data debt = данные отсутствуют в существующих структурах. Контракт (bus matrix, definition) есть, данные — нет.

### Dimensions (реестр сущностей)

| Dimension type | Есть | Отсутствует | Бизнес-последствие |
|---|---|---|---|
| GPU | 10 | Остальные модели (RTX 4060 Ti 16GB, RTX 4070, RTX 4080, RX 9070, etc.) | Неполный охват рынка. Сравнение только внутри 10 карт. |
| CPU | 0 | Все процессоры | Q5 не отвечен. Невозможно рекомендовать сборки. |
| Socket | 0 | AM5, LGA 1700, LGA 1851 | Нет графа совместимости. |
| Architecture | 0 | Zen 4, Zen 5, RDNA 3, RDNA 4, Blackwell, Alchemist | Нельзя группировать по поколениям. |
| Motherboard | 0 | Все чипсеты и модели | Нет стоимости платформы. |
| Memory | 0 | DDR4, DDR5 | Нет конфигураций памяти. |
| Price | 0 | Все цены | Q1 не отвечен. |
| Store | 0 | DNS, Ситилинк, OZON | Нет региональных цен. |
| Resolution | 1 (1440p) | 1080p, 4K, 720p | Нет данных для 1080p-гейминга и 4K. |
| CPU (в observation) | 0 | — | Все 440 наблюдений привязаны к R5 5600X, но CPU не выделен в dimension. |

### Evidence (наполнение фактами)

| Evidence type | Заполнено | Отсутствует | Бизнес-последствие |
|---|---|---|---|
| Gaming FPS (GPU) | 440+ observation | ~70% market coverage отсутствует | Неполные сравнения. |
| Gaming FPS (CPU) | 0 | Все CPU-бенчмарки | Нельзя сказать «7600X в CS2 даёт X FPS». |
| Цены | 0 | Все | Q1 не отвечен. |
| Thermal / Power | 0 | Отдельные замеры | Нельзя сказать «греется ли эта карта». |
| Release dates | 0 | Даты выхода | Нельзя фильтровать «что вышло в 2026». |

### Games (реестр игр)

| Статус | Количество | Бизнес-последствие |
|---|---|---|
| Всего | 71 игра | Неполный охват. Нет Baldur's Gate 3, нет многих AAA 2025–2026. |

---

## Часть 4. ADR-019 Assessment — Capability Gaps

ADR-019 зафиксирован как accepted, но capability-модель — это не «хорошо бы иметь», а **единственный контракт между агентом и складом**. Без capabilities агент не может ответить на читательские вопросы.

### Какой бизнес-ценности лишена ИгроЛаба без ADR-019

**1. Самообслуживание читателя (Q1, Q3)**

Без `comparison` и `semantic layer` читатель не может сам сравнить две карты. Каждый вопрос требует ручной работы редактора. Это не масштабируется: 10 GPU → 45 уникальных пар сравнения. 20 GPU → 190 пар. Ручное сравнение ломается на втором десятке карт.

**2. Доверие к рекомендациям (Q2)**

Без `lineage-trace` любая рекомендация — «потому что мы так сказали». В мире где LLM галлюцинируют, source grounding — единственная защита. Lineage делает ИгроЛабу проверяемой: «вы рекомендуете 5060 Ti для 1440p → покажите замеры → вот видео → вот reviewer → вот дата».

**3. Актуальность (Q4)**

Без `stale-check` и `impact-analysis` контент молчаливо устаревает. Вышел драйвер с +15% FPS — все обзоры с предыдущими замерами стали неверными. Система не знает об этом. Читатель получает устаревшую рекомендацию и теряет доверие.

**4. Инженерная память (pattern-promote)**

Агент находит закономерность («GDDR7 компенсирует узкую шину на xx60-классе»), но не может её сохранить. Следующий агент переоткрывает то же самое заново. Инженерные инсайты не накапливаются.

**5. Production-масштаб (artifact-compile)**

Сейчас контент-пайплайн: редактор → ручной обзор. С 10 GPU это возможно. С 50 GPU — нет. `artifact-compile` позволяет агенту собирать structured comparison tables, из которых писатель делает prose. Это разделение труда: машина — structured data, человек — нарратив.

### Приоритет реализации ADR-019

| Приоритет | Capability | Почему |
|---|---|---|
| P0 | fact-read | Агент не может прочитать observation. Это слепота. |
| P0 | comparison | Q3 — самый частый вопрос читателя. Без него нет продукта. |
| P0 | bus-lookup | Каждый новый агент заново учится резолвить алиасы. |
| P1 | lineage-trace | Q2 — доверие. Можно временно без полного DAG, достаточно source → observation. |
| P1 | dim-upsert | Ручное создание dimensions не масштабируется. |
| P1 | bus-register | Каждый новый dimension должен быть в матрице. |
| P2 | pattern-promote | Инженерная память. Важно, но не блокирует Q1-Q4. |
| P2 | impact-analysis | Работает только при наличии lineage. |
| P2 | stale-check | Полезно когда есть artifact-compile. |
| P3 | artifact-compile | Production-масштаб. Когда 20+ GPU — станет P0. |
| P3 | scd-version | Нужен для SCD, который пока не используется. |

---

## Часть 5. Новые Architectural Concepts

Три концепта от консультанта, не зафиксированные в существующих ADR:

### 5.1 Decision Lineage

ADR-017 фиксирует lineage для Facts и Laws. Консультант расширяет: lineage должна проходить через Decision.

```
Decision («брать 5060 Ti для 1440p»)
  ↓
Evidence (средний FPS по 25 играм = 78)
  ↓
Observation (Cyberpunk 2077: 68 fps, драйвер 572.16, 1440p Ultra)
  ↓
Source (видео «RTX 5060 Ti Review», канал Hardware Unboxed, 2026-03-15)
```

ADR-017 определяет типы рёбер (observes, derived_from, generalizes, etc.), но не включает Decision как узел графа. Decision — это уровень 4 в иерархии (выше Artifact), и он должен иметь lineage до Source.

**Необходимо:** расширить ADR-017 — добавить Decision как тип узла, ребро `decides` (Decision → Evidence).

### 5.2 Data Catalog

В production это DataHub/Amundsen/OpenMetadata. У нас — YAML-файл или SKILL.md, который отвечает на вопросы:
- Какие сущности есть в системе? (GPU, CPU, Game, etc.)
- Кто владелец данных? (какой capability их производит)
- Какой источник? (YouTube, TechPowerUp, training data)
- Когда последнее обновление?
- Какой confidence?

Для Decision Types — расширенный каталог:
- Какие типы решений допустимы? (comparison, recommendation, upgrade-path, bottleneck-detect)
- Какие обязательные поля?
- Какой алгоритм генерации?
- Какие валидаторы?
- Какой UI Renderer?

**Необходимо:** новый ADR или секция в этом ADR — Data Catalog как capability.

### 5.3 Evidence Warehouse vs Decision Warehouse

Классический DW разделяет Physical Layer и Semantic Layer. У нас разделение глубже:

- **Evidence Warehouse** — то что есть сейчас: observations, definitions, bus matrix. Отвечает на «что измерили».
- **Decision Warehouse** — marts/ и artifacts/. Отвечает на «что рекомендовать».

Decision Warehouse не хранит данные — он ссылается на Evidence и строит выводы. Это важно архитектурно: Decision не может существовать без lineage к Evidence. И Evidence может меняться независимо от Decision (stale-check).

**Необходимо:** зафиксировать границу. Evidence Warehouse уже существует (warehouse/), Decision Warehouse — marts/ + artifacts/ — отсутствует.

### 5.4 Knowledge Refinement Pipeline

```
Raw Data          ← YouTube, TechPowerUp, manual (acquisition)
  ↓
Canonical Facts   ← dimensions с атрибутами (warehouse/dim/)
  ↓
Evidence          ← observations (warehouse/fact/)
  ↓
Derived Metrics   ← avg_fps, fps_per_ruble (semantic layer)
  ↓
Decision          ← comparison, recommendation (marts/)
  ↓
Explanation       ← lineage-trace, narrative (marts/ + agent)
  ↓
Reader Experience ← artifact-compile, UI (artifacts/)
```

**Текущее покрытие minerva:** слои 1–3 частично. Слои 4–7 отсутствуют.

---

## Часть 6. Приоритеты

На основе бизнес-ценности, не сложности реализации:

### P0 — Без этого продукта нет

1. **fact-read** — агент должен читать observation. Базовая операция.
2. **comparison** — вопрос «что лучше» должен быть отвечен системой, не редактором вручную.
3. **bus-lookup** — без него каждый агент тратит токены на резолвинг алиасов.
4. **CPU dimensions** — без CPU нет сборок. Без сборок нет половины контента.
5. **minerva/SKILL.md** (оркестратор) — агент должен знать как компоновать capabilities.

### P1 — Без этого нет доверия

6. **lineage-trace** — source grounding. Доверие читателя.
7. **dim-upsert** + **bus-register** — масштабирование dimensions.
8. **semantic layer computing** — avg_fps, relative_performance должны вычисляться, не угадываться.
9. **Price dimension** — FPS/рубль — ключевая consumer-метрика.

### P2 — Качество и масштаб

10. **stale-check** + **impact-analysis** — актуальность контента.
11. **pattern-promote** — накопление инженерных знаний.
12. **Data Catalog** — прозрачность системы.
13. **Decision lineage** — полная прослеживаемость.

### P3 — Production

14. **artifact-compile** — автоматическая сборка страниц.
15. **scd-version** — исторические данные.
16. **acquisition connectors** — автоматический сбор бенчмарков.

---

## Что НЕ фиксируем

- **Конкретные implementation details** — какой формат catalog-файла, как реализован поиск Fact по dim_ref. Это в capability SKILL.md.
- **Сроки** — это planning, не architecture decision.
- **UI/UX** — Reader Experience — самый дальний слой. Не трогаем пока нет Decision Engine.
- **Cross-domain** — hardware только. Coffee, другие bounded contexts — когда появится второй.

## Последствия

**Что становится проще:**
- **Планирование.** Каждый новый запрос (фича, контент) можно сверить с этим регистром: в каком слое лежит, какой долг блокирует.
- **Onboarding.** Новый разработчик видит полную архитектурную картину: что обещано, что сделано, что в приоритете.
- **Принятие решений.** Выбор между «добавить GPU бенчмарк» и «сделать comparison capability» — resolved: comparison (P0) важнее ещё одного observation (P2).

**Что требует дисциплины:**
- **Регистр должен обновляться.** Закрыли tech debt → обновили статус в ADR-030.
- **Новые ADR → проверка на добавление долга.** Каждый новый ADR создаёт promises. Если они не закрываются в том же спринте — это новый tech debt, должен быть зафиксирован здесь.
- **Data debt — непрерывный.** Всегда будут GPU без бенчмарков, игры без dimensions. Это не баг, это backlog. Но он должен быть видимым.
