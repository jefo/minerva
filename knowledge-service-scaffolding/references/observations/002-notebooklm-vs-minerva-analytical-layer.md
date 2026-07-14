# Observation 002: NotebookLM exploratory synthesis vs minerva analytical layer

**Date:** 2026-07-11
**Status:** open
**Type:** architectural analysis — external tool capability mapping

## Контекст

Анализ NotebookLM как инструмента research-driven content production выявил capability gap в текущей архитектуре minerva. NotebookLM даёт unsupervised cross-source pattern discovery — способность находить emergent insights без предопределённых запросов. minerva Tier 4 (`comparison`, `cross-reference`, `recommendation`) покрывает структурные запросы, но не закрывает фазу открытия.

## Наблюдение

### 1. Две принципиально разные фазы research

| Фаза | Инструмент | Характер | Формализация |
|---|---|---|---|
| **Exploratory synthesis** | NotebookLM | Unsupervised patterns, emergent insights, cross-source surprises | Вредна — premature structure убивает discovery |
| **Structured analysis** | minerva Tier 3–4 | Deterministic queries, воспроизводимые выводы, traceability | Необходима — без неё нет integrity |

### 2. Что NotebookLM даёт такого, чего minerva не планирует

- **Emergent insight:** «GDDR7 на 128-битной шине даёт bandwidth 355 GB/s — столько же, сколько GDDR6X на 256-битной у RTX 4070» — паттерн, который не был предопределён в схеме данных
- **Cross-source gap detection:** находит отсутствующие данные не по явному запросу `gap-analysis`, а как побочный продукт synthesis
- **Unsupervised contradiction discovery:** «утверждение A в KB-записи противоречит официальной спецификации B» — без явного `consistency-audit`
- **Работа с сырыми источниками:** PDF, URL, YouTube transcript — до того как они формализованы в Primitives

### 3. Где этот gap находится в архитектуре minerva

```
[Сырые источники: PDF, URL, specs, transcripts]
        │
        ▼
   ╔═══════════════════════════════════╗
   ║  GAP: exploratory synthesis      ║  ← NotebookLM закрывает это
   ║  Паттерны, гипотезы, инсайты     ║     minerva не покрывает
   ╚═══════════════════════════════════╝
        │
        ▼
[minerva Tier 1: primitive-create]     ← формализация найденного
        │
        ▼
[minerva Tier 2: composition]
        │
        ▼
[minerva Tier 3–4: integrity + analysis]
```

minerva начинает с формализации (Tier 1). Но exploratory synthesis — это фаза где формализация вредна: premature structure убивает serendipitous discovery.

### 4. Ключевое архитектурное различие

- **NotebookLM:** работает в фазе «я не знаю что ищу». Модель видит все источники одновременно и находит паттерны, которые не были запрограммированы как вопросы
- **minerva:** работает в фазе «я знаю какие вопросы задать данным». Capabilities — это направленные операции над структурированными знаниями

### 5. NotebookLM ≠ замена minerva

NotebookLM не даёт:
- Детерминированности (один и тот же запрос → разный ответ)
- Структурной целостности (нет consistency audit)
- Traceability к источнику в machine-readable форме
- Pipeline integration (выход — prose, не structured artifact)

## Гипотеза

Архитектура minerva должна включать **pre-Tier-1 capability** — «research notebook» или «exploratory surface», которая:

- Принимает сырые источники (PDF, URL, transcripts)
- Даёт интерфейс свободного исследования (чат с корпусом)
- Позволяет маркировать найденные паттерны как candidate Primitives
- Имеет явный переход: «найдено → формализовано в KB»

Это не замена NotebookLM, а **архитектурное признание того что формализации предшествует exploration**. Без этого gap'а minerva требует чтобы аналитик уже знал что формализовывать — а это не так в реальном исследовательском процессе.

## Следствия для архитектуры

1. **Tier 0 может быть не только навигацией, но и exploration.** Сейчас Tier 0 — это «где что лежит». Но exploration — это «что здесь интересного», качественно другой вопрос
2. **pre-Tier-1 capability требует другого интерфейса.** Не structured forms (primitive-create), а open-ended chat с source grounding
3. **Переход exploration → formalization — критическая точка.** Без явного gate'а exploration превращается в бесконечный browsing без продукта

## Связанные артефакты

- Observation 001: Atomic Design vs Aggregate — аналогичное напряжение между формализацией и целостностью
- ADR-011: Capability roadmap — Tier 0–4, но нет pre-Tier-1
- ADR-006: KB = файлы, агенты работают напрямую — но pre-Tier-1 может требовать других premises
