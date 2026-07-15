---
capability: impact-analysis
layer: analysis
contract:
  in:
    params:
      - name: fact_ref
        type: string
        required: true
        description: "Observation ID или путь к файлу"
  out:
    result: impact_report
    format: |
      {
        fact: {id, file_path},
        affected: [
          {derived_id, derived_type, level, statement, impact: "DIRECT"|"INDIRECT"},
          ...
        ],
        stats: {laws: N, patterns: N, comparisons: N, artifacts: N},
        recommendation: "REVIEW_RECOMMENDED" | "STALE_MARKED" | "NO_IMPACT"
      }
  errors:
    - code: FACT_NOT_FOUND
      meaning: "Observation не существует"
idempotency: "read"
---

# impact-analysis — найти всё, что затронуто изменением observation

Обратное lineage-trace: observation изменился (новый драйвер, новый замер,
исправлена ошибка) → какие Law, Pattern, Comparison, Artifact нужно перепроверить?

## Model

Поиск по всем derived-файлам в `marts/`: в каких `lineage.nodes` фигурирует
этот observation. Для каждого найденного derived → категория воздействия.

**Типы воздействия:**
- `DIRECT` — observation — один из evidence-узлов Law. Law может стать неверным.
- `INDIRECT` — observation входит в Comparison, который используется Law.
  Law может быть затронут через цепочку.

## Invariants

- Возвращает пустой список если observation нигде не используется (NO_IMPACT)
- Если найден хотя бы один Law с этим observation → recommendation = REVIEW_RECOMMENDED
- Поиск по всем подкаталогам `marts/`

## Пример

```
impact-analysis(fact_ref="amd-ryzen-7-7800x3d-1080p-low-counter-strike-2-native")

→ fact: {id: "amd-ryzen-7-7800x3d-1080p-low-counter-strike-2-native",
         fps_avg: 520, source: training_data}
→ affected:
    DIRECT: Law "3D V-Cache даёт +15-20% FPS в CPU-bound" (Level 2)
    DIRECT: Law "Zen 4 gaming performance ceiling" (Level 2)
→ stats: 2 laws affected
→ recommendation: REVIEW_RECOMMENDED
```

Теперь агент знает: если перетестировать 7800X3D в CS2 с новым драйвером и
получить 540 fps вместо 520 — оба Law требуют пересмотра.

## Pitfalls

- **Не автоматическое.** Impact-analysis находит затронутые Law, но не пересчитывает их. Решение о пересмотре — за агентом или редактором.
- **Поиск — по всем marts/** — O(N) по числу derived-файлов. На сотнях Law может быть медленным. На десятках — мгновенно.
- **INDIRECT работает только при полном lineage.** Если Comparison не сохранён как derived — цепочка прерывается.
