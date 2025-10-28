# UML Диаграммы: Обработка изображений

## Функция 3: Обработка медицинских изображений (ResNet-50)

### 1. Use Case Diagram (Диаграмма вариантов использования)

![Диаграмма](/img/diagrams/uml-image-processing-1.png)

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

![Диаграмма](/img/diagrams/uml-image-processing-2.png)

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

![Диаграмма](/img/diagrams/uml-image-processing-3.png)

**Ключевые моменты:**
- gRPC для высокопроизводительного inference
- Grad-CAM для визуализации решений модели
- Параллельное сохранение в Redis и PostgreSQL

---

### 4. Class Diagram (Диаграмма классов)

![Диаграмма](/img/diagrams/uml-image-processing-4.png)

**Паттерны:**
- **Strategy:** ImagePreprocessor (разные стратегии препроцессинга)
- **Factory:** TensorFlowClient (создание gRPC каналов)
- **Repository:** CacheService (абстракция над Redis)

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** Image Inference Task

![Диаграмма](/img/diagrams/uml-image-processing-5.png)

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

![Component Diagram](/img/diagrams/uml-image-processing-6.png)

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

