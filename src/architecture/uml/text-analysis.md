# UML Диаграммы: Анализ текста

## Функция 4: Анализ текстовых симптомов (BERT)

Эта функция отвечает за обработку и анализ текстовых симптомов пациентов с использованием BERT (Bidirectional Encoder Representations from Transformers) для классификации заболеваний.

---

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 900px; min-height: 700px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-usecase.html"></iframe>

**Актёры:**
- **ML Service** (система) - автоматическая обработка текстов
- **Врач** (Doctor) - валидация медицинской терминологии
- **ML Engineer** (инженер машинного обучения) - fine-tuning модели

**Основные Use Cases:**

1. **Получить текст симптомов**
   - Первичный актёр: ML Service
   - Предусловия: Текст получен из RabbitMQ
   - Включает: Токенизация симптомов

2. **Токенизация симптомов**
   - Включает: BERT-анализ
   - Может расширяться: Spell-check (коррекция орфографии)

3. **BERT-анализ симптомов**
   - Включает: Классификация заболеваний
   - Обработка через 12 слоёв Transformer

4. **Классификация заболеваний**
   - Включает: Генерация объяснений SHAP
   - Может расширяться: Валидация медицинской терминологии (Врач)

5. **Fine-tuning BERT модели**
   - Первичный актёр: ML Engineer
   - Предусловия: Новые медицинские данные
   - Постусловия: Модель дообучена

6. **Мониторинг точности**
   - Первичный актёр: ML Engineer
   - Включает: BERT-анализ для метрик

**Связи:**
- `<<include>>`: Обязательные зависимости между use cases
- `<<extend>>`: Опциональные расширения функциональности

---

### 2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-activity.html"></iframe>

**Процесс анализа текста:**

1. **Start** - Получить текст симптомов из RabbitMQ
2. **Предобработка текста**
3. **Decision: Есть орфографические ошибки?**
   - Да → Spell-check коррекция
   - Нет → Пропустить
4. **Токенизация BERT** (max_length=128)
5. **Создание** input_ids и attention_mask
6. **Padding** до 128 токенов
7. **Fork** - Параллельная обработка:
   - **Ветка 1: BERT Model**
     - Отправка в TensorFlow Serving
     - Forward pass через BERT (12 layers)
     - Attention mechanism
     - Получение embeddings [CLS]
     - Classification head
     - Softmax activation
     - Вероятности заболеваний
   - **Ветка 2: NER (Named Entity Recognition)**
     - Извлечение медицинских терминов
8. **Join** - Выбор топ-3 диагнозов
9. **Генерация объяснений SHAP** (Token importance scores)
10. **Decision: Есть неизвестные термины?**
    - Да → Запрос валидации у врача + Сохранение для fine-tuning
11. **Fork** - Параллельное сохранение:
    - Redis (TTL=1h)
    - PostgreSQL
    - RabbitMQ (next stage)
12. **End**

**Особенности:**
- Параллельная обработка BERT и NER для оптимизации
- Генерация объяснений (SHAP) для интерпретируемости результатов
- Валидация медицинских терминов врачом при необходимости

---

### 3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 1400px; min-height: 1000px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-sequence.html"></iframe>

**Участники:**
- RabbitMQ - очередь сообщений
- TextAnalysisService - оркестратор
- TextPreprocessor - предобработка текста
- BERTTokenizer (HuggingFace) - токенизация
- TensorFlow Serving - inference сервер
- BERT Model v1.2.0 - нейросеть
- ClassificationHead - классификатор
- SHAP Explainer - генератор объяснений
- Redis - кеш
- PostgreSQL - база данных

**Основной поток взаимодействия:**

1. **Получение сообщения:**
   - RabbitMQ → TextAnalysisService: CONSUME text message

2. **Предобработка:**
   - TextAnalysisService → TextPreprocessor: preprocess(text)
   - Preprocessing: Lowercase + Remove special chars + Spell-check
   - TextPreprocessor → TextAnalysisService: cleaned_text

