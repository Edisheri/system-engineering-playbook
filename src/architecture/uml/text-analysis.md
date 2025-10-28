# UML Диаграммы: Анализ текста

## Функция 4: Анализ текстовых симптомов (BERT)

### 1. Use Case Diagram (Диаграмма вариантов использования)

```mermaid
graph TB
    subgraph "Actors"
        MLService[🤖 ML Service]
        Doctor[👨‍⚕️ Врач]
        MLEngineer[👨‍💻 ML Engineer]
    end
    
    subgraph "Use Cases"
        Tokenize[Токенизация симптомов]
        BERTAnalysis[BERT-анализ симптомов]
        Validate[Валидация медицинской терминологии]
        FineTune[Fine-tuning BERT модели]
    end
    
    MLService --> Tokenize
    MLService --> BERTAnalysis
    Doctor --> Validate
    MLEngineer --> FineTune
    Validate -.->|extends| BERTAnalysis
    
    style MLService fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style Doctor fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style MLEngineer fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style Tokenize fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style BERTAnalysis fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style Validate fill:#9966ff,stroke:#7744cc,stroke-width:2px,color:#fff
    style FineTune fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
```

**Актёры:**
- **ML Service** (система)
- **Врач** (Doctor)
- **ML Engineer** (инженер машинного обучения)

**Варианты использования:**
1. **Токенизация симптомов**
   - Первичный актёр: ML Service
   - Предусловия: Текст симптомов получен
   - Постусловия: Токены готовы для BERT
   
2. **BERT-анализ симптомов**
   - Первичный актёр: ML Service
   - Предусловия: Токены подготовлены
   - Постусловия: Вероятности заболеваний получены
   
3. **Валидация медицинской терминологии**
   - Первичный актёр: Врач
   - Связь: `<<extend>>` для анализа
   
4. **Fine-tuning BERT модели**
   - Первичный актёр: ML Engineer
   - Предусловия: Новые медицинские данные
   - Постусловия: Модель дообучена

**Связи:**
- `<<include>>`: Анализ включает токенизацию
- `<<extend>>`: Spell-check расширяет токенизацию

---

### 2. Activity Diagram (Диаграмма активностей)

```mermaid
flowchart TD
    Start([Начало: Text from RabbitMQ])
    
    A[Получить symptom_text из сообщения]
    B{Текст на английском?}
    C[Перевод на английский Google Translate API]
    D[Очистка текста lowercase, удаление спецсимволов]
    E[Проверка орфографии медицинских терминов]
    F{Термины корректны?}
    G[Коррекция через медицинский словарь]
    H[Токенизация через BERT Tokenizer]
    I[Добавление специальных токенов CLS, SEP]
    J[Padding до max_length=128]
    K[Создание attention_mask]
    L[Преобразование в input_ids]
    
    M[BERT Encoding]
    N[Named Entity Recognition]
    O[Получение embeddings]
    P[Классификация симптомов]
    Q[Извлечение медицинских сущностей]
    R[Объединение результатов]
    S[Сохранение в Redis TTL=1h]
    T[Отправка результата в очередь]
    End([Конец])
    
    Start --> A
    A --> B
    B -->|Нет| C
    C --> D
    B -->|Да| D
    D --> E
    E --> F
    F -->|Нет| G
    G --> H
    F -->|Да| H
    H --> I
    I --> J
    J --> K
    K --> L
    
    L --> M
    L --> N
    M --> O
    N --> Q
    O --> P
    Q --> R
    P --> R
    R --> S
    S --> T
    T --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:3px
    style B fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style F fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style H fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style M fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style S fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
```mermaid
flowchart LR
    Start([Начало: Text from RabbitMQ])
    
    A[Получить symptom_text из сообщения]
    B{Текст на английском?}
    C[Перевод на английский Google Translate API]
    D[Очистка текста lowercase, удаление спецсимволов]
    E[Проверка орфографии медицинских терминов]
    F{Термины корректны?}
    G[Коррекция через медицинский словарь]
    H[Токенизация через BERT Tokenizer]
    I[Добавление специальных токенов CLS, SEP]
    J[Padding до max_length=128]
    K[Создание attention_mask]
    L[Преобразование в input_ids]
    
    M[BERT Encoding]
    N[Named Entity Recognition]
    O[Получение embeddings]
    P[Классификация через Dense Layer]
    Q[Softmax activation вероятности]
    R[Сопоставление с базой заболеваний]
    S[Ранжирование топ-5 диагнозов]
    T[Генерация объяснений LIME/SHAP]
    U[Сохранение в Redis TTL=1h]
    V[Сохранение в PostgreSQL + объяснения]
    W[Отправка уведомления врачу]
    End([Конец])
    
    Start --> A
    A --> B
    B -->|Нет| C
    C --> D
    B -->|Да| D
    D --> E
    E --> F
    F -->|Нет| G
    G --> H
    F -->|Да| H
    H --> I
    I --> J
    J --> K
    K --> L
    
    L --> M
    L --> N
    M --> O
    N --> T
    O --> P
    P --> Q
    Q --> R
    R --> S
    S --> T
    T --> U
    T --> V
    U --> W
    V --> W
    W --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:3px
    style B fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style F fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style H fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style M fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style U fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style V fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
