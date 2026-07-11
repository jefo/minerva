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

**Примеры:**
- Espresso, Arabica, Burr Grinder, Extraction (Concept)
- Dose = 18 g, Temperature = 93°C, TDS = 1.35% (Metric/Specification)
- Bloom phase: 30 s at grind size 15 (Observation)
- extraction ∝ surface_area × contact_time / particle_size (Law)
- Espresso —[requires]→ Fine Grind (Relation)

**Типы Primitives** — см. раздел 3.

### 2.2 Components — устойчивые композиции знаний

**Определение:** связанные Primitives, образующие осмысленную единицу. Появляется семантика, которой нет у отдельных Primitives.

**Критерий:** Component содержит минимум 2 Primitives и отвечает на вопрос «что это вместе значит?».

**Примеры:**
- Brewing Parameters = Dose + Temperature + Pressure + Time
- Grind Quality = Particle Size + Uniformity + Burr Type
- Water Chemistry = Mineral Content + pH + Hardness

### 2.3 Modules — законченные модели

**Определение:** полное описание подсистемы, процесса или сущности. Module — это то, что может быть independently verified специалистом в предметной области.

**Критерий:** Module содержит Components и Primitives в количестве, достаточном для полного понимания подсистемы без обращения к внешним источникам.

**Примеры:**
- Espresso Extraction Model
- Burr Grinder Engineering Model
- Water Filtration System
- Roast Profile Model

### 2.4 Views — аналитические схемы

**Определение:** шаблон, определяющий структуру анализа. View не содержит контента — только схему: из каких секций состоит анализ, в каком порядке, с какими акцентами.

**Критерий:** если из документа убрать все факты и оставить заголовки секций — получится View.

**Примеры:**
- Brewing Method Analysis: Principle → Equipment → Parameters → Technique → Taste Profile → Recommendations
- Equipment Comparison: Context → Specifications → Performance → Ergonomics → Value → Verdict
- Process Guide: Goal → Prerequisites → Step-by-Step → Common Mistakes → Troubleshooting

### 2.5 Artifacts — конечные продукты

**Определение:** конкретная страница — обзор, сравнение, гайд, статья. Собирается как композиция View + конкретных Modules, Components, Primitives.

**Критерий:** Artifact почти ничего своего не содержит. Он — композиция существующих знаний. Если из Artifact убрать все ссылки на нижние уровни и остаётся полноценный документ — это не Artifact, а самостоятельный документ (нарушение модели).

**Примеры:**
- Espresso Brewing Guide = Process Guide View + Espresso Extraction Module + Brewing Parameters Component
- Grinder Comparison = Equipment Comparison View + два Burr Grinder Module + Grind Quality Component
- Water for Coffee = Brewing Method Analysis View + Water Chemistry Component + Water Filtration Module

## 3. Типы Primitives

Шесть типов — каждый отвечает на свой вопрос.

### 3.1 Concept

**Вопрос:** что это за сущность?

**Форма:** именованный концепт с определением. Может иметь атрибуты (синонимы, аббревиатуры, контекст использования).

**Примеры:** Espresso, Arabica, Burr Grinder, Extraction, Bloom, Crema

**Граница:** Concept — это понятие, не факт. «Espresso» — Concept. «Espresso готовится при давлении 9 bar» — Specification.

### 3.2 Metric

**Вопрос:** какое значение у измеримой/вычисляемой величины?

**Форма:** имя + значение + единица измерения + метод получения (вычислено/измерено).

**Примеры:** Extraction Yield = 20%, TDS = 1.35%, Flow Rate = 2.5 ml/s

**Граница:** Metric — вычисленная или измеренная величина. Если значение заявлено производителем оборудования — это Specification. Если получено в конкретном тесте — Observation.

### 3.3 Observation

**Вопрос:** что показал конкретный тест/измерение?

**Форма:** источник + условия + значение. Observation всегда имеет provenance: где, когда, кем, при каких условиях.

**Примеры:** Bloom phase 30 s at grind size 15 (Baratza Encore, Ethiopia Yirgacheffe), extraction yield 21.3% (VST refractometer, 2026-06-15)

