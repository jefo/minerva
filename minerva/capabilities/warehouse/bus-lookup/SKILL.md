---
capability: bus-lookup
layer: warehouse
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware', 'memory'"
      - name: dim_type
        type: string
        required: true
        description: "Тип dimension: gpu, game_title, cpu, socket, ..."
      - name: alias
        type: string
        required: true
        description: "Source-значение или user-facing имя для резолвинга"
  out:
    result: bus_lookup_result
    format: "{resolved_dim_id: string, dim_type: string, file_path: string}"
  errors:
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
    - code: DIM_TYPE_NOT_REGISTERED
      meaning: "dim_type не зарегистрирован в bus-matrix"
    - code: AMBIGUOUS_ALIAS
      meaning: "Несколько кандидатов — нужен уточняющий контекст"
    - code: NOT_FOUND
      meaning: "Alias не резолвится — ни в aliases, ни как прямой dim_id, ни как canonical_name"
idempotency: "read"
---

# bus-lookup — резолвинг source-значения в dimension_ref

Единая точка резолвинга для всех capability и агентов. Никакой capability не должен резолвить alias вручную.

## Model

Bus matrix (`warehouse/{domain}/bus-matrix.yaml`) для каждого dim_type определяет:
- `aliases` — маппинг source/user-facing значений → canonical dim_id
- `canonical_dim` — шаблон пути к dimension-файлу
- `id_format` — формат dim_id

Резолвинг трёхуровневый:
1. **Alias match** — ищем в `dimensions.{dim_type}.aliases`
2. **Direct dim_id match** — alias уже является валидным dim_id (файл существует)
3. **Canonical name match** — ищем по `canonical_name` во всех dim-файлах этого типа

## Invariants

- dim_type зарегистрирован в bus matrix (`dimensions.{dim_type}`)
- Результат всегда ведёт на существующий dim-файл
- Если несколько кандидатов — AMBIGUOUS_ALIAS с перечислением
- Если 0 кандидатов — NOT_FOUND с ближайшими candidates

## Примеры

```
bus-lookup(domain="hardware", dim_type="gpu", alias="RTX 5060")
→ aliases match: "RTX 5060" → "nvidia-rtx-5060"
→ dim_file: warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml
→ {resolved_dim_id: "nvidia-rtx-5060", file_path: "warehouse/hardware/dim/gpu/nvidia-rtx-5060.yaml"}

bus-lookup(domain="hardware", dim_type="gpu", alias="nvidia-rtx-5060")
→ direct match: dim_id уже валиден, файл существует
→ {resolved_dim_id: "nvidia-rtx-5060", ...}

bus-lookup(domain="hardware", dim_type="game_title", alias="CP2077")
→ aliases: нет матча
→ canonical_name search: "Cyberpunk 2077" содержит "2077" → candidates: ["cyberpunk-2077", "cyberpunk-2077-phantom-liberty"]
→ AMBIGUOUS_ALIAS {candidates: [...]}

bus-lookup(domain="hardware", dim_type="gpu", alias="GTX 1080")
→ aliases: нет матча
→ direct: нет файла
→ canonical_name search: нет матча
→ closest: ["nvidia-rtx-5060", "nvidia-rtx-5050"] (по similarity)
→ NOT_FOUND {candidates: [...]}
```

## Pitfalls

- **Не создавай dimension при NOT_FOUND.** Bus-lookup только читает. Создание — через dim-upsert + bus-register
- **Не кэшируй результат между сессиями.** Bus matrix может измениться (новый alias)
- **Передавай alias как строку от пользователя.** Не пытайся нормализовать заранее — bus-lookup сам обработает casing, пробелы
- **При AMBIGUOUS_ALIAS — спрашивай пользователя.** Не угадывай
