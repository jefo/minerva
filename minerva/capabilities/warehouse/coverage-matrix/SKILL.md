---
capability: coverage-matrix
layer: warehouse
tier: 2  # Composition — аналитика поверх склада
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware'"
      - name: game_set
        type: "[string]"
        required: false
        description: "Фильтр по играм (canonical_name или slug). Если не указан — все игры"
      - name: resolution
        type: string
        required: false
        description: "Фильтр: '1080p', '1440p', '4K'. Если не указан — все"
      - name: preset
        type: string
        required: false
        description: "Фильтр: 'Ultra', 'High', ... Если не указан — все"
  out:
    result: coverage_report
    format: |
      {cells: [{gpu, game, resolution, preset, mode, status, best_fps, confidence}], summary: {total, green, yellow, red, coverage_pct}}
  errors:
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
idempotency: "read"
---

# coverage-matrix — матрица покрытия данных

## Model

Coverage Matrix — это кросс-продукт GPU × Game × Resolution × Preset × Mode, показывающий для каждой ячейки есть ли данные в складе.

**Mode** извлекается из conditions Fact'а:
- `raster` — upscaler=native, frame_gen=false
- `upscaled` — upscaler ≠ native, frame_gen=false
- `frame_gen` — frame_gen ≠ false (любой FG/MFG)

**Статус ячейки:**
- 🟢 `covered` — ≥1 observation с confidence ≥ 0.85
- 🟡 `partial` — ≥1 observation с confidence < 0.85
- 🔴 `gap` — 0 observations

## Invariants

- Domain должен существовать (warehouse/{domain}/bus-matrix.yaml)
- GPU список — все зарегистрированные в dim/gpu/
- Game список — все зарегистрированные в dim/game_title/ (или отфильтрованные game_set)
- Resolution и Preset — из bus matrix canonical_values
- Ячейка с несколькими observations → показывается best_fps (максимальный confidence)

## Output

```yaml
coverage:
  filters:
    domain: hardware
    resolution: 1440p
    preset: Ultra
  matrix:
    - gpu: "RTX 4070 Ti Super"
      game: "Cyberpunk 2077"
      resolution: "1440p"
      preset: "Ultra"
      raster: covered      # 87 fps, conf 0.75
      upscaled: covered    # 112 fps, conf 0.75
      frame_gen: gap
  summary:
    total_cells: 120
    covered: 45
    partial: 12
    gap: 63
    coverage_pct: 37.5
```

## Pitfalls

- Mode извлекается из conditions, не из filename. Два Fact'а могут попасть в одну ячейку с разным confidence — брать максимальный
- GPU с разными source-именами (RTX 4070 Ti vs RTX 4070 Ti Super) — разные строки матрицы
- Игры с разными canonical_name (Hogwarts Legacy vs Hogwarts Legacy) — резолвятся в один slug через bus matrix
