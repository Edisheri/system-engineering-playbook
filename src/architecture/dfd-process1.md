# 3.1.4. DFD: Процесс P1 — Приём данных

## Диаграмма потоков данных P1

```mermaid
flowchart LR
    Patient[Пациент<br/>Внешняя сущность] -->|"Поток 1.1: HTTP POST запрос<br/>(multipart/form-data)"| P1(("P1: Приём данных"))
    P1 -->|"Поток 1.2: Файлы<br/>(JPEG/PNG)"| D1[("D1: AWS S3<br/>Хранилище данных")]
    P1 -->|"Поток 1.3: Метаданные<br/>(user_id, file_id, s3_url)"| D2[("D2: PostgreSQL<br/>Хранилище данных")]
    P1 -->|"Поток 1.4: Сообщение<br/>(JSON/AMQP)"| RabbitMQ[RabbitMQ<br/>Внешняя сущность]
    P1 -->|"Поток 1.5: Подтверждение<br/>(JSON)"| Patient
    
    style P1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style Patient fill:#ff9800,stroke:#e68900,stroke-width:2px
    style RabbitMQ fill:#ff9800,stroke:#e68900,stroke-width:2px
    style D1 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style D2 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
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

