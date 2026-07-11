# PC Hardware Knowledge Base

Файловая база знаний по компьютерному железу. Компоненты, концепты, связи — в формате, оптимизированном для работы LLM.

## Архитектура

```
catalog/        — дерево компонентов (CPU, GPU, MB, RAM, ...)
concepts/       — сквозные концепты (VRM, PCIe lanes, тайминги)
scripts/        — инструменты query-слоя
```

### Принципы

1. **Progressive disclosure** — каждый уровень содержит `index.md`, который LLM загружает для ориентирования. Группировка в подпапки — только там, где файлов становится >5–7 штук.
2. **Один компонент — один файл.** Связанные компоненты группируются в папки (например, `motherboard/am5/`).
3. **SysML-связи в frontmatter.** Каждый компонент ссылается на связанные сущности через `links:` с относительными путями. LLM идёт по графу, загружая только нужное.
4. **Query layer.** Python-скрипты в `scripts/` обеспечивают выборки по vendor, socket, type и другим атрибутам — независимо от структуры файловой системы.

### Frontmatter-схема

```yaml
---
id: "msi-b650-tomahawk"          # URL-safe slug
type: "motherboard"               # cpu | gpu | motherboard | memory | storage | psu | cooling | case | monitor
title: "MSI MAG B650 TOMAHAWK"
vendor: "msi"
status: "draft"                   # draft | review | verified
tags: ["am5", "b650", "ddr5"]
last_updated: "2025-06-03"
links:
  socket: "catalog/cpu/amd-ryzen-7000.md"
  memory_type: "catalog/memory/ddr5.md"
  chipset: "catalog/motherboard/am5/b650.md"
---
```

### Как работает LLM

1. Загружает `catalog/index.md` → карта всего каталога
2. По задаче выбирает ветку, загружает её `index.md`
3. `index.md` содержит не просто список файлов, а **семантическую карту**: что лежит, ключевые параметры, указатели на концепты
4. Загружает конкретный entry → структурированные знания с перекрёстными ссылками

### Query layer

```bash
python scripts/query.py --type motherboard --socket am5
python scripts/query.py --vendor msi
python scripts/query.py --tag ddr5 --tag atx
python scripts/query.py --links-to catalog/memory/ddr5.md
```

Возвращает пути к файлам. LLM дальше загружает что нужно.

## Статус

- [x] Скелет каталога (все index.md)
- [x] Образцовые entry: MSI B650 Tomahawk, AMD Zen 4, DDR5
- [x] Python query layer
- [ ] Наполнение контентом (непрерывный процесс)

## Конвенции

- `index.md` — **обязателен** в каждой директории. Это точка входа для LLM.
- Имена файлов: `vendor-model.md` (строчные, дефисы). Пример: `msi-b650-tomahawk.md`
- Статусы: `draft` → `review` → `verified`. Только `verified` считается авторитетным.
- Все пути в `links:` — от корня репо. Пример: `catalog/cpu/amd-ryzen-7000.md`
