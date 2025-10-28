# UML Диаграммы: Анализ текста

## Функция 4: Анализ текстовых симптомов (BERT)

### 1. Use Case Diagram (Диаграмма вариантов использования)

![Диаграмма](/img/diagrams/uml-text-analysis-1.png)

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

![Диаграмма](/img/diagrams/uml-text-analysis-2.png)

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

![Диаграмма](/img/diagrams/uml-text-analysis-3.png)

**Ключевые особенности:**
- Использование pre-trained BERT с fine-tuned classification head
- SHAP для объяснения предсказаний
- Параллельное сохранение результатов

---

### 4. Class Diagram (Диаграмма классов)

![Диаграмма](/img/diagrams/uml-text-analysis-4.png)

**Паттерны:**
- **Pipeline:** TextPreprocessor → Tokenizer → BERT → Classifier
- **Strategy:** Разные стратегии объяснений (SHAP/LIME)
- **Repository:** DiseaseDatabase абстракция

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Text Analysis Task

![Диаграмма](/img/diagrams/uml-text-analysis-5.png)

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

```mermaid
graph TB
    subgraph "Text Analysis Service"
        MC[MessageConsumer<br/>RabbitMQ]
        AO[AnalysisOrchestrator<br/>Pipeline Controller]
        NLP[NLP Pipeline]
        
        subgraph "NLP Pipeline"
            TP[TextPreprocessor<br/>Clean & Normalize]
            BT[BERTTokenizer<br/>Tokenization]
            TC[TensorFlowClient<br/>gRPC Client]
            DC[DiseaseClassifier<br/>Classification]
            ES[ExplainabilityService<br/>SHAP/LIME]
        end
    end
    
    subgraph "External Services"
        TFS[TensorFlow Serving<br/>gRPC Server<br/>BERT Model]
        HF[HuggingFace<br/>Transformers<br/>Python Library]
        DD[DiseaseDatabase<br/>PostgreSQL]
        REDIS[Redis<br/>Cache Layer]
    end
    
    subgraph "Infrastructure"
        GPU[GPU Cluster<br/>NVIDIA Tesla V100]
        K8S[Kubernetes<br/>Container Orchestration]
    end
    
    MC --> AO
    AO --> NLP
    NLP --> TP
    NLP --> BT
    NLP --> TC
    NLP --> DC
    NLP --> ES
    
    TC --> TFS
    TFS --> GPU
    GPU --> K8S
    BT --> HF
    
    DC --> DD
    ES --> REDIS
    
    style MC fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style AO fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style TFS fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style GPU fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style DD fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style REDIS fill:#dc382d,stroke:#a02822,stroke-width:2px,color:#fff
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

