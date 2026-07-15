# Terminology — Gaming Performance DWH

## Benchmarks

| Термин | Значение |
|---|---|
| **fps_avg** | Средний FPS за время замера |
| **fps_1_percent_low** | 1% самых низких кадров. Показывает стабильность, микрофризы |
| **native** | Без апскейлинга (DLSS/FSR/XeSS off). Эталонный замер |
| **frame_gen** | Генерация кадров (MFG, FSR FG). Увеличивает FPS, добавляет input lag |
| **upscaler** | Технология масштабирования: DLSS, FSR, XeSS. Quality/Balanced/Performance режимы |
| **CPU-bound** | Сценарий где процессор — ограничитель. Низкое разрешение + высокий FPS |
| **GPU-bound** | Сценарий где видеокарта — ограничитель. Высокое разрешение + ультра настройки |

## Architectures

| Термин | Значение |
|---|---|
| **Zen 4** | AMD микроархитектура (Ryzen 7000). AM5, DDR5, TSMC N5 |
| **Zen 5** | AMD микроархитектура (Ryzen 9000). AM5, DDR5, TSMC N4P |
| **3D V-Cache** | Дополнительный L3 кэш поверх CCD. +10-20% FPS в играх |
| **Raptor Lake** | Intel микроархитектура (Core 13/14 gen). LGA1700, гибридная (P+E ядра) |
| **Arrow Lake** | Intel микроархитектура (Core Ultra 200). LGA1851, новый техпроцесс |
| **Blackwell** | NVIDIA GPU архитектура (RTX 50 series). GDDR7, DLSS 4, MFG |
| **Ada Lovelace** | NVIDIA GPU архитектура (RTX 40 series). GDDR6X, DLSS 3 |
| **RDNA 4** | AMD GPU архитектура (RX 9000 series) |
| **Xe2-HPG** | Intel GPU архитектура (Arc B-series, Battlemage) |

## DWH Operations

| Термин | Значение |
|---|---|
| **fact-insert** | Создание нового Observation. Единственная точка записи в DWH |
| **dim-read** | Чтение Dimension из dim/{type}/{id}.yaml |
| **bus-lookup** | Резолвинг source-значения → dim_id через bus-matrix aliases |
| **compile-context-map** | Перегенерация context-map.yaml из данных склада. Tool, не reasoning |
| **lineage-trace** | Прослеживание Observation → Law. Обратный трейс |
| **contradiction-detect** | Поиск observation с одинаковыми dimensions но разными мерами |
| **stale-check** | Поиск устаревших observation (старые драйверы, патчи игр) |

## Data Quality

| Термин | Значение |
|---|---|
| **confidence** | Оценка достоверности данных. 0.75 = training_data, 0.9+ = реальный замер |
| **source_url** | Обязательное поле. Откуда данные: URL, "training_data", "manual" |
| **data_debt** | Observation без source_url или с неизвестным происхождением |
