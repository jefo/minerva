---
id: "physical-stereotypes"
type: "concept"
title: "Физические стереотипы компонентов PCBO"
status: "draft"
last_updated: "2026-06-03"
links:
  profiles_dictionary: "concepts/epistemological-profiles.md"
  modifiers_catalog: "concepts/modifiers.md"
  intents_catalog: "catalog/intents/index.md"
---

# Физические стереотипы компонентов PCBO

## Что такое физический стереотип

Физический стереотип (в терминах SysML — structural stereotype) — **бинарное
свойство компонента**, не зависящее от интента или поведенческого профиля.
В отличие от поведенческих профилей (steel-man / failure-mode / какой ценой),
физический стереотип отвечает на вопрос «влезает или нет», «поддерживает или нет».

**Пример:** SFX-БП всегда SFX, независимо от того, собираем мы esports или
data engineering. Это не «поведение», это физический факт.

## Отличие от профилей и модификаторов

| Слой | Тип | Пример | Проверка |
|---|---|---|---|
| Поведенческий профиль | Как компонент ВЕДЁТ СЕБЯ под нагрузкой | `cache_dominant_gaming` | `evaluate_profiles.py` |
| Модификатор | Что ДОБАВЛЕНО поверх профиля | `+hardware_codec` | Саб-агент-инженер |
| Физический стереотип | Бинарное свойство (да/нет) | `sfx_form_factor_locked` | `validate_physical_constraints.py` |

Физические стереотипы проверяются **детерминированно** — либо компонент
удовлетворяет constraint, либо нет. Никаких WARN/BLOCK с весами.

## Схема физического стереотипа

```yaml
stereotype_id:
  applies_to_categories: ["psu", "mb", "case", ...]
  description: "Бинарное свойство компонента"
  check_type: "presence" | "absence" | "numeric"
  # presence: стереотип ДОЛЖЕН присутствовать (SFX — да)
  # absence: стереотип НЕ ДОЛЖЕН присутствовать (ATX — нет)
  # numeric: значение ДОЛЖНО быть в диапазоне
  incompatible_with: ["other_stereotype_id"]
  intent_effect: "BLOCK" | "WARN"
  intent_effect_note: "Что происходит если стереотип не удовлетворён"
```

## Каталог физических стереотипов v1

### sfx_form_factor_locked

```yaml
sfx_form_factor_locked:
  applies_to_categories: ["psu"]
  description: >
    Блок питания форм-фактора SFX (125×100×63.5mm) или SFX-L (125×125×63.5mm).
    Не путать с ATX (140×150×86mm) — ATX физически не влезает в SFF-корпус.
  check_type: "presence"
  incompatible_with: ["atx_form_factor"]
  intent_effect: "BLOCK"
  intent_effect_note: >
    Для интента sff_compact_itx_portable: отсутствие SFX → невозможность
    установки БП в корпус < 11L. BLOCK безусловный.
  target_intents: ["sff_compact_itx_portable"]
  detection: >
    Проверяется по полю `physical_stereotypes` в entry компонента
    (catalog/psu/*.md frontmatter). Если `sfx_form_factor_locked: true` —
    стереотип присутствует.
  example_components:
    - "Corsair SF750 (SFX, 750W, Platinum)"
    - "Cooler Master V750 SFX Gold"
    - "Lian Li SP750 (SFX, 750W, Gold)"
```

### atx_form_factor

```yaml
atx_form_factor:
  applies_to_categories: ["psu"]
  description: >
    Стандартный ATX-БП (140×150×86mm). Абсолютное большинство БП на рынке.
    Не влезает в SFF-корпус.
  check_type: "absence"
  incompatible_with: ["sfx_form_factor_locked"]
  intent_effect: "BLOCK"
  intent_effect_note: >
    Интент sff_compact_itx_portable: ATX-БП не влезает физически. BLOCK.
  target_intents: ["sff_compact_itx_portable"]
```