**Граница:** Observation ≠ Metric. Extraction Yield — это Metric (свойство). «Extraction yield = 21.3% для Ethiopia Yirgacheffe на Encore, помол 15» — Observation (конкретное измерение).

### 3.4 Specification

**Вопрос:** что заявлено производителем или авторитетным источником?

**Форма:** источник (даташит, стандарт, спецификация) + значение. Отличается от Observation тем, что это заявленная, а не измеренная характеристика.

**Примеры:** Pump pressure 9 bar (модель Rancilio Silvia), Burr diameter 40 mm (модель Baratza Encore), Basket capacity 18 g

**Граница:** «Pump pressure 9 bar» — Specification (заявлено Rancilio). «Measured pressure at group head = 8.7 bar» — Observation (измерено).

### 3.5 Law

**Вопрос:** какая закономерность или формула связывает величины?

**Форма:** формула + объяснение. Law не содержит конкретных значений — только отношения.

**Примеры:** extraction ∝ surface_area × contact_time / particle_size, flow_rate ∝ pressure / resistance, TDS × brew_weight = extraction_yield × dose

**Граница:** Law — это отношение, не факт. «Extraction yield = 20%» — это Metric. «extraction ∝ surface_area × contact_time / particle_size» — это Law.

### 3.6 Relation

**Вопрос:** как сущности связаны друг с другом?

**Форма:** субъект + предикат + объект. Именованная связь между двумя или более Concepts.

**Примеры:** Espresso —[requires]→ Fine Grind, Arabica —[has_variety]→ Bourbon, Burr Grinder —[produces]→ Uniform Particles

**Граница:** Relation — бинарная или N-арная связь. Если связь имеет внутреннюю структуру (например, «помол влияет на экстракцию через площадь поверхности и время контакта») — это Component или Law.

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
- Module: полное описание — специалисту не нужно искать другие источники
- View: полная схема анализа — автору Artifact не нужно додумывать структуру
- Artifact: готовый продукт — читателю не нужно знать о существовании уровней

### 4.4 Один источник

Каждый Primitive, Component и Module существует ровно в одном экземпляре. Если два Artifact используют один Module — они ссылаются на один и тот же Module, не копируют его. Это фундаментальное правило, отличающее Knowledge Services от коллекции документов.

## 5. Пример: полная цепочка композиции

Espresso Brewing Guide — от Primitives до Artifact:

```
Primitives:
  Concept: Espresso, Arabica, Burr Grinder, Extraction, Bloom, Crema, Portafilter
  Specification: Pump pressure 9 bar, Basket 18 g, Temperature stability ±1°C
  Metric: Extraction yield 20%, TDS 1.35%, Flow rate 2.5 ml/s, Brew ratio 1:2
  Observation: Bloom 30 s at grind 15 (Encore, Yirgacheffe), yield 21.3% (refractometer)
  Law: extraction ∝ surface_area × contact_time / particle_size
  Relation: Espresso —[requires]→ Fine Grind, Arabica —[has_variety]→ Bourbon

Components:
  Brewing Parameters = Dose + Temperature + Pressure + Time + Ratio
  Grind Quality = Particle Size + Uniformity + Burr Type
  Water Chemistry = Mineral Content + pH + Hardness

Modules:
  Espresso Extraction Model = Brewing Parameters + Grind Quality + Extraction Law + Water Chemistry
  Burr Grinder Engineering Model = Burr Type + Particle Distribution + Motor + Adjustment Mechanism

View:
  Process Guide = Goal → Prerequisites → Step-by-Step → Common Mistakes → Troubleshooting

Artifact:
  Espresso Brewing Guide = Process Guide View
                         + Espresso Extraction Module
                         + Burr Grinder Engineering Module
                         + Brewing Parameters Component
                         + Grind Quality Component
                         + Water Chemistry Component
                         + Taste Profile Notes (editorial)
```

Artifact не содержит ни одного факта, которого нет на нижних уровнях. Он содержит композицию и нарратив.
