---
capability: fact-insert
layer: warehouse
tier: 1
contract:
  in:
    params:
      - name: domain
        type: string
        required: true
        description: "Bounded context: 'hardware', 'memory'"
      - name: fact_type
        type: string
        required: true
        description: "Тип факта: 'observation', 'metric', 'memory_entry'"
      - name: source
        type: map[string]string
        required: true
        description: "Сырые source-значения: {gpu: 'RTX 5060', game_title: 'Cyberpunk 2077', ...}"
      - name: measures
        type: map[string]number
        required: true
        description: "Числовые измерения: {fps_avg: 103, fps_1pct_low: 85, ...}"
      - name: conditions
        type: map[string]string
        required: false
        default: "{}"
        description: "Контекст замера: {upscaler: 'DLSS 4 Quality', frame_gen: '4x', ...}"
      - name: meta
        type: map
        required: true
        description: "Provenance: confidence, confidence_basis, observed_at, observed_by, source_url (обязательно)"
  out:
    result: fact_insert_result
    format: |
      {fact_id: string, file_path: string, resolved_dimensions: map, warnings: [string]}
  errors:
    - code: DOMAIN_NOT_FOUND
      meaning: "Bounded context не существует"
    - code: BUS_MATRIX_NOT_FOUND
      meaning: "bus-matrix.yaml для domain не найден"
    - code: MISSING_MANDATORY_DIMENSION
      meaning: "В source отсутствует обязательный dimension"
    - code: UNKNOWN_DIMENSION_VALUE
      meaning: "source-значение не резолвится через aliases и dim-файл не существует"
    - code: UNKNOWN_MEASURE
      meaning: "measure не входит в allowed_measures bus matrix"
    - code: VALIDATION_FAILED
      meaning: "Нарушено бизнес-правило (validation_rules bus matrix)"
    - code: DUPLICATE_FACT
      meaning: "Fact с теми же mandatory_dimensions уже существует"
    - code: MISSING_SOURCE_URL
      meaning: "meta.source_url отсутствует или пуст"
idempotency: "write"
---

# fact-insert — записать Fact в warehouse

Единственная точка записи Fact-файлов. Домен-нейтральный: любой bounded context на платформе.

## Model

Warehouse построен по dimensional model (Kimball):

```
warehouse/{domain}/
├── bus-matrix.yaml        # контракт домена: dimensions, facts, aliases, measures, validation_rules
├── definitions/           # семантика метрик (average-fps.yaml, ...)
├── dim/{type}/{id}.yaml  # Dimensions — описательные атрибуты
└── fact/{type}/{id}.yaml # Facts — измерения, ссылаются на Dimensions через source-значения
```

**Source layer (ADR-025):** Fact хранит source-значения как сырые строки (`gpu: "RTX 5060"`), не dimension ID (`gpu: "nvidia-rtx-5060"`). Резолвинг source → dim_id происходит при чтении (bus matrix aliases), не при записи. Fact не знает о существовании dimension-файлов.

**Platform/app split (ADR-026):** fact-insert — платформенный capability. Не содержит доменной логики. Прикладной ingestion-скрипт нормализует сырые данные (markdown, CSV) → вызывает fact-insert.

**Bus matrix** для каждого domain определяет:
- `mandatory_dimensions` — без них Fact невалиден
- `allowed_measures` — только перечисленные меры
- `validation_rules` — бизнес-правила (например, `fps_avg > fps_1pct_low`)
- `aliases` — source-значение → canonical dim_id (например, `"RTX 5060" → "nvidia-rtx-5060"`)

## Invariants

Нарушение любого инварианта — ошибка, Fact не создаётся.

| # | Инвариант | Механизм проверки |
|---|---|---|
| 1 | Domain и bus matrix существуют | Файловая система |
| 2 | Все mandatory_dimensions bus matrix присутствуют в source | Сравнение ключей |
| 3 | Каждое source-значение резолвится в dimension | Aliases → direct dim_id → canonical_name search |
| 4 | Все measures входят в allowed_measures | Сравнение ключей |
| 5 | Все validation_rules выполняются | Проверка выражений (measure > measure, ...) |
| 6 | Fact уникален по mandatory_dimensions | Проверка существующих Fact-файлов |
| 7 | Структура файла — строго по шаблону | Платформа диктует формат |
| 8 | meta.source_url — обязательное поле | Проверка наличия и непустоты |

## Template

Каждый Fact-файл имеет идентичную структуру. Вариации не допускаются — это платформенная гарантия.

```yaml
fact:
  id: "{slugified_dimensions}-{config_suffix}"
  type: "{fact_type}"
source:
  {dim_type}: "{original_source_value}"   # сырые строки, не dim_id
measures:
  {measure_name}: {value}
conditions:                               # опционально — контекст замера
  {key}: "{value}"
meta:
  confidence: {number}                    # обязательно
  confidence_basis: "{string}"            # обязательно
  source_url: "{string}"                  # обязательно — URL источника или "training_data" / "manual"
  source_title: "{string}"                # опционально — название видео/статьи
  observed_at: "{string}"
  observed_by: "{string}"
  source_channel: "{string}"
  note: "{string}"
lineage:
  nodes: []
  edges: []
```

Обязательные поля: `fact`, `source` (все mandatory dims), `measures`, `meta.confidence`, `meta.confidence_basis`, `meta.source_url`, `lineage`.

Опциональные: `source`-поля optional_dims, `conditions` (нет условий → секция отсутствует), `meta.source_title`, `meta.note`, `meta.source_timestamp`.

## Naming

**fact_id** собирается платформой (приложение не выбирает ID):

```
{gpu_slug}-{game_slug}-{res}-{preset_slug}-{config_suffix}
```

- `slug` — lowercase, спецсимволы удалены, пробелы → дефисы
- `config_suffix` — отличает Fact от других с теми же dimensions: `native`, `dlss4-q`, `dlss4-q-mfg4x`, `rt-high`
- Порядок слагов фиксирован: GPU, game, resolution, preset
- domain и fact_type НЕ входят в fact_id — они в пути файла

Путь: `warehouse/{domain}/fact/{fact_type}/{fact_id}.yaml`

Пример: `warehouse/hardware/fact/observations/rtx-5060-cyberpunk-2077-1080p-ultra-native.yaml`

## Batch

Массовый импорт: для каждого элемента батча — полный цикл валидации. Ошибка в одном Fact не откатывает предыдущие (не транзакционно).

Возвращается сводка: `{inserted: N, errors: [...], warnings: [...]}`.

## Pitfalls

- **Не заменять source-значения на dim_id при записи.** Source хранит `"RTX 5060"`, не `"nvidia-rtx-5060"`. Резолвинг — для валидации и ответа, не для мутации данных
- **confidence — обязательное.** Приложение должно указать. Нет default
- **source_url — обязательное.** Без него факт невалиден. Допустимые значения: HTTP(S) URL → реальный источник; `"training_data"` → данные из knowledge модели; `"manual"` → ручной замер без публичной ссылки
- **fact_id генерируется, не принимается.** Приложение не может диктовать ID файла
- **Batch не атомарен.** Не полагаться на откат
- **Dimensions создаются отдельно.** Если source-значение не резолвится — ошибка, не создавай dim на лету
- **Формат файла — не предмет переговоров.** Шаблон един для всех Fact одного типа. Не добавляй поля, не меняй порядок ключей