```

**Особенности:**
- Параллельная обработка BERT и NER
- Генерация объяснений для интерпретируемости

---

### 3. Sequence Diagram (Диаграмма последовательности)

**Участники:**
- RabbitMQ
- TextAnalysisService
- TextPreprocessor
- BERTTokenizer
- TensorFlowServing
- BERTModel
- ClassificationHead
- DiseaseDatabase
- ExplainabilityService
- Redis
- PostgreSQL

```mermaid
sequenceDiagram
    participant R as RabbitMQ
    participant T as TextAnalysisService
    participant P as TextPreprocessor
    participant TK as BERTTokenizer
    participant TF as TensorFlowServing
    participant B as BERTModel
    participant C as ClassificationHead
    participant D as DiseaseDatabase
    participant E as ExplainabilityService
    participant REDIS as Redis
    participant PG as PostgreSQL
    
    R->>T: msg {text}
    T->>P: clean(text)
    P->>P: lowercase, remove special chars
    P->>P: spell check
    P-->>T: cleaned_text
    T->>TK: tokenize(cleaned_text)
    TK->>TK: convert to tokens
    TK->>TK: add [CLS], [SEP]
    TK->>TK: padding to 128
    TK->>TK: create attention_mask
    TK-->>T: token_ids, attention_mask
    T->>TF: predict(token_ids, attention_mask)
    TF->>B: gRPC call
    B->>B: BERT encoding
    B->>C: embeddings
    C->>C: classification
    C-->>TF: logits
    TF-->>T: probabilities
    T->>D: match_diseases(probabilities)
    D-->>T: disease_matches
    T->>E: generate_explanations(text, probabilities)
    E->>E: LIME/SHAP analysis
    E-->>T: explanations
    T->>REDIS: cache(results)
    REDIS-->>T: OK
    T->>PG: save(results, explanations)
    PG-->>T: OK
```
   |          |            |            |          |         |       |         |          |        |        |
   |          |<--tokens-----------------|         |         |       |         |          |        |        |
   |          |  {input_ids, attention_mask}       |         |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--encode(tokens)-------------------->|        |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |            |            |     [gRPC call]    |       |         |          |        |        |
   |          |            |            |          |-------->|       |         |          |        |        |
   |          |            |            |          | forward_pass   |         |          |        |        |
   |          |            |            |          |<--------|       |         |          |        |        |
   |          |            |            |      [768-dim embeddings] |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |<--embeddings------------|          |         |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--classify(embeddings)-------------------------->|    |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |            |            |          |    [Dense(768 → 256)]    |          |        |        |
   |          |            |            |          |    [ReLU]                |          |        |        |
   |          |            |            |          |    [Dropout(0.3)]        |          |        |        |
   |          |            |            |          |    [Dense(256 → num_classes)]     |        |        |
   |          |            |            |          |    [Softmax]             |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |<--probabilities---------|          |         |<------|         |          |        |        |
   |          |  [0.45, 0.32, 0.15, ...]           |         |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--lookup_diseases(top_k=5)--------------------|------>|         |          |        |        |
   |          |            |            |          |         |       |  SELECT |          |        |        |
   |          |<--disease_names---------|          |         |       |<--------|          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--generate_explanation(text, probs)----------|-------|---------|--------->|        |        |
   |          |            |            |          |         |       |         |  SHAP   |        |        |
   |          |<--explanation_json------|          |         |       |         |<---------|        |        |
   |          |  {key_symptoms: [...], impact: [...]}        |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |            |   [Parallel save]     |         |       |         |          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--cache(results)------------------------------------------->|    |          |        |        |
   |          |            |            |          |         |       | SET     |          |        |        |
   |          |            |            |          |         |       |<--------|          |        |        |
   |          |            |            |          |         |       |         |          |        |        |
   |          |--save(results, explanation)------------------------------>|    |          |------->|        |
   |          |            |            |          |         |       |         |   INSERT |        |        |
   |          |            |            |          |         |       |         |          |<-------|        |
   |          |            |            |          |         |       |         |          |        |        |
   |<--ACK----|            |            |          |         |       |         |          |        |        |
```

