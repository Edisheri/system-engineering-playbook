# UML Диаграммы: Обработка изображений

## Функция 3: Обработка медицинских изображений (ResNet-50)

### 1. Use Case Diagram (Диаграмма вариантов использования)

```plantuml
left to right direction

actor "ML Service" as MLService
actor "ML Engineer" as MLEngineer
actor "GPU Cluster" as GPU

MLService --> (Препроцессинг изображения)
MLService --> (Классификация изображения\nResNet-50)
MLEngineer --> (Обновление модели)
MLEngineer --> (Мониторинг производительности)
GPU --> (GPU Inference)

(Классификация изображения\nResNet-50) ..> (Препроцессинг изображения): <<include>>
(Классификация изображения\nResNet-50) ..> (GPU Inference): <<include>>
(Классификация изображения\nResNet-50) ..> (Генерация Grad-CAM): <<include>>
(Классификация изображения\nResNet-50) <.. (Кэширование результатов): <<extend>>
(Мониторинг производительности) <.. (Классификация изображения\nResNet-50): <<extend>>

note right of (Классификация изображения\nResNet-50)
  Обязательные шаги:
  - Препроцессинг изображения
  - GPU Inference
  - Генерация Grad-CAM
end note

note right of (Кэширование результатов)
  Опциональный шаг:
  Выполняется только если
  результат не найден в кэше
end note

```

**Актёры:**
- **ML Service** (система)
- **ML Engineer** (инженер машинного обучения)
- **GPU Cluster** (инфраструктура)

**Варианты использования:**
1. **Препроцессинг изображения**
   - Первичный актёр: ML Service
   - Предусловия: Изображение загружено в S3
   - Постусловия: Тензор готов для inference
   
2. **Классификация изображения (ResNet-50)**
   - Первичный актёр: ML Service
   - Предусловия: Тензор подготовлен
   - Постусловия: Результаты классификации получены
   
3. **Обновление модели**
   - Первичный актёр: ML Engineer
   - Предусловия: Новая версия модели обучена
   - Постусловия: Модель развёрнута в TensorFlow Serving

4. **Мониторинг производительности**
   - Первичный актёр: ML Engineer
   - Связь: `<<extend>>` для всех сценариев

**Связи:**
- `<<include>>`: Классификация включает препроцессинг
- `<<extend>>`: Кэширование расширяет классификацию

---

### 2. Activity Diagram (Диаграмма активностей)

```plantuml
start

:Получение сообщения из RabbitMQ;

:Загрузка изображения из S3;

if (Изображение в кэше?) then (Да)
  :Получить результат из Redis;
  :Вернуть результат;
  stop
else (Нет)
  :Декодирование изображения OpenCV;
  :Проверка размерности;
  
  if (Размер корректен?) then (Нет)
    :Изменить размер до 224x224;
  endif
  
  :Нормализация пикселей;
  :Преобразование в тензор CHW;
  :Добавление batch dimension;
  :Отправка в TensorFlow Serving gRPC;
  :Ожидание GPU inference ≤2 сек;
  :Получение вероятностей классов;
  :Постпроцессинг: выбор топ-3 класса;
  :Генерация heatmap Grad-CAM;
  
  fork
    :Сохранение в Redis TTL=1h;
  fork again
    :Сохранение в PostgreSQL + heatmap URL;
  end fork
  
  :Отправка уведомления в WebSocket;
  stop
endif

```

**Особенности:**
- Параллельное сохранение для оптимизации
- Кэширование для повторных запросов

---

### 3. Sequence Diagram (Диаграмма последовательности)

**Участники:**
- RabbitMQ
- MLInferenceService
- S3Client
- ImagePreprocessor
- TensorFlowServing
- ResNetModel
- GradCAM
- Redis
- PostgreSQL
- WebSocketNotifier

```plantuml
participant "RabbitMQ" as Queue
participant "MLInferenceService" as Service
participant "ImagePreprocessor" as Preproc
participant "TensorFlowClient" as TF
participant "ResNetModel" as Model
participant "PostProcessor" as Post
participant "Redis" as Cache
database "PostgreSQL" as DB

Queue -> Service: Message(fileId)
activate Service

Service -> Cache: get(fileId)
activate Cache
Cache --> Service: null
deactivate Cache

alt Кэш пуст
    Service -> Preproc: loadFromS3(fileId)
    activate Preproc
    Preproc -> Preproc: Загрузка из S3
    Preproc --> Service: Image
    deactivate Preproc
    
    Service -> Preproc: preprocess(image)
    activate Preproc
    Preproc -> Preproc: Декодирование JPEG/PNG
    Preproc -> Preproc: Изменение размера (224x224)
    Preproc -> Preproc: Нормализация [0,1]
    Preproc --> Service: Tensor(224x224x3)
    deactivate Preproc
    
    Service -> TF: predict(tensor)
    activate TF
    TF -> Model: forward(tensor)
    activate Model
    Model -> Model: Convolution layers
    Model -> Model: Batch normalization
    Model -> Model: ReLU activation
    Model -> Model: Global average pooling
    Model -> Model: Dense layer
    Model --> TF: Logits
    deactivate Model
    TF -> TF: Softmax
    TF --> Service: Probabilities
    deactivate TF
    
    par Параллельная обработка
        Service -> Post: topK(probs, 3)
        activate Post
        Post --> Service: Top3Results
        deactivate Post
    and
        Service -> Post: generateGradCAM()
        activate Post
        Post -> Model: Получение градиентов
        Post -> Post: Взвешенная сумма активаций
        Post --> Service: Heatmap
        deactivate Post
    end
    
    Service -> Cache: set(fileId, results, TTL=1h)
    activate Cache
    Cache --> Service: OK
    deactivate Cache
    
    Service -> DB: saveResults(results, heatmap)
    activate DB
    DB -> DB: INSERT INTO results
    DB --> Service: OK
    deactivate DB
else Кэш найден
    Cache -> Service: Results
    Service -> Service: Возврат из кэша
end

Service -> Queue: notify(userId, results)
activate Queue
Queue --> Service: ACK
deactivate Queue

deactivate Service

```

