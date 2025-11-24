# UML Диаграммы: Система медицинской диагностики с ИИ

## Полный набор UML диаграмм для AI Medical Diagnosis System

Система использует машинное обучение (ResNet-50 и BERT) для анализа медицинских изображений и текстовых симптомов, предоставляя врачам автоматическую диагностику с объяснениями (Grad-CAM, SHAP).

---

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 900px; min-height: 700px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-usecase.html"></iframe>

**Актёры:**
- **Пациент** - загружает медицинские данные, просматривает результаты
- **Врач** - просматривает диагнозы, подтверждает/редактирует заключения (наследует от Пациента)
- **Администратор** - управляет пользователями, настройками, метриками (наследует от Врача)
- **ML Engineer** - обновляет ML модели, проводит A/B тестирование

**Основные Use Cases:**

**Пациент:**
- Регистрация (включает: валидация email, хеширование BCrypt, отправка активации)
- Вход в систему
- Загрузить медицинское изображение (включает: валидация JPEG/PNG, проверка ≤10MB, сохранение в S3, отправка в RabbitMQ)
- Ввести текстовые симптомы (включает: валидация ≤1000 символов, сохранение в PostgreSQL)
- Просмотреть результаты диагностики (расширяется: просмотр Grad-CAM heatmap, SHAP объяснений)

**Врач (дополнительно):**
- Просмотр всех диагнозов пациентов
- Подтверждение диагноза
- Редактирование заключения
- Экспорт отчёта в PDF (включает: генерация через PDFKit)
- Интеграция с MIS (включает: отправка через REST API)

**Администратор (дополнительно):**
- Управление пользователями
- Настройка моделей ML
- Просмотр метрик системы
- Управление политиками безопасности

**ML Engineer:**
- Обновление модели ResNet-50
- Обновление модели BERT
- A/B тестирование моделей
- Мониторинг точности моделей

---

### 2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-activity.html"></iframe>

**Процесс медицинской диагностики:**

1. **Start** - Пациент заходит в систему
2. **Decision: Авторизован?**
   - Нет → Ввод email/пароля → Проверка JWT → Decision: Токен валиден?
   - Да → Токен действителен
3. **Выбор типа диагностики**
4. **Fork (параллельная загрузка):**
   - **Ветка 1: Загрузка изображения**
     - Валидация формата (JPEG/PNG) → Decision: Формат корректен?
     - Проверка размера ≤10MB → Decision: Размер корректен?
     - Сохранение в AWS S3 (AES-256)
     - Сохранение метаданных в PostgreSQL
   - **Ветка 2: Ввод симптомов**
     - Валидация длины ≤1000 символов → Decision: Длина корректна?
     - Сохранение в PostgreSQL
5. **Join** - Отправка задачи в RabbitMQ
6. **Препроцессинг данных**
7. **Fork (параллельный препроцессинг):**
   - **Изображение**: Загрузка из S3 → OpenCV декодирование → Resize 224x224 → Нормализация ImageNet → Тензор float32
   - **Текст**: Токенизация BERT → input_ids + attention_mask → Padding до 128 tokens
8. **Join** - ИИ-анализ через GPU кластер
9. **Fork (параллельный ML inference):**
   - **Изображение**: ResNet-50 → Softmax → Grad-CAM heatmap
   - **Текст**: BERT → Классификация → SHAP объяснения
10. **Join** - Объединение результатов → Топ-3 диагноза
11. **Сохранение**: Redis (TTL=1h) + PostgreSQL
12. **Формирование отчёта**
13. **Fork (параллельная генерация):**
    - PDF через PDFKit (A4 portrait, heatmap, результаты)
    - HTML через Jinja2 (Bootstrap 5, responsive)
14. **Join** - Отправка WebSocket уведомления
15. **Decision: Интеграция с MIS включена?**
    - Да → Отправка в Clinic MIS (REST API, retry 3 раза)
16. **End** - Пациент получает результаты

---

### 3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 1400px; min-height: 1000px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-sequence.html"></iframe>

**Участники:**
- Пациент
- WebUI (React)
- API Gateway (Kong)
- Auth Service (Spring Boot)
- Data Upload Service (Spring Boot)
- AWS S3
- PostgreSQL
- RabbitMQ
- Preprocessing Service (Python)
- ML Inference Service (TensorFlow Serving)
- GPU Cluster (NVIDIA T4)
- Report Service (Node.js)
- Redis Cache
- WebSocket Notifier
- Clinic MIS