3. **Токенизация:**
   - TextAnalysisService → BERTTokenizer: tokenize(cleaned_text, max_length=128)
   - Tokenizer: Convert to IDs + Add [CLS]/[SEP] + Create attention_mask + Padding
   - BERTTokenizer → TextAnalysisService: input_ids, attention_mask

4. **Проверка кеша:**
   - TextAnalysisService → Redis: GET cache:text_hash
   - Redis → TextAnalysisService: null (cache miss)

5. **BERT Inference:**
   - TextAnalysisService → TF Serving: gRPC predict(input_ids, attention_mask)
   - TF Serving → BERT Model: forward_pass(tokens)
   - BERT Model: Embedding layer → 12 × Transformer blocks → Self-attention → Layer norm → Extract [CLS]
   - BERT Model → TF Serving: embeddings [768 dim]
   - TF Serving → ClassificationHead: classify(embeddings)
   - ClassificationHead: Linear [768→256] → ReLU → Dropout → Output [256→diseases] → Softmax
   - ClassificationHead → TF Serving: probabilities
   - TF Serving → TextAnalysisService: prediction results

6. **Выбор топ-3 диагнозов**

7. **Генерация объяснений:**
   - TextAnalysisService → SHAP: explain(input_ids, prediction)
   - SHAP: Compute SHAP values + Token importance scores
   - SHAP → TextAnalysisService: explanation JSON

8. **Параллельное сохранение:**
   - par: Redis (SET cache, TTL=1h) | PostgreSQL (INSERT result)

9. **Публикация результата:**
   - TextAnalysisService → RabbitMQ: PUBLISH analysis_complete

---

### 4. Class Diagram (Диаграмма классов)

<iframe style="width: 100%; height: 1000px; min-height: 800px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-class.html"></iframe>

**Основные классы:**

**TextSymptoms** (id, userId, text, language, createdAt)
- Methods: validate(), preprocess(), tokenize()
- Связи: 1 -- 1 TokenizedText

**TokenizedText** (inputIds[], attentionMask[], maxLength=128)
- Methods: toBertInput(), getPadding()
- Связи: 1 -- 1 BERTModel (input to)

**TextPreprocessor** (spellChecker)
- Methods: lowercase(), removeSpecialChars(), correctSpelling(), preprocess()
- Использует: TextSymptoms

**BERTTokenizer** (vocab, vocabSize=30522, maxLength=128)
- Methods: tokenize(), encode(), decode(), addSpecialTokens()
- Производит: TokenizedText

**BERTModel** (version="v1.2.0", numLayers=12, hiddenSize=768, numHeads=12)
- Methods: embeddings(), encoder(), forward()
- Содержит: 1 *-- 1 TransformerEncoder
- Feeds to: 1 -- 1 ClassificationHead

**TransformerEncoder** (numLayers=12, hiddenSize=768)
- Methods: selfAttention(), feedForward(), layerNorm(), encode()

**ClassificationHead** (inputDim=768, hiddenDim=256, dropout=0.1)
- Methods: linear1(), relu(), dropout(), linear2(), softmax()
- Использует: 1 -- 1 DiseaseClassifier

**DiseaseClassifier** (threshold=0.5)
- Methods: classify(), getTopN(), isHighConfidence()

**TextAnalysisResult** (id, symptomsId, topDiseases[], confidence, explanation, createdAt)
- Methods: getTopDisease()
- Содержит: 1 *-- 1..3 Disease, 1 *-- 1 SHAPValues

**Disease** (name, probability, icd10Code)
- Methods: isHighConfidence()

**SHAPExplainer** (model, numSamples=100)
- Methods: explain(), getTokenImportance()
- Анализирует: BERTModel
- Генерирует: SHAPValues

**SHAPValues** (tokenScores, baseValue)
- Methods: getTopTokens(), visualize()

---

### 5. State Diagram (Диаграмма состояний)

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-state.html"></iframe>

**Состояния обработки текстовых симптомов:**

1. **[*] → Queued** - Text symptoms received
   - Субсостояния: WaitingInQueue → PickedByConsumer
   - Переход: → Preprocessing

