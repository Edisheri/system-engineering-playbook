# UML Диаграммы: Обработка изображений

## Функция 3: Обработка медицинских изображений (ResNet-50)

Эта функция отвечает за препроцессинг изображений и классификацию заболеваний с использованием свёрточной нейросети ResNet-50.

---

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe style="width: 100%; height: 900px; min-height: 700px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-image-processing-usecase.html"></iframe>

**Актёры:**
- **ML Service** - автоматическая обработка изображений
- **ML Engineer** - обновление моделей и мониторинг
- **GPU Cluster** - вычислительная инфраструктура

**Основные Use Cases:**

1. **Получить изображение из очереди**
   - Первичный актёр: ML Service
   - Включает: Загрузить из S3

2. **Декодирование через OpenCV**
   - Включает: Изменение размера до 224×224
   - Включает: Нормализация ImageNet

3. **Конвертация в тензор float32**
   - Включает: Классификация через ResNet-50

4. **Классификация через ResNet-50**
   - Первичный актёр: ML Service + GPU Cluster
   - Включает: Генерация Grad-CAM heatmap
   - Включает: Кэширование результатов Redis
   - Включает: Сохранение в PostgreSQL
   - Может расширяться: Мониторинг точности ≥95%

5. **Обновление модели**
   - Первичный актёр: ML Engineer
   - Предусловия: Новая версия обучена
   - Постусловия: Модель развёрнута

6. **Мониторинг точности ≥95%**
   - Первичный актёр: ML Engineer
   - Расширяет: Классификация

---

### 2. Activity Diagram (Диаграмма активностей)

<iframe style="width: 100%; height: 1200px; min-height: 900px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-image-processing-activity.html"></iframe>

**Процесс обработки изображений:**

1. **Start** - Получить сообщение из RabbitMQ
2. **Извлечь** fileId и s3Url
3. **Загрузить** изображение из S3
4. **Проверка Redis кеша** → Decision: Cache hit?
   - Да → Вернуть результаты из кеша → Stop
   - Нет → Продолжить обработку
5. **Декодирование через OpenCV** (cv2.imdecode)
6. **Изменение размера** до 224×224
7. **Нормализация ImageNet**:
   - mean=[0.485, 0.456, 0.406]
   - std=[0.229, 0.224, 0.225]
8. **Конвертация в тензор float32**
9. **Отправка в TensorFlow Serving** (gRPC)
10. **ResNet-50 Forward Pass**:
    - Convolution layers
    - Batch normalization
    - ReLU activations
    - Global average pooling
11. **Softmax activation**
12. **Получение вероятностей классов**
13. **Выбор топ-3 диагнозов**
14. **Fork** - Параллельная обработка:
    - Генерация Grad-CAM heatmap + Визуализация
    - Сохранение в Redis (TTL=1h)
    - Сохранение в PostgreSQL
    - Отправка в RabbitMQ (next stage)
15. **Decision**: Точность < 95%?
    - Да → Уведомление ML Engineer + Требуется fine-tuning
16. **Stop**

---

### 3. Sequence Diagram (Диаграмма последовательности)

<iframe style="width: 100%; height: 1400px; min-height: 1000px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="../../img/diagrams/uml/uml-image-processing-sequence.html"></iframe>

**Участники:**
- RabbitMQ
- MLInferenceService
- AWS S3
- Redis
- ImagePreprocessor (OpenCV)
- TensorFlow Serving (gRPC)
- ResNet-50 v2.3.0
- Grad-CAM
- PostgreSQL

**Основной поток:**

1. **Получение сообщения:**
   - RabbitMQ → MLInferenceService: CONSUME image_message

2. **Проверка кеша:**
   - MLInferenceService → Redis: GET cache:fileId
   - Redis → MLInferenceService: null (cache miss)

3. **Загрузка изображения:**
   - MLInferenceService → S3: GET /medical-images-raw/{fileId}
   - S3 → MLInferenceService: Image binary (JPEG/PNG)

4. **Препроцессинг:**
   - MLInferenceService → ImagePreprocessor: preprocess(image_bytes)
   - Preprocessor:
     - cv2.imdecode()
     - cv2.resize((224, 224))
     - Normalize ImageNet mean/std
     - np.transpose((2, 0, 1))
     - Convert to float32
   - Preprocessor → MLInferenceService: tensor [1, 3, 224, 224]

5. **ResNet-50 Inference:**
   - MLInferenceService → TF Serving: gRPC predict(tensor)
   - TF Serving → ResNet-50: forward_pass(tensor)
   - ResNet-50:
     - Conv1 + BN + ReLU
     - Max Pooling
     - Layer1 (64 channels)
     - Layer2 (128 channels)
     - Layer3 (256 channels)
     - Layer4 (512 channels)
     - Global Average Pooling
     - Fully Connected
     - Softmax
   - ResNet-50 → TF Serving: logits + probabilities
   - TF Serving → MLInferenceService: prediction results

6. **Выбор топ-3 диагнозов**

7. **Генерация объяснений:**
   - MLInferenceService → Grad-CAM: generate_heatmap(tensor, class_idx)
   - Grad-CAM:
     - Compute gradients
     - Get feature maps
     - Weight × feature maps
     - ReLU + Normalize
   - Grad-CAM → MLInferenceService: heatmap PNG

8. **Параллельное сохранение** (par):
   - MLInferenceService → Redis: SET cache:fileId results (TTL=1h)
   - MLInferenceService → PostgreSQL: INSERT INTO image_analysis_results

9. **Публикация результата:**
   - MLInferenceService → RabbitMQ: PUBLISH analysis_complete

---

## Связь с другими диаграммами

- **IDEF0 A0**: Функция "Диагностика заболеваний" - обработка изображений ключевая часть
- **IDEF0 A2**: Функция "Препроцессинг данных" - подготовка изображений
- **IDEF0 A3**: Функция "ИИ-анализ" - классификация через ResNet-50
- **IDEF3 P3**: Процесс "Классификация диагноза"
- **DFD P3**: Поток данных "ИИ-анализ" обрабатывает тензоры изображений
- **Требования**: FR-3.1 (ResNet-50 классификация), NFR-1.1 (Время обработки ≤2с), NFR-5.1 (Точность ≥95%)

## Технические детали

**Препроцессинг:**
- Размер входа: 224×224×3 (RGB)
- Тип данных: float32
- Нормализация: ImageNet statistics
- Инструмент: OpenCV

**ResNet-50 Model:**
- Версия: v2.3.0
- Предобучена: ImageNet
- Fine-tuned: CheXNet (медицинский датасет)
- Точность: ≥95%
- Параметры: 25.6M

**Grad-CAM:**
- Class Activation Mapping
- Визуализация активаций последнего свёрточного слоя
- Формат: PNG heatmap
- Применение: Интерпретируемость результатов

**Производительность:**
- GPU: NVIDIA T4 или A100
- Batch size: 1 (real-time inference)
- Latency: ≤2 секунды (P95)
- TensorFlow Serving: gRPC protocol

**Кэширование:**
- Redis TTL: 1 час
- Ключ: cache:fileId
- Eviction: LRU
