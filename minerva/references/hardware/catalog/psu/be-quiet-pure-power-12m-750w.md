---
id: "be-quiet-pure-power-12m-750w"
type: "psu"
title: "be quiet! Pure Power 12 M 750W"
vendor: "be-quiet"
status: "draft"
tags: ["atx3.1", "750w", "gold", "fully-modular", "12v-2x6", "semi-passive"]
last_updated: "2026-06-05"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 750
  standard: "ATX 3.1"
  certification: "80 Plus Gold"
  cabling: "полностью модульные"
  fan: "120mm be quiet! Silent Wings (rifle bearing)"
  acoustic_profile: "semi_passive"  # fan stop до ~200W, 0 dBA в idle/desktop
  protections: ["OCP", "OVP", "UVP", "OPP", "OTP", "SCP"]
  12v_2x6: true
  12v_2x6_power: "600W (native)"
  12v_2x6_count: 1
  pcie_8pin_count: 4
  topology: "LLC + DC-DC"
  warranty: "10 лет"
price_ru:
  median: 10000
  source: "price.ru (оценка, параллельный импорт)"
  date: "2026-06-05"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "750W Gold ATX 3.1 с родным 12V-2x6 на 600W. Полностью модульный. Semi-passive до ~200W — 0 dBA в простое и лёгкой работе. 10 лет гарантии. Лучший semi-passive PSU в бюджете до 10K."
    capability_level: 2
    failure_mode_desc: "750W — недостаточно для RTX 5090. Rifle bearing вентилятор при высокой нагрузке слышнее FDB-аналогов. Не Platinum — КПД ниже на 2-3%."
    optimal_for_intents: ["aaa_1440p_high", "esports_1080p_240hz", "software_development", "streaming", "office_productivity"]
    failure_for_intents: ["aaa_4k_path_tracing", "llm_training_lora_24h"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
verdict: "Золотой стандарт тихого среднебюджетного PSU. Semi-passive до 200W, ATX 3.1, 10 лет гарантии. Для RTX 5070 Ti и ниже — лучший выбор по acoustic/цена. ~10 000 ₽."
---

# be quiet! Pure Power 12 M 750W

## Позиционирование

be quiet! Pure Power 12 M — обновлённая версия популярной линейки Pure Power. Переход на ATX 3.1, родной 12V-2x6 на 600W, полностью модульные кабели. Ключевое преимущество перед DeepCool PN-D серией — **semi-passive режим**: вентилятор выключен до ~200W нагрузки. В простое и при лёгкой работе (браузер, IDE, терминал) — 0 dBA.

В иерархии be quiet!: Pure Power 12M (mid-range Gold) → Straight Power 12 (premium Platinum) → Dark Power 13 (flagship Titanium).

## Характеристики

- **Мощность:** 750W
- **Стандарт:** ATX 3.1
- **Сертификат:** 80 Plus Gold
- **Кабели:** полностью модульные
- **12V-2x6:** 1× 600W native (не переходник)
- **PCIe 8-pin:** 4× (2 кабеля)
- **Вентилятор:** 120mm be quiet! Silent Wings (rifle bearing)
- **Режим вентилятора:** semi-passive — 0 RPM до ~200W
- **Защиты:** OCP, OVP, UVP, OPP, OTP, SCP
- **Топология:** LLC + DC-DC
- **Гарантия:** 10 лет

## Semi-passive: почему это важно для тихих сборок

Pure Power 12M держит вентилятор выключенным до ~200W потребления системы. При typical desktop load (60–100W) ПК бесшумен со стороны PSU. В отличие от DeepCool PN750D, чей вентилятор вращается всегда (~22 dBA в простое).

Для контекста: RTX 5060 (150W) + Ryzen 9 7900 (65W) = 215W под нагрузкой. В играх/работе вентилятор включится, но на низких оборотах (~600 RPM = < 15 dBA). В простое — 0 RPM, 0 dBA.

**Semi-passive ≠ всегда тише под нагрузкой.** При 500W+ вентилятор раскручивается до слышимого уровня. Но в смешанном сценарии (работа + редкие пиковые нагрузки) semi-passive проводит 80–90% времени в fan-stop.

## Совместимость с GPU

- **RTX 5060 Ti (180W):** с огромным запасом
- **RTX 5070 (250W):** уверенно
- **RTX 5070 Ti (300W):** достаточно, с запасом
- **RTX 5080 (360W):** на пределе, но допустимо (12V-2x6 600W)
- **RTX 5090 (575W):** недостаточно (нужен 1000W минимум)

## Российский рынок (июнь 2026)

**Медиана ~10 000 ₽** (параллельный импорт). Прямые конкуренты в сегменте semi-passive 750W Gold:

- Corsair RM750e (~9 500 ₽, semi-passive, ATX 3.0)
- Seasonic Focus GX-750 (~12 000 ₽, semi-passive, ATX 3.0)
- DeepCool PN750D (~6 950 ₽ — дешевле, но без semi-passive)
- Thermaltake Toughpower GF A3 750W (~9 000 ₽, semi-passive, ATX 3.0)

Pure Power 12M занимает нишу «semi-passive дешевле Seasonic, надёжнее Thermaltake». 10 лет гарантии — лучший показатель в классе (Corsair — 7, Seasonic — 10, Thermaltake — 7).

## Для кого

**Идеален:**
- Тихие сборки с требованием 0 dBA в простое
- Mid-range игровые ПК (до RTX 5070 Ti)
- Рабочие станции в жилых помещениях (слышимость важна)

**Не подходит:**
- Сборки с RTX 5080 и выше (брать 850W+)
- Бюджетные сборки с приоритетом «цена/ватт» (смотреть DeepCool PN750D)
- Круглосуточный тренинг LLM (брать Platinum)

## Источники

1. be quiet! Pure Power 12 M Product Page (bequiet.com)
2. Cybenetics — сертификация 80 Plus Gold и Lambda A (шум)
3. Price.ru — рыночные цены, Москва (оценка, 05.06.2026)
4. Tom's Hardware / KitGuru — обзоры Pure Power 12M 750W
