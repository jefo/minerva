# SCD Contract (Slowly Changing Dimension)

Агент знает SCD из DW-методологии (Kimball). Этот контракт фиксирует
правила выбора SCD-типа и формат версионирования.

## SCD Type 0 — Immutable

**Когда:** атрибуты не меняются после выпуска продукта.
GPU, CPU, Architecture, Socket, Chipset — характеристики фиксированы.

**Действие при изменении:** `write_file` поверх существующего файла.
Старое состояние теряется (но git-history сохраняет).

## SCD Type 2 — Versioned

**Когда:** атрибуты меняются со временем и история имеет значение.
Driver version — единственный текущий пример.

**Формат версии:**
```
dim/driver_version/{dim_id}_v{yyyy-mm}.yaml
```
Пример: `nvidia-geforce-572.16_v2026-03.yaml`

**Заголовочный файл** (без `_v`) указывает текущую версию:
```yaml
dimension:
  id: "nvidia-geforce-572.16"
  scd_type: 2
  current_version: "nvidia-geforce-572.16_v2026-03"
  versions:
    - {file: "nvidia-geforce-572.16_v2026-03", date: "2026-03", changes: "Initial release"}
```

**Действие при изменении:**
1. Создать новый версионный файл: `{dim_id}_v{yyyy-mm}.yaml`
2. Обновить заголовочный файл: `current_version`, добавить запись в `versions`
3. Старые версии — не удалять (lineage может на них ссылаться)

## Связь с lineage

ADR-017: lineage всегда ссылается на конкретную версию dimension.
Если Law основан на observation с драйвером `nvidia-geforce-572.16_v2026-03`,
lineage указывает именно этот файл.

При выходе нового драйвера:
- Новый observation → ссылается на новую версию
- Старый Law → ссылается на старую версию (сохраняет контекст)
- impact-analysis → показывает что Law требует проверки на новом драйвере
