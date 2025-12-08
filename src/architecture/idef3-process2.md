# 3.1.3. IDEF3: Процесс P2 — Загрузка медицинских данных

## Диаграмма процесса P2

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/IDEF3_P2.drawio"></iframe>

## Описание процесса P2

### Участники
- **Пациент** — инициирует загрузку данных
- **Web UI (React)** — интерфейс загрузки файлов
- **API Gateway** — валидация и маршрутизация запросов
- **DataUploadController** — обработка загрузки
- **AWS S3** — хранилище файлов
- **PostgreSQL** — база метаданных
- **RabbitMQ** — очередь сообщений

### Временные связи

| Событие | Последующее событие | Условие | Задержка |
|---------|---------------------|---------|----------|
| E1 → E2 | POST запрос отправлен | Файлы выбраны | 100 мс |
| E2 → E3 | Валидация успешна | Формат и размер корректны | 10-25 мс |
| E3 → E4 | Файл загружен в S3 | S3 upload успешен | 500-1200 мс |
| E4 → E5 | Метаданные сохранены | PostgreSQL INSERT успешен | 50-120 мс |
| E4 → E6 | Сообщение в очереди | RabbitMQ PUBLISH успешен | 10-30 мс |
| E5 → E6 | Синхронизация | Оба завершены | 0 мс |
| E6 → E7 | Подтверждение отправлено | Все операции успешны | 50 мс |

### Точки синхронизации
- **После E3**: Обязательна валидация перед загрузкой
- **После E4**: Параллельное выполнение сохранения метаданных и отправки в очередь (AND junction)
- **После E5 и E6**: Синхронизация перед отправкой подтверждения

### UOB (Unit of Behavior)

**UOB-1: Выбор файлов**
- Input: Файлы от пользователя (изображения/текст)
- Process: File picker UI, drag & drop
- Output: FileList объект

**UOB-2: Отправка POST запроса**
- Input: FileList, userId, metadata
- Process: Multipart form-data encoding, HTTP POST
- Output: HTTP request с файлами

**UOB-3: Валидация формата и размера**
- Input: File object, MIME-type, size
- Process: Проверка формата (JPEG/PNG/TXT), размера (≤10MB)
- Output: Валидированные данные или ошибка

**UOB-4: Сохранение в S3**
- Input: Binary file data, fileId, userId
- Process: AES-256 encryption, S3 PUT request
- Output: S3 URL (s3://bucket/key)

**UOB-5: Сохранение метаданных**
- Input: userId, fileId, s3Url, fileName, timestamp
- Process: SQL INSERT INTO medical_data
- Output: Database record ID

**UOB-6: Отправка в очередь**
- Input: {fileId, userId, s3Url, fileType}
- Process: RabbitMQ PUBLISH в очередь ml_inference
- Output: Message ID

### Junction
- **После UOB-3**: XOR junction (если валидация не прошла → ошибка, иначе → UOB-4)
- **После UOB-4**: AND junction (параллельное выполнение UOB-5 и UOB-6)

### Референсы
- Референс на P1: Регистрация обязательна для загрузки (precondition)

### Временная диаграмма

```
t=0s      Начало загрузки (выбор файлов)
t=0.1s    POST запрос отправлен
t=0.11s   Валидация формата (10-25 мс)
t=0.61s   Загрузка в S3 (500-1200 мс)
t=0.66s   Сохранение метаданных (50-120 мс) [параллельно]
t=0.64s   Отправка в RabbitMQ (10-30 мс) [параллельно]
t=0.69s   Синхронизация (оба завершены)
t=0.74s   Подтверждение отправлено
t=0.74s   Конец процесса
```

### Временные характеристики

| Этап | Среднее время | P95 |
|------|---------------|-----|
| Валидация формата | 10 мс | 25 мс |
| Загрузка в S3 (5MB) | 500 мс | 1200 мс |
| Сохранение метаданных | 50 мс | 120 мс |
| Отправка в RabbitMQ | 10 мс | 30 мс |
| **Итого** | **570 мс** | **1375 мс** |

### Компоненты
- Nginx (балансировка нагрузки)
- API Gateway (валидация запросов)
- AWS S3 (объектное хранилище)
- RabbitMQ (очередь сообщений)
- PostgreSQL (реляционная БД)

## Источники
- IDEF3 Process Description Capture Method
- AWS S3 Documentation
- RabbitMQ Best Practices

