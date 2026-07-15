# Mental Models — Gaming Performance DWH

## Coverage
Покрытие — доступность данных по комбинации Dimension × Сценарий.
Не все CPU имеют gaming-замеры. Не все GPU протестированы во всех играх.
Перед любым действием проверяй coverage через context-map.
Цель: diagnostic triad (720p Low, 1080p Low, 1440p Ultra) для каждого CPU.

## Confidence
Два режима достоверности:
- **training_data** (0.75) — synthetic/экстраполированные данные. Заполняют пробелы, но не авторитетны для финальных выводов.
- **real_benchmark** (0.9+) — данные из реальных тестов с source_url на видео/статью.

При использовании training_data всегда указывай confidence 0.75 и предупреждай об этом.
Экстраполяция FPS от соседнего CPU даёт ±10% погрешность.

## Lineage
Каждый Law прослеживается до исходных Observation.
Observation → (comparison) → Law.
Без lineage — не Law, а мнение.

## Source Layer
Observation хранит source-значения (человеческие имена), не dim_id.
"RTX 5060" — не "nvidia-rtx-5060".
Резолвинг через bus-matrix aliases при чтении.
Это позволяет разным источникам использовать разные имена одного компонента.

## Provenance
Каждый observation обязан иметь source_url.
Без source_url observation невалиден.
Значения source_url: URL на видео/статью, "training_data", "manual".
Контракт: contracts/fact.md.

## Context Map
Автогенерируемый индекс склада. Не редактировать вручную.
После любого изменения данных → python3 tools/compile-context-map/generate.py.
Consumer начинает с context-map чтобы понять что уже есть.

## Evidence Triad (CPU)
Три диагностических точки покрывают все пользовательские сценарии:
- 720p Low — extreme CPU-bound. Максимальная разница между CPU.
- 1080p Low — основной CPU-bound сценарий.
- 1440p Ultra — mixed-bound, ближе к реальному gaming.
Не нужно хранить все разрешения — presentation layer экстраполирует.