### 8_layer_daisy_chain

```yaml
8_layer_daisy_chain:
  applies_to_categories: ["mb"]
  description: >
    Материнская плата с 8-слойным текстолитом и Daisy-Chain топологией
    разводки слотов памяти. Обеспечивает стабильную работу DDR5 на частотах
    7200–8000 MT/s. Платы с 6-слойным текстолитом или T-topology —
    нестабильны выше 6400 MT/s.
  check_type: "presence"
  incompatible_with: []
  intent_effect: "WARN"
  intent_effect_note: >
    Для интентов с ручным разгоном памяти (overclocking): без 8-слойного
    текстолита DDR5-7200+ нестабилен. WARN, не BLOCK — можно снизить частоту.
  target_intents: ["overclocking_hobby"]
  detection: >
    Проверяется по полю `physical_stereotypes` в entry компонента.
    Если `8_layer_daisy_chain: true` — стереотип присутствует.
  example_components:
    - "ASRock X870 Steel Legend (8-layer PCB)"
    - "MSI MPG X670E CARBON WIFI (8-layer, Daisy-Chain)"
    - "GIGABYTE X870E AORUS MASTER (8-layer server-grade)"
```

### 6_layer_budget_pcb

```yaml
6_layer_budget_pcb:
  applies_to_categories: ["mb"]
  description: >
    Бюджетный 6-слойный текстолит. Стабилен до DDR5-6400.
    Выше — ошибки памяти (BSOD, instability).
  check_type: "absence"
  incompatible_with: ["8_layer_daisy_chain"]
  intent_effect: "WARN"
  intent_effect_note: >
    Если интент требует DDR5-7200+ → плата не обеспечит стабильность.
    WARN — можно снизить частоту до 6400.
  target_intents: ["overclocking_hobby"]
```

### dual_bios

```yaml
dual_bios:
  applies_to_categories: ["mb"]
  description: >
    Две микросхемы BIOS на плате. Защита от brick при неудачном обновлении.
  check_type: "presence"
  incompatible_with: []
  intent_effect: "WARN"
  intent_effect_note: >
    Для production-машин без права на простой: отсутствие Dual BIOS —
    риск brick'а при обновлении прошивки. WARN — можно принять риск.
  target_intents: ["production_workstation", "remote_server"]
```

### itx_form_factor

```yaml
itx_form_factor:
  applies_to_categories: ["mb"]
  description: >
    Mini-ITX (170×170mm). Единственный форм-фактор для SFF-корпусов < 11L.
  check_type: "presence"
  incompatible_with: ["atx_form_factor", "matx_form_factor"]
  intent_effect: "BLOCK"
  intent_effect_note: >
    Интент sff_compact_itx_portable: mATX/ATX физически не помещаются. BLOCK.
  target_intents: ["sff_compact_itx_portable"]
```

## Использование в entry компонентов

Физические стереотипы указываются в frontmatter entry:

```yaml
# catalog/psu/corsair-sf750.md
---
id: "corsair-sf750"
type: "psu"
physical_stereotypes:
  sfx_form_factor_locked: true
  atx_form_factor: false
---
```

```yaml
# catalog/motherboard/am5/asrock-x870-steel-legend.md
---
id: "asrock-x870-steel-legend"
type: "motherboard"
physical_stereotypes:
  8_layer_daisy_chain: true
  dual_bios: false
  itx_form_factor: false
---
```

## Проверка

Физические стереотипы проверяются через `scripts/validate_physical_constraints.py`
(Skill 9 пайплайна PCBO). На вход: интент → список требуемых/запрещённых
стереотипов → проверка каждого компонента сборки → BLOCK/WARN/PASS.

## Связи

- **Поведенческие профили:** `concepts/epistemological-profiles.md`
- **Модификаторы:** `concepts/modifiers.md`
- **Интенты с физическими constraints:** `catalog/intents/sff_compact_itx_portable.yaml`