**Ключевые особенности:**
- Использование pre-trained BERT с fine-tuned classification head
- SHAP для объяснения предсказаний
- Параллельное сохранение результатов

---

### 4. Class Diagram (Диаграмма классов)

```
┌─────────────────────────────────┐
│   TextAnalysisService           │
├─────────────────────────────────┤
│ - preprocessor: TextPreprocessor│
│ - tokenizer: BERTTokenizer      │
│ - bertClient: TensorFlowClient  │
│ - classifier: Classifier        │
│ - explainer: Explainability     │
├─────────────────────────────────┤
│ + analyzeSymptoms(text): Result │
│ + processMessage(msg): void     │
└─────────────────────────────────┘
           │ uses
           ↓
┌─────────────────────────────────┐         ┌─────────────────────────────┐
│   TextPreprocessor              │         │   BERTTokenizer             │
├─────────────────────────────────┤         ├─────────────────────────────┤
│ - medicalDict: Dictionary       │         │ - vocab: Vocabulary         │
│ - translator: Translator        │         │ - maxLength: int = 128      │
│ - spellChecker: SpellChecker    │         │ - padToken: String = "[PAD]"│
├─────────────────────────────────┤         ├─────────────────────────────┤
│ + clean(text): String           │         │ + tokenize(text): Tokens    │
│ + normalize(text): String       │         │ + encode(tokens): InputIds  │
│ + spellCheck(text): String      │         │ + decode(ids): String       │
│ + translate(text, lang): String │         │ + createAttentionMask(): [] │
└─────────────────────────────────┘         └─────────────────────────────┘

┌─────────────────────────────────┐
│        Tokens                   │
├─────────────────────────────────┤
│ - inputIds: int[]               │
│ - attentionMask: int[]          │
│ - tokenTypeIds: int[]           │
├─────────────────────────────────┤
│ + getInputIds(): int[]          │
│ + getPaddingLength(): int       │
│ + toBatch(): BatchTokens        │
└─────────────────────────────────┘

┌─────────────────────────────────┐         ┌─────────────────────────────┐
│   TensorFlowClient              │────────>│     BERTModel               │
├─────────────────────────────────┤         ├─────────────────────────────┤
│ - serverUrl: String             │         │ - hiddenSize: int = 768     │
│ - modelName: String = "bert"    │         │ - numLayers: int = 12       │
│ - timeout: Duration             │         │ - numAttentionHeads: int=12 │
├─────────────────────────────────┤         ├─────────────────────────────┤
│ + encode(tokens): Embeddings    │         │ + forward(ids, mask): Emb   │
│ + getEmbeddings(text): Vector   │         │ + getPooledOutput(): Tensor │
└─────────────────────────────────┘         │ + getSequenceOutput(): Tensor│
                                            └─────────────────────────────┘

┌─────────────────────────────────┐
│   ClassificationHead            │
├─────────────────────────────────┤
│ - dense1: Dense(768 → 256)      │
│ - dropout: Dropout(0.3)         │
│ - dense2: Dense(256 → classes)  │
│ - activation: Softmax           │
├─────────────────────────────────┤
│ + classify(embeddings): Probs   │
│ + train(X, y): void             │
│ + predict(embeddings): Probs    │
└─────────────────────────────────┘

┌─────────────────────────────────┐         ┌─────────────────────────────┐
│   DiseaseClassifier             │────────>│   DiseaseDatabase           │
├─────────────────────────────────┤         ├─────────────────────────────┤
│ - classificationHead: Head      │         │ - connection: PostgreSQL    │
│ - diseaseDB: DiseaseDatabase    │         ├─────────────────────────────┤
│ - threshold: float = 0.1        │         │ + getDiseaseByClass(id): Disease│
├─────────────────────────────────┤         │ + searchBySymptoms(symp): []│
│ + classify(embeddings): Results │         │ + getAllDiseases(): List    │
│ + topK(probs, k): List          │         └─────────────────────────────┘
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   ExplainabilityService         │
├─────────────────────────────────┤
│ - shapExplainer: SHAPExplainer  │
│ - limeExplainer: LIMEExplainer  │
├─────────────────────────────────┤
│ + explain(text, pred): Explanation│
│ + getFeatureImportance(): Map   │
│ + visualize(): Image            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│    AnalysisResult               │
├─────────────────────────────────┤
│ - id: UUID                      │
│ - predictions: List<Disease>    │
│ - confidenceScores: float[]     │
│ - explanation: Explanation      │
│ - processedText: String         │
│ - timestamp: Timestamp          │
├─────────────────────────────────┤
│ + getTopPrediction(): Disease   │
│ + toJSON(): String              │
│ + isHighConfidence(): boolean   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        Disease                  │
├─────────────────────────────────┤
│ - id: int                       │
│ - name: String                  │
│ - icd10Code: String             │
│ - description: String           │
│ - symptoms: List<String>        │
│ - probability: float            │
├─────────────────────────────────┤
│ + toString(): String            │
│ + matchesSymptoms(symp): bool   │
└─────────────────────────────────┘
```

