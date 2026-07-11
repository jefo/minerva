---
name: minerva
description: Композиционный движок знаний — имплементация Knowledge Services
version: 0.1.0
status: draft
triggers:
  - Работа с Knowledge Services workspace
  - Навигация по knowledge base
  - Запрос на чтение знаний из KB
---

# minerva — Knowledge Services Implementation

Имплементация композиционного движка знаний. Предоставляет capabilities для работы с workspace: навигация, создание, валидация, компиляция.

## Capabilities

| Capability | Назначение | Статус |
|---|---|---|
| `workspace-orientation` | Понять устройство workspace: контексты, служебные файлы | MVP |
| `context-exploration` | Войти в контекст, прочитать index.md, увидеть уровни | MVP |
| `level-browsing` | Список знаний на уровне композиции с аннотациями | MVP |
| `knowledge-retrieval` | Прочитать конкретное знание | MVP |

## Оркестрация

Оркестратор маршрутизирует запросы к нужной capability на основе интента:

| Интент пользователя | Capability |
|---|---|
| «Что есть в этой KB?» / «Какие контексты?» | `workspace-orientation` |
| «Расскажи про контекст coffee» / «Что внутри equipment?» | `context-exploration` |
| «Какие Primitives в coffee?» / «Покажи Modules в equipment» | `level-browsing` |
| «Прочитай espresso.md» / «Дай мне Extraction Model» | `knowledge-retrieval` |

## Правила оркестратора

1. Оркестратор не содержит реализации операций — только маршрутизация.
2. При неоднозначном интенте — спросить пользователя, какой контекст/уровень.
3. Если capability возвращает ошибку — передать её пользователю, не пытаться исправить самостоятельно.
4. Оркестратор знает контракты всех capabilities. Изменение контракта capability → обновление оркестратора.

## Зависимости

- ADR-002: Five-level hierarchy
- ADR-006: Filesystem premises
- ADR-007: Workspace structure
- ADR-009: MVP capabilities
