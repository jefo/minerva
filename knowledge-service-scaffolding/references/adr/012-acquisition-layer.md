---
id: adr-012
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [architecture, acquisition, exploratory-research, tactical-ddd, layers]
based_on: [adr-011, observation-002]
---

# ADR-012: Слой Acquisition — pre-structured research поверх minerva

## Контекст

Observation 002 выявил capability gap в архитектуре minerva: система начинает с формализации знаний (Tier 1 — `primitive-create`), но реальный исследовательский процесс начинается раньше — с сырых источников, извлечения информации и exploratory reasoning. Это та фаза, где формализация вредна: premature structure убивает serendipitous discovery.

NotebookLM силён именно в этой фазе — unsupervised cross-source synthesis, emergent pattern discovery, работа с сырыми источниками. Но он не интегрирован в архитектуру minerva и не имеет перехода к structured layer.

Текущая архитектура (ADR-011) определяет четыре тира поверх structured знаний, но не определяет **откуда эти знания берутся до формализации**. Это создаёт разрыв: аналитик должен уже знать что формализовывать, но в реальности discovery предшествует formalization.

## Решение

Ввести **слой Acquisition** — архитектурный слой над тактическим DDD (minerva), отвечающий за работу с сырыми источниками до их формализации в structured KB.

### Слоистая архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    ACQUISITION LAYER                         │
│  Сырые источники → Извлечение → Exploratory reasoning        │
│  (PDF, URL, YT transcript, specs, benchmarks)                │
│  Интерфейс: open-ended chat с source grounding               │
│  Продукт: candidate patterns, hypotheses, extracted facts    │
├─────────────────────────────────────────────────────────────┤
│                    TACTICAL DDD LAYER (minerva)              │
│  Tier 0: Навигация                                          │
│  Tier 1: Primitive Management (формализация кандидатов)      │
│  Tier 2: Composition                                        │
│  Tier 3: Integrity & Governance                             │
│  Tier 4: Analysis & Query                                   │
└─────────────────────────────────────────────────────────────┘
```

### Границы слоя Acquisition

**Вход:** сырые, неструктурированные источники — PDF, URL, YouTube transcripts, спецификации производителей, бенчмарки, статьи, заметки.

**Процесс:** свободное исследование корпуса — вопросы, synthesis, pattern discovery. Без обязательной формализации. Модель работает в режиме «я не знаю что ищу».

**Выход:** candidate assertions с source grounding:
- Candidate facts (specification values, observations, measurements)
- Candidate patterns (повторяющиеся архитектурные решения, корреляции)
- Candidate contradictions (расхождения между источниками)
- Candidate gaps (что не покрыто источниками)

### Переход Acquisition → Tactical DDD

Ключевое архитектурное решение: **явный gate между слоями.** Acquisition не пишет в structured KB напрямую. Переход происходит через:

1. **Promote:** аналитик (человек или агент) решает что candidate достоин формализации
2. **Validate:** `primitive-create` → `primitive-validate` создаёт structured Primitive из candidate
3. **Trace:** Primitive сохраняет ссылку на сырой источник через `source:` в frontmatter

```
Acquisition: "GDDR7 на 128-bit даёт bandwidth сравнимый с GDDR6X на 256-bit"
    │
    ▼ [promote]
minerva: primitive-create(type=Law, title="GDDR7 Bandwidth Compensation Law")
    │
    ▼ [validate]
minerva: primitive-validate → PASS
    │
    ▼ [trace]
Law frontmatter: source: "acquisition/session-2026-07-11/raw/nvidia-rtx-5060-spec.pdf"
```

### Почему не новый Tier

Слой Acquisition принципиально отличается от Tiers 0–4:
- **Tiers оперируют структурированными знаниями** (Primitives, Components, Modules). У них есть контракты, схемы, валидация
- **Acquisition оперирует сырыми данными.** У него нет схемы — источники гетерогенны. Нет контракта — выход probabilistic, не deterministic

Добавление Acquisition как Tier −1 сломало бы архитектурную чистоту Tiers: они все работают с Primitives, а Acquisition — с источниками. Это разные bounded contexts.

### Отношение к DDD

**Acquisition = Strategic DDD-контекст?** Возможно. Он работает с доменом на уровне «что здесь происходит», не «как это смоделировать». Tactical DDD (minerva) — это Bounded Contexts, Aggregates, Entities. Acquisition — это exploration поверхности домена до его разбиения на контексты.

## Что НЕ фиксируем

- **NotebookLM как единственная реализация.** Acquisition layer — архитектурная потребность. NotebookLM может быть одной из реализаций (и сейчас лучшей), но архитектура не должна быть привязана к конкретному продукту Google
- **Формат хранения сырых источников.** Файлы? Векторная БД? Это implementation detail
- **Интерфейс acquisition.** Чат? CLI? API? Решается при реализации

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Встроить acquisition в Tier 1 (primitive-bulk-import с reasoning) | Меньше слоёв, проще | Смешивает probabilistic reasoning с deterministic validation — contamination | Acquisition требует свободы exploration; Tier 1 требует структурной дисциплины. Разные режимы мышления |
| Использовать NotebookLM как есть, без архитектурной интеграции | Ноль затрат на разработку | Нет перехода к structured KB, нет traceability, знания теряются между сессиями | Уже пробовали — работает для discovery, но найденное не попадает в KB |
| Расширить Tier 4 до acquisition-запросов | Использует существующую архитектуру | Tier 4 работает со structured данными, не с сырыми источниками | Category error: `comparison` сравнивает Primitives, а не PDF-файлы |
| Сделать acquisition отдельным продуктом, не частью minerva | Чистые границы | Два продукта с overlap'ом по данным, сложнее пользователю | Acquisition без перехода к minerva — тупик: нашёл паттерн и куда его дел? |

## Связь

- **ADR-011:** определяет Tiers 0–4. Acquisition — слой над ними, не новый Tier
- **Observation 001:** напряжение Atomic Design vs Aggregate — относится к structured layer, не к acquisition
- **Observation 002:** документирует capability gap, который этот ADR закрывает
- **ADR-006:** KB = файлы. Сырые источники могут жить в acquisition/ директории в том же репо

## Последствия

**Что становится проще:**
- Исследовательский процесс получает архитектурный дом: «я в фазе acquisition» или «я в фазе formalization» — две разные деятельности с разными инструментами
- Найденные паттерны не теряются: promote gate гарантирует что ценное попадает в structured KB
- Traceability от structured знания к сырому источнику — архитектурно обеспечена, не ad-hoc
- Можно менять реализацию acquisition (NotebookLM → своя RAG-система → etc.) не трогая structured layer

**Что усложняется:**
- Два слоя вместо одного — ментальная модель сложнее. Пользователь должен понимать когда он в acquisition, а когда в tactical DDD
- Promote gate требует дисциплины: не всё что найдено в acquisition достойно формализации. Без критериев promote превращается в dump
- Сырые источники нужно где-то хранить и версионировать (git плохо работает с бинарными PDF)

**Что требует внимания:**
- Критерии promote: когда candidate становится Primitive? Ответ: «проходит primitive-validate» — это необходимый, но не достаточный критерий. Нужен ещё relevance threshold
- Acquisition может генерировать противоречащие candidate assertions — это нормально для exploration, но требует resolve при promote
- Не допустить чтобы acquisition стал «песочницей где всё можно и ничего не формализуется» — acquisition без promote = бесконечный browsing без продукта
