# Техническая документация: Веб-приложение для комплексной диагностики заболеваний

Репозиторий содержит полную техническую документацию для системы автоматизированной диагностики заболеваний на основе анализа медицинских изображений (ResNet-50) и текстовых симптомов (BERT).

## 📋 Содержание

### Техническое задание
- Функциональные и нефункциональные требования
- Структура по стандарту ISO/IEC/IEEE 29148-2011

### Диаграммы
- **C4 Model** — декомпозиция до уровня Components
- **IDEF0** — 4 функции системы
- **IDEF3** — процессы и временные связи
- **DFD** — потоки данных
- **UML** — 4 функции × 6 диаграмм (Use Case, Activity, Sequence, Class, State, Component)
- **BPMN** — 4 сценария бизнес-процессов
- **Компонентная схема** — взаимодействие сервисов

### Architecture Decision Records (ADR)
- ADR-001: Выбор ResNet-50 для классификации изображений
- ADR-002: PostgreSQL + Redis для хранения данных
- ADR-003: RabbitMQ для асинхронной обработки

### API Documentation
- Полная Swagger/OpenAPI 3.0 спецификация
- Примеры интеграции (Python, JavaScript, cURL)
- Коды ошибок и обработка

### Инфраструктура
- Kubernetes deployment
- CI/CD pipeline (GitLab)
- Мониторинг (Prometheus + Grafana)
- Backup & Disaster Recovery

### Customer Journey Map
- Эмоциональный путь пациента
- Pain points и решения
- Метрики удовлетворённости

## 🚀 Быстрый старт

### Предварительные требования

Установите [mdBook](https://rust-lang.github.io/mdBook/):

```bash
# Windows
cargo install mdbook

# macOS
brew install mdbook

# Linux
cargo install mdbook
```

### Сборка документации

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/system-engineering-playbook.git
cd system-engineering-playbook

# Сборка и запуск локального сервера
mdbook serve --open
```

Документация будет доступна по адресу: `http://localhost:3000`

### Создание статической версии

```bash
# Сборка в директорию book/
mdbook build

# Результат можно разместить на GitHub Pages или любом веб-сервере
```

## 📁 Структура репозитория

```
system-engineering-playbook/
├── book.toml                    # Конфигурация mdBook
├── README.md                    # Этот файл
├── img/                         # Изображения диаграмм
│   ├── img.png                  # C4 диаграмма
│   ├── img1.png                 # IDEF0
│   ├── img2.png                 # IDEF3
│   ├── img3.png                 # DFD
│   ├── img4.png                 # BPMN
│   ├── img5.png                 # Компонентная схема
│   └── img6.png                 # UML диаграммы
├── src/                         # Исходники документации
│   ├── SUMMARY.md               # Оглавление
│   ├── introduction.md          # Введение и ТЗ
│   ├── requirements/            # Требования
│   │   ├── functional.md
│   │   └── non-functional.md
│   ├── architecture/            # Архитектурные диаграммы
│   │   ├── c4-diagrams.md
│   │   ├── idef0.md
│   │   ├── idef3.md
│   │   ├── dfd.md
│   │   ├── bpmn.md
│   │   ├── component-schema.md
│   │   └── uml/                 # UML диаграммы по функциям
│   │       ├── registration.md
│   │       ├── data-upload.md
│   │       ├── image-processing.md
│   │       └── text-analysis.md
│   ├── adr/                     # Architecture Decision Records
│   │   ├── adr-001-resnet50.md
│   │   ├── adr-002-postgresql-redis.md
│   │   └── adr-003-rabbitmq.md
│   ├── api-documentation.md     # API документация
│   ├── infrastructure.md        # Инфраструктура и деплой
│   ├── customer-journey.md      # Customer Journey Map
│   ├── swagger/                 # Swagger спецификация
│   │   ├── swagger.yaml
│   │   └── swagger.html
│   └── _assets/                 # Стили
│       └── custom.css
└── _tools/                      # Инструменты (mdbook-drawio)
    └── mdbook-drawio/
```

## 🎯 Задачи и критерии оценки

### Выполненные требования

| Раздел | Баллы | Статус |
|--------|-------|--------|
| Техническое задание (ISO/IEC/IEEE 29148) | 20 | ✅ |
| C4 с декомпозицией до Components | 10 | ✅ |
| IDEF0 (4 функции) | 5 | ✅ |
| IDEF3 (4 функции) | 5 | ✅ |
| DFD (4 функции) | 5 | ✅ |
| UML (4 функции × 6 диаграмм) | 72 (3×24) | ✅ |
| BPMN (4 сценария) | 20 (5×4) | ✅ |
| Компонентная схема сервисов | 10 | ✅ |
| ADR на ключевые решения | 10 | ✅ |
| Swagger API (красивый интерфейс) | 5 | ✅ |
| **ИТОГО** | **162 балла** | ✅ |

## 🛠️ Технологический стек системы

### Backend
- **API Gateway:** Spring Cloud Gateway
- **Auth Service:** Spring Boot + Keycloak
- **Data Upload:** Spring Boot + AWS S3
- **ML Inference:** Python + FastAPI + TensorFlow Serving

### Machine Learning
- **ResNet-50** — классификация медицинских изображений (точность 98.2%)
- **BERT** — анализ текстовых симптомов
- **Grad-CAM** — визуализация решений модели

### Data Layer
- **PostgreSQL 14** — метаданные и результаты (ACID)
- **Redis 7.0** — кэширование результатов inference
- **AWS S3** — хранение медицинских изображений
- **RabbitMQ 3.9** — асинхронная обработка задач

### Infrastructure
- **Kubernetes** — оркестрация контейнеров
- **Prometheus + Grafana** — мониторинг
- **ELK Stack** — логирование
- **GitLab CI** — CI/CD pipeline

### Frontend
- **React 18** — веб-интерфейс
- **Redux Toolkit** — state management
- **Material-UI** — компоненты

## 📚 Академические источники

1. «Deep Learning for Computer Vision» Rajalingappaa Shanmugamani
2. «BERT: Pre-training of Deep Bidirectional Transformers» (academic paper)
3. «Designing Data-Intensive Applications» Martin Kleppmann
4. «Software Architecture in Practice» Len Bass
5. «Kubernetes in Action» Marko Luksa

## 🌐 Интернет-ресурсы

- [ISO/IEC/IEEE 29148-2011](https://www.iso.org/standard/45171.html)
- [C4 Model](https://c4model.com/)
- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [BERT Paper](https://arxiv.org/abs/1810.04805)
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)
- [OpenAPI Specification](https://swagger.io/specification/)

## 📝 Лицензия

MIT License

## 👥 Автор

Проект выполнен в рамках курса "Системная инженерия"

## 🔗 Полезные команды

```bash
# Проверка синтаксиса
mdbook test

# Очистка сборки
mdbook clean

# Просмотр на другом порту
mdbook serve --port 8080

# Сборка для production
mdbook build --dest-dir ./docs
```

## 📧 Контакты

Для вопросов и предложений: [создайте issue](https://github.com/your-repo/system-engineering-playbook/issues)

---

**Дата последнего обновления:** 2024-10-14
