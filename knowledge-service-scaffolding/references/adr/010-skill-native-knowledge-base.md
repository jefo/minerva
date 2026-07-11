---
id: adr-010
status: accepted
date: 2026-07-11
supersedes: []
superseded_by: []
tags: [architecture, skill, references, progressive-disclosure, deployment]
based_on: [adr-005, adr-006, adr-007]
---

# ADR-010: Bounded contexts как references скилла — skill-native knowledge management

## Контекст

ADR-007 определил workspace как отдельную директорию с контекстами и `index.md`. Навигация по workspace — собственная реализация progressive disclosure: `workspace/index.md` → `context/index.md` → файлы знаний.

Но Hermes **уже имеет** встроенный progressive disclosure для скиллов:
- `skill_view("minerva")` → `SKILL.md` (entry point)
- `linked_files` → каталог файлов скилла
- `skill_view("minerva", file_path="references/...")` → конкретный файл

Это тот же паттерн entry → catalog → content, реализованный платформой. Наша навигация по workspace — дублирование существующего механизма.

## Решение

**Bounded contexts Knowledge Services размещаются в `references/` скилла minerva.**

Скилл и knowledge base — одно целое:

```
minerva/
├── SKILL.md                        # entry point: описание KB + оркестрация
├── capabilities/                   # операции над KB
│   ├── workspace-orientation/      # → теперь: читает SKILL.md и linked_files
│   ├── context-exploration/        # → теперь: skill_view(file_path='references/coffee/index.md')
│   ├── level-browsing/             # → теперь: фильтрует linked_files по пути
│   └── knowledge-retrieval/        # → теперь: skill_view(file_path='references/coffee/primitives/...')
└── references/                     # = workspace
    ├── coffee/                     # = bounded context
    │   ├── index.md
    │   ├── primitives/
    │   ├── components/
    │   ├── modules/
    │   ├── views/
    │   └── artifacts/
    ├── equipment/                  # = bounded context
    │   └── ...
    └── context-map.md
```

### Как меняется навигационный flow

| Раньше | Теперь |
|---|---|
| `read_file(workspace/index.md)` | `skill_view("minerva")` — SKILL.md уже содержит карту контекстов |
| `ls workspace/` → найти контексты | `linked_files` — список всех контекстов и их файлов |
| `read_file(context/index.md)` | `skill_view("minerva", file_path="references/coffee/index.md")` |
| `ls context/primitives/` | фильтр `linked_files` по префиксу `references/coffee/primitives/` |
| `read_file(primitives/espresso.md)` | `skill_view("minerva", file_path="references/coffee/primitives/espresso.md")` |

### Что даёт skill-native подход

**1. Zero-cost discoverability.** Агент, загрузивший скилл, через `linked_files` сразу видит всё содержимое KB — все контексты, все уровни, все файлы. Не нужно реализовывать `ls` и `find` — платформа уже сделала это. Возможности Workspace Orientation и Level Browsing становятся встроенным поведением платформы, не нашей capability.

**2. Навигация через один механизм.** Агент не переключается между «читаю workspace» и «читаю скилл». Всё — `skill_view`. Три шага навигации — это три вызова одного и того же инструмента с разными параметрами. Кривая обучения агента — flat.

**3. Skill = деплой-единица.** `git clone` → symlink в `~/.hermes/skills/` → агент в любом окружении получает и скилл, и KB как одно целое. Никакого разделения «установить скилл» и «создать workspace». Knowledge base приходит вместе с инструментом для работы с ней.

**4. KB — это references скилла.** Не метафора, а буквально: файлы знаний лежат в `references/`, платформа их индексирует как `linked_files`, агент читает их через `skill_view`. Knowledge base является полноправной частью скилла без дополнительного кода.

### Не-regression: ADR-006 продолжает работать

Файлы в `references/` остаются обычными `.md` с YAML frontmatter. Claude Code читает их напрямую. Codex открывает PR. Git работает. `skill_view` — это convenience layer, не платформенный lock-in. Скилл можно вынуть из Hermes — останется директория с файлами, которую любой агент читает через `read_file`.

Skill-native — это про устранение дублирующего слоя навигации. Не про замыкание на платформу.

### Что происходит с workspace как отдельной сущностью

Workspace перестаёт быть отдельной концепцией верхнего уровня. Теперь:
- **Workspace = references/ скилла.** Или: workspace — это скилл minerva, развёрнутый в конкретную KB.
- **Контекст = поддиректория в references/.**
- **context-map.md = references/context-map.md.**
- **index.md контекста** остаётся, но теперь он доступен через `skill_view(file_path=...)`.

Workspace не исчезает как концепт — он переопределяется: workspace это не «директория с контекстами», а «инстанс скилла minerva с заполненными references».

## Альтернативы

| Вариант | Плюсы | Минусы | Почему нет |
|---|---|---|---|
| Workspace отдельно от скилла (ADR-007) | Изоляция: скилл не зависит от данных | Дублирование progressive disclosure. Агент использует два механизма навигации | Избыточно. Платформа уже даёт навигацию |
| Workspace = git submodule в references/ | Можно обновлять KB независимо от скилла | Усложняет деплой. Не решает проблему дублирования навигации | Не устраняет корневую проблему |
| Оставить оба варианта (workspace снаружи И references внутри) | Гибкость: пользователь выбирает | Два способа делать одно и то же. Confusion у агентов и пользователей | Нарушает SSOT |

## Последствия

**Что становится проще:**
- Capabilities навигации: вместо `read_file` + `ls` + парсинг — вызовы `skill_view` и работа с `linked_files`
- Деплой: `git clone` + один symlink → скилл и KB готовы
- Onboarding агента: `skill_view("minerva")` → агент сразу в контексте всей KB
- Поддержка: не нужно синхронизировать два механизма progressive disclosure

**Что усложняется:**
- Крупные KB (1000+ файлов): `linked_files` может стать большим. Решается индексными файлами на уровне контекстов
- Мульти-инстанс: одна KB на несколько проектов. Теперь каждый инстанс — это копия скилла со своими references. Решается git-ветками или форком репо (ADR-006: всё — файлы, git решает)

**Что требует внимания:**
- `SKILL.md` не должен раздуваться от описания KB. Он остаётся entry point и оркестратором. Детали контекстов — в `references/coffee/index.md`
- `linked_files` обновляется при изменении файлов. Агент должен перечитывать его после изменений
- Не потерять ADR-006: skill-native — это удобство, не обязательство. Если платформа завтра исчезнет — файлы останутся
