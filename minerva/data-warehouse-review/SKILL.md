---
name: data-warehouse-review
description: "Программная проверка целостности data warehouse после импорта данных: structural integrity, dimension resolution, duplicates, DQ."
version: 1.0.0
triggers:
  - "Ревью склада"
  - "Проверка warehouse"
  - "Всё ли в порядке с данными"
  - "Data quality audit"
  - "После массового импорта"
---

# Data Warehouse Review

Систематическая проверка склада minerva: все ли observation-файлы консистентны, все ли dimensions резолвятся, нет ли дубликатов.

## Model

Warehouse: `warehouse/{domain}/` с bus-matrix.yaml, dim/ и fact/. Observation-файлы в `fact/observations/*.yaml`. Bus matrix содержит: aliases для резолвинга source-значений, mandatory_dimensions, allowed_measures, validation_rules. Dimensions в `dim/{type}/{id}.yaml`.

## Проверки

Выполняются программно (execute_code), не вручную. Порядок важен — от быстрых синтаксических к глубоким.

### 1. Structural Integrity

```
Для каждого observation:
  - fact.id == filename.stem
  - required keys: fact (id, type), source (all mandatory_dims), measures, meta (confidence, confidence_basis), lineage
  - все measure-ключи ∈ allowed_measures bus matrix
```

### 2. Dimension Resolution

```
Для каждого source-значения:
  1. bus matrix aliases → dim_id
  2. Прямой slug-матч → dim-файл
  3. Fuzzy: canonical_name dim-файла ≡ source-значение
```

### 3. Data Quality

```
Если fps_1pct_low > 0 и fps_avg > 0: проверить fps_avg > fps_1pct_low
Нарушения — source-data anomaly, маркировать в meta.note, не удалять.
```

### 4. Duplicate Detection

```
Группировать по ключу: (gpu, game_title, resolution, graphics_preset,
  upscaler, frame_gen, ray_tracing, ray_reconstruction, path_tracing)
Группа > 1 → DUP
```

### 5. Confidence Distribution

Сгруппировать по meta.confidence. Ожидаемые: 0.90 (precise), 0.85 (youtube), 0.70 (narrative).

### 6. Coverage

Сгруппировать по GPU, game_title. Проверить что все карты имеют минимальное покрытие.

## Порядок исправления

1. **Aliases + missing dims** — быстро, массово, bus matrix + dim-файлы
2. **Bool→string нормализация** — один проход, все `frame_gen: True` → `frame_gen: "true"` и т.д.
3. **Дубликаты** — удалять старые файлы без суффикса, оставлять более новые с `-native`/`-dlss-q` суффиксом
4. **DQ violations** — маркировать source-data, цифры не исправлять
5. **Structural fixes** — чинить причины (добавить меры в allowed_measures), не костылить

## Pitfalls

- **fg2x vs fg2x2x** — разные FG multiplier'ы с одинаковыми conditions. Исправлять conditions (FG=True → FG=2x), не удалять файлы
- **Python bool vs string** — YAML парсит `true` как bool. Все frame_gen должны быть строками
- **Resolution mismatch** — filename говорит 1440p, source.resolution = 1080p. Исправлять source, верить filename
- **"Alan Wake 2" vs "Alan Wake II"** — алиас в bus matrix есть, dim-файл не создан. Создавать dim
- **НЕ удалять observation с разными fps при одинаковых conditions** — это разные замеры, не дубликаты
