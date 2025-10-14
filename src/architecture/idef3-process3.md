# IDEF3: Процесс P3 — GPU-обработка данных

## Диаграмма процесса P3

```mermaid
graph TB
    Start([Получено сообщение<br/>из RabbitMQ])
    
    subgraph "Параллельная обработка"
        P1[Препроцессинг<br/>изображения OpenCV]
        P2[Токенизация<br/>текста BERT]
        
        P3[ResNet-50<br/>inference]
        P4[BERT<br/>inference]
    end
    
    J1((Синхронизация))
    
    E1[Агрегация<br/>результатов]
    E2[Генерация<br/>heatmap Grad-CAM]
    E3[Сохранение в Redis]
    E4[Сохранение в PostgreSQL]
    E5[Отправка WebSocket<br/>уведомления]
    
    End([Конец])
    
    Start --> P1
    Start --> P2
    P1 --> P3
    P2 --> P4
    P3 --> J1
    P4 --> J1
    J1 --> E1
    E1 --> E2
    E2 --> E3
    E2 --> E4
    E3 --> E5
    E4 --> E5
    E5 --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style P3 fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style P4 fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style J1 fill:#e6a23c,stroke:#b8821e,stroke-width:3px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:2px
```

## Временные характеристики GPU

| Этап | GPU Time | CPU Time |
|------|----------|----------|
| ResNet-50 inference | 30 мс | 450 мс |
| BERT inference | 75 мс | 890 мс |
| Grad-CAM generation | 50 мс | N/A |
| **Параллельно** | **75 мс** | **890 мс** |

