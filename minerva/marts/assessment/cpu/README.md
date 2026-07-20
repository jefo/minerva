# CPU Assessment Marts

**Назначение:** подготовить данные DWH к представлению — без вердиктов.

## Архитектурная позиция

DWH (SSOT) → Assessment Marts → Backend API → SPA Dashboard → Human Decision

Assessment Mart — **read model**, не принимает решений. Предоставляет картину:
измеренные значения, референсные пороги, запас до порога, качество покрытия,
контекст платформы. Последний шаг — за человеком.

## Принципы

1. **No verdicts.** Не «X лучше Y» и не `meets_sufficiency: true`. Только «вот
   значение, вот порог, вот запас ±N%».

2. **Workload-first.** Навигация идёт от задачи (competitive gaming, AAA),
   не от сущности (CPU).

3. **Honest gaps.** Нет данных → `coverage: none` и `gaps: [...]`. Никакой
   синтетики для закрытия дыр.

4. **Provenance transparent.** Каждый профиль несёт `confidence` и `basis`,
   унаследованные от source observations. Training data ≠ real benchmarks.

## Структура

```
marts/assessment/cpu/
├── README.md              ← этот файл
├── workloads.yaml         ← таксономия: 6 usage-моделей с порогами
├── profiles/              ← per-CPU assessment (29 шт.)
│   └── {cpu_id}.yaml
└── compute.py             ← скрипт: DWH → profiles
```

## Data quality (на 2026-07-19)

| Слой | Покрытие | Статус |
|---|---|---|
| 1080p low gaming | 16 CPU × 5 игр | compute-ready |
| 1440p ultra gaming | 12 CPU × 5 игр | compute-ready — mixed-bound, GPU сжимает разницу |
| 720p low gaming | 12 CPU × 5 игр | compute-ready — extreme CPU-bound |
| Geekbench 6 ST | 28 CPU | compute-ready — реальные scores (не дефектные) |
| Geekbench 6 MT | 28 CPU | compute-ready |
| Cinebench R23 ST/MT | 28 CPU | **DEFECTIVE**: score = строки-лейблы, не числа |
| Productivity (Blender) | 8 CPU | compute-ready — секунды рендера |
| Productivity (7-Zip) | 8 CPU | compute-ready |
| Pricing | 0 CPU | warehouse-pricing не заполнен |

**Что computable сейчас:**
- competitive-gaming — 1080p/720p low по 5 играм (12-16 CPU)
- aaa-gaming — 1440p ultra + 1080p low (12 CPU)
- content-creation — Geekbench MT + Blender (8-28 CPU)
- software-development — Geekbench 1T + MT (28 CPU)
- streaming-gaming — gaming + ядра (прокси)
- budget-gaming — всё ещё заблокирован (нет цен)

**Data defect:** Cinebench R23 (28 CPU) — поле `score` содержит строки-лейблы
(`synthetic-mt`, `synthetic-1t`) вместо чисел. Использовать Geekbench 6 как
замену до исправления Cinebench.
