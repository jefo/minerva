     1|---
     2|id: "am5-motherboard-index"
     3|type: "index"
     4|title: "Материнские платы AM5"
     5|status: "verified"
     6|last_updated: "2026-06-07"
     7|---
     8|
     9|# AM5 (LGA1718) — материнские платы
    10|
    11|Сокет AM5 для процессоров AMD Ryzen 7000 (Zen 4) и Ryzen 9000 (Zen 5).
    12|
    13|## Чипсеты AM5
    14|
    15|| Чипсет | PCIe 5.0 GPU | PCIe 5.0 M.2 | USB 3.2 Gen2x2 | Позиционирование |
    16||---|---|---|---|---|
    17|| **B650** | Нет (4.0) | Да (1 порт) | Опционально | Средний сегмент |
    18|| **B650E** | Да | Да | Опционально | Средний + PCIe 5.0 |
    19|| **X670** | Нет | Да | Да | Энтузиасты (dual chipset) |
    20|| **X670E** | Да | Да | Да | Флагман |
    21|| **B850** | Нет | Да (Gen5) | Да | Обновлённый средний |
    22|| **X870** | Да | Да | Да | Обновлённый флагман |
    23|
    24|## Модели
    25|
    26|| Файл | Вендор | Чипсет | Форм-фактор | VRM | Цена (₽) |
    27||---|---|---|---|---|---|
| `msi-b650-tomahawk.md` | MSI | B650 | ATX | 14+2+1 (80A SPS) | ~17 000 |
| `asrock-b650e-pg-riptide.md` | ASRock | B650E | ATX | 14+2+1 (60A DrMOS) | ~16 000 |
| `asus-b650-creator.md` | ASUS | B650 | ATX | 12+2 (60A DrMOS) | ~18 000 |
| `gigabyte-b650m-s2h.md` | Gigabyte | B650 | mATX | 6+2+1 | ~8 800 |
    30|| `asrock-b850-riptide.md` | ASRock | B850 | ATX | 14+2+1 (80A SPS) | ~18 000 |
    31|| `gigabyte-x670e-aorus-master.md` | X670E | E-ATX | 4× M.2 (1× Gen5) | Intel 2.5GbE | ~52 000 |
| `asrock-x870-steel-legend.md` | ASRock | X870 | ATX | 16+2+1 (80A SPS) | ~28 000 |
    32|| `asrock-x670e-taichi.md` | ASRock | X670E | E-ATX | 24+2+1 (105A SPS) | ~50 000 |
    33||| `asus-b650e-proart.md` | ASUS | B650E | ATX | 12+2+2 (80A DrMOS) | ~25 400 |
    34||| `asus-proart-x870e-creator.md` | ASUS | X870E | ATX | 18+2+2 (110A SPS) | ~55 000 |
    35|
    36|### Что ещё нужно заполнить
    37|
- B650E: ASUS Strix
- Другие производители X870/B850: MSI, Gigabyte
    40|
    41|## Что смотреть при выборе AM5-платы
    42|
    43|1. **VRM-фазы и сила тока** — достаточно ли для целевого CPU (см. `../../../concepts/vrm-phases.md`)
    44|2. **PCIe-конфликты** — какие слоты отключаются при использовании M.2 (см. `../../../concepts/pcie-lanes.md`)
    45|3. **Flashback без CPU** — критично для обновления BIOS под новые поколения
    46|4. **Сетевой контроллер** — Intel i225/i226 vs Realtek (стабильность под Windows)
    47|