**Основные потоки:**

**1. Авторизация:**
- Пациент → WebUI → Gateway → Auth Service → PostgreSQL (SELECT user)
- Auth → BCrypt проверка пароля → Gateway → JWT Token (TTL=15min) → WebUI → Пациент

**2. Загрузка данных:**
- Пациент → WebUI → Gateway (JWT проверка, Rate Limiting 100 req/min)
- Gateway → Upload Service → Валидация (формат + размер)
- Upload → S3 (PUT с AES-256 шифрованием)
- Upload → PostgreSQL (INSERT метаданные)
- Upload → RabbitMQ (PUBLISH message) → ACK → 201 Created

**3. Препроцессинг (параллельно):**
- RabbitMQ → Preprocessing Service
- Preproc → S3 (GET изображение) + PostgreSQL (SELECT симптомы)
- Параллельно: OpenCV (decode, resize, normalize, tensor) | BERT tokenization
- Preproc → RabbitMQ (PUBLISH preprocessed)

**4. ML Inference:**
- RabbitMQ → ML Service → Redis (CHECK cache)
- ML → GPU (gRPC predict): ResNet-50 + BERT параллельно
- GPU → Convolution layers, Batch norm, Pooling → Softmax
- GPU → BERT Attention → Disease classification
- Параллельно: Grad-CAM generation | SHAP explanations
- ML → Redis (SET cache TTL=1h) + PostgreSQL (INSERT diagnosis)
- ML → RabbitMQ (PUBLISH results)

**5. Формирование отчёта:**
- RabbitMQ → Report Service
- Параллельно: PDFKit (PDF) | Jinja2 (HTML Bootstrap 5)
- Report → S3 (PUT /reports/{reportId}.pdf)
- Report → PostgreSQL (UPDATE report_url)
- Report → WebSocket (SEND notification) → Пациент
- Alt: Report → MIS (POST /reports, retry 3x)

**6. Просмотр:**
- Пациент → WebUI → Gateway → Report Service
- Report → Redis (GET cached) → WebUI → Диагноз + heatmap

---

### 4. Class Diagram (Диаграмма классов)

<iframe style="width: 100%; height: 1000px; min-height: 800px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-class.html"></iframe>

**Основные классы:**

**User** (id, email, passwordHash, role, createdAt, isActive)
- Methods: login(), register(), activate()
- Связи: 1 -- 0..* MedicalImage, 1 -- 0..* TextSymptoms, 1 -- 0..* Diagnosis

**UserRole** (enum): PATIENT, DOCTOR, ADMIN, ML_ENGINEER

**MedicalImage** (id, userId, fileName, s3Url, format, sizeBytes, uploadedAt)
- Methods: validate(), getPreprocessed()
- Связи: 1 -- 0..1 Diagnosis

**ImageFormat** (enum): JPEG, PNG

**TextSymptoms** (id, userId, text, language, createdAt)
- Methods: validate(), tokenize()
- Связи: 1 -- 0..1 Diagnosis

**TokenizedText** (inputIds[], attentionMask[], maxLength)
- Methods: toBertInput()

**ImagePreprocessor** (targetSize, mean[], std[])
- Methods: decode(), resize(), normalize(), toTensor()
- Использует: MedicalImage

**TextPreprocessor** (tokenizer, maxLength)
- Methods: tokenize(), pad()
- Использует: TextSymptoms

**ResNet50Model** (version, inputShape[], numClasses, accuracy)
- Methods: predict(), gradCAM()
- Анализирует: MedicalImage

**BERTModel** (version, vocabSize, hiddenSize)
- Methods: encode(), classify(), explain()
- Анализирует: TokenizedText

**Diagnosis** (id, userId, imageId, symptomsId, topDiseases[], confidence, heatmapUrl, explanation, createdAt, confirmedByDoctor)
- Methods: getTopDisease(), confirm()
- Связи: 1 *-- 1..3 Disease, 1 -- 1 Report

**Disease** (name, probability, icd10Code)
- Methods: isHighConfidence()

**Report** (id, diagnosisId, pdfUrl, htmlContent, generatedAt)
- Methods: generatePDF(), generateHTML(), sendToMIS()

**CacheService** (redis, ttl)
- Methods: get(), set(), invalidate()
- Кеширует: Diagnosis

**MessageQueue** (queueName, connection)
- Methods: publish(), consume(), ack()
- Очереди: MedicalImage, TextSymptoms

