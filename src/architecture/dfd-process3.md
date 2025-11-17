# 3.1.4. DFD: Процесс P3 — ИИ-анализ

## Диаграмма потоков данных P3

```mermaid
flowchart LR
    P2(("P2: Валидация")) -->|"Поток 3.1: Валидированные данные"| P3(("P3: ИИ-анализ"))
    D1[("D1: AWS S3<br/>Хранилище данных")] -->|"Поток 3.2: Файлы<br/>(бинарные)"| P3
    Config[Конфигурация<br/>Внешняя сущность] -->|"Поток 3.3: Параметры моделей"| P3
    P3 -->|"Поток 3.4: Тензоры<br/>(gRPC)"| TFS[TensorFlow Serving<br/>Внешняя сущность]
    P3 -->|"Поток 3.5: Токены BERT<br/>(gRPC)"| TFS
    TFS -->|"Поток 3.6: Результаты inference"| P3
    P3 -->|"Поток 3.7: Результаты<br/>(JSON, TTL=1h)"| D3[("D3: Redis<br/>Хранилище данных")]
    P3 -->|"Поток 3.8: Результаты диагностики"| D2[("D2: PostgreSQL<br/>Хранилище данных")]
    P3 -->|"Поток 3.9: Метрики"| Prometheus[Prometheus<br/>Внешняя сущность]
    
    style P2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style P3 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style TFS fill:#ff9800,stroke:#e68900,stroke-width:2px
    style Prometheus fill:#ff9800,stroke:#e68900,stroke-width:2px
    style Config fill:#ff9800,stroke:#e68900,stroke-width:2px
    style D1 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style D2 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
    style D3 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
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

