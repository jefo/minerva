# Hardware KB → Minerva: План миграции

**Цель:** перевести `pc_hardware_knowledge_base` с legacy-таксономии (`type: gpu`, `specs:`, `profiles:`) на minerva-таксономию (Primitives: Concept, Specification, Observation, Law, Relation, Metric).

**Стратегия:** feature branch `v2` в том же репо. Оригинал на `main` остаётся нетронутым.

## Фазы

### Фаза 0 — Подготовка

- [ ] В репо `kaizin-lab/pc_hardware_knowledge_base` создать ветку `v2` от `main`
- [ ] В корне `v2` создать `minerva/` — новый корень для мигрированной структуры
- [ ] В `minerva/` создать `references/hardware/` с поддиректориями: `primitives/`, `components/`, `modules/`, `views/`, `artifacts/`
- [ ] Создать `minerva/references/hardware/index.md` — карта контекста

### Фаза 1 — Декомпозиция GPU (15 записей)

Для каждой GPU-записи из `catalog/gpu/*.md`:

1. **Извлечь Primitives:**
   - `Concept` — карта как сущность (название, архитектура, позиционирование)
   - `Specification` — каждый параметр из `specs:` (cuda_cores, vram, tbp, etc.)
   - `Observation` — `engineering_notes`, `failure_mode_desc`
   - `Law` — инварианты (например, «500W требует БП 1000W+»)
   - `Metric` — измеряемые показатели (vram_bandwidth, boost_clock)
   - `Relation` — связи из `links:` + «requires», «competes_with»

2. **Создать через `primitive-create`:** контекст `hardware`, тип по таксономии, поля из декомпозиции

3. **Валидировать через `primitive-validate`:** PASS/WARN/FAIL

### Фаза 2 — Декомпозиция CPU (29 записей)

Аналогично GPU, но с CPU-специфичными параметрами (cores, threads, socket, tdp, etc.)

### Фаза 3 — Концепты (12 записей)

`concepts/*.md` → Primitives типа Concept или Law (в зависимости от характера)

### Фаза 4 — Композиция (Tier 2)

- `component-compose` — собрать Components (например, «GPU Architecture GB202» из Primitives RTX 5090)
- `module-assemble` — собрать Modules (например, «RTX 50 Series» из Components)
- `view-define` — схемы анализа GPU/CPU
- `artifact-compile` — готовые страницы обзоров

### Фаза 5 — Верификация

- [ ] Все Primitives проходят `primitive-validate`
- [ ] `references/index.md` обновлён с новым контекстом
- [ ] `skill_view` читает все файлы
- [ ] Push `v2` → PR в `main`

## Результат

После merge PR:
```
pc_hardware_knowledge_base/
├── catalog/          # оригинал (main), legacy
├── concepts/         # оригинал (main), legacy
├── docs/             # оригинал (main)
└── minerva/          # v2, minerva-таксономия
    └── references/
        └── hardware/
            ├── index.md
            ├── primitives/    # 200+ Primitives
            ├── components/
            ├── modules/
            ├── views/
            └── artifacts/
```

Две версии сосуществуют. Оригинал кормит существующие пайплайны. Minerva-версия — dogfooding target.