**Паттерны:**
- **Pipeline:** TextPreprocessor → Tokenizer → BERT → Classifier
- **Strategy:** Разные стратегии объяснений (SHAP/LIME)
- **Repository:** DiseaseDatabase абстракция

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Text Analysis Task

```
          [Text received]
                 ↓
           ┌──────────┐
      ●───>│  Queued  │
           │(В очереди)│
           └──────────┘
                 │ consumer picks up
                 ↓
           ┌──────────────┐
           │Preprocessing │
           │(Очистка)     │
           └──────────────┘
                 │
            ┌────┼────┐
            │    │    │
    invalid │    │    │ valid
        ┌───┘    │    └───┐
        │        │        │
        ↓        ↓        ↓
   ┌────────┐ ┌──────────────┐
   │Invalid │ │ Tokenizing   │
   │(Ошибка)│ │(Токенизация) │
   └────────┘ └──────────────┘
                     │
                     │ tokens ready
                     ↓
               ┌──────────────┐
               │   Encoding   │
               │(BERT кодирование)│
               └──────────────┘
                     │
                ┌────┼────┐
                │    │    │
       timeout  │    │    │ success
            ┌───┘    │    └───┐
            │        │        │
            ↓        ↓        ↓
       ┌────────┐ ┌──────────────┐
       │Timeout │ │Classifying   │
       │(Таймаут)│ │(Классификация)│
       └────────┘ └──────────────┘
                       │
                       │ classified
                       ↓
                 ┌──────────────┐
                 │  Explaining  │
                 │(Генерация объяснений)│
                 └──────────────┘
                       │
                  ┌────┼────┐
                  │    │    │
                  │    │    │
                  ↓    ↓    ↓
            ┌──────────────┐ ┌──────────────┐
            │   Caching    │ │   Saving     │
            │(Кэширование) │ │ (Сохранение) │
            └──────────────┘ └──────────────┘
                  │                │
                  └────────┬───────┘
                           ↓
                     ┌──────────┐
                     │Completed │
                     │(Готово)  │
                     └──────────┘
                           │
                           ↓
                           ●
```

**Состояния:**
1. **Queued:** Задача в RabbitMQ
2. **Preprocessing:** Очистка и нормализация текста
3. **Tokenizing:** Токенизация через BERT Tokenizer
4. **Encoding:** Получение embeddings от BERT
5. **Classifying:** Классификация заболеваний
6. **Explaining:** Генерация объяснений (SHAP)
7. **Caching:** Сохранение в Redis
8. **Saving:** Сохранение в PostgreSQL
9. **Completed:** Задача завершена
10. **Invalid/Timeout:** Ошибки

