# UML Диаграммы: Анализ текста

## Функция 4: Анализ текстовых симптомов (BERT)

### 1. Use Case Diagram (Диаграмма вариантов использования)

```plantuml
left to right direction

actor "ML Service" as MLService
actor Врач
actor "ML Engineer" as MLEngineer

MLService --> (Токенизация симптомов)
MLService --> (BERT-анализ симптомов)
Врач --> (Валидация медицинской
терминологии)
MLEngineer --> (Fine-tuning BERT модели)

(BERT-анализ симптомов) ..> (Токенизация симптомов): <<include>>
(BERT-анализ симптомов) ..> (Генерация объяснений): <<include>>
(Токенизация симптомов) <.. (Spell-check): <<extend>>
(BERT-анализ симптомов) <.. (Валидация медицинской
терминологии): <<extend>>

note right of (BERT-анализ симптомов)
  Обязательные шаги:
  - Токенизация симптомов
  - Генерация объяснений
end note

note right of (Spell-check)
  Опциональный шаг:
  Выполняется только если
  обнаружены орфографические
  ошибки
end note
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

```plantuml
start

:Получить symptom_text из сообщения;

if (Текст на английском?) then (Нет)
  :Перевод на английский Google Translate API;
endif

:Очистка текста lowercase, удаление спецсимволов;
:Проверка орфографии медицинских терминов;

if (Термины корректны?) then (Нет)
  :Коррекция через медицинский словарь;
endif

:Токенизация через BERT Tokenizer;
:Добавление специальных токенов CLS, SEP;
:Padding до max_length=128;
:Создание attention_mask;
:Преобразование в input_ids;

fork
  :BERT Encoding;
  :Получение embeddings;
  :Классификация через Dense Layer;
  :Softmax activation вероятности;
fork again
  :Named Entity Recognition;
  :Извлечение медицинских сущностей;
end fork

:Сопоставление с базой заболеваний;
:Ранжирование топ-5 диагнозов;
:Генерация объяснений LIME/SHAP;

fork
  :Сохранение в Redis TTL=1h;
fork again
  :Сохранение в PostgreSQL + объяснения;
end fork

:Отправка уведомления врачу;
stop
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

```plantuml
participant "RabbitMQ" as Queue
participant "TextAnalysisService" as Service
participant "TextPreprocessor" as Preproc
participant "BERTTokenizer" as Tokenizer
participant "TensorFlowClient" as TF
participant "BERTModel" as BERT
participant "DiseaseClassifier" as Classifier
participant "SHAPExplainer" as SHAP
participant "Redis" as Cache
database "PostgreSQL" as DB

Queue -> Service: Message(symptom_text)
activate Service

Service -> Preproc: clean(text)
activate Preproc
Preproc -> Preproc: Удаление спецсимволов
Preproc -> Preproc: Нормализация пробелов
Preproc --> Service: CleanedText
deactivate Preproc

Service -> Preproc: spellCheck(text)
activate Preproc
Preproc -> Preproc: Проверка орфографии
Preproc -> Preproc: Автокоррекция
Preproc --> Service: CorrectedText
deactivate Preproc

Service -> Tokenizer: tokenize(text)
activate Tokenizer
Tokenizer -> Tokenizer: Разбиение на токены
Tokenizer -> Tokenizer: Добавление [CLS] и [SEP]
Tokenizer --> Service: Tokens
deactivate Tokenizer

Service -> TF: encode(tokens)
activate TF
TF -> BERT: forward(tokens)
activate BERT
BERT -> BERT: Token embeddings
BERT -> BERT: Position embeddings
BERT -> BERT: Segment embeddings
BERT -> BERT: Transformer layers (12)
BERT -> BERT: Pooler layer
BERT --> TF: Embeddings(768-dim)
deactivate BERT
TF --> Service: Embeddings
deactivate TF

Service -> Classifier: classify(embeddings)
activate Classifier
Classifier -> Classifier: Dense layer
Classifier -> Classifier: Softmax
Classifier --> Service: Probabilities
deactivate Classifier

par Параллельная обработка
    Service -> Classifier: topK(probs, 5)
    activate Classifier
    Classifier --> Service: Top5Diseases
    deactivate Classifier
and
    Service -> SHAP: explain(text, probs)
    activate SHAP
    SHAP -> BERT: Получение внимания
    SHAP -> SHAP: Вычисление SHAP values
    SHAP --> Service: Explanation
    deactivate SHAP
end

Service -> Cache: set(key, results, TTL=1h)
activate Cache
Cache --> Service: OK
deactivate Cache

Service -> DB: saveResults(results, explanation)
activate DB
DB -> DB: INSERT INTO text_results
DB --> Service: OK
deactivate DB

Service -> Queue: notify(doctorId, results)
activate Queue
Queue --> Service: ACK
deactivate Queue

deactivate Service
```

