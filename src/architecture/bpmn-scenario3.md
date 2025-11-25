# 3.1.5. BPMN Сценарий 3: ИИ-анализ (параллельная обработка)

## Участники
- **ML Inference Service**
- **GPU Cluster**
- **Cache (Redis)**
- **Database (PostgreSQL)**

## BPMN Диаграмма

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/BPMN_SCENARIO3.drawio"></iframe>

## Процесс

1. **Старт:** Получение сообщения из RabbitMQ
2. **Шлюз (AND/Parallel):** Параллельная обработка
   - **Ветка 1: Обработка изображения**
     - Препроцессинг (OpenCV)
     - ResNet-50 inference
   - **Ветка 2: Обработка текста**
     - Токенизация (BERT Tokenizer)
     - BERT inference
3. **Шлюз (AND/Join):** Ожидание завершения обеих веток
4. **Задача:** Агрегация результатов
5. **Шлюз (AND/Parallel):** Параллельное сохранение
   - **Ветка 1:** Сохранение в Redis (кэш)
   - **Ветка 2:** Сохранение в PostgreSQL (постоянное хранилище)
6. **Конец:** Результаты готовы

## Особенности
- **Параллельный шлюз (AND):** Обе ветки выполняются одновременно
- **Синхронизация:** Агрегация только после завершения обеих задач
- **GPU-оптимизация:** Batch processing для ResNet и BERT
