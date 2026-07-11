---
id: adr-004
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [architecture, primitives, taxonomy, ontology]
---

# ADR-004: Knowledge Primitives taxonomy — шесть типов неделимых знаний

## Контекст

Primitives — первый уровень композиции, «атомы знаний». Но что именно считать неделимым? «Espresso» — это Primitive? А «Pump pressure 9 bar»? А «extraction ∝ surface_area × contact_time / particle_size»?

Без формальной таксономии типов примитивов граница между Primitive и Component размывается. Разные авторы будут проводить её по-разному, что разрушит композиционную модель.

Нужна таксономия, которая отвечает на вопрос: «Что является неделимым знанием в данной предметной области?»

## Решение

Шесть типов Knowledge Primitives:

| Тип | Назначение | Пример | Форма |
|---|---|---|---|
| **Concept** | Понятие, сущность предметной области | Espresso, Extraction, Burr Grinder, Bloom | Именованный концепт с определением |
| **Metric** | Измеримая/вычислимая величина | Extraction Yield 20%, TDS 1.35%, Flow Rate 2.5 ml/s | Имя + значение + единица измерения |
| **Observation** | Зафиксированный эмпирический факт | Bloom 30 s при помоле 15 (Encore, Yirgacheffe), yield 21.3% (рефрактометр) | Источник + условия + значение |
| **Specification** | Заявленная производителем характеристика | Pump pressure 9 bar, Basket 18 g, Burr diameter 40 mm | Источник (даташит) + значение |
| **Law** | Закономерность, формула, отношение | extraction ∝ surface_area × contact_time / particle_size, flow_rate ∝ pressure / resistance | Формула + объяснение |
| **Relation** | Именованная связь между сущностями | Espresso —[requires]→ Fine Grind, Arabica —[has_variety]→ Bourbon | Субъект + предикат + объект |

**Почему именно шесть, а не три или десять:**

- Concept и Relation покрывают онтологию (что есть и как связано)
- Metric, Observation и Specification покрывают факты трёх разных природ (вычисляемое, эмпирическое, заявленное)
- Law покрывает инженерные закономерности (то, что не является ни фактом, ни сущностью)

Шесть типов — минимально достаточно, чтобы не было «miscellaneous», и максимально компактно, чтобы не было паралича выбора.

## Граница между Primitive и Component

Критерий: если знание можно логически разложить на более мелкие знания того же порядка — это Component, не Primitive.

| Знание | Primitive или Component? | Почему |
|---|---|---|
| Espresso | **Primitive** (Concept) | Понятие «Espresso» не разлагается на более мелкие онтологические единицы |
| Brewing Parameters | **Component** | Разлагается на Dose (Metric), Temperature (Metric), Pressure (Specification), Time (Metric) |
| Pump pressure 9 bar | **Primitive** (Specification) | Неделимая характеристика |
| Extraction Model | **Component/Module** | Разлагается на Brewing Parameters, Grind Quality, Water Chemistry, Extraction Law, ... |

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---------|-------|--------|------------|
| Только Concept + Metric | Простота | Law и Relation не влезают ни в одну категорию | Потеря значимых типов знаний |
| Concept + Fact (Observation, Spec, Metric объединены) | Меньше типов | Разная природа фактов: эмпирический ≠ заявленный ≠ вычисленный. При объединении теряется provenance | Разная достоверность и процедура обновления |
| Всё — Concept (плоский словарь) | Предельная простота | Pump pressure 9 bar — не «понятие»; Law — не «понятие»; категориальная ошибка | Размывает семантику |
| Открытый набор типов (extensible) | Гибкость | Без контроля типы будут плодиться; потеря совместимости между доменами | Таксономия должна быть стабильной |

## Последствия

**Что становится проще:**
- Автоматическая валидация: каждый Primitive должен принадлежать одному из шести типов
- Query layer: «дай все Metric для Espresso», «покажи Relation от Burr Grinder»
- Происхождение знания: Observation всегда имеет источник (тест), Specification — даташит, Metric — формулу

**Что усложняется:**
- При создании Primitive нужно выбрать тип — дополнительное решение
- Пограничные случаи: «Pump pressure 9 bar» — это Specification или Metric? (ответ: Specification, потому что заявлено производителем; Metric — когда вычислено или измерено)
- Law наиболее редкий и может быть перепутан с Relation

**Что требует внимания:**
- Не плодить подтипы — шести достаточно
- Если появляется знание, которое не влезает ни в один тип — это сигнал, что это не Primitive, а Component
- Metric со временем устаревает (цена, доступность) — нужен механизм актуализации
