# UML Диаграммы: Обработка изображений

## Функция 3: Обработка медицинских изображений (ResNet-50)

### 1. Use Case Diagram (Диаграмма вариантов использования)

```mermaid
graph TB
    subgraph "Actors"
        MLService[🤖 ML Service]
        MLEngineer[👨‍💻 ML Engineer]
        GPUCluster[⚡ GPU Cluster]
    end
    
    subgraph "Use Cases"
        Preprocess[Препроцессинг изображения]
        Classify[Классификация изображения ResNet-50]
        UpdateModel[Обновление модели]
        Monitor[Мониторинг производительности]
    end
    
    MLService --> Preprocess
    MLService --> Classify
    MLEngineer --> UpdateModel
    MLEngineer --> Monitor
    GPUCluster --> Preprocess
    GPUCluster --> Classify
    Monitor -.->|extends| Preprocess
    Monitor -.->|extends| Classify
    Monitor -.->|extends| UpdateModel
    
    style MLService fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style MLEngineer fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style GPUCluster fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Preprocess fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style Classify fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UpdateModel fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style Monitor fill:#9966ff,stroke:#7744cc,stroke-width:2px,color:#fff
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

```mermaid
flowchart TD
    Start([Начало: Message from RabbitMQ])
    
    A[Получить fileId из сообщения]
    B[Загрузить изображение из S3]
    C{Изображение в кэше?}
    D[Получить результат из Redis]
    E[Вернуть результат]
    
    F[Декодирование изображения OpenCV]
    G[Проверка размерности]
    H{Размер корректен?}
    I[Изменить размер до 224x224]
    J[Нормализация пикселей]
    K[Преобразование в тензор CHW]
    L[Добавление batch dimension]
    
    M[Отправка в TensorFlow Serving gRPC]
    N[Ожидание GPU inference ≤2 сек]
    O[Получение вероятностей классов]
    P[Сохранение в Redis TTL=1h]
    Q[Отправка результата в очередь]
    End([Конец])
    
    Start --> A
    A --> B
    B --> C
    C -->|Да| D
    D --> E
    E --> End
    C -->|Нет| F
    
    F --> G
    F --> H
    G --> I
    H -->|Нет| I
    H -->|Да| J
    I --> J
    J --> K
    K --> L
    L --> M
    
    M --> N
    M --> O
    N --> P
    O --> P
    P --> Q
    Q --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:3px
    style C fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style H fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style F fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style M fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style P fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
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

```mermaid
sequenceDiagram
    participant R as RabbitMQ
    participant M as MLInferenceService
    participant S as S3Client
    participant P as ImagePreprocessor
    participant T as TensorFlowServing
    participant N as ResNetModel
    participant G as GradCAM
    participant C as Redis
    participant DB as PostgreSQL
    participant W as WebSocketNotifier
    
    R->>M: msg {fileId}
    M->>S: download(fileId)
    S->>S: GET from S3
    S-->>M: bytes
    M->>P: preprocess(image)
    P->>P: decode image
    P->>P: resize 224x224
    P->>P: normalize
    P->>P: to_tensor
    P-->>M: tensor
    M->>T: predict(tensor)
    T->>N: gRPC call forward_pass
    N-->>T: logits
    T->>T: softmax
    T-->>M: probabilities [0.95, 0.03, 0.02, ...]
    M->>G: generate_heatmap(tensor, probabilities)
    G-->>M: heatmap_image
    M->>C: cache(results)
    C->>C: SET
    C-->>M: OK
    M->>DB: save(results, heatmap)
    DB->>DB: INSERT
    DB-->>M: OK
    M->>W: notify(userId, results)
    W->>W: send message
    W-->>M: ACK
```

**Ключевые моменты:**
- gRPC для высокопроизводительного inference
- Grad-CAM для визуализации решений модели
- Параллельное сохранение в Redis и PostgreSQL

---

### 4. Class Diagram (Диаграмма классов)

