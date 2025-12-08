# 3.1.4. DFD: Процесс P1 — Приём данных

## Диаграмма потоков данных P1

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P1.drawio"></iframe>

### Декомпозиция P1

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P1_DECOMPOSITION.drawio"></iframe>

## Потоки данных

| Поток | Источник | Назначение | Данные | Формат |
|-------|----------|------------|--------|--------|
| 1.1 | Пациент | P1 | Файлы + метаданные | multipart/form-data |
| 1.2 | P1 | D1 (AWS S3) | Binary file | JPEG/PNG, encrypted |
| 1.3 | P1 | D2 (PostgreSQL) | user_id, file_name, s3_url, uploaded_at | SQL INSERT |
| 1.4 | P1 | RabbitMQ | {fileId, userId, s3Url, fileType, timestamp} | JSON/AMQP |
| 1.5 | P1 | Пациент | {taskId, status: "uploaded"} | JSON/HTTP 200 |
| 1.6 | P1 | Пациент | {error: "validation_failed", details: [...]} | JSON/HTTP 400 |

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

## Обработка ошибок

**Поток ошибки валидации (1.6):**
- Источник: P1 (после проверки формата/размера)
- Назначение: Пациент
- Данные: {error: "validation_failed", code: "INVALID_FORMAT" | "FILE_TOO_LARGE" | "RATE_LIMIT_EXCEEDED", message: "..."}
- Формат: JSON/HTTP 400 Bad Request

**Условия ошибок:**
- Неподдерживаемый формат файла → INVALID_FORMAT
- Размер файла > 10 МБ → FILE_TOO_LARGE
- Превышен rate limit → RATE_LIMIT_EXCEEDED
- Ошибка загрузки в S3 → S3_UPLOAD_FAILED
- Ошибка сохранения в БД → DATABASE_ERROR

