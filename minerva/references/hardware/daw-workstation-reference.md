---
id: "daw-workstation-reference"
type: "reference"
title: "DAW Workstation Reference — Processor, Motherboard & Audio Interface Selection"
status: "verified"
last_updated: "2026-06-07"
source: "Eugene Kaizin — executive summary on DAW workstation configuration"
domain: "audio_production"
links:
  dpc_latency_concept: "concepts/dpc-latency.md"
  audio_interface_drivers: "concepts/audio-interface-drivers.md"
  daw_acoustic_class: "concepts/daw-acoustic-class.md"
  daw_intent: "catalog/intents/daw_zero_dpc_latency.yaml"
---

# DAW Workstation Reference — Processor, Motherboard & Audio Interface Selection

> **Статус:** Верифицированный референсный документ. Основан на реальных тестах DAWBench DSP, отзывах профессионального сообщества (VI-Control, Gearspace), данных производителей и официальных рекомендациях Steinberg.
>
> **Назначение:** Якорный документ для домена `audio_production` в PCBO. Используется как source of truth при синтезе DAW-сборок и при JIT Ingestion аудио-специфичных компонентов (кулеров, интерфейсов, материнских плат).

---

## 1. Процессоры для DAW

По результатам DAWBench DSP-тестов:

| Процессор | Ядра (P+E)/Потоки | Boost, ГГц | TDP, Вт | DAW-бенч | Цена, ₽ (июнь 2026) |
|---|---|---|---|---|---|
| Intel Core i9-285K (15th Gen) | 8P+16E / 24 | 6.0 / 4.0 | ≈260 (до 312) | Лидер DAWBench DSP, очень горячий | ~60 000 |
| Intel Core i9-14900K (14th Gen) | 8P+16E / 24 | 5.8 / 4.3 | 253 | Высокая, близка к 9950X | ~48 000 |
| Intel Core i7-14700K (14th Gen) | 8P+12E / 20 | 5.6 / 4.3 | 253 | Подобен Ryzen 9 9900X, 20 потоков | ~32 000 |
| Intel Core i5-14600K (14th Gen) | 6P+8E / 14 | 5.3 / 3.5 | 125 (до 181) | Лучшая цена/частота, ~64-буфер | ~23 000 |
| AMD Ryzen 9 9950X | 12 / 24 | 5.0 | 170 (148 ср.) | +18% к i9-285K при схожем потреблении | ~50 000 |
| AMD Ryzen 9 9900X | 12 / 24 | 4.9 | 170 | Близок к 9950X | ~48 000 |
| AMD Ryzen 9 9800X3D | 8 / 16 | 4.5 | 105 | **Лучший на ASIO64** (L3-кэш) | ~45 000 |
| AMD Ryzen 7 9700X | 8 / 16 | 5.1 | 105 | Оптимальный баланс цена/производительность | ~22 000 |
| AMD Ryzen 7 7700 | 8 / 16 | 5.3 | 65 | Очень эффективен (65W), бюджетный | ~17 000 |

**Выводы по выбору CPU:**
- **Микширование / многопоток:** больше ядер/потоков (9950X, i9-14900K) → больше треков и плагинов одновременно
- **Реальное время / низкий буфер:** X3D-модели (9800X3D) или новые Intel с высокой IPC — L3-кэш даёт выигрыш на малых буферах
- **Бюджет:** Ryzen 7 9700X/7700 или i5-14600K — хорошая мощность при низком энергопотреблении

---

## 2. Материнские платы: критерии и модели

### Критерии для аудио-платформы

1. **Минимум лишних контроллеров.** RGB-контроллеры, дублированные 2.5/10 GbE, Wi-Fi/BT увеличивают DPC Latency
2. **Сетевой чип.** Предпочтителен Intel 2.5 GbE или Realtek RTL8125BG (без Wi-Fi/BT). Избегать плат с несколькими сетевыми чипами
3. **USB-топология.** Качественные контроллеры (Intel/Asmedia). Достаточно прямых портов USB-C/USB-A на задней панели. Аудиоинтерфейс должен висеть на CPU-direct USB
4. **Thunderbolt/USB4.** Желательно встроенное или через header — для профессиональных аудиоинтерфейсов
5. **BIOS/питание.** Серии ProArt/Creator, Taichi, Aorus Master — длительная история обновлений BIOS, стабильное питание
6. **Безопасность.** Wi-Fi, Bluetooth, RGB — отключать в UEFI для чистоты DPC

### Рекомендованные модели

| Платформа | Модель | Ключевое | Цена, ₽ |
|---|---|---|---|
| AM5 | ASUS ProArt X870E-Creator | TB4, Dual 5 GbE, USB4 | ~45 000 |
| AM5 | ASUS B650E-ProArt | USB4, 2.5 GbE | ~35 000 |
| AM5 | ASRock X670E Taichi | 10GbE Sage + 2.5 GbE, TB | ~40 000 |
| AM5 | ASRock B850 Riptide | Лучший DPC Latency AM5, Realtek 2.5GbE | ~18 000 |
| AM5 | Gigabyte X670E Aorus Master | 10GbE, PCIe5 | ~30 000 |
| AM5 | MSI MAG B650 Tomahawk | Wi-Fi 6E, 2.5GbE (WiFi отключить) | ~15 000 |
| LGA1700 | ASUS ProArt Z790-E | USB4/TB4 | ~40 000 |
| LGA1700 | ASRock Z790 Taichi | TB, 10GbE | ~35 000 |
| LGA1700 | MSI MEG Z790 Ace | USB4/TB, premium | ~40 000 |

