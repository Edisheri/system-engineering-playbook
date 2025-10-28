# BPMN Сценарий 3: ИИ-анализ (параллельная обработка)

## Участники
- **ML Inference Service**
- **GPU Cluster**
- **Cache (Redis)**
- **Database (PostgreSQL)**

## BPMN Диаграмма

```mermaid
graph TB
    Start([Начало])
    
    subgraph "Пул: ML Inference Service"
        M1[Получение сообщения<br/>из RabbitMQ]
        M2[Параллельная<br/>обработка]
        M3[Агрегация<br/>результатов]
    end
    
    subgraph "Пул: GPU Cluster"
        G1[Обработка<br/>изображения]
        G2[Анализ<br/>симптомов]
        G3[ResNet-50<br/>inference]
        G4[BERT<br/>inference]
    end
    
    subgraph "Пул: Cache (Redis)"
        R1[Сохранение в<br/>Redis кэш]
    end
    
    subgraph "Пул: Database (PostgreSQL)"
        D1[Сохранение в<br/>PostgreSQL]
    end
    
    Start --> M1
    M1 --> M2
    M2 --> G1
    M2 --> G2
    G1 --> G3
    G2 --> G4
    G3 --> M3
    G4 --> M3
    M3 --> R1
    M3 --> D1
    R1 --> End([Конец])
    D1 --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style M2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style G3 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style G4 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style R1 fill:#dc382d,stroke:#a02822,stroke-width:2px,color:#fff
    style D1 fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
```

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
