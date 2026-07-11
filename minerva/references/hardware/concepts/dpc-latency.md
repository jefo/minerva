---
id: "dpc-latency"
type: "concept"
title: "DPC Latency — концепт для аудио-домена"
status: "verified"
last_updated: "2026-06-07"
domain: "audio_production"
links:
  audio_interface_drivers: "concepts/audio-interface-drivers.md"
  daw_acoustic_class: "concepts/daw-acoustic-class.md"
tags: ["dpc", "latency", "audio", "system-level", "emergent-property"]
---

# DPC Latency — Deferred Procedure Call Latency

> **DPC Latency — системное эмерджентное свойство, а не характеристика компонента.** Ни один компонент не имеет параметра «DPC Latency» в спецификации. DPC — результат взаимодействия драйверов, BIOS, чипсета и ОС.

---

## Определение

**DPC (Deferred Procedure Call)** — механизм Windows, при котором высокоприоритетный код драйвера откладывает менее срочную работу в очередь DPC. Если DPC-процедура занимает слишком много времени, она блокирует поток реального времени (аудио), вызывая дропауты и щелчки.

**DPC Latency** измеряется в микросекундах (μs) — максимальное время, которое ядро Windows тратит на обслуживание DPC-очереди перед возвратом к аудио-потоку.

---

## Пороговые классы

```yaml
DPC_Classes:
  A_Studio_Grade:
    max_dpc_us: 50
    description: "Студийный класс. Гарантированная работа на 32 сэмплах без дропаутов."
    typical_system: "Аудио-оптимизированная сборка без dGPU, Wi-Fi/BT отключены"
    
  B_Professional:
    max_dpc_us: 100
    description: "Профессиональный класс. Стабильно 64 сэмпла, 32 сэмпла с редкими дропаутами."
    typical_system: "Хорошая сборка с dGPU, Wi-Fi отключён"
    
  C_Acceptable:
    max_dpc_us: 200
    description: "Приемлемо для 128+ сэмплов. Могут быть редкие дропауты на 64."
    typical_system: "Стандартная сборка с dGPU, Wi-Fi включён"
    
  D_Unusable:
    max_dpc_us: ">200"
    description: "Непригодно для аудио. Дропауты даже на 256 сэмплах."
    failure_mode: "CLIFF_DROP — аудио непригодно независимо от бюджета"
```

---

## Источники DPC-спайков (ранжированы по вкладу)

| Источник | Типичный вклад | Механизм | Mitigation |
|---|---|---|---|
| NVIDIA драйвер (dGPU) | 100-500 μs | Смена Power States (P0→P8), рекламная телеметрия | Отказ от dGPU → iGPU |
| Wi-Fi адаптер | 50-200 μs | Сканирование сетей, Background Roaming, BT coexistence | Отключить в UEFI / физически удалить |
| Bluetooth | 30-150 μs | Device discovery, HID polling | Отключить в UEFI |
| Realtek аудио-кодек | 30-100 μs | HD Audio Bus polling | Отключить (используется внешний интерфейс) |
| RGB-контроллер | 20-80 μs | USB polling эффектов (Corsair iCUE, ASUS Aura) | Отключить в UEFI / не подключать |
| Intel LAN (I225-V, I226-V) | 20-60 μs | Периодический polling, отчёты о состоянии | Предпочесть Realtek RTL8125BG для аудио |
| Антивирус / Defender | 10-50 μs | Real-time сканирование файлов | Исключить аудио-директории, отключить real-time |
| NVMe драйвер | 5-20 μs | Фоновый TRIM/garbage collection | Стандартный драйвер Microsoft NVMe |
| HPET (High Precision Event Timer) | переменный | Таймер высокого разрешения | Отключить в UEFI (Windows использует TSC) |

---

## Измерение

**Инструмент:** LatencyMon (Resplendence) — стандарт де-факто.

```yaml
Measurement_Protocol:
  tool: "LatencyMon v7+"
  duration_min: 10
  conditions: 
    - "Система в простое (рабочий стол, без открытых приложений)"
    - "Все драйверы установлены, система перезагружена (uptime >5 min)"
  metrics:
    highest_dpc_routine_us: "Максимальное время DPC-процедуры"
    highest_isr_routine_us: "Максимальное время ISR-процедуры"
    total_hard_pagefaults: "Должно быть 0 после прогрева"
    driver_with_highest_dpc: "Драйвер-виновник"
  pass_criteria:
    studio: "highest_dpc < 50 μs AND highest_isr < 50 μs"
    professional: "highest_dpc < 100 μs AND highest_isr < 100 μs"
```

---

## Отличие от ASIO-латентности

| Параметр | DPC Latency | ASIO Round-Trip Latency |
|---|---|---|
| **Что измеряет** | Задержка ОС в обработке прерываний | Полный путь аудиосигнала (вход→обработка→выход) |
| **Единицы** | Микросекунды (μs) | Миллисекунды (ms) |
| **Источник** | Драйверы, BIOS, чипсет, ОС | Аудиоинтерфейс + ASIO-драйвер + буфер |
| **Целевое значение** | <50 μs | <5 ms (3 ms — комфорт для живого мониторинга) |
| **Связь** | DPC — корневая причина дропаутов. ASIO — следствие. | |

**DPC > аудиобуфер → гарантированный дропаут.** При буфере 32 сэмпла (≈0.7 ms = 700 μs) один DPC-спайк в 500 μs от NVIDIA-драйвера забирает 70% времени буфера. Оставшихся 200 μs недостаточно для обработки плагинов.

---

## PCBO-интеграция

```yaml
DPC_in_PCBO:
  type: "L3_Behavioral_Constraint"
  layer: "L3"
  evaluation: "Пост-синтезный чек (Engine не симулирует драйверы)"
  constraint:
    - "Нет dGPU → минус основной источник спайков"
    - "Wi-Fi/BT отключены в UEFI → минус сетевые DPC"
    - "Realtek LAN для аудио (не Intel I225/I226) → снижение сетевых DPC"
    - "RGB-контроллеры отключены → минус USB DPC"
    - "NVMe на стандартном драйвере Microsoft → без сторонних DPC"
  domain_gap: "PCBO Engine v3.0 не симулирует DPC Latency. Проверка — ручная (LatencyMon) или через SIVS-03 (IRQ Contention Map)."
```

---

## Антипаттерны DPC-утверждений

### ANTI-DPC-01 — Прилагательное вместо класса
```
ANTI-PATTERN: «Плата с хорошим DPC»
PROBLEM: «Хороший» — нечисловая оценка.
CORRECT: «ASRock B850 Riptide показывает DPC <30 μs в тестах Gearspace (класс A_Studio_Grade)»
```

### ANTI-DPC-02 — Атрибуция DPC одному компоненту
```
ANTI-PATTERN: «У этого процессора низкий DPC Latency»
PROBLEM: CPU не имеет DPC — это свойство системы драйверов.
CORRECT: «Система на базе этого CPU с оптимизированным набором драйверов показывает DPC <50 μs»
```

### ANTI-DPC-03 — Игнорирование dGPU как источника
```
ANTI-PATTERN: «Можно поставить RTX 4060 — она не влияет на звук»
PROBLEM: NVIDIA-драйверы дают DPC-спайки 100-500 μs независимо от модели GPU.
CORRECT: «Для DPC <50 μs dGPU должен быть исключён. Альтернатива: iGPU (RDNA2/UHD)»
```
