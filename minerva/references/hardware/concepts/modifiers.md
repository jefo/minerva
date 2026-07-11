---
id: "modifiers-catalog"
type: "concept"
title: "Каталог модификаторов профилей PCBO"
status: "draft"
last_updated: "2026-06-03"
links:
  profiles_dictionary: "concepts/epistemological-profiles.md"
  intents_catalog: "catalog/intents/index.md"
---

# Каталог модификаторов профилей PCBO

## Что такое модификатор

Модификатор (applied stereotype в терминах SysML/MBSE) — это **надстройка над
базовым профилем**, которая добавляет или изменяет один специфичный аспект
поведения компонента, не переопределяя профиль целиком.

**Пример:** у AMD Ryzen 7 7700 (базовый профиль: `balanced_monolithic_norm`)
есть iGPU с RDNA 2. Модификатор `+hardware_codec` добавляет к steel-man
«аппаратное декодирование H.265/AV1», но не меняет фундаментальный характер
процессора как универсального 8-ядерника.

**Чем модификатор отличается от профиля:**
- Профиль — **это что компонент IS** (steel-man) и чем он жертвует (failure-mode)
- Модификатор — **это что компонент ALSO HAS** поверх базового профиля
- Профиль самостоятелен, модификатор — всегда при базовом профиле

## Схема модификатора

```yaml
modifier_id:
  applies_to_categories: ["cpu", "gpu", "mb", ...]  # на какие типы компонентов
  compatible_base_profiles: ["profile_a", ...]       # или ["*"] = любой
  incompatible_base_profiles: ["profile_x"]          # или [] = без ограничений
  steel_man_addendum: >
    Что добавляется к steel-man базового профиля.
  failure_mode_addendum: >
    Какие новые риски/ограничения появляются (дополнительно к failure-mode базового).
  intent_effects:                                       # как меняются интенты
    adds_optimal_for: ["intent_a"]                     # новые optimal
    removes_optimal_for: ["intent_b"]                  # перестаёт быть optimal
    adds_failure_for: ["intent_c"]                     # новые failure
    removes_failure_for: []                            # перестаёт быть failure (редко)
  physical_implications: {}                            # влияние на физические constraints
```

## Каталог модификаторов v1

### +hardware_codec

```yaml
+hardware_codec:
  applies_to_categories: ["cpu", "gpu"]
  compatible_base_profiles: ["*"]
  incompatible_base_profiles: []
  steel_man_addendum: >
    Аппаратное декодирование H.265 10-bit 4:2:2, AV1, HEVC. Таймлайн
    в Premiere Pro / DaVinci Resolve летает без создания прокси.
    Стриминг через аппаратный энкодер (NVENC / QuickSync / VCE) без
    нагрузки на CPU-ядра.
  failure_mode_addendum: >
    Проигрывает non-iGPU/non-encoder вариантам в чистой вычислительной
    мощности на доллар (часть кристалла занята медиаблоком вместо ядер).
    iGPU потребляет 5–15W в простое — паразитное энергопотребление
    если кодеки не используются.
  intent_effects:
    adds_optimal_for: ["video_editing_pro", "streaming", "media_server"]
    removes_optimal_for: []
    adds_failure_for: []
    removes_failure_for: []
  physical_implications:
    min_psu_wattage: "+15W"
    heat_output: "iGPU добавляет 5–15W к TDP в простое"
  example_components:
    - "Intel Core Ultra 5 245K (QuickSync, AV1 encode/decode)"
    - "AMD Ryzen 7 7700 (RDNA 2 iGPU, базовое декодирование)"
    - "NVIDIA RTX 4060 (NVENC 8th gen, AV1 encode)"
```

### +ecc_support

```yaml
+ecc_support:
  applies_to_categories: ["cpu", "mb", "memory"]
  compatible_base_profiles: ["balanced_monolithic_norm", "multi_ccd_disaggregated"]
  incompatible_base_profiles: ["cache_dominant_gaming"]
  steel_man_addendum: >
    Коррекция однобитовых ошибок памяти (ECC). Критично для:
    научных вычислений (молекулярная динамика), финансового моделирования,
    ZFS-хранилищ (защита метаданных), длительных симуляций без перезапуска.
  failure_mode_addendum: >
    Штраф 2–5% latency на ECC-проверку. ECC-память дороже на 20–30%
    чем non-ECC того же объёма. Несовместим с 3D V-Cache (X3D-чипы
    не поддерживают ECC на AM5 потребительских платах).
  intent_effects:
    adds_optimal_for: ["scientific_computing", "data_engineering", "zfs_nas"]
    removes_optimal_for: ["esports_1080p_360hz", "esports_1080p_240hz"]
    adds_failure_for: []
    removes_failure_for: []
  physical_implications: {}
  example_components:
    - "AMD Ryzen 9 7950X (ECC supported on most AM5 boards)"
    - "ASRock X870 Steel Legend (официальная поддержка ECC)"
```

