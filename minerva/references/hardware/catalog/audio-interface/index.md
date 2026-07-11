---
id: "audio-interface-index"
type: "index"
title: "Аудиоинтерфейсы"
status: "draft"
last_updated: "2026-06-07"
links:
  driver_taxonomy: "concepts/audio-interface-drivers.md"
  dpc_latency: "concepts/dpc-latency.md"
---

# Аудиоинтерфейсы

> **Статус:** 8 entry. Наполнен через JIT Ingestion из DAW-референса (2026-06-07).

## Driver Tiers (см. audio-interface-drivers.md)

| Tier | Производители | Мин. буфер | Примечание |
|---|---|---|---|
| T0 | RME | 32 сэмпла | Эталон |
| T1 | MOTU, Lynx | 64 сэмпла | Профессиональный |
| T2 | Focusrite Clarett, UA Apollo | 128 сэмплов | Полупрофессиональный |
| T3 | Focusrite Scarlett, consumer | 128+ сэмплов | Потребительский |

## Карта каталога

| Файл | Модель | Tier | Входы | RTT @64 | Цена |
|---|---|---|---|---|---|
| `rme-babyface-pro-fs.md` | RME Babyface Pro FS | T0 | 12 | ~2.5 ms | ~70 000 ₽ |
| `rme-fireface-ufx-ii.md` | RME Fireface UFX II | T0 | 30 | ~2.0 ms | ~120 000 ₽ |
| `motu-ultralite-mk5.md` | MOTU UltraLite Mk5 | T1 | 18 | ~3.0 ms | ~50 000 ₽ |
| `motu-828es.md` | MOTU 828es | T1 | 28 | ~2.8 ms | ~70 000 ₽ |
| `focusrite-clarett-plus-8pre.md` | Focusrite Clarett+ 8Pre | T2 | 18 | ~4.0 ms | ~55 000 ₽ |
| `ua-apollo-twin-x.md` | UA Apollo Twin X | T2 | 2 | ~3.0 ms* | ~65 000 ₽ |
| `ua-apollo-x8.md` | UA Apollo x8 | T2 | 18 | ~3.0 ms* | ~150 000 ₽ |
| `focusrite-scarlett-2i2.md` | Focusrite Scarlett 2i2 | T3 | 2 | ~5.5 ms | ~15 000 ₽ |

> *UA Apollo: на Windows native — стабилен только на 128+ сэмплах. RTT указан для Mac.

## Entry Content Standards

1. **Полный frontmatter** со всеми обязательными полями
2. **Раздел позиционирования** — для какого Tier интентов этот интерфейс
3. **Технические спецификации** — входы/выходы, преампы, RTT на разных буферах
4. **Сравнение с конкурентами** — таблица с ключевыми различиями в том же Tier
5. **Для кого подходит / не подходит** — явные сценарии использования
6. **Источники** — тесты Gearspace RTL, отзывы VI-Control

## Связи

- **Driver Taxonomy:** `concepts/audio-interface-drivers.md` — Tier-система
- **DPC Latency:** `concepts/dpc-latency.md` — взаимодействие драйверов с DPC