**Переходы:**
- `invalid text` → Invalid
- `BERT timeout` → Timeout (retry with exponential backoff)
- `low confidence` → Request human review

---

### 6. Component Diagram (Диаграмма компонентов)

```
┌─────────────────────────────────────────────────────────────┐
│           Text Analysis Service                             │
│                                                             │
│  ┌──────────────────────┐       ┌──────────────────┐       │
│  │                      │       │                  │       │
│  │  MessageConsumer     │──────>│AnalysisOrchestrator     │
│  │   (RabbitMQ)         │triggers                  │       │
│  └──────────────────────┘       └──────────────────┘       │
│                                           │                 │
│                                           │ orchestrates    │
│                                           ↓                 │
│                         ┌──────────────────────────────┐    │
│                         │  NLP Pipeline               │    │
│                         │                              │    │
│                         │  - TextPreprocessor          │    │
│                         │  - BERTTokenizer             │    │
│                         │  - TensorFlowClient          │    │
│                         │  - DiseaseClassifier         │    │
│                         │  - ExplainabilityService     │    │
│                         └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                    │                        │
                    │ uses                   │ uses
                    ↓                        ↓
     ┌────────────────────────┐   ┌─────────────────────┐
     │                        │   │                     │
     │  TensorFlow Serving    │   │   HuggingFace       │
     │    (gRPC Server)       │   │   Transformers      │
     │                        │   │   (Python Library)  │
     │  - BERT Model          │   │                     │
     │  - bert-base-uncased   │   │  - Tokenizers       │
     │  + Classification Head │   │  - Model loading    │
     └────────────────────────┘   └─────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         Medical Knowledge Components                        │
│                                                             │
│  ┌──────────────────────┐       ┌──────────────────┐       │
│  │                      │       │                  │       │
│  │ DiseaseDatabase      │       │ MedicalDictionary│       │
│  │ (PostgreSQL)         │       │ (JSON/Redis)     │       │
│  └──────────────────────┘       └──────────────────┘       │
│           │                               │                 │
│           │ queries                       │ validates       │
│           ↓                               ↓                 │
│  ┌──────────────────────────────────────────────────┐       │
│  │         Disease Ontology                         │       │
│  │                                                  │       │
│  │  - ICD-10 codes                                  │       │
│  │  - Symptom mappings                              │       │
│  │  - Disease relationships                         │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           Explainability Components                         │
│                                                             │
│  ┌──────────────────────┐       ┌──────────────────┐       │
│  │                      │       │                  │       │
│  │  SHAPExplainer       │       │  LIMEExplainer   │       │
│  │  (Python Library)    │       │  (Python Library)│       │
│  └──────────────────────┘       └──────────────────┘       │
│           │                               │                 │
│           │ generates                     │ generates       │
│           ↓                               ↓                 │
│  ┌──────────────────────────────────────────────────┐       │
│  │         Explanation Visualizer                   │       │
│  │                                                  │       │
│  │  - Feature importance plots                      │       │
│  │  - Token highlighting                            │       │
│  │  - Confidence intervals                          │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Storage & Cache                                │
│                                                             │
│  ┌──────────────────┐           ┌──────────────────┐       │
│  │                  │           │                  │       │
│  │  CacheService    │           │ ResultRepository │       │
│  │   (Redis)        │           │  (PostgreSQL)    │       │
│  └──────────────────┘           └──────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

**Интерфейсы:**
- `gRPC`: BERT model API
- `REST API`: Disease database queries
- `AMQP`: RabbitMQ messaging
- `Python API`: HuggingFace transformers

**Внешние библиотеки:**
- HuggingFace Transformers (BERT)
- SHAP (explainability)
- LIME (local explanations)
- SpaCy (NER для медицинских терминов)

---

## Источники

- [BERT Paper](https://arxiv.org/abs/1810.04805)
- [BioBERT для медицины](https://arxiv.org/abs/1901.08746)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- «Natural Language Processing with Transformers» Lewis Tunstall

