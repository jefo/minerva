---
id: adr-011
status: accepted
date: 2026-07-11
supersedes: [adr-009]
superseded_by: []
tags: [architecture, capabilities, roadmap, analytical-layer, domain-agnostic]
based_on: [adr-002, adr-004, adr-005, adr-009]
---

# ADR-011: Capability roadmap — от создания знаний до аналитического слоя

## Контекст

ADR-009 определил MVP — четыре capabilities навигации по workspace. Это достаточный минимум чтобы агент мог «видеть» knowledge base. Но Knowledge Services задуман как композиционный движок знаний с аналитическим слоем — не просто хранилище фактов, а система, в которой знания собираются в модели, модели — в анализ, анализ — в готовые артефакты.

Традиционные KB (включая `pc_hardware_knowledge_base`) останавливаются на уровне «каталог фактов + query layer». Связи между фактами не формализованы. Инженерные модели существуют только в головах авторов. Аналитика каждый раз пишется с нуля.

Knowledge Services решает эту проблему через архитектуру композиции (ADR-002) и capabilities как Use Cases (ADR-005). Но нужна дорожка: в каком порядке capabilities появляются и почему.

## Решение

Четыре тира capabilities. Каждый следующий тир зависит от предыдущего — не технически, а семантически: нельзя анализировать то, что не скомпоновано; нельзя компоновать то, что не создано.

### Фундаментальный принцип: capabilities домен-агностичны

Ни одна capability не знает о hardware, кофе или любой другой предметной области. `comparison` сравнивает два Module — неважно, GPU это или кофемолки. `recommendation` подбирает лучший Module под constraints — неважно, видеокарта это или метод заваривания.

Домен живёт в данных — Primitives, Components, Modules. Capabilities — это операции над данными, выраженные в терминах таксономии Knowledge Services (ADR-002, ADR-004), не в терминах домена.

### Tier 1 — Primitive Management

Создание словаря предметной области. Без этого тира невозможно ничего построить — Primitives это «атомы», из которых собирается всё остальное.

| Capability | Бизнес-операция | Пример (абстрактный) |
|---|---|---|
| `primitive-create` | Создать новый Primitive с валидным frontmatter | Создать `.md` файл с `type: Concept`, `title: Espresso` |
| `primitive-validate` | Проверить frontmatter на соответствие таксономии | Все обязательные поля? `type` из списка 6? |
| `primitive-bulk-import` | Массовое создание Primitives из structured source | Импорт 15 GPU из datasheet |
| `primitive-update` | Изменить существующий Primitive | Обновить TDP с 250W на 280W |
| `primitive-deprecate` | Пометить Primitive как устаревший | `status: deprecated`, указать `superseded_by` |

**Зависит от:** ADR-002 (уровни), ADR-004 (таксономия типов), ADR-007 (структура контекста)

### Tier 2 — Composition

Сборка знаний в осмысленные единицы. Здесь Primitives перестают быть изолированными фактами и становятся частями моделей.

| Capability | Бизнес-операция | Пример |
|---|---|---|
| `component-compose` | Собрать Component из 2+ Primitives | Brewing Parameters = Dose + Temperature + Pressure + Time |
| `module-assemble` | Собрать Module из Components и Primitives | Espresso Extraction Model = Brewing Parameters + Grind Quality + Extraction Law |
| `view-define` | Создать аналитическую схему (View) | Brewing Method Analysis: Principle → Equipment → Parameters → Technique → Taste → Recommendations |
| `artifact-compile` | Собрать Artifact из View + конкретных Modules/Components | Espresso Brewing Guide = Process Guide View + Extraction Model + Brewing Parameters Component |

**Зависит от:** Tier 1 (Primitives должны существовать), ADR-002 (уровни), ADR-003 (downward visibility)

### Tier 3 — Integrity & Governance

Контроль качества knowledge base. Автоматические проверки, которые не дают KB деградировать при росте.

| Capability | Бизнес-операция | Пример |
|---|---|---|
| `integrity-check` | Проверить downward visibility, кросс-ссылки, дубликаты | «Этот Component ссылается на несуществующий Primitive» |
| `impact-analysis` | Показать, что затронет изменение | «Extraction Model используется в 3 Artifacts: Guide, Comparison, Troubleshooting» |
| `consistency-audit` | Найти противоречия, сирот, дрейф | «Два Observation для extraction yield: 20% и 21.3% — reconcile или пометить contested» |

**Зависит от:** Tier 2 (композиции должны существовать чтобы проверять их целостность), ADR-003, ADR-006 (git workflow)

### Tier 4 — Analysis & Query

Аналитический слой. KB перестаёт быть справочником и становится инструментом принятия решений.

| Capability | Бизнес-операция | Пример |
|---|---|---|
| `cross-reference` | Найти все Relation для заданной сущности | «Что связано с Espresso?» → requires Fine Grind, brewed_at 9 bar, has_variant Ristretto |
| `comparison` | Side-by-side двух сущностей одного уровня | Espresso vs Filter Coffee: dose, temperature, pressure, extraction |
| `tradeoff-analysis` | Идентифицировать gains/losses между альтернативами | «Espresso: +intensity, +body, −volume vs Filter» |
| `recommendation` | Подобрать сущность под заданные constraints | «Лучший метод заваривания для: bright acidity, light body, quick prep» → Filter |
| `gap-analysis` | Показать недозаполненные уровни | «Контекст coffee: 6 Primitives, 0 Components, 0 Modules, 0 Artifacts» |

**Зависит от:** Tier 3 (анализ на нецелостных данных производит ложные выводы), ADR-002, ADR-004

## Что НЕ входит в roadmap

- **Визуализация графа композиции.** Полезно, но отдельный продукт.
- **NLP-интерфейс.** «Спроси KB на естественном языке» — отдельная capability, не этого этапа.
- **Мульти-воркспейс федерация.** Связи между разными инстансами minerva — будущее.
- **Real-time collaborative editing.** Git + PR покрывают 80%. Google Docs-style — не цель.

## Приоритет

1. **Tier 1** — немедленно. Без Primitives нечего компоновать. `primitive-create` + `primitive-validate` — входной билет.
2. **Tier 2** — следом. `component-compose` — первый уровень где появляется смысл. `artifact-compile` — конечная цель: страница собирается, не пишется.
3. **Tier 3** — когда KB достигает размера, при котором ручной контроль невозможен (~50+ Primitives, 10+ Components).
4. **Tier 4** — когда KB содержит достаточно моделей чтобы на их основе принимать решения.

## Связь с ADR-009 (MVP)

ADR-009 (MVP-навигация) остаётся в силе как Tier 0. Четыре capabilities навигации — это pre-requisite для всех последующих тиров. Без навигации агент не может найти Primitives чтобы их создать или скомпоновать.

ADR-011 расширяет, не заменяет.

## Последствия

**Что становится проще:**
- Планирование: каждый тир — веха, можно мерить прогресс
- Параллельная разработка: разные команды могут делать Tier 1 и Tier 3 одновременно (контракты уже определены)
- Приоритизация: если пользователь спрашивает «почему не делаете recommendation» — ответ: «потому что не пройден Tier 2, не из чего рекомендовать»

**Что требует внимания:**
- Не начинать Tier 2 пока Tier 1 не стабилен. Иначе Components собираются из невалидированных Primitives — мусор на входе, мусор на выходе
- Capabilities не должны знать домен. Если `comparison` начинает спрашивать «GPU или CPU?» — ошибка архитектуры
- Каждый тир должен быть independently releasable. Пользователь может остановиться на Tier 2 и это будет полезный продукт
