# UML Диаграммы: Загрузка данных

## Функция 2: Загрузка медицинских данных

### 1. Use Case Diagram (Диаграмма вариантов использования)

![Диаграмма](img/diagrams/uml-data-upload-1.png)

**Актёры:**
- **Пациент** (Patient)
- **Система хранения** (Storage System)

**Варианты использования:**
1. **Загрузка изображений**
   - Первичный актёр: Пациент
   - Предусловия: Пациент аутентифицирован
   - Постусловия: Изображение сохранено в S3
   
2. **Загрузка описания симптомов**
   - Первичный актёр: Пациент
   - Предусловия: Пациент аутентифицирован
   - Постусловия: Текст сохранён, отправлен в очередь
   
3. **Валидация файлов**
   - Первичный актёр: Система
   - Связь: `<<include>>` для обоих сценариев загрузки

**Связи:**
- `<<include>>`: Загрузка включает валидацию
- `<<extend>>`: Предпросмотр расширяет загрузку изображения

---

### 2. Activity Diagram (Диаграмма активностей)

![Диаграмма](img/diagrams/uml-data-upload-2.png)

**Параллельные активности:**
- Fork: Разделение на параллельные потоки
- Join: Синхронизация потоков

---

### 3. Sequence Diagram (Диаграмма последовательности)

**Участники:**
- Patient (Пациент)
- WebUI (React)
- APIGateway (Spring Cloud)
- DataUploadController
- FileValidator
- S3Client
- PostgreSQL
- RabbitMQ

![Диаграмма](img/diagrams/uml-data-upload-3.png)

---

### 4. Class Diagram (Диаграмма классов)

![Диаграмма](img/diagrams/uml-data-upload-4.png)

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** File Upload

![Диаграмма](img/diagrams/uml-data-upload-5.png)

**Состояния:**
1. **Validating:** Проверка формата и размера
2. **Uploading:** Загрузка в S3
3. **Uploaded:** Файл сохранён в S3
4. **InQueue:** Сообщение в RabbitMQ
5. **Processing:** ML Service обрабатывает
6. **Completed:** Обработка завершена
7. **Failed:** Ошибка на любом этапе
8. **Archived:** Перемещён в долгосрочное хранилище

---

### 6. Component Diagram (Диаграмма компонентов)

```mermaid
graph TB
    subgraph "Data Upload Module"
        DataUploadController[DataUploadController]
        UploadService[UploadService]
        FileValidator[FileValidator]
        RESTAPI[REST API<br/>POST /upload]
    end
    
    subgraph "Storage Layer"
        S3Client[AWS S3 Client<br/>Object Storage]
        MetadataRepo[Metadata Repo<br/>JPA/PostgreSQL]
    end
    
    subgraph "Message Producer"
        RabbitMQProducer[RabbitMQProducer]
        MessageBuilder[MessageBuilder]
    end
    
    subgraph "External Services"
        S3[(AWS S3<br/>Bucket)]
        PostgreSQL[(PostgreSQL<br/>Database)]
        RabbitMQ[RabbitMQ<br/>medical_data Queue]
    end
    
    DataUploadController --> UploadService
    DataUploadController --> FileValidator
    DataUploadController --> RESTAPI
    UploadService --> S3Client
    UploadService --> MetadataRepo
    S3Client --> S3
    MetadataRepo --> PostgreSQL
    RabbitMQProducer --> MessageBuilder
    RabbitMQProducer --> RabbitMQ
    
    style DataUploadController fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UploadService fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style S3Client fill:#6db33f,stroke:#4a7c2f,stroke-width:2px
    style RabbitMQProducer fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style S3 fill:#ff9900,stroke:#cc7700,stroke-width:2px
    style PostgreSQL fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style RabbitMQ fill:#ff6600,stroke:#cc5200,stroke-width:2px,color:#fff
```

**Внешние зависимости:**
- AWS SDK (S3 Client)
- Spring AMQP (RabbitMQ)
- Spring Data JPA (PostgreSQL)

---

## Источники

- «Clean Architecture» Robert Martin
- [AWS S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)
- [RabbitMQ Patterns](https://www.rabbitmq.com/getstarted.html)

