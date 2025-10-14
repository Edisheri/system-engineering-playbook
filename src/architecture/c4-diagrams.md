# C4 Модель архитектуры

## Введение в C4

C4 (Context, Containers, Components, Code) — методология визуализации архитектуры ПО, разработанная Simon Brown.

### Зачем использовать C4?

- **Уровни абстракции:** Позволяет описать систему от общего контекста до кода
- **Стандартизация:** Упрощает коммуникацию между разработчиками, DevOps и заказчиками

![Диаграмма C4](img/img.png)

### C4 Context Diagram (Интерактивная версия)

```mermaid
graph TB
    Patient[👤 Пациент]
    Doctor[👨‍⚕️ Врач]
    Admin[👨‍💼 Администратор]
    
    System[🏥 Medical Diagnosis Platform<br/>Система диагностики заболеваний]
    
    MIS[🏥 Clinic MIS<br/>Клиническая информационная система]
    Email[📧 Email Service<br/>Почтовый сервис]
    
    Patient -->|Загружает изображения<br/>и симптомы| System
    System -->|Возвращает диагноз<br/>и отчёты| Patient
    
    Doctor -->|Просматривает<br/>результаты| System
    Admin -->|Управляет<br/>пользователями| System
    
    System -->|Отправляет отчёты<br/>через REST API| MIS
    System -->|Отправляет уведомления| Email
    
    style System fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style Patient fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style Doctor fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style Admin fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style MIS fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Email fill:#e6a23c,stroke:#b8821e,stroke-width:2px
```

## 4.1.1. C4-Context (Уровень 1: Контекст)

**Система:** Medical Diagnosis Platform

**Внешние сущности:**
- **Пациент:** Взаимодействует через веб-интерфейс (React)
- **Clinic MIS:** Интеграция через REST API (Spring Web)
- **Администратор:** Управляет правами доступа (Keycloak)

**Связи:**
- Пациент → Система: `POST /upload` (изображения/текст)
- Система → MIS: `POST /report` (JSON/PDF)

### Обоснование

Контекстная диаграмма помогает заказчикам понять границы системы (источник: [C4 Model](https://c4model.com/)).

---

## 4.1.2. C4-Container (Уровень 2: Контейнеры)

### Контейнеры:

#### Web-интерфейс (React)
- Фронтенд для загрузки данных и отображения результатов
- Связь с API Gateway через HTTP

#### API Gateway (Spring Cloud)
- Маршрутизация запросов
- Аутентификация (JWT), валидация данных (Spring Validator)

#### ML Inference Service (TensorFlow Serving)
- GPU-обработка изображений (ResNet-50) и текста (BERT)
- Асинхронное взаимодействие через RabbitMQ

#### Database Cluster
- **PostgreSQL 14:** Хранение метаданных (пациенты, отчёты)
- **Redis 7.0:** Кэширование результатов ИИ (скорость доступа)

#### Message Broker (RabbitMQ 3.9)
- Очередь `medical_data` для обработки запросов

### Зачем контейнеры?

**Масштабируемость:** Каждый контейнер можно обновлять и масштабировать независимо (источник: «Kubernetes in Action»).

### C4 Container Diagram (Интерактивная версия)

```mermaid
graph TB
    subgraph "Пользователи"
        Patient[👤 Пациент]
        Doctor[👨‍⚕️ Врач]
    end
    
    subgraph "Medical Diagnosis Platform"
        WebApp[🌐 Web Application<br/>React 18]
        APIGateway[🚪 API Gateway<br/>Spring Cloud]
        
        subgraph "Business Services"
            AuthService[🔐 Auth Service<br/>Spring Boot + Keycloak]
            DataUpload[📤 Data Upload Service<br/>Spring Boot]
            MLService[🤖 ML Inference Service<br/>Python + FastAPI]
            ReportService[📄 Report Service<br/>Spring Boot]
        end
        
        subgraph "Data Layer"
            PostgreSQL[(🗄️ PostgreSQL 14<br/>Метаданные)]
            Redis[(⚡ Redis 7.0<br/>Кэш)]
            S3[(📦 AWS S3<br/>Изображения)]
        end
        
        subgraph "Message Broker"
            RabbitMQ[🐰 RabbitMQ 3.9<br/>Очереди]
        end
        
        subgraph "ML/AI"
            TFServing[🧠 TensorFlow Serving<br/>ResNet-50 + BERT]
        end
    end
    
    Patient --> WebApp
    Doctor --> WebApp
    WebApp -->|HTTP/JSON| APIGateway
    
    APIGateway --> AuthService
    APIGateway --> DataUpload
    APIGateway --> ReportService
    
    AuthService --> PostgreSQL
    DataUpload --> S3
    DataUpload --> PostgreSQL
    DataUpload -->|AMQP| RabbitMQ
    
    RabbitMQ --> MLService
    MLService --> TFServing
    MLService --> Redis
    MLService --> PostgreSQL
    
    ReportService --> PostgreSQL
    ReportService --> Redis
    
    style WebApp fill:#61dafb,stroke:#20232a,stroke-width:2px
    style APIGateway fill:#6db33f,stroke:#4a7c2f,stroke-width:3px
    style AuthService fill:#6db33f,stroke:#4a7c2f,stroke-width:2px
    style DataUpload fill:#6db33f,stroke:#4a7c2f,stroke-width:2px
    style MLService fill:#ff6f00,stroke:#c43e00,stroke-width:2px
    style ReportService fill:#6db33f,stroke:#4a7c2f,stroke-width:2px
    style PostgreSQL fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style Redis fill:#dc382d,stroke:#a02822,stroke-width:2px,color:#fff
    style S3 fill:#ff9900,stroke:#cc7700,stroke-width:2px
    style RabbitMQ fill:#ff6600,stroke:#cc5200,stroke-width:2px,color:#fff
    style TFServing fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
```

---

## 4.1.3. C4-Component (Уровень 3: Компоненты)

### API Gateway компоненты:

- **AuthController:** Регистрация (JWT), управление ролями
- **DataUploadController:** Приём файлов (multipart/form-data) → отправка в RabbitMQ

### ML Inference Service компоненты:

- **ImagePreprocessor:** Resize (OpenCV), нормализация (TensorFlow)
- **BERTTokenizer:** Токенизация текста (HuggingFace)
- **ResNetModel:** Классификация изображений (CheXNet weights)

### Хранилище компоненты:

- **S3Client:** Сохранение сырых данных (AWS S3)
- **RedisCache:** Кэширование результатов (TTL=1h)

---

## Диаграммы

Полные диаграммы C4 с декомпозицией до уровня компонентов представлены на изображениях выше.

