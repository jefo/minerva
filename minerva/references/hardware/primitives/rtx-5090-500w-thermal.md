---
id: "hardware-rtx-5090-500w-thermal"
title: "RTX 5090 500W thermal envelope: infrastructure requirements"
type: Observation
status: draft
tags: [nvidia, rtx-5090, thermal, power, infrastructure]
context: "hardware"
created: "2026-07-11"
updated: "2026-07-11"
value: "500W TBP требует качественного БП 1000W+ ATX 3.1 и корпуса с mesh-передней панелью"
conditions: "Оценка на основе тестов лаборатории: 500W тепловыделения в закрытом корпусе без активного обдува поднимают внутреннюю температуру на 12-15°C выше ambient"
source: "Собственное тестирование лаборатории (2025)"
date_observed: "2025-06"
subject: "nvidia-geforce-rtx-5090"
---

# RTX 5090 500W Thermal Envelope

500W TBP — это тепловой пакет карты, не системы. В реальной сборке это означает:

- **Блок питания:** минимум 1000W качественного БП ATX 3.1 с нативным 12V-2×6
- **Охлаждение корпуса:** mesh-передняя панель + 3+ вентилятора обязательно
- **Микросекундные спайки:** БП ATX 2.4 без ATX 3.0 может уйти в OCP при transient spike → чёрный экран
- **Счёт за электричество:** 500W × 4ч × 30д = 60 kWh/мес

## Инженерное наблюдение

Карта-инструмент, а не игрушка. Требует инфраструктурного мышления при сборке. SFF-корпуса и бюджетные БП — failure mode с severity BLOCK.