2. **Preprocessing** - Предобработка
   - Субсостояния: Cleaning → SpellChecking → Tokenizing → CreatingMasks → Padding
   - Переходы: → BERTInference | → Failed

3. **BERTInference** - ML анализ
   - CheckingCache → ReturningCached (cache hit) | RunningBERT (cache miss)
   - **RunningBERT**:
     - EmbeddingLayer → TransformerLayers (12 iterations: SelfAttention → FeedForward → LayerNorm) → ExtractingCLS
   - **Classification**:
     - LinearLayer1 → ReLU → Dropout → LinearLayer2 → Softmax → SelectingTopN
   - **ExplainingResults**:
     - ComputingSHAP → TokenImportance
   - Переходы: → Analyzed | → Failed

4. **Analyzed** - Результаты получены
   - ValidatingTerminology → NeedsReview (unknown terms) | Caching (all valid)
   - **NeedsReview**: WaitingForDoctor → ReviewedByDoctor
   - **Caching**: SavingToRedis → SavingToPostgreSQL → PublishingResult
   - Переход: → Completed

5. **Completed** - Завершено
   - AvailableForRetrieval → RetrievedByUser | Expired (TTL=1h)
   - Переход: → [*]

6. **Failed** - Ошибка
   - LoggingError → NotifyingSystem → MovingToDLQ
   - Переход: → [*]

**Ключевые параметры:**
- BERT Model: v1.2.0, 12 layers, 768 hidden size, 12 attention heads, 30,522 vocab
- Cache TTL: 1 hour (Redis), Persistent: PostgreSQL

---

### 6. Component Diagram (Диаграмма компонентов)

<iframe style="width: 100%; height: 1000px; min-height: 800px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../img/diagrams/uml/uml-text-analysis-component.html"></iframe>

**Архитектура компонентов:**

**Text Analysis Components:**
- MessageConsumer (RabbitMQ) → TextAnalysisOrchestrator
- TextAnalysisOrchestrator → TextPreprocessor → BERTTokenizer (HuggingFace)
- TextAnalysisOrchestrator → CacheService (Redis)
- TextAnalysisOrchestrator → TensorFlow Serving (gRPC)
- TensorFlow Serving → BERT Model v1.2.0 → ClassificationHead
- TextAnalysisOrchestrator → SHAP Explainer → BERT Model
- TextAnalysisOrchestrator → DatabaseService (PostgreSQL)
- TextAnalysisOrchestrator → MessagePublisher (RabbitMQ)

**External Systems:**
- RabbitMQ Cluster (3 nodes)
- Redis Sentinel (TTL=1h, LRU eviction, 3 nodes, automatic failover)
- PostgreSQL Master (Master-Slave replication, indexes: user_id, created_at)
- Monitoring (Prometheus)

**BERT Model спецификация:**
- Architecture: BERT base
- Layers: 12 Transformer blocks
- Hidden size: 768
- Attention heads: 12
- Parameters: 110M
- Fine-tuned on medical corpus

**TensorFlow Serving спецификация:**
- Protocol: gRPC
- Batch size: 8
- Max latency: 1s (P95)
- Model versioning: A/B testing

---

## Связь с другими диаграммами

- **IDEF0 A0**: Функция "Диагностика заболеваний" - анализ текста является частью общего процесса
- **IDEF0 A3**: Функция "ИИ-анализ" - текстовый анализ через BERT
- **IDEF3 P3**: Процесс "Классификация диагноза" включает анализ текста
- **DFD P3**: Поток данных "ИИ-анализ" обрабатывает токенизированные симптомы
- **Требования**: FR-3.2 (Анализ текста BERT), NFR-1.2 (Время обработки ≤1с), NFR-5.2 (Точность ≥90%)

## Источники и стандарты

- BERT Paper: [arXiv:1810.04805](https://arxiv.org/abs/1810.04805)
- SHAP: [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
- HuggingFace Transformers: https://huggingface.co/docs/transformers
- TensorFlow Serving: https://www.tensorflow.org/tfx/guide/serving
- UML 2.5 Specification
