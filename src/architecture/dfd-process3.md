# 3.1.4. DFD: Процесс P3 — ИИ-анализ

## Диаграмма потоков данных P3

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://cdn.jsdelivr.net/gh/Edisheri/system-engineering-playbook@main/diagrams-codes/DFD_P3.drawio"></iframe>

## Декомпозиция процесса P3 (Image Processing Pipeline)

Подробная декомпозиция обработки изображений:

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=DFD%20P3%20Decomposition&url=https://cdn.jsdelivr.net/gh/Edisheri/system-engineering-playbook@main/diagrams-codes/DFD_P3_DECOMPOSITION.drawio"></iframe>

### Подпроцессы:

**3.1 Загрузка изображения:**
- Получение сообщения из RabbitMQ (fileId, s3Url)
- Чтение бинарных данных из S3

**3.2 Декодирование:**
- OpenCV: cv2.imdecode()
- Проверка целостности изображения
- Декодирование JPEG/PNG в numpy array

**3.3 Изменение размера:**
- OpenCV: cv2.resize()
- Целевой размер: 224x224 (ResNet-50 input)
- Метод: INTER_AREA для downsampling

**3.4 Нормализация:**
- Приведение к float32
- Нормализация по ImageNet: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
- Диапазон: [0, 1]

**3.5 Конверт в тензор:**
- Преобразование numpy → TensorFlow tensor
- Добавление batch dimension: (1, 224, 224, 3)
- Кэширование в Redis (TTL=10 min)

## Структура результатов

```json
{
  "taskId": "uuid",
  "imagePredictions": [
    {"disease": "Pneumonia", "probability": 0.952}
  ],
  "textPredictions": [
    {"disease": "Flu", "probability": 0.782}
  ],
  "processingTime": 2.3
}
```

