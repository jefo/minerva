---
capability: contradiction-detect
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
    result: contradiction_report
    format: |
      {
        contradictions: [
          {fact_a: {id, file_path, measures, source_url, confidence},
           fact_b: {id, file_path, measures, source_url, confidence},
           shared_dimensions: {gpu, game_title, resolution, preset},
           delta: {measure: {value_a, value_b, percent}},
           severity: "SIGNIFICANT"|"MINOR"},
          ...
        ],
        stats: {total_checked: N, conflicts: N}
      }
  errors:
    - code: NO_FACTS
      meaning: "Нет observation для домена"
idempotency: "read"
---

# contradiction-detect — найти противоречащие observation

Сканирует observation с одинаковыми mandatory dimensions но разными значениями
мер. Два источника показали разный FPS в одной игре — это не ошибка данных,
а сигнал к расследованию.

## Model

Группировка observation по mandatory_dimensions (gpu + game_title + resolution
+ graphics_preset + driver_version). Если в группе больше одного observation
и меры различаются на значимую величину — contradiction.

**Порог значимости:** разница > 10% по fps_avg или > 15% по fps_1pct_low.
Меньшие расхождения — в пределах погрешности измерения.

## Invariants

- Только для observation с одинаковыми mandatory dimensions
- Разные driver_version — разные группы (не contradiction, а NEWER_DRIVER в stale-check)
- source_url — ключевое поле для расследования: «reviewer A показал X, reviewer B показал Y»
- Не удаляет, не разрешает — только флажит

## Пример

```
contradiction-detect(domain="hardware")

→ найдено: 2 observation для RTX 5060 / Cyberpunk 2077 / 1440p / Ultra / 572.16
    fact_a: fps_avg=68, source_url=youtube.com/watch?v=ABC, confidence=0.85
    fact_b: fps_avg=74, source_url=youtube.com/watch?v=XYZ, confidence=0.85
    delta: 8.8% — MINOR (within threshold)
→ conflicts: 0 SIGNIFICANT, 1 MINOR
```

## Pitfalls

- **Не все расхождения — ошибки.** Разные сцены бенчмарка, разная память, разный cooling → разный FPS. Contradiction — приглашение к расследованию, не вердикт.
- **Training data — особый случай.** Два training_data observation с разными цифрами → не contradiction, а «оба приблизительны, нужен реальный замер».
- **Не блокирует fact-insert.** Contradiction обнаруживается постфактум. Не запрещает запись.
