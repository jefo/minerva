# Manual Import — как добавлять данные из YouTube

## 1. Скопируй шаблон

```
cp acquisition/templates/observation-template.yaml acquisition/manual/rtx5060-cp2077-1440p-high-driver572.yaml
```

Именуй файл по схеме: `{gpu}-{game}-{resolution}-{preset}-driver{version}.yaml`

## 2. Заполни source-поля (как в бенчмарке, без DIM ID)

Используй **ровно те имена**, которые есть в bus-matrix aliases:

### GPU (aliases)
- `RTX 5060`, `RTX 4060`, `RTX 4070`, `RTX 4060 Ti`
- `RX 9060 XT`, `RX 9070`, `RX 9070 XT`
- `Arc B580`, `Arc B570`

### Игры (aliases)
- `Cyberpunk 2077` (или `CP2077`)
- `Alan Wake 2` (или `AW2`)
- `Monster Hunter Wilds` (или `MH Wilds`)
- `The Last of Us Part II` (или `TLOU2`)
- `Black Myth: Wukong` (или `BM:W`)
- `Rainbow Six Siege` (или `R6 Siege`)
- `Hunt Showdown` (или `Hunt`)
- `Starfield`

### Разрешения
- `1080p`, `1440p`, `4K`

### Пресеты
- `Low`, `Medium`, `High`, `Ultra`, `RT Overdrive`

### Драйверы (aliases)
- `572.16`, `575.10`, `546.33`

## 3. Заполни measures (только цифры)

- `fps_avg`: средний FPS
- `fps_1pct_low`: 1% low FPS
- `fps_0_1pct_low`: 0.1% low (опционально)
- `frametime_ms_avg`: frametime в ms (опционально)

## 4. Заполни meta

- `confidence`: 0.85 для YouTube, 0.95 для своих замеров
- `observed_at`: когда сделан замер (`YYYY-MM`), не когда импортирован
- `source_url`: ссылка на видео
- `source_channel`: название канала
- `source_video_title`: название видео
- `source_timestamp`: где в видео показан результат (`MM:SS`)

## 5. Положи в правильную папку и сообщи мне

Файл → `acquisition/manual/{filename}.yaml`
Я проверю bus-matrix validation и добавлю в Warehouse.

## Приоритетные игры для закрытия coverage gaps

1. Alan Wake 2 (RT + DLSS)
2. The Last of Us Part II
3. Starfield
4. Black Myth: Wukong
5. Monster Hunter Wilds
