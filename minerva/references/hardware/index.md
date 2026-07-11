# Hardware Context

База знаний по компьютерному железу: GPU, CPU, чипсеты, память, питание.

## Статус

**В миграции.** Исходные данные в `catalog/` и `concepts/` (legacy-формат: `type: gpu`, `specs:`, `profiles:`). Постепенно декомпозируются в minerva Primitives в `primitives/`.

## Границы

В этом контексте: компоненты ПК как инженерные артефакты — архитектура, спецификации, поведенческие профили, совместимость. ПО, драйверы, бенчмарки — в отдельных контекстах.

## Структура

```
hardware/
├── catalog/        # legacy: GPU, CPU, MB, RAM, PSU, etc.
├── concepts/       # legacy: сквозные концепты (VRM, PCIe, тайминги)
├── docs/           # narrative arcs, schemas
├── primitives/     # minerva: Primitives всех типов ← пополняется
├── components/     # minerva: Components (сборки Primitives)
├── modules/        # minerva: Modules
├── views/          # minerva: Views (схемы анализа)
└── artifacts/      # minerva: Artifacts (готовые страницы)
```

## Primitives

| Файл | Тип | Суть |
|---|---|---|
| `nvidia-geforce-rtx-5090.md` | Concept | RTX 5090 как инженерный артефакт: архитектура, позиционирование |
| `rtx-5090-cuda-cores.md` | Specification | CUDA-ядра: 20480 (макс. конфигурация GB202) |
| `rtx-5090-500w-thermal.md` | Observation | 500W TBP → требования к БП и охлаждению |

Пополняется по мере миграции из `catalog/`.

## Правила

- Primitives создаются из данных `catalog/` и `concepts/` через `primitive-create`
- Каждый созданный Primitive валидируется через `primitive-validate`
- Legacy-записи (`catalog/gpu/*.md`) НЕ удаляются — служат источником и reference
- Новые Primitives могут ссылаться на legacy-записи через `source:` в frontmatter
