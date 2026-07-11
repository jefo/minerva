---
type: reference
domain: knowledge-services
covers: [taxonomy, semantics, atomic-design]
based_on: [adr-002, adr-003, adr-004]
---

# Таксономия и семантика Knowledge Services

Каноническое описание таксономии уровней и типов знаний. Основано на принципах Atomic Design, адаптированных для Knowledge Base.

## 1. Принципы Atomic Design в контексте знаний

Atomic Design в Knowledge Services — это **архитектура композиции знаний**, не визуальных компонентов.

| Принцип Atomic Design | Значение для Knowledge Services |
|---|---|
| Композиция от простого к сложному | Сложные артефакты собираются из более простых, а не пишутся с нуля |
| Однонаправленная зависимость | Нижние уровни не знают о верхних. Primitive не знает, в какой Artifact попадёт |
| Переиспользование | Один Module используется в десятках Artifacts без дублирования |
| Разделение ответственности | Автор Module думает о корректности модели. Автор Artifact — о композиции и нарративе |
| Progressive disclosure | Читатель идёт от Artifact вниз к Primitives, а не получает всё сразу |

## 2. Уровни композиции

Пять уровней — от неделимого знания до конечного продукта.

### 2.1 Primitives — неделимые знания

**Определение:** знание, которое нельзя логически разложить на более мелкие знания того же порядка. Словарь предметной области. Никакой аналитики.

**Критерий:** если знание можно разложить → это Component или Module, не Primitive.

**Примеры из GPU-домена:**
- RTX 5070, GB205, CUDA Core, DLSS (Concept)
- TDP 250W, Boost Clock 2.5 GHz, Bandwidth 672 GB/s (Metric/Specification)
- FPS = 87 в Cyberpunk 2077 (Observation)
- bandwidth = frequency × bus_width / 8 (Law)
- RTX 5070 —[uses]→ GB205 (Relation)

**Типы Primitives** — см. раздел 3.

### 2.2 Components — устойчивые композиции знаний

**Определение:** связанные Primitives, образующие осмысленную единицу. Появляется семантика, которой нет у отдельных Primitives.

**Критерий:** Component содержит минимум 2 Primitives и отвечает на вопрос «что это вместе значит?».

**Примеры:**
- Memory Subsystem = VRAM + Bus Width + Bandwidth + Compression
- Rendering Pipeline = Raster + RT + Tensor
- Power Delivery = TDP + Transient Spike + Connector + PSU Requirement

### 2.3 Modules — законченные инженерные модели

**Определение:** полное описание подсистемы или продукта. Module — это то, что может быть independently verified инженером.

**Критерий:** Module содержит Components и Primitives в количестве, достаточном для полного понимания подсистемы без обращения к внешним источникам.

**Примеры:**
- GPU Architecture (GB205)
- Compute Pipeline
- Memory Architecture
- Power Architecture
- Display Engine
- Intel Arrow Lake CPU

### 2.4 Views — аналитические схемы

**Определение:** шаблон, определяющий структуру анализа. View не содержит контента — только схему: из каких секций состоит анализ, в каком порядке, с какими акцентами.

**Критерий:** если из документа убрать все факты и оставить заголовки секций — получится View.

**Примеры:**
- GPU Analysis: Architecture → Memory → Power → Performance → Tradeoffs → Envelope → Recommendations
- CPU Review: Architecture → Cache → Memory Controller → Platform → Benchmarks → Positioning
- Comparison: Context → Dimensions → Side-by-Side → Verdict

### 2.5 Artifacts — конечные продукты

**Определение:** конкретная страница — обзор, сравнение, гайд, статья. Собирается как композиция View + конкретных Modules, Components, Primitives.

**Критерий:** Artifact почти ничего своего не содержит. Он — композиция существующих знаний. Если из Artifact убрать все ссылки на нижние уровни и остаётся полноценный документ — это не Artifact, а самостоятельный документ (нарушение модели).

**Примеры:**
- RTX 5070 Review = GPU Analysis View + GB205 Module + 16GB GDDR7 Component + Benchmarks + Price
- RTX 5070 vs RX 9070 XT = Comparison View + два GPU Module + Memory Components

## 3. Типы Primitives

Шесть типов — каждый отвечает на свой вопрос.

### 3.1 Concept

**Вопрос:** что это за сущность?

**Форма:** именованный концепт с определением. Может иметь атрибуты (синонимы, аббревиатуры, контекст использования).

**Примеры:** GPU, VRAM, PCIe Lane, CUDA Core, DLSS, Frame Generation, SM, L2 Cache

**Граница:** Concept — это понятие, не факт. «CUDA Core» — Concept. «CUDA Core выполняет одну операцию с плавающей точкой за такт» — это Specification или Metric.

### 3.2 Metric

**Вопрос:** какое значение у измеримой величины?

**Форма:** имя + значение + единица измерения + метод получения (вычислено/измерено).

**Примеры:** Bandwidth = 672 GB/s, Boost Clock = 2.5 GHz, Die Size = 378 mm²

**Граница:** Metric — вычисленная или измеренная величина. Если значение заявлено производителем — это Specification. Если получено в тесте — Observation.

