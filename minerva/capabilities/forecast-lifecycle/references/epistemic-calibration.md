# Epistemic Calibration — Forecast Lifecycle

Методология калибровки модели прогнозирования. Не «правильные ли цифры»,
а «правильно ли откалибрована неопределённость».

## Принцип

Модель должна **знать когда она не знает**. Хороший прогноз не тот где
точечная оценка совпала с реальностью — а тот где доверительный интервал
содержит реальность с заявленной вероятностью.

Если модель говорит «bottleneck probability 0.62, CI [0.48, 0.75]» —
это значит что реальность должна попадать в CI в ~68% случаев (1σ).
Если реальность попадает в 40% случаев — модель overconfident.
Если в 90% — underconfident (тоже плохо, теряем сигнал).

## Back-test Suite

Прогнать модель ретроспективно на известных исторических парах.
Каждый back-test: модель имеет доступ ТОЛЬКО к данным доступным на момент
«current year» (никакого future leaking).

### Тестовые пары

| # | CPU | GPU | Release | Current Year | Death Year | Age at Death |
|---|---|---|---|---|---|---|
| 1 | i5-2500K (4C/4T) | GTX 560 Ti | 2011 | 2012 | ~2016 | 5 лет |
| 2 | i7-4790K (4C/8T) | GTX 970 | 2014 | 2015 | ~2019 | 5 лет |
| 3 | i5-8400 (6C/6T) | GTX 1060 | 2017 | 2018 | ~2022 | 5 лет |
| 4 | Ryzen 5 3600 (6C/12T) | RTX 2060 | 2019 | 2020 | ~2025 | 6 лет |
| 5 | i7-8700K (6C/12T) | GTX 1080 Ti | 2017 | 2018 | ~2023 | 6 лет |

### Критерии оценки

Для каждого back-test:

1. **Inflection year accuracy:** Предсказанный год пересечения (±1 год — acceptable)
2. **CI coverage:** Сколько per-year прогнозов содержат реальность в CI
3. **Confidence drift:** Систематическое завышение/занижение confidence

### Калибровочные поправки

Если модель систематически overconfident:
- Понизить `forecast_confidence_baseline` на (1 − coverage_rate)
- Расширить CI на systematic_error_factor

Если модель систематически underconfident:
- Повысить baseline но сохранить CI width (underconfidence менее опасен)

## Категории неопределённости

### Aleatoric (неустранимая)
- Будущие архитектурные решения (Zen 6 IPC — никто не знает точно)
- Adoption rate новых технологий (AI NPC — when and how much)
- Рыночные факторы (цены, доступность)

→ Отражается в ширине confidence_interval

### Epistemic (устранимая — недостаток данных)
- Training data вместо реальных бенчмарков
- Отсутствие per-genre benchmark data
- Engine complexity — прокси-метрики вместо прямых измерений

→ Устраняется через наполнение Minerva реальными данными

## Calibration run protocol

```
1. Загрузить forecast-lifecycle capability
2. Для каждого back-test:
   a. Установить current_year = release_year + 1
   b. Прогнать forecast на horizon 6 лет
   c. Сравнить предсказанный inflection_year с реальным death_year
   d. Проверить coverage: реальность в CI?
3. Вычислить aggregate metrics:
   - Mean absolute error (inflection_year prediction)
   - CI coverage rate
   - Systematic bias direction
4. Применить калибровочные поправки к confidence_baseline
5. Сохранить calibration version (e.g. "back-test-4-cpu-v1")
```

## Current calibration status

**Версия:** не откалибрована — initial capability.

**Первый запуск:** после утверждения SKILL.md.

**Ожидаемый baseline confidence:** 0.65-0.70 (training_data + initial model).
