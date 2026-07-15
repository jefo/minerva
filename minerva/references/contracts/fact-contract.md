# Fact Contract

Агент создаёт fact-файл через `fact-insert` capability (write path) или читает
через `fact-read` (read path). Этот контракт фиксирует что должно быть истинно
для любого Fact в системе, независимо от fact_type.

## Инварианты (для любого Fact)

### 1. Grain определён в bus matrix

Каждый fact_type имеет `grain` — что означает одна строка.
Пример: `observation` → `single_benchmark_run`, `cpu_observation` → `single_cpu_benchmark_run`.

### 2. Mandatory dimensions заполнены

Bus matrix: `facts.{fact_type}.mandatory_dimensions`.
Fact должен содержать source-значения для всех mandatory dims.
Для observation: gpu + game_title + resolution + graphics_preset + driver_version.
Для cpu_observation: cpu + benchmark_scenario + game_title + resolution + graphics_preset + driver_version.

Исключение: `cpu_observation` с synthetic-сценарием — game_title не обязателен
(bus matrix validation_rules).

### 3. Source-значения — сырые строки

Fact хранит source-значения как строки (`source.gpu: "RTX 5060"`), не dim_id.
Резолвинг source → dim_id происходит при чтении (bus matrix aliases + bus-lookup).
Fact не знает о структуре dim/ директории. ADR-025.

### 4. Measures — только из allowed_measures

Bus matrix: `facts.{fact_type}.allowed_measures`.
Measure не может быть записан если не зарегистрирован в bus matrix.

### 5. Business validation rules выполняются

Bus matrix: `facts.{fact_type}.validation_rules`.
Пример: `fps_avg > fps_1pct_low`.

### 6. Fact уникален по mandatory dimensions

Не может быть двух Fact с одинаковым набором mandatory_dimensions.
Проверка при `fact-insert`: поиск существующих файлов с теми же dims.

### 7. Provenance: source_url обязателен

`meta.source_url` — откуда данные.
Допустимые значения: URL, `"training_data"`, `"manual"`.
Без source_url fact-insert отклоняет Fact.

## Структура файла

```yaml
fact:
  id: "{unique-fact-id}"
  type: "{fact_type}"
source:
  {dim_type}: "{original_source_value}"
measures:
  {measure_name}: {number}
conditions:                    # опционально
  {key}: "{value}"
meta:
  confidence: {0-1}
  confidence_basis: "{...}"
  source_url: "{url|training_data|manual}"
  source_title: "{...}"
  observed_at: "{iso-date}"
  observed_by: "{agent-id}"
lineage:
  nodes: []
  edges: []
```

## Связь с другими контрактами

- **Dimension Contract:** source-значения резолвятся в dimensions через bus matrix aliases
- **SCD Contract:** lineage ссылается на конкретную версию dimension (SCD Type 2)
- **Bus Matrix:** SSOT для grain, mandatory_dims, allowed_measures, validation_rules
