# Summary

**Стандарт:** ISO/IEC/IEEE 29148-2011 (Systems and software engineering — Life cycle processes — Requirements engineering)

- [1. Введение](./introduction.md)

---

# 2. Требования (Requirements)

- [2.1. Функциональные требования](./requirements/functional.md)
- [2.2. Нефункциональные требования](./requirements/non-functional.md)

---

# 3. Архитектура системы (System Architecture)

## 3.1. Диаграммы архитектуры

- [3.1.1. C4 Model](./architecture/c4-diagrams.md)

### 3.1.2. IDEF0 Диаграммы (4 функции)
- [3.1.2.1. IDEF0: Обзор](./architecture/idef0.md)
- [3.1.2.2. IDEF0: Функция A1 — Приём данных](./architecture/idef0-function1.md)
- [3.1.2.3. IDEF0: Функция A2 — Препроцессинг](./architecture/idef0-function2.md)
- [3.1.2.4. IDEF0: Функция A3 — ИИ-анализ](./architecture/idef0-function3.md)
- [3.1.2.5. IDEF0: Функция A4 — Формирование отчёта](./architecture/idef0-function4.md)

### 3.1.3. IDEF3 Диаграммы (4 процесса)
- [3.1.3.1. IDEF3: Обзор](./architecture/idef3.md)
- [3.1.3.2. IDEF3: Процесс P1 — Регистрация](./architecture/idef3-process1.md)
- [3.1.3.3. IDEF3: Процесс P2 — Загрузка данных](./architecture/idef3-process2.md)
- [3.1.3.4. IDEF3: Процесс P3 — GPU-обработка](./architecture/idef3-process3.md)
- [3.1.3.5. IDEF3: Процесс P4 — Логирование](./architecture/idef3-process4.md)

### 3.1.4. DFD Диаграммы (4 процесса)
- [3.1.4.1. DFD: Обзор](./architecture/dfd.md)
- [3.1.4.2. DFD: Процесс P1 — Приём данных](./architecture/dfd-process1.md)
- [3.1.4.3. DFD: Процесс P2 — Валидация](./architecture/dfd-process2.md)
- [3.1.4.4. DFD: Процесс P3 — ИИ-анализ](./architecture/dfd-process3.md)
- [3.1.4.5. DFD: Процесс P4 — Логирование](./architecture/dfd-process4.md)

### 3.1.5. BPMN Диаграммы
- [3.1.5.1. BPMN: Обзор](./architecture/bpmn.md)
- [3.1.5.2. BPMN Сценарий 1: Регистрация пациента](./architecture/bpmn-scenario1.md)
- [3.1.5.3. BPMN Сценарий 2: Загрузка данных](./architecture/bpmn-scenario2.md)
- [3.1.5.4. BPMN Сценарий 3: ИИ-анализ](./architecture/bpmn-scenario3.md)
- [3.1.5.5. BPMN Сценарий 4: Интеграция с MIS](./architecture/bpmn-scenario4.md)

### 3.1.6. UML Диаграммы
- [3.1.6.1. Функция 1: Регистрация пользователя](./architecture/uml/registration.md)
- [3.1.6.2. Функция 2: Загрузка данных](./architecture/uml/data-upload.md)
- [3.1.6.3. Функция 3: Обработка изображений](./architecture/uml/image-processing.md)
- [3.1.6.4. Функция 4: Анализ текста](./architecture/uml/text-analysis.md)

### 3.1.7. Компонентная схема
- [3.1.7.1. Компонентная схема системы](./architecture/component-schema.md)

---

# 4. Архитектурные решения (Architecture Decision Records)

- [4.1. ADR-001: Выбор ResNet-50](./adr/adr-001-resnet50.md)
- [4.2. ADR-002: PostgreSQL + Redis](./adr/adr-002-postgresql-redis.md)
- [4.3. ADR-003: RabbitMQ](./adr/adr-003-rabbitmq.md)

---

# 5. Интерфейсы (Interfaces)

- [5.1. Публичный API](./api-documentation.md)

---

# 6. Инфраструктура (Infrastructure)

- [6.1. Инфраструктура и деплой](./infrastructure.md)
- [6.2. Customer Journey Map](./customer-journey.md)

---

# 7. Приложения (Appendices)

- [7.1. Примеры: DrawIO](./drawio.md)
- [7.2. Примеры: Markdown](./md.md)
- [7.3. Swagger Example](./swagger.md)
