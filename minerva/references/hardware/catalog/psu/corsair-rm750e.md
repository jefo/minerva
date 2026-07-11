---
id: "corsair-rm750e"
type: "psu"
title: "Corsair RM750e 750W 80+ Gold"
vendor: "corsair"
status: "draft"
tags: ["atx3.0", "750w", "gold", "fully-modular", "12v-2x6", "semi-passive"]
last_updated: "2026-06-05"
links:
  concept_power: "../concepts/power-budget.md"
specs:
  wattage: 750
  standard: "ATX 3.0 / PCIe 5.0"
  certification: "80 Plus Gold"
  cabling: "полностью модульные"
  fan: "120mm rifle bearing (Corsair NR120L)"
  acoustic_profile: "semi_passive"  # fan stop до ~240W (Zero RPM Mode)
  protections: ["OCP", "OVP", "UVP", "OPP", "OTP", "SCP"]
  12v_2x6: true
  12v_2x6_power: "600W (native)"
  12v_2x6_count: 1
  pcie_8pin_count: 4
  topology: "LLC + DC-DC"
  capacitors: "тайваньские/китайские (105°C)"
  warranty: "7 лет"
price_ru:
  median: 9500
  source: "price.ru (оценка, параллельный импорт)"
  date: "2026-06-05"
profiles:
  atx_3x_transient_capable:
    steel_man_desc: "750W Gold ATX 3.0 с Zero RPM Mode. Массовый стандарт — самый продаваемый semi-passive PSU на рынке. Полностью модульный, тихий в простое. 7 лет гарантии. Совместимость с iCUE не требуется — работает автономно."
    capability_level: 2
    failure_mode_desc: "ATX 3.0 (не 3.1) — переходник на 12V-2x6, а не native разъём на плате. Rifle bearing громче FDB/Hydro под нагрузкой. Конденсаторы не японские — при 24/7 нагрузке деградация быстрее чем у Seasonic/be quiet!."
    optimal_for_intents: ["aaa_1440p_high", "esports_1080p_240hz", "software_development", "streaming", "office_productivity"]
    failure_for_intents: ["aaa_4k_path_tracing", "llm_training_lora_24h"]
    failure_severity: "WARN"
    failure_type: "GRACEFUL"
verdict: "Самый продаваемый semi-passive PSU. Zero RPM до 240W, полностью модульный, ATX 3.0 с 12V-2x6. Компромисс: неяпонские конденсаторы и 7 лет гарантии вместо 10. Цена ~9 500 ₽ — лучший semi-passive за эти деньги."
---

# Corsair RM750e 750W 80+ Gold

## Позиционирование

Corsair RM750e — массовый стандарт semi-passive PSU. Серия RMe (e = essential) — упрощённая версия премиальной RMx: те же 750W Gold + Zero RPM, но с упрощённой элементной базой (неяпонские конденсаторы, rifle bearing вместо FDB, 7 лет гарантии вместо 10).

Главное преимущество — **цена**. RM750e стабильно дешевле Pure Power 12M на 500–1 000 ₽ при тех же semi-passive характеристиках. Для сборок, где важна тишина в простое, но не критична долговечность при 24/7 нагрузке — оптимальный выбор.

## Характеристики

- **Мощность:** 750W
- **Стандарт:** ATX 3.0 (PCIe 5.0)
- **Сертификат:** 80 Plus Gold
- **Кабели:** полностью модульные
- **12V-2x6:** 1× 600W (через native кабель, не переходник)
- **PCIe 8-pin:** 4× (2 кабеля)
- **Вентилятор:** 120mm rifle bearing (Corsair NR120L)
- **Режим вентилятора:** Zero RPM Mode — 0 RPM до ~240W
- **Защиты:** OCP, OVP, UVP, OPP, OTP, SCP
- **Топология:** LLC + DC-DC
- **Конденсаторы:** тайваньские/китайские 105°C
- **Гарантия:** 7 лет

## Zero RPM Mode: как работает

Zero RPM срабатывает при нагрузке до ~240W (выше чем у Pure Power 12M — 200W и Seasonic GX — 200W). В типичных сценариях:
- **Idle (60–100W):** 0 RPM, 0 dBA
- **Desktop work (100–150W):** 0 RPM, 0 dBA
- **Gaming (200–350W):** вентилятор включается на ~600–800 RPM
- **Full load (400W+):** ~1 200 RPM, слышимо но не раздражающе

Более высокий порог fan-stop чем у конкурентов — палка о двух концах: дольше тишина, но при включении вентилятора старт с более высокой базовой температуры.

## ATX 3.0 vs 3.1: что теряется

RM750e сертифицирован по ATX 3.0 (не 3.1). Ключевое отличие — **hold-up time**: ATX 3.1 требует 17 мс (было 16 мс в 3.0) и более строгие transient-тесты. На практике для игровых и рабочих ПК разница незаметна. Если важны «абсолютно最新 стандарты» — be quiet! Pure Power 12M (ATX 3.1).

## Совместимость с GPU

- **RTX 5060 Ti (180W):** с огромным запасом
- **RTX 5070 (250W):** уверенно
- **RTX 5070 Ti (300W):** достаточно
- **RTX 5080 (360W):** на пределе, но допустимо на стоке
- **RTX 5090 (575W):** недостаточно

## Российский рынок (июнь 2026)

**Медиана ~9 500 ₽** (параллельный импорт). Прямые конкуренты в сегменте semi-passive 750W:

- be quiet! Pure Power 12M 750W (~10 000 ₽ — тише, ATX 3.1, 10 лет гарантии)
- Seasonic Focus GX-750 (~12 000 ₽ — японские конденсаторы, 10 лет)
- Thermaltake Toughpower GF A3 750W (~9 000 ₽ — дешевле, но шумнее)

RM750e — лучший компромисс «semi-passive / цена». Проигрывает be quiet! по качеству подшипника и Seasonic по долговечности, выигрывает по цене.

## Для кого

**Идеален:**
- Тихие среднебюджетные сборки (важна тишина в простое)
- Геймерские ПК с простоем 80% времени
- Сборки где 500 ₽ экономии на PSU идут в GPU/RAM

**Не подходит:**
- Рабочие станции 24/7 (неяпонские конденсаторы, 7 лет гарантии)
- Сборки с RTX 5080+ (брать 850W+)
- Абсолютная тишина под нагрузкой (брать be quiet! Straight Power 12)

## Источники

1. Corsair RM750e Product Page (corsair.com)
2. Cybenetics — сертификация 80 Plus Gold
3. Price.ru — рыночные цены, Москва (оценка, 05.06.2026)
4. Tom's Hardware / KitGuru — обзоры Corsair RMe series
