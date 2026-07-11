---
name: primitive-deprecate
type: capability
tier: 1
skill: minerva
status: scaffolding
contract:
  input: "путь к Primitive + причина + superseding_primitive (опционально)"
  output: "Primitive помечен как deprecated, отчёт об affected references"
based_on: [adr-004, adr-006, adr-011]
---

# Primitive Deprecation

Пометить Primitive как устаревший.

## Контракт

**Вход:**
- Путь к `.md` файлу
- Причина deprecation (текст)
- `superseded_by` — ID замещающего Primitive (опционально)

**Выход:**
- Файл обновлён: `status: deprecated`, `superseded_by` добавлен
- Отчёт: какие Components/Modules/Artifacts ссылаются на этот Primitive (из `impact-analysis`)

## Правила

1. `status` → `deprecated`. `updated` → текущая дата.
2. Если указан `superseded_by` — проверить, что замещающий Primitive существует.
3. Deprecation не удаляет файл. Файл остаётся в `primitives/` для traceability.
4. После deprecation — `impact-analysis` для предупреждения о сломанных ссылках.
5. Primitive в статусе `deprecated` исключается из `comparison` и `recommendation` (Tier 4).
6. Deprecation необратима без ручного вмешательства (как git revert).

## Пример

```
primitive-deprecate references/coffee/primitives/pump-pressure.md \
  reason: "Заменён на уточнённое значение 8.7 bar из Observation" \
  superseded_by: coffee-measured-pressure-8-7
```