### +dual_bios_recovery

```yaml
+dual_bios_recovery:
  applies_to_categories: ["mb"]
  compatible_base_profiles: ["*"]
  incompatible_base_profiles: []
  steel_man_addendum: >
    Две микросхемы BIOS. При неудачном обновлении прошивки или
    разгоне с нестабильными таймингами — автоматическое восстановление
    с резервного чипа. Критично для: production-машин без права на
    простой, оверклокеров, удалённых систем без физического доступа.
  failure_mode_addendum: >
    Добавляет $5–15 к цене платы. Резервный чип BIOS простаивает
    в 99.9% времени — паразитный компонент, который не улучшает
    производительность, только страхует.
  intent_effects:
    adds_optimal_for: ["overclocking_hobby", "remote_server", "production_workstation"]
    removes_optimal_for: []
    adds_failure_for: []
    removes_failure_for: []
  physical_implications: {}
  example_components:
    - "GIGABYTE B650 AORUS ELITE (Dual BIOS)"
    - "MSI MAG X670E TOMAHAWK (Flash BIOS Button + backup)"
```

### +passive_cooling_capable

```yaml
+passive_cooling_capable:
  applies_to_categories: ["gpu"]
  compatible_base_profiles: ["sub_75w_slot_powered", "mainstream_efficiency_gpu"]
  incompatible_base_profiles: ["enthusiast_unrestricted_gpu", "transient_spike_heavy"]
  steel_man_addendum: >
    Способность работать в полностью пассивном режиме (0 dB, 0 RPM)
    в простое и при лёгкой нагрузке. Вентиляторы останавливаются
    при T < 55°C. Идеально для: HTPC, аудио-студий, спален.
  failure_mode_addendum: >
    В пассивном режиме GPU греется до 60–70°C даже в браузере
    (воспроизведение видео). При старте игры вентиляторы резко
    раскручиваются — акустический шок. Не подходит для длительных
    нагрузок без airflow.
  intent_effects:
    adds_optimal_for: ["silent_build", "htpc", "music_production", "bedroom_pc"]
    removes_optimal_for: ["aaa_4k_ultra"]
    adds_failure_for: []
    removes_failure_for: []
  physical_implications:
    case_airflow_requirement: "Рекомендуется хотя бы 1 вентилятор на выдув"
  example_components:
    - "NVIDIA RTX 5060 (150W, большинство AIB — fan stop в простое)"
    - "Intel Arc B580 (ASRock Steel Legend — semi-passive)"
```

## Совместимость модификаторов (compat-матрица)

Можно ли навесить несколько модификаторов на один компонент одновременно?

| | +hardware_codec | +ecc_support | +dual_bios | +passive_cooling |
|---|---|---|---|---|
| **+hardware_codec** | — | ✅ | ✅ | ✅ |
| **+ecc_support** | ✅ | — | ✅ | ⚠️ (редко) |
| **+dual_bios** | ✅ | ✅ | — | ✅ |
| **+passive_cooling** | ✅ | ⚠️ (редко) | ✅ | — |

- ✅ Совместимы без конфликтов
- ⚠️ Технически совместимы, но комбинация встречается редко (узкий use-case)
- ❌ Несовместимы (физический или логический конфликт)

## Как саб-агент конструирует производный профиль

```
Вход: компонент + интент
  ↓
1. Подобрать БАЗОВЫЙ ПРОФИЛЬ из словаря
2. Проверить, нужны ли модификаторы для покрытия intent'а
3. Применить модификаторы (проверить совместимость через compat-матрицу)
4. Сгенерировать ПРОИЗВОДНЫЙ ПРОФИЛЬ:
   - steel-man = базовый.steel_man + модификатор.steel_man_addendum
   - failure-mode = базовый.failure_mode + модификатор.failure_mode_addendum
   - optimal_for = базовый.optimal_for ∪ модификатор.adds_optimal_for
   - failure_for = базовый.failure_for ∪ модификатор.adds_failure_for
```

## Связи

- **Словарь профилей:** `concepts/epistemological-profiles.md` — 26 базовых профилей
- **Интенты:** `catalog/intents/` — 5 полярных интентов, ссылающихся на профили
- **Физические стереотипы:** отдельный слой (не модификаторы), проверяются через `scripts/validate_physical_constraints.py`
