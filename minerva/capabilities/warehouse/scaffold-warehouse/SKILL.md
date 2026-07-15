---
name: scaffold-warehouse
description: "Scaffolding нового DWH-skill из шаблона Minerva. Создаёт самодостаточный Data Warehouse для домена."
triggers:
  - "создать DWH для"
  - "scaffold warehouse"
  - "новый склад данных"
  - "разверни data warehouse"
---

# Scaffold Warehouse

**Роль:** фабричный цех Minerva. Создаёт новый самодостаточный DWH-skill из шаблона.

## Контракт

```
IN:  domain (короткое имя: "hardware", "pricing", "content")
     domain_title (человеческое: "PC Hardware", "Market Pricing")
     description (одно предложение: что хранит склад)
OUT: Новый Hermes skill warehouse-{domain} в ~/.hermes/skills/warehouses/
     Готов к наполнению данными.
```

## Процесс

### Шаг 1 — Подтвердить параметры

Покажи пользователю:
```
Создаю DWH:
  Домен: {domain}
  Название: {domain_title}
  Описание: {description}
  Skill: warehouse-{domain}
```

### Шаг 2 — Скопировать шаблон

```bash
cp -r /root/projects/knowledge-services/minerva/templates/warehouse-skill \
     ~/.hermes/skills/warehouses/warehouse-{domain}
```

### Шаг 3 — Переименовать domain-зависимые пути

Шаблон содержит плейсхолдер `{domain}` в именах директорий. Их нужно переименовать:

```bash
cd ~/.hermes/skills/warehouses/warehouse-{domain}

# Переименовать директорию warehouse/{domain} → warehouse/{domain}
mv "warehouse/{domain}" "warehouse/{domain}"

# Переименовать директорию marts/{domain} → marts/{domain}
mv "marts/{domain}" "marts/{domain}"
```

### Шаг 4 — Заменить плейсхолдеры в файлах

Заменить все `{domain}`, `{domain_title}`, `{description}` в файлах:

```bash
cd ~/.hermes/skills/warehouses/warehouse-{domain}
for f in SKILL.md warehouse/{domain}/bus-matrix.yaml references/context-map.yaml; do
  sed -i "s/{domain}/{domain}/g; s/{domain_title}/{domain_title}/g; s/{description}/{description}/g" "$f"
done
```

Также заменить `{version}` на текущую версию Minerva и `{date}` на сегодня.

### Шаг 5 — Скопировать compile-context-map

compile-context-map — единственный capability, который копируется в DWH (он работает с данными конкретного склада). Остальные capabilities — shared lib из Minerva.

```bash
cp -r /root/projects/knowledge-services/minerva/capabilities/warehouse/compile-context-map \
     ~/.hermes/skills/warehouses/warehouse-{domain}/capabilities/warehouse/
```

### Шаг 6 — Скопировать контракты

```bash
cp /root/projects/knowledge-services/minerva/references/contracts/*.md \
   ~/.hermes/skills/warehouses/warehouse-{domain}/references/contracts/
```

### Шаг 7 — Сгенерировать пустую context-map

```bash
cd ~/.hermes/skills/warehouses/warehouse-{domain}
python3 capabilities/warehouse/compile-context-map/scripts/generate.py \
  --warehouse-root . --output references/context-map.yaml
```

### Шаг 8 — Верификация

Убедись что:
- `skill_view('warehouses/warehouse-{domain}')` работает
- `skill_view('warehouses/warehouse-{domain}', file_path='references/context-map.yaml')` отдаёт индекс
- Структура директорий создана, плейсхолдеры заменены

## Результат

Самодостаточный DWH-skill. Consumer загружает его, видит context-map, начинает наполнять данными.

## Shared capabilities

Все capabilities кроме compile-context-map — shared lib в Minerva. DWH-skill ссылается на них в своём SKILL.md:

```
Для аналитики используй capabilities из Minerva (shared lib):
- comparison: skill_view('minerva', file_path='capabilities/analysis/comparison/SKILL.md')
- pattern-promote: skill_view('minerva', file_path='capabilities/analysis/pattern-promote/SKILL.md')
```

Consumer не видит разницы — он просто вызывает capability.

## Pitfalls

- **Плейсхолдеры в именах директорий.** `mv "{domain}" "actual-name"` — не забыть кавычки, иначе shell раскроет фигурные скобки.
- **Два minerva skills.** В системе два скилла с именем minerva (igrolab/minerva и minerva). Использовать `igrolab/minerva`.
- **Права на запись.** `~/.hermes/skills/warehouses/` может не существовать — создать при необходимости.
