# UML Диаграммы: Загрузка данных

## Функция 2: Загрузка медицинских данных

Эта функция отвечает за приём медицинских изображений и текстовых симптомов от пациентов с валидацией, шифрованием и сохранением в S3 и PostgreSQL.

---

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-usecase.html"></iframe>

**Актёры:**
- **Пациент** - загружает медицинские данные
- **Система хранения** (S3, PostgreSQL) - сохраняет данные

**Основные Use Cases:**

1. **Аутентификация**
   - Проверка JWT токена
   - Rate Limiting: 100 req/min

2. **Загрузить изображение**
   - Включает: Валидация файла
   - Включает: Сохранение в S3 (с шифрованием AES-256)
   - Включает: Сохранение метаданных PostgreSQL
   - Включает: Отправка в RabbitMQ

3. **Валидация файла**
   - Включает: Проверка MIME-типа (JPEG/PNG)
   - Включает: Проверка размера ≤10MB

4. **Загрузить текстовые симптомы**
   - Включает: Валидация (≤1000 символов)
   - Включает: Сохранение метаданных
   - Включает: Отправка в очередь

---

### 2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-activity.html"></iframe>

**Процесс загрузки данных:**

1. **Start** - Пациент входит в систему
2. **Проверка JWT токена** → Decision: Токен валиден?
3. **Выбор типа данных**
4. **Fork** - Параллельная валидация:
   - **Ветка 1: Изображение**
     - Валидация формата (JPEG/PNG) → Decision
     - Проверка размера ≤10MB → Decision
   - **Ветка 2: Текст**
     - Валидация длины ≤1000 символов → Decision
5. **Join** после валидации
6. **Fork** - Параллельное сохранение:
   - Шифрование AES-256 → Сохранение в S3
   - INSERT INTO medical_data (PostgreSQL)
   - Формирование JSON → Отправка в RabbitMQ
7. **Rate Limiting проверка** (100 req/min) → Decision
8. **End** - Возврат 201 Created + fileId

---

### 3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-sequence.html"></iframe>

**Участники:**
- Пациент
- WebUI (React)
- API Gateway (Kong)
- DataUploadService (Spring Boot)
- FileValidator
- AWS S3
- PostgreSQL
- RabbitMQ

**Основной поток:**

1. **Выбор файла:**
   - Пациент → WebUI: Выбор файла

2. **Отправка запроса:**
   - WebUI → Gateway: POST /upload (multipart/form-data, JWT)
   - Gateway: Проверка JWT + Rate Limiting (100 req/min)

3. **Валидация:**
   - Gateway → DataUploadService → FileValidator
   - Validator: Проверка MIME-типа + Проверка размера ≤10MB
   - Alt: Валидация не прошла → 400 Bad Request

4. **Параллельное сохранение** (par):
   - **S3**: PUT /medical-images-raw/{userId}/{fileId} + Шифрование AES-256
   - **PostgreSQL**: INSERT INTO medical_data
   - **RabbitMQ**: PUBLISH message {fileId, userId, s3Url, fileType}

5. **Ответ:**
   - DataUploadService → Gateway: 201 Created + {fileId, s3Url}
   - Gateway → WebUI → Пациент: Загрузка успешна

---

## Связь с другими диаграммами

- **IDEF0 A1**: Функция "Приём данных" - загрузка является ключевой частью
- **IDEF3 P1**: Процесс "Регистрация" - после регистрации пациент загружает данные
- **DFD P1**: Поток данных "Загрузка" обрабатывает файлы и симптомы
- **Требования**: FR-1.2 (Приём изображений), FR-1.3 (Приём симптомов), NFR-2.3 (Шифрование AES-256)

---

### 4. Class Diagram (Диаграмма классов)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-class.html"></iframe>

**Основные классы:**

**MedicalFile** (id, userId, fileName, fileType, sizeBytes, uploadedAt)
- Methods: validate(), getS3Url()
- Связи: 1 -- 1 FileType

**FileUploadController** (validator, s3Service, dbService, queueService)
- Methods: uploadFile(), handleUpload()
- Использует: FileValidator, S3StorageService, DatabaseService, MessageQueueService
- Обрабатывает: FileUploadRequest
- Производит: FileUploadResult

**FileValidator** (maxSizeBytes=10MB, allowedMimeTypes)
- Methods: validateFormat(), validateSize(), validateMimeType()

**S3StorageService** (bucketName, region)
- Methods: uploadFile(), encryptAES256(), generatePresignedUrl()

**DatabaseService** (connection)
- Methods: saveMetadata(), updateStatus(), getFileInfo()

**MessageQueueService** (queueName, rabbitMQ)
- Methods: publishMessage(), createMessage()

**FileUploadResult** (fileId, s3Url, status)
- Methods: isSuccess()
- Связи: 1 -- 1 UploadStatus (SUCCESS, FAILED_VALIDATION, FAILED_STORAGE, FAILED_QUEUE)

---

### 5. State Diagram (Диаграмма состояний)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-state.html"></iframe>

**Состояния загрузки файла:**

1. **[*] → Received** - File uploaded
   - Субсостояния: CheckingAuth → ValidatingJWT → RateLimitCheck
   - Переходы: → Rejected (Auth failed) | → Validating (Authorized)

2. **Validating** - Валидация
   - Субсостояния: CheckingFormat → CheckingMimeType → CheckingSize
   - Переходы: → Rejected (Validation failed) | → Storing (Valid file)

3. **Storing** - Сохранение
   - Субсостояния: Encrypting (AES-256) → UploadingToS3 → SavingMetadata (INSERT + Indexes)
   - Переходы: → Failed (Storage error) | → Queuing (Stored successfully)

4. **Queuing** - Очередь
   - Субсостояния: CreatingMessage → PublishingToQueue → WaitingForAck
   - Переходы: → Failed (Queue error) | → Completed (Message sent)

5. **Completed** - Завершено
   - ReturningResponse → 201 Created → [*]

6. **Rejected** - Отклонено
   - LoggingError → Returning400 → [*]

7. **Failed** - Ошибка
   - LoggingError → RollingBack → Returning500 → [*]

---

### 6. Component Diagram (Диаграмма компонентов)

<iframe style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-component.html"></iframe>

**Компоненты системы загрузки:**

**Data Upload Service:**
- UploadController → FileValidator → S3Client → DatabaseClient → QueuePublisher

**External Systems:**
- PostgreSQL (table: medical_data, indexes: user_id, uploaded_at)
- RabbitMQ (queue: medical_data, format: JSON/AMQP, retry: 3 attempts)
- AWS S3 (bucket: medical-images-raw, encryption: AES-256, region: us-east-1)
- API Gateway (Kong) - rate limiting, JWT validation

**Frontend:**
- WebUI (React) → API Gateway (HTTPS POST /upload)

---

## Технические детали

**Валидация:**
- MIME-типы: image/jpeg, image/png
- Максимальный размер: 10 МБ
- Текст: ≤1000 символов

**Хранение:**
- S3 Bucket: medical-images-raw
- Шифрование: AES-256
- Структура: {userId}/{fileId}.{ext}

**База данных:**
- Таблица: medical_data
- Поля: user_id, file_id, file_name, s3_url, uploaded_at
- Индексы: user_id, uploaded_at

**Очередь:**
- RabbitMQ queue: medical_data
- Формат: JSON/AMQP
- Payload: {fileId, userId, s3Url, fileType, timestamp}