**Ключевые моменты:**
- gRPC для высокопроизводительного inference
- Grad-CAM для визуализации решений модели
- Параллельное сохранение в Redis и PostgreSQL

---

### 4. Class Diagram (Диаграмма классов)

```plantuml
class MLInferenceService {
  -messageConsumer: RabbitMQ
  -preprocessor: ImagePreprocessor
  -tfClient: TensorFlowClient
  -postProcessor: PostProcessor
  -cacheService: CacheService
  +processMessage(msg): void
  +runInference(file): Result
}

class ImagePreprocessor {
  -targetSize: int[]
  -mean: float[]
  -std: float[]
  +decode(bytes): Image
  +resize(image): Image
  +normalize(image): Tensor
}

class TensorFlowClient {
  -serverUrl: String
  -modelName: String
  -channel: gRPCChannel
  +predict(tensor): Tensor
}

class PostProcessor {
  -classLabels: Map
  -threshold: float
  +softmax(logits): Probs
  +topK(probs, k): List
  +generateGradCAM(): Image
}

class InferenceResult {
  -fileId: UUID
  -predictions: List<Prediction>
  -heatmapUrl: String
  -inferenceTime: Duration
  +getTopPrediction(): Prediction
}

MLInferenceService --> ImagePreprocessor
MLInferenceService --> TensorFlowClient
MLInferenceService --> PostProcessor
PostProcessor --> InferenceResult

```

**Паттерны:**
- **Strategy:** ImagePreprocessor (разные стратегии препроцессинга)
- **Factory:** TensorFlowClient (создание gRPC каналов)
- **Repository:** CacheService (абстракция над Redis)

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Image Inference Task

```plantuml
[*] --> Queued: Message received
Queued --> Downloading: consumer picks up
Downloading --> Preprocessing: file downloaded
Preprocessing --> Inferencing: preprocessing done
Inferencing --> Postprocessing: inference complete
Postprocessing --> Caching: results ready
Caching --> Completed: saved to cache
Completed --> [*]: task finished

Queued --> Failed: download error
Downloading --> Failed: S3 error
Preprocessing --> Failed: format error
Inferencing --> Failed: model error
Postprocessing --> Failed: processing error
Caching --> Failed: cache error

Failed --> Queued: retry
Failed --> [*]: max retries exceeded

```

**Состояния:**
1. **Queued:** Задача в RabbitMQ
2. **Downloading:** Загрузка изображения из S3
3. **Preprocessing:** Подготовка тензора
4. **Inferencing:** GPU inference (ResNet-50)
5. **PostProcessing:** Обработка результатов
6. **Generating Heatmap:** Grad-CAM визуализация
7. **Caching:** Сохранение в Redis
8. **Saving:** Сохранение в PostgreSQL
9. **Completed:** Задача завершена
10. **Failed:** Ошибка на любом этапе

**Переходы с таймаутами:**
- Downloading → Failed (если S3 недоступен > 30 сек)
- Inferencing → Failed (если GPU timeout > 5 сек)

---

### 6. Component Diagram (Диаграмма компонентов)

```plantuml
package "ML Inference Service" {
  [MessageConsumer\nRabbitMQ] as Consumer
  [InferenceOrchestrator] as Orchestrator
  [ImagePreprocessor\nOpenCV] as Preproc
  [TensorFlowClient\ngRPC Client] as TF
  [PostProcessor] as Post
  [GradCAMGenerator] as GradCAM
}

package "External Services" {
  [TensorFlow Serving\ngRPC Server\nResNet-50] as TFServing
  [AWS S3] as S3
  [Redis\nCache] as Redis
  database "PostgreSQL" as DB
}

package "Infrastructure" {
  [GPU Cluster\nNVIDIA Tesla V100] as GPU
}

Consumer --> Orchestrator
Orchestrator --> Preproc
Orchestrator --> TF
Orchestrator --> Post
Orchestrator --> GradCAM
Preproc --> S3
TF --> TFServing
TFServing --> GPU
Post --> Redis
Post --> DB

```

**Интерфейсы:**
- `gRPC`: TensorFlow Serving API
- `AMQP`: RabbitMQ message protocol
- `Redis Protocol`: Cache communication
- `JDBC`: PostgreSQL connection

---

## Источники

- «Deep Learning» Ian Goodfellow
- [ResNet Paper](https://arxiv.org/abs/1512.03385)
- [Grad-CAM](https://arxiv.org/abs/1610.02391)
- [TensorFlow Serving Guide](https://www.tensorflow.org/tfx/guide/serving)

