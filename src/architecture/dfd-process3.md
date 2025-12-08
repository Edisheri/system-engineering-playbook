# 3.1.4. DFD: Процесс P3 — ИИ-анализ

## Диаграмма потоков данных P3

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P3.drawio"></iframe>

## Декомпозиция процесса P3 (Image Processing Pipeline)

Подробная декомпозиция обработки изображений:

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=DFD%20P3%20Decomposition&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P3_DECOMPOSITION.drawio"></iframe>

### Подпроцессы:

**3.1 Загрузка изображения:**
- Получение сообщения из RabbitMQ (fileId, s3Url)
- Чтение бинарных данных из S3

**3.2 Декодирование:**
- OpenCV: cv2.imdecode()
- Проверка целостности изображения
- Декодирование JPEG/PNG в numpy array

**3.3 Изменение размера:**
- OpenCV: cv2.resize()
- Целевой размер: 224x224 (ResNet-50 input)
- Метод: INTER_AREA для downsampling

**3.4 Нормализация:**
- Приведение к float32
- Нормализация по ImageNet: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
- Диапазон: [0, 1]

**3.5 Конверт в тензор:**
- Преобразование numpy → TensorFlow tensor
- Добавление batch dimension: (1, 224, 224, 3)
- Кэширование в Redis (TTL=10 min)

## Потоки данных

| Поток | Источник | Назначение | Данные | Формат |
|-------|----------|------------|--------|--------|
| 3.1 | RabbitMQ | P3 | {fileId, userId, s3Url, fileType} | JSON/AMQP |
| 3.2 | D1 (AWS S3) | P3 | Binary file data | JPEG/PNG/TXT |
| 3.3 | P3 | TensorFlow Serving | Image tensor (224x224x3) | gRPC protobuf |
| 3.4 | P3 | TensorFlow Serving | Text tokens {input_ids, attention_mask} | gRPC protobuf |
| 3.5 | TensorFlow Serving | P3 | Image predictions (softmax) | gRPC protobuf |
| 3.6 | TensorFlow Serving | P3 | Text predictions (softmax) | gRPC protobuf |
| 3.7 | P3 | D3 (Redis) | {fileId, predictions, timestamp} | JSON, TTL=1h |
| 3.8 | P3 | D2 (PostgreSQL) | Results data | SQL INSERT |
| 3.9 | P3 | Пациент | {taskId, predictions, status: "completed"} | JSON/HTTP 200 |
| 3.10 | P3 | Пациент | {error: "inference_failed", details: [...]} | JSON/HTTP 500 |

## Хранилища данных

**D1: AWS S3** (источник файлов)
- Доступ: P3 читает файлы для обработки

**D2: PostgreSQL** (таблица results)
- Доступ: P3 записывает результаты диагностики
```sql
CREATE TABLE results (
    id UUID PRIMARY KEY,
    file_id UUID REFERENCES medical_data(id),
    user_id BIGINT,
    image_predictions JSONB,
    text_predictions JSONB,
    combined_diagnosis JSONB,
    processing_time FLOAT,
    created_at TIMESTAMP
);
```

**D3: Redis** (кэш результатов)
- Key format: `result:{fileId}`
- Value: JSON с предсказаниями
- TTL: 1 час

## Обработка ошибок

**Поток ошибки inference (3.10):**
- Источник: P3 (после ошибки TensorFlow Serving или GPU)
- Назначение: Пациент
- Данные: {error: "inference_failed", code: "GPU_TIMEOUT" | "MODEL_UNAVAILABLE" | "PROCESSING_ERROR", message: "..."}
- Формат: JSON/HTTP 500 Internal Server Error

**Условия ошибок:**
- GPU timeout (> 5 секунд) → GPU_TIMEOUT
- TensorFlow Serving недоступен → MODEL_UNAVAILABLE
- Ошибка обработки изображения/текста → PROCESSING_ERROR
- Ошибка сохранения результатов → STORAGE_ERROR

## Структура результатов

**Успешный результат:**
```json
{
  "taskId": "uuid",
  "status": "completed",
  "imagePredictions": [
    {"disease": "Pneumonia", "probability": 0.952, "confidence": "high"}
  ],
  "textPredictions": [
    {"disease": "Flu", "probability": 0.782, "confidence": "medium"}
  ],
  "combinedDiagnosis": {
    "primary": "Pneumonia",
    "probability": 0.867,
    "confidence": "high"
  },
  "processingTime": 2.3,
  "modelVersions": {
    "resnet": "v2.3",
    "bert": "v1.1"
  }
}
```

**Результат с ошибкой:**
```json
{
  "taskId": "uuid",
  "status": "error",
  "error": {
    "code": "GPU_TIMEOUT",
    "message": "GPU inference timeout after 5 seconds",
    "partialResults": {
  "textPredictions": [
    {"disease": "Flu", "probability": 0.782}
      ]
    }
  }
}
```

