# 3.1.3. IDEF3: Процесс P3 — GPU-обработка данных

## Диаграмма процесса P3

```mermaid
flowchart LR
    Start([Начало]) --> UOB1["UOB-1: Получение сообщения<br/>из RabbitMQ"]
    UOB1 --> UOB2["UOB-2: Загрузка файла<br/>из S3"]
    UOB2 --> Junction1{OR}
    Junction1 --> UOB3["UOB-3: Препроцессинг<br/>изображения"]
    Junction1 --> UOB4["UOB-4: Препроцессинг<br/>текста"]
    UOB3 --> UOB5["UOB-5: Inference ResNet-50"]
    UOB4 --> UOB6["UOB-6: Inference BERT"]
    UOB5 --> Junction2{AND}
    UOB6 --> Junction2
    Junction2 --> UOB7["UOB-7: Агрегация<br/>результатов"]
    UOB7 --> Junction3{AND}
    Junction3 --> UOB8["UOB-8: Сохранение в Redis"]
    Junction3 --> UOB9["UOB-9: Сохранение в PostgreSQL"]
    UOB8 --> End([Конец])
    UOB9 --> End
    
    style UOB1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB3 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB4 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB5 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB6 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB7 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB8 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB9 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style Junction1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Junction2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Junction3 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#67c23a,stroke:#4a9428,stroke-width:3px
```

## Временные характеристики GPU

| Этап | GPU Time | CPU Time |
|------|----------|----------|
| ResNet-50 inference | 30 мс | 450 мс |
| BERT inference | 75 мс | 890 мс |
| Grad-CAM generation | 50 мс | N/A |
| **Параллельно** | **75 мс** | **890 мс** |