**Избегать:** плат с Realtek Ethernet (для чувствительных сборок), «добитым» PCIe, бюджетных серий (MSI PRO, B660/B650) с DPC-артефактами.

---

## 3. Аудиоинтерфейсы и драйверы

### Driver Quality Taxonomy

| Tier | Производители | DPC-вклад | Мин. буфер | Примечание |
|---|---|---|---|---|
| **Tier 0** | RME | <10 μs | 32 сэмпла | Эталон стабильности. TotalMix FX, DigiCheck |
| **Tier 1** | MOTU, Lynx | <50 μs | 64 сэмпла | AVB, PCIe-опции. Хорошие драйверы |
| **Tier 2** | Focusrite Clarett, UA Apollo | <100 μs | 128 сэмплов | UA Apollo: DSP, но ≥128 на Windows native |
| **Tier 3** | Focusrite Scarlett, consumer | <200 μs | 128+ сэмплов | Бюджетный сегмент |

### Сравнение моделей

| Интерфейс | Подключение | Входы/Выходы | RTT (при 64 сэмплах) | Цена, ₽ |
|---|---|---|---|---|
| RME Babyface Pro FS | USB 3.1 (C) | 12 in / 14 out | ~2.5 мс | ~70 000 |
| RME Fireface UFX II | USB 3.0, TB2 | 30 in / 30 out | ~2.0 мс | ~120 000 |
| MOTU UltraLite Mk5 | USB-C, TB | 18 in / 14 out | ~3.0 мс | ~50 000 |
| MOTU 828es | USB 2.0, TB | 28 in / 32 out | ~2.8 мс | ~70 000 |
| Focusrite Clarett+ 8Pre | USB-C | 8 in / 6 out | ~4.0 мс | ~55 000 |
| Focusrite Scarlett 2i2 | USB 2.0 | 2 in / 2 out | ~5.5 мс | ~15 000 |
| UA Apollo Twin X | Thunderbolt | 2 in / 6 out | ~3.0 мс* | ~65 000 |
| UA Apollo x8 | Thunderbolt | 8 in / 10 out | ~3.0 мс* | ~150 000 |

> *UA Apollo: RTT на Mac. На Windows native — стабилен только на ≥128 сэмплах. DSP-плагины работают через Console.

---

## 4. Типовые конфигурации (без аудиоинтерфейса)

| Компонент | Бюджет (~70-80k) | Оптимум (~120k) | Профи (>220k с интерфейсом) |
|---|---|---|---|
| CPU | i5-14600K / R7 7700 | R9 9700X / i7-14700K | R9 9950X / i9-14900K |
| MB | MSI MAG B650 Tomahawk | Gigabyte X670E Aorus Master | ASUS ProArt X870E-Creator |
| RAM | 32GB DDR5-5600 | 64GB DDR5-6000 | 128GB DDR5-6000 |
| SSD | 1TB PCIe4 (KC3000) | 1TB PCIe5 (MP700) | 2×1TB PCIe5 |
| PSU | 650W Gold | 750W Gold | 850W Platinum |
| Кулер | Воздушный 120-140mm | Лучший воздушный / AIO 240 | AIO 280 / топовый воздушный |
| Корпус | Mid-Tower без RGB | С шумопоглощением | Full-Tower с демпфингом |

---

## 5. Чек-лист валидации DAW-станции

1. **BIOS/драйверы:** обновить BIOS, драйверы чипсета/графики/сетевых карт. Отключить C-States, SpeedStep/Cool'n'Quiet, Turbo
2. **LatencyMon:** DPC <100-200 μs в простое. Скриншот отчёта
3. **DAWBench:** запустить DSP/VI-тесты, определить max плагинов при 64/32 буфере
4. **Реальный проект Cubase:** открыть тяжёлый проект (150+ треков Kontakt + FX), буфер 64/32. Проверить дропауты, CPU %, ASIO-пик
5. **Итоговые метрики:** DPC <50-100 μs; DAWBench ≥1000 pts DSP; Cubase без нарушений

---

## 6. Тюнинг Windows под DAW (Steinberg)

- **Энергоплан:** «Высокая производительность», сон/гибернация — никогда, USB Selective Suspend — отключить
- **Фоновое ПО:** удалить/отключить Wi-Fi, Bluetooth, OneDrive/Dropbox, антивирус, RGB-утилиты
- **Видео-драйвер:** без «игровых» надстроек (PhysX, GeForce Experience, Adrenaline)
- **BIOS:** C-State OFF, EIST OFF, Hyper-Threading/SMT — опционально
- **ASIO-Guard:** включить в Cubase
- **Повторный LatencyMon:** после всех оптимизаций
