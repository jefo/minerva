---
name: compile-context-map
description: "Генерирует context-map.yaml — семантический индекс всего DWH: dimensions, observation, laws, patterns. Вызывается после любого изменения данных в складе."
triggers:
  - "обнови карту контекстов"
  - "сгенерируй context-map"
  - "compile context map"
  - "перестрой индекс склада"
---

# Compile Context Map

**Назначение:** генерирует `references/context-map.yaml` — AI-native индекс склада, по которому consumer (редактор, агент) ориентируется без знания fs-структуры.

## Контракт

```
IN:  корень DWH (директория, содержащая warehouse/ и marts/)
OUT: references/context-map.yaml — семантический индекс
```

## Бизнес-логика

Consumer приходит в DWH. Ему не нужно знать, что observation лежат в `fact/observations/`, а законы — в `marts/engineering/laws/`. Он загружает `context-map.yaml` и видит:

- Какие сущности есть (10 GPU, 28 CPU, 71 игра)
- Какие данные покрыты (439 GPU observation, 320 CPU)
- Какие законы выведены (3 закона с темами)
- Какие capabilities доступны (comparison, lineage-trace, ...)

Дальше — точечная загрузка нужных файлов через `skill_view`.

## Процесс

### Шаг 1 — Запуск генератора

```bash
cd <DWH_ROOT>
python3 capabilities/warehouse/compile-context-map/scripts/generate.py \
  --warehouse-root . \
  --output references/context-map.yaml
```

Скрипт:
- Обходит `warehouse/hardware/dim/` → собирает dimensions по типам (id, canonical_name, ключевые атрибуты)
- Обходит `warehouse/hardware/fact/observations/` → группирует: сколько, по каким GPU/CPU, игры, разрешения
- Обходит `marts/` → законы, паттерны (id, statement, confidence)
- Сканирует `capabilities/` → список доступных capabilities
- Генерирует `context-map.yaml`

### Шаг 2 — Верификация

Убедись что `references/context-map.yaml` создан и содержит все секции: `dimensions`, `observations`, `marts`, `capabilities`.

## Когда вызывать

- После добавления новых dimension (новый GPU/CPU в каталоге)
- После массового импорта observation
- После создания нового law/pattern
- После любого структурного изменения склада

## Pitfalls

- **Устаревшая карта.** Если данные изменились, а context-map не перегенерирована — consumer видит неактуальную картину. Правило: любое изменение склада → регенерация.
- **Большие склады.** При 1000+ observation генерация может занять секунды. Это нормально.
- **Битая YAML.** Если observation содержит синтаксическую ошибку — скрипт пропускает файл с warning в stderr.
