---
id: "daw-acoustic-class"
type: "concept"
title: "DAW Acoustic Class — расширение акустической модели для студийной тишины"
status: "verified"
last_updated: "2026-06-07"
domain: "audio_production"
links:
  dpc_latency: "concepts/dpc-latency.md"
  audio_interface_drivers: "concepts/audio-interface-drivers.md"
  acoustic_model: "pcbo:ontology/L3_behavior/acoustic" 
tags: ["acoustic", "silence", "studio", "daw", "A0_Studio"]
---

# DAW Acoustic Class — «Студийная тишина»

> **Расширение стандартной акустической модели PCBO (A0-A4) для аудио-продакшена.** Студийные требования строже: не просто «тихо», а «не слышно микрофоном» + «нет тональных шумов».

---

## Класс A0_Studio — «Студийная тишина»

Дополняет `A0_Passive` из стандартной модели. Отличие: A0_Passive допускает слышимый шум при максимальной нагрузке; A0_Studio требует тишины при любых рабочих нагрузках.

```yaml
A0_Studio:
  extends: "A0_Passive"
  dba_range: "<15 dBA на 0.5м"
  description: >
    Система неразличима на слух с 0.5 метра при ЛЮБОЙ рабочей нагрузке 
    (микширование, запись живого звука). Микрофон конденсаторного типа 
    (чувствительность -35 dBV) не регистрирует шум корпуса.
  
  requirements:
    psu:
      - "Semi-passive: fan-stop при системном потреблении до 200W"
      - "ИЛИ: fanless PSU (доступны до 500W)"
      - "Без coil whine в слышимом спектре"
      
    gpu:
      - "ОТСУТСТВУЕТ (iGPU). dGPU — автоматический BLOCK."
      - "Fan-stop режим не релевантен — дискретной карты нет"
      
    cpu_cooler:
      - "Top-flow (NH-C14S, Dark Rock TF 2) ИЛИ overrated tower (260W на 65W CPU)"
      - "AIO — BLOCK. Помпа гудит ~2000 Hz — тональный шум в слышимом спектре"
      - "Вентиляторы ≤600 RPM при нагрузке (120mm/140mm)"
      
    case_fans:
      - "140mm на ≤500 RPM ИЛИ 120mm на ≤400 RPM"
      - "Резиновые виброразвязки (антивибрационные крепления)"
      
    storage:
      - "ТОЛЬКО NVMe SSD. HDD — BLOCK (шпиндель 7200 RPM — тональный шум)"
      - "SSD без активного охлаждения с вентилятором (пассивные радиаторы)"
      
  typical_system_power_W: "<150W под нагрузкой"
  
  failure_modes:
    tonal_noise_pump:
      description: "Помпа AIO на ~2000 Hz — попадает в зону максимальной чувствительности слуха (1-4 kHz)"
      severity: "BLOCK — несовместимо с записью живого звука"
      
    tonal_noise_coil_whine:
      description: "Coil whine на GPU/PSU/VRM — высокочастотный писк, модулированный нагрузкой"
      severity: "BLOCK — конденсаторный микрофон регистрирует"
      
    broadband_fan_noise:
      description: "Вентиляторы >800 RPM — широкополосный шум, маскирует тихие источники при сведении"
      severity: "WARN — критично для сведения, менее критично для записи"
```

---

## Сравнение с классами общей модели

| Класс | dBA | Нагрузка | Применимость к DAW | Ограничение |
|---|---|---|---|---|
| A0_Passive | 0 dBA | idle | ✅ Idle | НЕ гарантирует тишину под нагрузкой |
| A0_Studio | <15 dBA | любая рабочая | ✅ Запись, сведение | Требует отказа от dGPU, AIO |
| A1_Ambient | <25 dBA | idle | ⚠️ Сведение | Слышен при записи (конденсаторный микрофон) |
| A2_LowHum | 25-35 dBA | нагрузка | ❌ Только предпродакшен | Шум потока слышен в наушниках открытого типа |
| A3_Noticeable | 35-45 dBA | нагрузка | ❌ Непригодно | Явный шум |
| A4_Loud | >45 dBA | нагрузка | ❌ Непригодно | Дискомфорт |

