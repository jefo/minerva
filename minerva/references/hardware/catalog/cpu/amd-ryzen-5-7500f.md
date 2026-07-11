---
id: "amd-ryzen-5-7500f"
type: "cpu"
title: "AMD Ryzen 5 7500F (OEM)"
vendor: "amd"
status: "verified"
tags: ["amd", "zen4", "am5", "ddr5", "oem", "no-igpu", "65w", "6-core"]
last_updated: "2026-06-03"
external_audit_verification: planned
links:
  platform: "catalog/motherboard/am5/index.md"
  memory_type: "catalog/memory/ddr5.md"
  family: "catalog/cpu/amd-ryzen-7000.md"
  competitor_intel: "catalog/cpu/intel-core-13400f.md"
  concept_power: "concepts/power-budget.md"
specs:
  socket: "AM5 (LGA1718)"
  architecture: "Zen 4 (Raphael)"
  lithography: "TSMC 5nm (CCD) + 6nm (IOD)"
  cores: 6
  threads: 12
  base_clock: "3.7 GHz"
  boost_clock: "5.0 GHz"
  l3_cache: "32 MB"
  tdp: "65W"
  pcie_lanes: "28 (24 usable), PCIe 5.0"
  memory: "DDR5 only, dual-channel, до 5200 JEDEC / 6000+ EXPO"
  igpu: null
  box_cooler: null
  package: "OEM (без кулера и коробки)"
profiles:
  balanced_monolithic_norm:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Универсальный процессор: 6–8 ядер, единый кристалл (1 CCD), TDP 65–105W. Игры, разработка, офис — всё на хорошем уровне без специализации."
    failure_mode_desc: "Отсутствие 3D V-Cache — проигрыш X3D в киберспорте на 15–25%. Отсутствие E-ядер — фоновая многозадачность менее эффективна."
    optimal_for_intents: ["software_development", "office_productivity", "aaa_1080p_ultra", "aaa_1440p_high", "streaming"]
    failure_for_intents: ["esports_1080p_360hz"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  dense_thermal_concentration:
    power_envelope: "mid"
    capability_level: 2
    steel_man_desc: "Импульсные однопоточные нагрузки (burst): CPU сбрасывает частоту до того как тепло преодолеет IHS. Максимальный буст на 2–3 секунды."
    failure_mode_desc: "Длительная нагрузка. Тепловое сопротивление толстой IHS (≥ 1.7 мм, AM5) → 89–95°C даже под СЖО. Thermal throttling 5–8%."
    optimal_for_intents: ["office_productivity", "software_development"]
    failure_for_intents: ["3d_rendering_cpu", "scientific_computing", "heavy_compilation", "silent_build"]
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
  sub_5nm_lithography:
    power_envelope: "mid"
    steel_man_desc: "Максимальная производительность на ватт. ITX-сборки, лимит энергопотребления."
    failure_mode_desc: "Разгон с V > 1.35В → ускоренная электромиграция и выход из строя."
    optimal_for_intents: ["sff_build", "silent_build"]
    failure_for_intents: []
    failure_severity: "WARN"
    failure_type: "LINEAR_DEGRADATION"
price_ru:
  min: 8962
  median: 9800
  max: 11110
  source: "price.ru"
  date: "2026-06-03"
verdict: "Лучший бюджетный вход в AM5. По сути — Ryzen 5 7600 без iGPU и −100MHz. Экономия 3–4 тыс. ₽ относительно 7600. Идеален для сборок с дискретной видеокартой."
---

# AMD Ryzen 5 7500F (OEM)

## Позиционирование

Ryzen 5 7500F — OEM-процессор, не предназначенный для розничной продажи в коробочном исполнении. Поставляется без кулера, без коробки, без iGPU. По сути — это Ryzen 5 7600 с отключённой встроенной графикой и сниженной на 100 МГц максимальной частотой.

Для сборщика с дискретной видеокартой разницы с 7600 практически нет. Экономия — 3 000–4 000 ₽, которые можно направить на нормальный кулер (боксовый Wraith Stealth у 7600 всё равно шумный и слабый).

## Характеристики

| Параметр | 7500F | 7600 | 7600X |
|---|---|---|---|
| Ядер/потоков | 6C/12T | 6C/12T | 6C/12T |
| Базовая частота | 3.7 GHz | 3.8 GHz | 4.7 GHz |
| Boost | 5.0 GHz | 5.1 GHz | 5.3 GHz |
| L3-кэш | 32 MB | 32 MB | 32 MB |
| TDP | 65W | 65W | 105W |
| iGPU | Нет | RDNA 2 (2 CU) | RDNA 2 (2 CU) |
| Кулер в комплекте | Нет | Wraith Stealth | Нет |
| Цена (РФ) | ~9 800 ₽ | ~13 000 ₽ | ~16 000 ₽ |

## Производительность

В играх разница с 7600 — в пределах погрешности (1–3%). В рабочих задачах — аналогично. По сути, 7500F = 7600 с отключённым iGPU.

**Cinebench R23:**
- Single: ~1 800 баллов
- Multi: ~14 000 баллов

Для 1080p-гейминга с любой дискретной видеокартой вплоть до RTX 5070 / RX 9070 — процессор не будет узким местом. В 1440p — тем более.

## Память

Как все Zen 4 — **DDR5 only**. Оптимальная частота: DDR5-6000 с MCLK:UCLK = 1:1. На частотах выше 6000 контроллер переходит в режим 1:2 с ростом latency.

7500F без проблем держит DDR5-6000 на большинстве плат B650. Для бюджетных сборок DDR5-5600 CL36 — достаточный минимум, разница в играх с 6000 CL30 — 2–4%.

## Охлаждение

65W TDP — чрезвычайно холодный процессор. Достаточно башенного кулера за 1 500–2 500 ₽:
- ID-COOLING SE-224-XTS
- Deepcool AK400
- Thermalright Assassin X 120

В играх потребление редко превышает 50–60W. Даже бюджетный кулер справляется с запасом.

## Российский рынок (июнь 2026)

**Диапазон: 8 962–11 110 ₽, медиана ~9 800 ₽.**

За 10 000 ₽ это лучший вход в AM5. Ближайший конкурент — Intel Core i5-13400F (~12 000–14 000 ₽, но на тупиковом LGA1700).

Поставки: стабильные. OEM-процессоры доступны у всех крупных ритейлеров (DNS, Citilink, Регард).

## Для кого

**Идеален:**
- Бюджетные игровые сборки AM5 с дискретной GPU
- Первый ПК с перспективой апгрейда на Zen 5/6
- Сборки где iGPU не нужен (всегда есть видеокарта)

**Не подходит:**
- Системы без дискретной видеокарты (нет iGPU — не запустится)
- Рабочие станции с многопоточными нагрузками (нужен Ryzen 7/9)
- Сборки с несколькими мониторами без GPU

## Связки

Рекомендуемая платформа:
- **MB:** GIGABYTE B650M S2H / ASRock B650M-HDV — бюджетный вход
- **MB:** MSI B650 Tomahawk — с заделом под будущий Ryzen 7/9
- **Кулер:** ID-COOLING SE-224-XTS (~2 200 ₽)
- **RAM:** 32GB DDR5-6000 CL30 (G.Skill Ripjaws S5 / Kingston Fury)

## Источники

1. AMD Zen 4 Product Specifications (amd.com)
2. Price.ru — рыночные цены, Москва (03.06.2026)
3. Собственное тестирование лаборатории в составе сборки EST-2026-0422-K1
