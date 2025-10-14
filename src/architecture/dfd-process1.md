# DFD: Процесс P1 — Приём данных

## Диаграмма потоков данных P1

```mermaid
graph TB
    Patient[👤 Пациент]
    
    P1[P1<br/>Приём<br/>данных]
    
    D1[(D1<br/>AWS S3<br/>Изображения)]
    D2[(D2<br/>PostgreSQL<br/>Метаданные)]
    
    Queue[RabbitMQ<br/>medical_data]
    
    Patient -->|HTTP POST<br/>multipart/form-data| P1
    P1 -->|Файлы| D1
    P1 -->|Метаданные<br/>user_id, file_id| D2
    P1 -->|Сообщение<br/>JSON| Queue
    P1 -->|202 Accepted<br/>taskId| Patient
    
    style P1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style D1 fill:#ff9900,stroke:#cc7700,stroke-width:2px
    style D2 fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style Queue fill:#ff6600,stroke:#cc5200,stroke-width:2px,color:#fff
```

## Потоки данных

| Поток | Источник | Назначение | Данные | Формат |
|-------|----------|------------|--------|--------|
| 1 | Пациент | P1 | Файлы + метаданные | multipart/form-data |
| 2 | P1 | AWS S3 | Binary file | JPEG/PNG |
| 3 | P1 | PostgreSQL | user_id, file_name, s3_url | SQL INSERT |
| 4 | P1 | RabbitMQ | {fileId, s3Url, type} | JSON/AMQP |
| 5 | P1 | Пациент | {taskId, status} | JSON/HTTP |

## Хранилища данных

**D1: AWS S3**
- Bucket: medical-images-raw
- Key format: {userId}/{fileId}.jpg
- Access: Private (signed URLs)

**D2: PostgreSQL - таблица medical_data**
```sql
CREATE TABLE medical_data (
    id UUID PRIMARY KEY,
    user_id BIGINT,
    file_name VARCHAR(255),
    s3_url TEXT,
    uploaded_at TIMESTAMP
);
```

