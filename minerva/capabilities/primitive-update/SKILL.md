---
name: primitive-update
type: capability
tier: 1
skill: minerva
status: scaffolding
contract:
  input: "путь к Primitive + поля для обновления"
  output: "обновлённый файл, bumped updated date"
based_on: [adr-004, adr-006, adr-011]
---

# Primitive Update

Изменить существующий Primitive.

## Контракт

**Вход:**
- Путь к `.md` файлу
- Поля для изменения (ключ→новое значение)

**Выход:**
- Обновлённый файл
- `updated` bumped до текущей даты
- Список изменённых полей

## Правила

1. Изменять только указанные поля frontmatter. Тело markdown — только если явно передано.
2. `updated` всегда bumped до текущей даты.
3. Не менять `id`, `type`, `created` — это immutable после создания.
4. После обновления — `primitive-validate`.
5. Если новое значение невалидно (например, `status: invalid_value`) — FAIL с объяснением.
6. Изменение `type` — особая операция. Требует подтверждения: «Вы меняете тип с Concept на Metric. Это может сломать ссылки. Продолжить?»

## Пример

```
primitive-update references/coffee/primitives/extraction-yield.md \
  value: 21.5 \
  status: verified
```
