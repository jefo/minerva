---
id: "intents-root"
type: "index"
title: "Каталог интентов PCBO"
status: "draft"
last_updated: "2026-06-03"
links:
  profiles_dictionary: "concepts/epistemological-profiles.md"
  modifiers_catalog: "concepts/modifiers.md"
---

# Каталог интентов PCBO

**Навигационная карта** — 5 полярных интентов, покрывающих все технологические домены.
Каждый интент — формальный YAML-файл, определяющий граничные условия и профильные
требования для синтеза сборки ПК.

## ⚠️ ДИРЕКТИВА ДЛЯ LLM-АГЕНТА

При встрече ссылки вида **`path/to/file.md#section-name`** в YAML-файлах интентов:

1. **Загрузи** указанный файл через read_file
2. **Найди** секцию `## section-name` или `### section-name` в файле
3. **Извлеки** определение профиля/концепта: steel-man, failure-mode, intents
4. **Не выполняй расчёты или выбор компонентов без загрузки конкретики из файла по ссылке**

Физический путь ведёт к реальному .md-файлу в репозитории `pc_hardware_knowledge_base/`.
Это не абстрактный URI — это navigable reference.

**Пример:** `concepts/epistemological-profiles.md#cache_dominant_gaming`
→ read_file("concepts/epistemological-profiles.md") → найти `## cache_dominant_gaming` → извлечь steel_man_desc, failure_mode_desc, optimal_for_intents, failure_for_intents.

## Карта интентов

| Интент | Домен | Файл | Тип | Параметры |
|---|---|---|---|---|
| AAA Gaming | A: Гейминг | `aaa_gaming_base.yaml` | **Абстрактный** | resolution, settings, target_fps |
| AI Inference | B: Compute | `ai_inference_base.yaml` | **Абстрактный** | model_size, quantization, context_length |
| Data Engineering | B: Compute | `data_engineering_base.yaml` | **Абстрактный** | dataset_size, workload |
| Киберспорт 360Hz | A: Гейминг | `esports_competitive_360hz.yaml` | Конкретный | — |
| SFF Compact Portable | C: Physical | `sff_compact_itx_portable.yaml` | Конкретный | — |
| **DAW Zero-DPC Latency** | **D: Audio** | `daw_zero_dpc_latency.yaml` | **Конкретный** | — |

**Устаревшие (удалены):**
- ~~`aaa_gaming_4k_unrestricted.yaml`~~ → `aaa_gaming_base`
- ~~`ai_inference_local_pro.yaml`~~ → `ai_inference_base`
- ~~`data_engineering_spark_local.yaml`~~ → `data_engineering_base`

### Абстрактный интент AAA Gaming Base

Покрывает ВСЕ разрешения через параметризацию. Агент НЕ использует
`mandatory_steel_man` напрямую (он пустой). Вместо этого:

1. Парсит NL-запрос → `{resolution, settings, target_fps}`
2. Вызывает `scripts/pcbo/dynamic_constraints.py::evaluate_dynamic_constraints()`
3. Получает конкретные профили, VRAM, MAUT-веса под это разрешение

**Примеры (7 сценариев):**

| Разрешение | Настройки | FPS | VRAM | GPU-профиль | Bandwidth |
|---|---|---|---|---|---|
| 1080p | high | 60 | 8 GB | mainstream_efficiency | WARN |
| 1080p | ultra | 120 | 10 GB | balanced_performance | WARN |
| 1440p | high | 60 | 12 GB | balanced_performance | WARN |
| 1440p | ultra | 60 | 14 GB | balanced_performance | ⚠️ BLOCK |
| 4K | high | 60 | 16 GB | enthusiast_unrestricted | ⚠️ BLOCK |
| 4K | ultra | 60 | 18 GB | enthusiast_unrestricted | ⚠️ BLOCK |
| 4K | path_tracing | 60 | 20 GB | enthusiast_unrestricted | ⚠️ BLOCK |

**Устаревший:** `aaa_gaming_4k_unrestricted.yaml` — заменён на `aaa_gaming_base`.
Оставлен для обратной совместимости, но новые сборки — только через base.
| SFF Compact Portable | C: Physical | `sff_compact_itx_portable.yaml` | SFX PSU, GPU ≤320mm, cooler ≤155mm |

## Как использовать

1. **Загрузи** YAML-файл интента
2. **Пройди по ссылкам** в `profile_interaction_matrix.mandatory_steel_man_profiles` и `strict_block_failure_profiles` — каждая ссылка ведёт к физическому .md-файлу
3. **Извлеки constraints** — максимальный шум, термальное состояние, минимальный объём RAM/Storage
4. **Примени MAUT-веса** для многокритериального ранжирования компонентов
5. **Вызови Python-навыки** (`evaluate_profiles.py`, `validate_physical_constraints.py`) для детерминированной проверки

## Связи

- **Профили компонентов:** `../concepts/epistemological-profiles.md` — полный словарь из 26 профилей с steel-man/failure-mode
- **Модификаторы:** `../concepts/modifiers.md` — каталог модификаторов для конструирования производных профилей
- **Физические стереотипы:** проверяются через `scripts/validate_physical_constraints.py`