### 3.3 Observation

**Вопрос:** что показал тест/измерение?

**Форма:** источник + условия + значение. Observation всегда имеет provenance: где, когда, кем, на каком стенде.

**Примеры:** FPS = 87 в Cyberpunk 2077 (1440p, Ultra), температура под нагрузкой = 72°C (FurMark, 30 мин)

**Граница:** Observation ≠ Metric. Metric — это свойство (Bandwidth), Observation — это конкретное измерение свойства в конкретных условиях.

### 3.4 Specification

**Вопрос:** что заявлено производителем?

**Форма:** источник (даташит, спецификация) + значение. Отличается от Observation тем, что это заявленная, а не измеренная характеристика.

**Примеры:** 16 GB GDDR7, PCIe 5.0 x16, 3× DisplayPort 2.1, TDP 250W

**Граница:** TDP 250W — Specification (заявлено NVIDIA). Реальное энергопотребление под нагрузкой 280W — Observation (измерено).

### 3.5 Law

**Вопрос:** какая закономерность или формула связывает величины?

**Форма:** формула + объяснение. Law не содержит конкретных значений — только отношения.

**Примеры:** bandwidth = frequency × bus_width / 8, performance ∝ CUDA cores × clock, latencyₜₒₜₐₗ = latencyₘₑₘ + latencyₛₘ + latencyₚ𝒸ᵢₑ

**Граница:** Law — это отношение, не факт. «RTX 5070 имеет bandwidth 672 GB/s» — это Specification. «bandwidth = frequency × bus_width / 8» — это Law.

### 3.6 Relation

**Вопрос:** как сущности связаны друг с другом?

**Форма:** субъект + предикат + объект. Именованная связь между двумя или более Concepts.

**Примеры:** RTX 5070 —[uses]→ GB205, GB205 —[manufactured_on]→ TSMC 4N, DLSS 4 —[requires]→ Tensor Core

**Граница:** Relation — бинарная или N-арная связь. Если связь имеет внутреннюю структуру (например, «RTX 5070 использует GB205 для рендеринга и отдельный чип для дисплея») — это Component.

## 4. Правила композиции

### 4.1 Downward visibility

Уровень N знает только об уровнях < N. Никогда об уровнях > N.

| Уровень | Знает о | Не знает о |
|---|---|---|
| Primitive | Ничего (или другие Primitives) | Components, Modules, Views, Artifacts |
| Component | Primitives | Modules, Views, Artifacts |
| Module | Components, Primitives | Views, Artifacts |
| View | Modules, Components, Primitives | Artifacts |
| Artifact | Все нижние уровни | Другие Artifacts |

### 4.2 Композиция, не наследование

Уровни не наследуют свойства друг друга. Component — это не «Primitive с дополнительными полями». Component — это новая сущность, которая ссылается на Primitives. Отношение — композиция (has-a), не наследование (is-a).

### 4.3 Полнота на своём уровне

Каждый уровень должен быть самодостаточен для своей аудитории:
- Primitive: понятен читателю, который знает предметную область
- Component: понятен читателю без обращения к отдельным Primitives
- Module: полное описание — инженеру не нужно искать другие источники
- View: полная схема анализа — автору Artifact не нужно додумывать структуру
- Artifact: готовый продукт — читателю не нужно знать о существовании уровней

### 4.4 Один источник

Каждый Primitive, Component и Module существует ровно в одном экземпляре. Если два Artifact используют один Module — они ссылаются на один и тот же Module, не копируют его. Это фундаментальное правило, отличающее Knowledge Services от коллекции документов.

## 5. Пример: полная цепочка композиции

RTX 5070 Review — от Primitives до Artifact:

```
Primitives:
  Concept: RTX 5070, GB205, GDDR7, CUDA Core, DLSS 4, ...
  Specification: 16 GB, PCIe 5.0, TDP 250W, 6144 CUDA Cores
  Metric: Bandwidth 672 GB/s, Boost Clock 2.51 GHz
  Observation: FPS Cyberpunk 1440p Ultra = 87, Power peak = 280W
  Law: bandwidth = freq × width / 8
  Relation: RTX 5070 —[uses]→ GB205, GB205 —[process]→ TSMC 4N

Components:
  Memory Subsystem = VRAM + Bus Width + Bandwidth + Compression
  Rendering Pipeline = Raster + RT + Tensor
  Power Delivery = TDP + Transient Spike + Connector + PSU

Modules:
  GB205 Architecture = SM + CUDA Core + RT Core + Tensor Core + Cache + ...
  Blackwell Memory Architecture = GDDR7 + Controller + Compression

View:
  GPU Analysis = Architecture → Memory → Power → Performance → Tradeoffs → Envelope → Recommendations

Artifact:
  RTX 5070 Review = GPU Analysis View
                  + GB205 Module
                  + Blackwell Memory Architecture Module
                  + Memory Subsystem Component
                  + Power Delivery Component
                  + Benchmarks (Observations)
                  + Price (Metric)
                  + Engineering Commentary
```

Artifact не содержит ни одного факта, которого нет на нижних уровнях. Он содержит композицию и нарратив.
