# 3.1.3. IDEF3: Процесс P3 — GPU-обработка данных

## Диаграмма процесса P3

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/IDEF3_P3.drawio"></iframe>

## Описание процесса P3

### Участники
- **ML Inference Service** — основной сервис обработки
- **RabbitMQ** — очередь сообщений
- **AWS S3** — источник файлов
- **TensorFlow Serving** — ML inference сервер
- **GPU Cluster** — вычислительные ресурсы
- **Redis** — кэш результатов
- **PostgreSQL** — постоянное хранилище

### Временные связи

| Событие | Последующее событие | Условие | Задержка |
|---------|---------------------|---------|----------|
| E1 → E2 | Сообщение получено | RabbitMQ ACK | 10 мс |
| E2 → E3 | Файл загружен из S3 | S3 GET успешен | 200-500 мс |
| E3 → E4 | Препроцессинг изображения | OpenCV обработка | 50-100 мс |
| E3 → E5 | Препроцессинг текста | BERT Tokenizer | 20-50 мс |
| E4 → E6 | ResNet-50 inference | GPU inference | 30-450 мс |
| E5 → E7 | BERT inference | GPU inference | 75-890 мс |
| E6 → E8 | Агрегация результатов | Оба завершены (AND) | 10 мс |
| E7 → E8 | Агрегация результатов | Оба завершены (AND) | 10 мс |
| E8 → E9 | Сохранение в Redis | Redis SET | 5-15 мс |
| E8 → E10 | Сохранение в PostgreSQL | SQL INSERT | 50-120 мс |
| E9 → E11 | Результаты готовы | Оба сохранены (AND) | 0 мс |
| E10 → E11 | Результаты готовы | Оба сохранены (AND) | 0 мс |

### Точки синхронизации
- **После E3**: Разветвление на обработку изображений и текста (OR junction)
- **После E6 и E7**: Синхронизация перед агрегацией (AND junction)
- **После E8**: Параллельное сохранение в Redis и PostgreSQL (AND junction)

### UOB (Unit of Behavior)

**UOB-1: Получение сообщения из RabbitMQ**
- Input: Message из очереди ml_inference
- Process: RabbitMQ CONSUME, ACK
- Output: {fileId, userId, s3Url, fileType}

**UOB-2: Загрузка файла из S3**
- Input: s3Url
- Process: S3 GET request, download binary
- Output: Binary file data

**UOB-3: Препроцессинг изображения**
- Input: Binary image data
- Process: OpenCV decode, resize (224x224), normalize
- Output: Tensor (1, 224, 224, 3, float32)

**UOB-4: Препроцессинг текста**
- Input: Text data (JSON symptoms)
- Process: BERT Tokenizer, padding до max_length=128
- Output: {input_ids, attention_mask}

**UOB-5: ResNet-50 inference**
- Input: Image tensor
- Process: TensorFlow Serving gRPC call, GPU inference
- Output: Softmax probabilities [num_classes]

**UOB-6: BERT inference**
- Input: Tokenized text
- Process: TensorFlow Serving gRPC call, GPU inference
- Output: Classification probabilities [num_classes]

**UOB-7: Агрегация результатов**
- Input: Image predictions, Text predictions
- Process: Weighted combination, top-5 selection
- Output: Combined diagnosis with confidence scores

**UOB-8: Сохранение в Redis**
- Input: Results JSON
- Process: Redis SET с TTL=1h
- Output: Cache key

**UOB-9: Сохранение в PostgreSQL**
- Input: Results data
- Process: SQL INSERT INTO results table
- Output: Database record ID

### Junction
- **После UOB-2**: OR junction (разветвление на обработку изображений и текста)
- **После UOB-5 и UOB-6**: AND junction (синхронизация перед агрегацией)
- **После UOB-7**: AND junction (параллельное сохранение в Redis и PostgreSQL)

### Референсы
- Референс на P2: Данные обрабатываются после валидации (precondition)

### Временная диаграмма

```
t=0s       Получение сообщения из RabbitMQ
t=0.01s    Загрузка файла из S3 (200-500 мс)
t=0.3s     Препроцессинг изображения (50-100 мс) [параллельно]
t=0.25s    Препроцессинг текста (20-50 мс) [параллельно]
t=0.75s    ResNet-50 inference (30-450 мс) [параллельно]
t=0.89s    BERT inference (75-890 мс) [параллельно]
t=1.78s    Агрегация результатов (после обоих)
t=1.79s    Сохранение в Redis (5-15 мс) [параллельно]
t=1.79s    Сохранение в PostgreSQL (50-120 мс) [параллельно]
t=1.91s    Результаты готовы (после обоих сохранений)
t=1.91s    Конец процесса
```

### Временные характеристики GPU

| Этап | GPU Time | CPU Time |
|------|----------|----------|
| ResNet-50 inference | 30 мс | 450 мс |
| BERT inference | 75 мс | 890 мс |
| Grad-CAM generation | 50 мс | N/A |
| **Параллельно** | **75 мс** | **890 мс** |

### Компоненты
- TensorFlow Serving (ML inference сервер)
- GPU кластер (NVIDIA Tesla V100)
- Redis (in-memory cache)
- PostgreSQL (постоянное хранилище)
- AWS S3 (источник данных)

## Источники
- IDEF3 Process Description Capture Method
- TensorFlow Serving Documentation
- GPU Computing Best Practices

