# UML Диаграммы: Загрузка данных

## Функция 2: Загрузка медицинских данных

Эта функция отвечает за приём медицинских изображений и текстовых симптомов от пациентов с валидацией, шифрованием и сохранением в S3 и PostgreSQL.

---

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 900px; min-height: 700px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-usecase.html"></iframe>

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

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-activity.html"></iframe>

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

<iframe style="width: 100%; height: 1400px; min-height: 1000px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-data-upload-sequence.html"></iframe>

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
