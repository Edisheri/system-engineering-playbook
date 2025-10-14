# Summary

[Введение](./introduction.md)

---

# Требования

- [Функциональные требования](./requirements/functional.md)
- [Нефункциональные требования](./requirements/non-functional.md)

---

# Архитектура системы

## Диаграммы

- [C4 Model](./architecture/c4-diagrams.md)

### IDEF0 Диаграммы (4 функции × 5 баллов = 20 баллов)
- [IDEF0: Обзор](./architecture/idef0.md)
- [IDEF0: Функция A1 — Приём данных](./architecture/idef0-function1.md)
- [IDEF0: Функция A2 — Препроцессинг](./architecture/idef0-function2.md)
- [IDEF0: Функция A3 — ИИ-анализ](./architecture/idef0-function3.md)
- [IDEF0: Функция A4 — Формирование отчёта](./architecture/idef0-function4.md)

### IDEF3 Диаграммы (4 процесса × 5 баллов = 20 баллов)
- [IDEF3: Обзор](./architecture/idef3.md)
- [IDEF3: Процесс P1 — Регистрация](./architecture/idef3-process1.md)
- [IDEF3: Процесс P2 — Загрузка данных](./architecture/idef3-process2.md)
- [IDEF3: Процесс P3 — GPU-обработка](./architecture/idef3-process3.md)
- [IDEF3: Процесс P4 — Логирование](./architecture/idef3-process4.md)

### DFD Диаграммы (4 процесса × 5 баллов = 20 баллов)
- [DFD: Обзор](./architecture/dfd.md)
- [DFD: Процесс P1 — Приём данных](./architecture/dfd-process1.md)
- [DFD: Процесс P2 — Валидация](./architecture/dfd-process2.md)
- [DFD: Процесс P3 — ИИ-анализ](./architecture/dfd-process3.md)
- [DFD: Процесс P4 — Логирование](./architecture/dfd-process4.md)

- [BPMN Диаграммы](./architecture/bpmn.md)
- [Компонентная схема](./architecture/component-schema.md)

## UML Диаграммы

- [Функция 1: Регистрация пользователя](./architecture/uml/registration.md)
- [Функция 2: Загрузка данных](./architecture/uml/data-upload.md)
- [Функция 3: Обработка изображений](./architecture/uml/image-processing.md)
- [Функция 4: Анализ текста](./architecture/uml/text-analysis.md)

---

# Architecture Decision Records (ADR)

- [ADR-001: Выбор ResNet-50](./adr/adr-001-resnet50.md)
- [ADR-002: PostgreSQL + Redis](./adr/adr-002-postgresql-redis.md)
- [ADR-003: RabbitMQ](./adr/adr-003-rabbitmq.md)

---

# Публичный API

- [API Documentation (Swagger)](./api-documentation.md)

---

# Инфраструктура

- [Инфраструктура и деплой](./infrastructure.md)
- [Customer Journey Map](./customer-journey.md)

---

# Справочные материалы

- [Примеры: DrawIO](./drawio.md)
- [Примеры: Markdown](./md.md)
- [Swagger Example](./swagger.md)