```mermaid
classDiagram
    class MLInferenceService {
        -RabbitMQ messageConsumer
        -ImagePreprocessor preprocessor
        -TensorFlowClient tfClient
        -PostProcessor postprocessor
        -CacheService cacheService
        +processMessage(msg) void
        +runInference(file) Result
        +saveResults(result) void
    }
    
    class ImagePreprocessor {
        -int[] targetSize
        -float[] mean
        -float[] std
        +decode(bytes) Image
        +resize(image) Image
        +normalize(image) Tensor
        +preprocess(image) Tensor
    }
    
    class TensorFlowClient {
        -String serverUrl
        -String modelName
        -gRPCChannel channel
        +predict(tensor) Tensor
        +batchPredict(tensors) Tensor[]
        +getModelMetadata() Meta
    }
    
    class Tensor {
        -int[] shape
        -DataType dtype
        -ByteBuffer data
        +reshape(shape) Tensor
        +toArray() float[]
        +getShape() int[]
    }
    
    class ResNetModel {
        -int[] inputShape
        -int numClasses
        -String weights
        +forward(tensor) Logits
        +getLayer(name) Layer
        +loadWeights(path) void
    }
    
    class PostProcessor {
        -Map~int,String~ classLabels
        -float threshold
        +softmax(logits) Probs
        +topK(probs, k) List
        +formatResult(probs) Result
    }
    
    class GradCAM {
        -ResNetModel model
        -String targetLayer
        +generate(tensor, class) Image
        +computeGradients() Tensor
        +applyColormap(heatmap) Image
    }
    
    class InferenceResult {
        -UUID fileId
        -List~Prediction~ predictions
        -String heatmapUrl
        -Duration inferenceTime
        -Timestamp timestamp
        +getTopPrediction() Prediction
    }
    
    MLInferenceService --> ImagePreprocessor : uses
    MLInferenceService --> TensorFlowClient : uses
    MLInferenceService --> PostProcessor : uses
    ImagePreprocessor --> Tensor : produces
    TensorFlowClient --> ResNetModel : uses
    PostProcessor --> InferenceResult : creates
    GradCAM --> ResNetModel : uses
```

**Паттерны:**
- **Strategy:** ImagePreprocessor (разные стратегии препроцессинга)
- **Factory:** TensorFlowClient (создание gRPC каналов)
- **Repository:** CacheService (абстракция над Redis)

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Image Inference Task

```mermaid
stateDiagram-v2
    direction TB
    
    [*] --> Queued : Message received
    Queued --> Downloading : consumer picks up
    Downloading --> Preprocessing : file downloaded
    Preprocessing --> Inferencing : preprocessing done
    Inferencing --> Postprocessing : inference complete
    Postprocessing --> Caching : results ready
    Caching --> Completed : saved to cache
    Completed --> [*] : task finished
    
    Queued --> Failed : download error
    Downloading --> Failed : S3 error
    Preprocessing --> Failed : format error
    Inferencing --> Failed : model error
    Postprocessing --> Failed : processing error
    Caching --> Failed : cache error
    
    Failed --> Queued : retry
    Failed --> [*] : max retries exceeded
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

```mermaid
graph TB
    subgraph "ML Inference Service"
        MC[MessageConsumer<br/>RabbitMQ]
        IO[InferenceOrchestrator<br/>Pipeline Controller]
        PC[Pipeline Components]
        
        subgraph "Pipeline Components"
            IP[ImagePreprocessor<br/>OpenCV]
            TC[TensorFlowClient<br/>gRPC Client]
            PP[PostProcessor<br/>Results Handler]
            GC[GradCAMGenerator<br/>Visualization]
        end
    end
    
    subgraph "External Services"
        TFS[TensorFlow Serving<br/>gRPC Server<br/>ResNet-50 Model]
        OCV[OpenCV Library<br/>C++ Backend]
        S3[AWS S3<br/>Image Storage]
        REDIS[Redis<br/>Cache Layer]
        PG[PostgreSQL<br/>Metadata DB]
    end
    
    subgraph "Infrastructure"
        GPU[GPU Cluster<br/>NVIDIA Tesla V100]
        K8S[Kubernetes<br/>Container Orchestration]
    end
    
    MC --> IO
    IO --> PC
    PC --> IP
    PC --> TC
    PC --> PP
    PC --> GC
    
    IP --> OCV
    TC --> TFS
    TFS --> GPU
    GPU --> K8S
    
    IP --> S3
    PP --> REDIS
    PP --> PG
    
    style MC fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style IO fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style TFS fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style GPU fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style S3 fill:#ff9900,stroke:#cc7700,stroke-width:2px
    style REDIS fill:#dc382d,stroke:#a02822,stroke-width:2px,color:#fff
    style PG fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
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

