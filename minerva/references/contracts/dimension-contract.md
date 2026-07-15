# Dimension Contract

Агент создаёт dimension-файл через native fs-примитивы (`write_file`).
Этот контракт описывает что должно быть истинным — агент сам проверяет
и self-enforces. Никаких «шаг 1, шаг 2».

## Инварианты (должны быть истинны всегда)

### 1. Файл соответствует схеме dim_type

Схема определена в bus matrix: `dimensions.{dim_type}.attributes`.
Агент читает bus matrix → знает какие поля обязательны для этого типа.

Пример — GPU: attributes = [vendor, architecture, vram.size_gb, vram.type, ...]
Все обязательные поля должны присутствовать в файле.

### 2. Ссылки на другие dimensions резолвятся

Поля-ссылки (architecture, socket, predecessor) должны вести на существующие
dimension-файлы. Проверка: `dim-read` по ссылке → файл существует.

Пример — CPU:
```yaml
architecture: "amd-zen-4"  # → dim-read(architecture, amd-zen-4) → OK
socket: "am5"               # → dim-read(socket, am5) → OK
```

### 3. Alias зарегистрирован в bus matrix

Каждый dimension должен иметь хотя бы один alias в bus matrix.
Формат: `dimensions.{dim_type}.aliases: {"Human Name": "dim_id"}`.

Агент добавляет alias через `patch` в bus-matrix.yaml.
Правило: короткая форма (7600X) + полная форма (Ryzen 5 7600X) + canonical_name.

### 4. Surrogate key = dim_id

dim_id — стабильный идентификатор, не меняется при переименовании.
Формат: `{vendor}-{model}` (nvidia-rtx-5060) или `{vendor}-{name}` (amd-zen-4).

Natural key — `canonical_name`. Может меняться при ребрендинге.
Surrogate key (dim_id) — неизменен.

### 5. Файл создаётся по шаблону пути

Путь: `warehouse/{domain}/dim/{dim_type}/{dim_id}.yaml`
Шаблон определён в bus matrix: `dimensions.{dim_type}.canonical_dim`.

## SCD (Slowly Changing Dimension)

scd_type в dimension определяет поведение при изменении атрибутов:

| scd_type | Поведение | Пример |
|---|---|---|
| 0 | Immutable — перезапись | GPU, CPU, Game, Architecture |
| 2 | Versioned — новая версия файла | Driver version |

Для SCD Type 0: агент делает `write_file` поверх существующего.
Для SCD Type 2: агент создаёт `{dim_id}_v{date}.yaml`, обновляет `current_version`.

## Проверка целостности

После создания/изменения dimension:
- `dim-read` по новому dim_id → файл читается, атрибуты на месте
- `bus-lookup` по alias → возвращает dim_id
- `dim-read` по всем reference-полям → все резолвятся