**Ключевые особенности:**
- Использование pre-trained BERT с fine-tuned classification head
- SHAP для объяснения предсказаний
- Параллельное сохранение результатов

---

### 4. Class Diagram (Диаграмма классов)

```plantuml
class TextAnalysisService {
  -preprocessor: TextPreprocessor
  -tokenizer: BERTTokenizer
  -bertClient: TensorFlowClient
  -classifier: DiseaseClassifier
  -explainer: ExplainabilityService
  +analyzeSymptoms(text): Result
}

class TextPreprocessor {
  -medicalDict: Dictionary
  -translator: Translator
  -spellChecker: SpellChecker
  +clean(text): String
  +normalize(text): String
  +spellCheck(text): String
  +translate(text, lang): String
}

class BERTTokenizer {
  -vocab: Vocabulary
  -maxLength: int
  +tokenize(text): Tokens
  +encode(tokens): InputIds
}

class TensorFlowClient {
  -serverUrl: String
  -modelName: String
  +encode(tokens): Embeddings
}

class DiseaseClassifier {
  -classificationHead: ClassificationHead
  -diseaseDB: DiseaseDatabase
  +classify(embeddings): Results
  +topK(probs, k): List
}

class ExplainabilityService {
  -shapExplainer: SHAPExplainer
  -limeExplainer: LIMEExplainer
  +explain(text, pred): Explanation
}

TextAnalysisService --> TextPreprocessor
TextAnalysisService --> BERTTokenizer
TextAnalysisService --> TensorFlowClient
TextAnalysisService --> DiseaseClassifier
TextAnalysisService --> ExplainabilityService
```

**Паттерны:**
- **Pipeline:** TextPreprocessor → Tokenizer → BERT → Classifier
- **Strategy:** Разные стратегии объяснений (SHAP/LIME)
- **Repository:** DiseaseDatabase абстракция

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Text Analysis Task

```plantuml
[*] --> Queued: Text received
Queued --> Preprocessing: consumer picks up
Preprocessing --> Tokenizing: preprocessing done
Tokenizing --> Encoding: tokens ready
Encoding --> Classifying: embeddings ready
Classifying --> Explaining: classified
Explaining --> Caching: explanation ready
Caching --> Completed: saved
Completed --> [*]: task finished

Preprocessing --> Invalid: invalid text
Tokenizing --> Timeout: BERT timeout
Encoding --> Timeout: timeout
Classifying --> Timeout: timeout
Timeout --> Queued: retry
Timeout --> [*]: max retries
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

```plantuml
package "Text Analysis Service" {
  [MessageConsumer
RabbitMQ] as Consumer
  [AnalysisOrchestrator] as Orchestrator
  [TextPreprocessor] as Preproc
  [BERTTokenizer] as Tokenizer
  [TensorFlowClient] as TF
  [DiseaseClassifier] as Classifier
  [ExplainabilityService] as Explain
}

package "External Services" {
  [TensorFlow Serving
gRPC Server
BERT Model] as TFServing
  [HuggingFace
Transformers] as HF
  [SHAP Library] as SHAP
}

package "Storage" {
  [Redis
Cache] as Redis
  database "PostgreSQL
Disease DB" as DB
}

Consumer --> Orchestrator
Orchestrator --> Preproc
Orchestrator --> Tokenizer
Orchestrator --> TF
Orchestrator --> Classifier
Orchestrator --> Explain
Tokenizer --> HF
TF --> TFServing
Classifier --> DB
Explain --> SHAP
Orchestrator --> Redis
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

