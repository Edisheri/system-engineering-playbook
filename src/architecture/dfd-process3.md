# DFD: Процесс P3 — ИИ-анализ

## Диаграмма потоков данных P3

```mermaid
graph TB
    Queue[RabbitMQ<br/>medical_data]
    
    P3[P3<br/>ИИ-анализ<br/>ResNet + BERT]
    
    TFServing[TensorFlow<br/>Serving]
    
    D3[(D3<br/>Redis<br/>Cache)]
    D2[(D2<br/>PostgreSQL<br/>Results)]
    
    Queue -->|Тензоры<br/>и токены| P3
    P3 -->|gRPC<br/>request| TFServing
    TFServing -->|Predictions<br/>probabilities| P3
    P3 -->|Результаты<br/>TTL=1h| D3
    P3 -->|Результаты<br/>persistent| D2
    
    style P3 fill:#ff6f00,stroke:#c43e00,stroke-width:3px,color:#fff
    style TFServing fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style D3 fill:#dc382d,stroke:#a02822,stroke-width:2px,color:#fff
    style D2 fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
```

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

