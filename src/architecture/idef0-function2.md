# 3.1.2. IDEF0: Функция A2 — Препроцессинг данных

## Диаграмма функции A2

```mermaid
flowchart TB
    subgraph Inputs["Входы (I)"]
        I1["I1: Сообщения из RabbitMQ (fileId, s3Url, fileType)"]
        I2["I2: Файлы из S3 (бинарные данные)"]
    end
    
    subgraph Controls["Управление (C)"]
        C1["C1: Параметры нормализации"]
        C2["C2: Правила токенизации (BERT vocab)"]
        C3["C3: Правила изменения размера"]
    end
    
    subgraph Function["Функция A2"]
        AA2["Препроцессинг<br/><br/>A2"]
    end
    
    subgraph Outputs["Выходы (O)"]
        O1["O1: Тензоры изображений (224x224x3, float32)"]
        O2["O2: Токены BERT (input_ids, attention_mask)"]
        O3["O3: Метаданные препроцессинга"]
    end
    
    subgraph Mechanisms["Механизмы (M)"]
        M1["M1: OpenCV (декодирование, изменение размера)"]
        M2["M2: HuggingFace Tokenizer"]
        M3["M3: NumPy/TensorFlow"]
    end
    
    I1 --> AA2
    I2 --> AA2
    C1 --> AA2
    C2 --> AA2
    C3 --> AA2
    AA2 --> O1
    AA2 --> O2
    AA2 --> O3
    M1 -.-> AA2
    M2 -.-> AA2
    M3 -.-> AA2
    
    style AA2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style I1 fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style I2 fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style O1 fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style O2 fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style O3 fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style C1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style C2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style C3 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style M1 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style M2 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style M3 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
```


## Описание функции A2: Препроцессинг данных

### Назначение
Подготовка медицинских изображений и текстовых данных для обработки моделями машинного обучения.

### Входы (Inputs)
1. **Сырые изображения из S3**
   - Формат: JPEG/PNG
   - Размер: Произвольный (до 10 МБ)
   - Цветовое пространство: RGB

2. **Текст симптомов**
   - Формат: JSON/Plain text
   - Язык: Русский/Английский
   - Длина: До 1000 символов

### Управление (Control)
1. **Параметры нормализации**
   - Mean: [0.485, 0.456, 0.406] (ImageNet)
   - Std: [0.229, 0.224, 0.225]
   - Range: [0, 1]

2. **Правила токенизации**
   - Vocabulary: BERT base uncased
   - Max length: 128 tokens
   - Padding: right
   - Truncation: enabled

3. **Стандарты размера**
   - ResNet-50 input: 224×224×3
   - Interpolation: BILINEAR
   - Aspect ratio: preserved with padding

### Механизмы (Mechanisms)
1. **OpenCV (Image processing)**
   - Версия: 4.5+
   - Функции: resize, normalize, cvtColor
   - Backend: OpenCL (GPU acceleration)

2. **HuggingFace Tokenizer**
   - Model: bert-base-uncased
   - Fast tokenizer: Rust-based
   - Special tokens: [CLS], [SEP], [PAD]

3. **NumPy Arrays**
   - Dtype: float32
   - Memory layout: C-contiguous
   - SIMD optimization

4. **TensorFlow Preprocessing**
   - tf.image.resize
   - tf.keras.preprocessing
   - Batch processing support

### Выходы (Outputs)
1. **Тензоры изображений**
   - Shape: (1, 224, 224, 3)
   - Dtype: float32
   - Normalized: [0, 1]

2. **Токены BERT**
   - input_ids: [batch_size, 128]
   - attention_mask: [batch_size, 128]
   - token_type_ids: [batch_size, 128]

3. **Нормализованные данные**
   - JSON metadata
   - Processing timestamp
   - Validation flags

## Алгоритм препроцессинга изображений

```python
def preprocess_image(image_bytes):
    # 1. Decode image
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 2. Resize to 224x224
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_LINEAR)
    
    # 3. Normalize to [0, 1]
    image = image.astype(np.float32) / 255.0
    
    # 4. Apply ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = (image - mean) / std
    
    # 5. Add batch dimension
    image = np.expand_dims(image, axis=0)
    
    return image
```

## Алгоритм препроцессинга текста

```python
def preprocess_text(text):
    # 1. Clean text
    text = text.lower().strip()
    
    # 2. Tokenize
    tokens = tokenizer(
        text,
        max_length=128,
        padding='max_length',
        truncation=True,
        return_tensors='tf'
    )
    
    # 3. Extract components
    input_ids = tokens['input_ids']
    attention_mask = tokens['attention_mask']
    
    return {
        'input_ids': input_ids,
        'attention_mask': attention_mask
    }
```

## Метрики производительности

| Метрика | Целевое значение | Текущее |
|---------|------------------|---------|
| Image preprocessing | < 50 ms | 35 ms |
| Text tokenization | < 10 ms | 7 ms |
| Memory usage | < 500 MB | 380 MB |
| Batch throughput | ≥ 50 samples/sec | 65 samples/sec |

## Источники
- OpenCV Documentation
- HuggingFace Tokenizers
- TensorFlow Image Preprocessing
- ImageNet Statistics