---

## Правила маппинга (дополнение к ACOUSTIC-COOLING)

```yaml
DAW_Acoustic_Rules:
  - id: "DAW-AC-01"
    condition: "cooler_type IN ['AIO_240', 'AIO_280', 'AIO_360', 'AIO_420']"
    constraint: "AcousticClass != A0_Studio"
    reason: "Помпа AIO создаёт тональный шум на ~2000 Hz"
    severity: "BLOCK — несовместимо со студийной тишиной"
    
  - id: "DAW-AC-02"
    condition: "gpu_present = true"
    constraint: "AcousticClass != A0_Studio"
    reason: "Кулер GPU — источник широкополосного шума при нагрузке + DPC-спайки"
    severity: "BLOCK — несовместимо со студийной тишиной"
    
  - id: "DAW-AC-03"
    condition: "storage_type IN ['HDD_7200', 'HDD_5400']"
    constraint: "AcousticClass != A0_Studio AND AcousticClass != A1_Ambient"
    reason: "Шпиндель HDD создаёт тональный шум + вибрацию"
    severity: "BLOCK"
    
  - id: "DAW-AC-04"
    condition: "cooler_type = 'Air_TopFlow' AND cpu_tdp_w <= 65"
    constraint: "AcousticClass CAN BE A0_Studio"
    reason: "Top-flow кулер с запасом 4× по TDP: вентиляторы на 500 RPM — бесшумны + downdraft охлаждает M.2"
    note: "Dark Rock TF 2 (230W) на 65W CPU = идеально. NH-C14S (150W) на 65W CPU = достаточно."
```

---

## PCBO-интеграция

```yaml
DAW_Acoustic_in_PCBO:
  extends: "L3_behavior/acoustic"
  trigger: "Intent.daw_zero_dpc_latency OR Context.noise_constraint = 'studio_silence'"
  
  integration_points:
    cooler_selection:
      - "Filter: form_factor IN ['top-flow', 'tower'] (не AIO)"
      - "Filter: tdp_rating >= cpu_tdp * 3 (запас для низких оборотов)"
      
    case_selection:
      - "Filter: sound_dampened = true (битумные маты, виброразвязка)"
      - "Check: airflow sufficient for M.2/chipset without dGPU (top-flow or directed fan)"
      
    psu_selection:
      - "Filter: acoustic_class = 'semi_passive'"
      - "Check: fan_stop_threshold_w > system_peak_w"
      
  domain_gaps:
    - "PCBO Engine v3.0: нет симуляции тонального шума (помпа AIO)"
    - "PCBO Engine v3.0: нет проверки coil whine (вероятностная модель в reliability.md)"
    - "Решение: SIVS-04 (Acoustic Integration) документирует эти риски явно"
```

---

## Антипаттерны акустических утверждений для DAW

### ANTI-DAW-01 — AIO как «тихое решение»
```
ANTI-PATTERN: «AIO 360 тише воздуха — у него вентиляторы на 400 RPM»
PROBLEM: Игнорируется помпа. Вентиляторы тихие, но помпа гудит на 2000 Hz — 
         конденсаторный микрофон регистрирует этот тон.
CORRECT: «AIO 360 — отлично для игр, непригодно для студийной тишины. 
         Top-flow воздушный кулер с 4× запасом TDP — правильно.»
```

### ANTI-DAW-02 — dGPU как «fan-stop и тихо»
```
ANTI-PATTERN: «RTX 4060 в fan-stop не шумит в простое»
PROBLEM: 
  1. DPC-спайки от драйвера 100-500μs — независимо от fan-stop
  2. При любой 3D-нагрузке (даже лёгкой) вентиляторы включаются
  3. Coil whine возможен в любом режиме
CORRECT: «Для студийной тишины dGPU исключён. iGPU RDNA2 держит 3× 4K монитора без шума и DPC.»
```
