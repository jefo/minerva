---
capability: stale-check
layer: analysis
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware'"
      - name: fact_type
        type: string
        required: false
        default: "observation"
        description: "Тип факта для проверки"
  out:
    result: staleness_report
    format: |
      {
        stale_facts: [
          {fact_id, reason: "NEWER_DRIVER"|"SUPERSEDED"|"TRAINING_DATA", newer_fact_id?, ...},
          ...
        ],
        affected_derived: [
          {derived_id, derived_type, impacted_by: [fact_id, ...]},
          ...
        ],
        stats: {total_checked: N, stale: N, affected_laws: N},
        recommendation: "REVIEW_RECOMMENDED" | "NO_STALE_DATA"
      }
  errors:
    - code: NO_FACTS
      meaning: "Нет observation для домена"
idempotency: "read"
---

# stale-check — найти устаревшие данные и затронутые выводы

Сканирует observation на устаревание. Для каждого stale-observation
запускает impact-analysis — находит Laws, которые нужно перепроверить.

## Model

**Три причины устаревания:**

1. **NEWER_DRIVER** — тот же GPU + игра + разрешение + пресет, но с более новым драйвером. Старый observation — исторический интерес, не operational truth.

2. **SUPERSEDED** — тот же набор mandatory dimensions, но новый observation с более высоким confidence. Старый — кандидат на замену.

3. **TRAINING_DATA** — observation помечен как training_data. Флаг для контент-отдела: «эти цифры нужно заменить реальными замерами перед публикацией». Не ошибка данных, а приоритет acquisition.

## Invariants

- Проверяются ВСЕ observation в `warehouse/{domain}/fact/{fact_type}/`
- Для каждого stale-observation → impact-analysis → affected_derived
- Если ни одного stale-observation → NO_STALE_DATA
- Если есть affected Laws → REVIEW_RECOMMENDED

## Пример

```
stale-check(domain="hardware", fact_type="observation")

→ всего проверено: 440 GPU observations
→ stale (NEWER_DRIVER): 15 observation на драйвере 546.33,
   когда есть более свежие на 572.16 для тех же GPU+игр
→ stale (TRAINING_DATA): 320 cpu_observations
→ affected_derived: 0 (Laws ещё не созданы)
→ recommendation: REVIEW_RECOMMENDED

Контент-отдел видит:
- 15 GPU-замеров устарели (новый драйвер) → перетестировать или пометить как historical
- 320 CPU-замеров — training_data → prioritise replacement с реальными замерами
```

## Pitfalls

- **NEWER_DRIVER — не всегда перетест.** Если разница между драйверами < 3% (в пределах погрешности) — observation может быть всё ещё валидным. Stale-check флажит, агент решает.
- **TRAINING_DATA ≠ ошибка.** Это валидные данные с пониженным confidence для prioritisation. Не удалять.
- **Не пересчитывает автоматически.** Stale-check находит проблемы, не исправляет их.
