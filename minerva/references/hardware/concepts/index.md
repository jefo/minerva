---
id: "concepts-index"
type: "index"
title: "Сквозные концепты"
status: "verified"
last_updated: "2025-06-03"
---

# Сквозные концепты

Знания, не привязанные к одному типу компонентов. Объясняют *как работает*, а не *что купить*.

## Карта

| Файл | Концепт | Связанные компоненты |
|---|---|---|
| `vrm-phases.md` | Фазы питания, удвоители, real vs advertised | motherboard, cpu |
| `pcie-lanes.md` | Линии PCIe, sharing groups, конфликты | motherboard, gpu, storage |
| `memory-timings.md` | Тайминги, ранги, MCLK:UCLK, Gear-режимы | memory, cpu, motherboard |
| `power-budget.md` | Бюджет мощности, пики, ATX-спецификации | psu, cpu, gpu |
| `dpc-latency.md` | DPC Latency — системное эмерджентное свойство. Пороги, источники, измерение | motherboard, cpu, gpu, audio_interface |
| `audio-interface-drivers.md` | Driver Quality Taxonomy (Tier 0-3) для аудиоинтерфейсов | audio_interface |
| `daw-acoustic-class.md` | A0_Studio — расширение акустической модели для студийной тишины | cooler, psu, case, audio_interface |

## Как использовать

Загрузи концепт, когда entry-файл ссылается на него через `links:`. Концепт — это разовый ликбез. LLM загружает один раз и применяет ко всем компонентам.