---

### 5. State Diagram (Диаграмма состояний)

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-state.html"></iframe>

**Состояния обработки медицинского файла:**

1. **[*] → Uploaded** - Файл загружен
   - Субсостояния: ValidatingFormat → ValidatingSize → SavedToS3
   - Переход: → Failed (валидация не прошла)

2. **SavedToS3** - Сохранение в хранилище
   - Субсостояния: EncryptingAES256 → StoringMetadata → QueuedForProcessing
   - Переход: → Queued

3. **Queued** - В очереди
   - Субсостояния: WaitingInRabbitMQ → PickedByConsumer
   - Переход: → Preprocessing

4. **Preprocessing** - Препроцессинг
   - Fork: LoadingFromS3 → DecodingImage | TokenizingText
   - Параллельно: ResizingImage → NormalizingImage → ConvertingToTensor
   - Параллельно: CreatingAttentionMask → PaddingTokens
   - Join → Препроцессинг завершён
   - Переходы: → MLInference | → Failed

5. **MLInference** - ML анализ
   - CheckingCache → ReturningCached (cache hit) | GPUInference (cache miss)
   - GPUInference:
     - Fork: ResNet50Forward + BERTForward
     - ResNet50Forward → ResNet50Softmax + GeneratingGradCAM
     - BERTForward → DiseaseClassification + GeneratingSHAP
     - Join → MergingResults → SelectingTop3 → CachingResults → SavingToPostgreSQL
   - Переходы: → Diagnosed | → Failed

6. **Diagnosed** - Диагноз получен
   - GeneratingReport → Fork (CreatingPDF + CreatingHTML) → Join
   - SendingWebSocketNotification
   - CheckingMISIntegration → SendingToMIS (с retry) | завершение
   - Переход: → Completed

7. **Completed** - Завершено
   - AwaitingDoctorReview → UnderReview → Confirmed | Rejected
   - Переход: → Archived (через 30 дней) → [*]

8. **Failed** - Ошибка
   - LoggingError → NotifyingUser → MovingToDeadLetterQueue → [*]

---

### 6. Component Diagram (Диаграмма компонентов)

<iframe style="width: 100%; height: 1000px; min-height: 800px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-medical-component.html"></iframe>

**Архитектура микросервисов:**

**Frontend Layer:**
- Web Application (React)
- Mobile App (React Native)
- → HTTPS → API Gateway

**API Gateway Layer:**
- Kong Gateway (TLS 1.3, Rate limiting: 100 req/min, CORS)
- Authentication Service (JWT)
- Rate Limiter
- → Routes to Backend Services

**Backend Services:**
- Data Upload Service (Spring Boot) → S3 + PostgreSQL + RabbitMQ
- Preprocessing Service (Python FastAPI) → S3 + RabbitMQ
- ML Inference Service (TensorFlow Serving + gRPC) → GPU + Redis + PostgreSQL
- Report Generation Service (Node.js) → S3 + PostgreSQL + WebSocket + MIS
- User Management Service (Spring Boot) → PostgreSQL + Redis + SMTP
- Notification Service (Node.js WebSocket) → Clients

**ML Infrastructure:**
- ResNet-50 Model v2.3.0 + BERT Model v1.2.0
- GPU Cluster (NVIDIA T4)
- Model Registry (MLflow)

**Data Storage:**
- PostgreSQL (Master-Slave, RTO≤5min, RPO≤1min)
- Redis (Sentinel, 3+ nodes, автоматический failover, TTL=1h)
- MongoDB (Replica Set) - архив старых данных
- AWS S3 (medical-images-raw, AES-256, daily backup)

**Message Queue:**
- RabbitMQ (Clustered 3 nodes, DLQ, persistence)

**Monitoring:**
- ELK Stack (Filebeat → Logstash → Elasticsearch → Kibana)
- Prometheus → Grafana
- Метрики: logs, performance, GPU utilization

**External Services:**
- Clinic MIS (REST API, retry 3x)
- Email Service (SMTP)
- File Scanner (Antivirus)

---

## Источники и стандарты

- UML 2.5 Specification
- Medical Device Software Standards (IEC 62304)
- HIPAA Security Rule
- GDPR Data Protection
- ResNet Paper: [arXiv:1512.03385](https://arxiv.org/abs/1512.03385)
- BERT Paper: [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- Grad-CAM: [arXiv:1610.02391](https://arxiv.org/abs/1610.02391)
- SHAP: [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
