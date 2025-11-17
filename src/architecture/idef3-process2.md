# 3.1.3. IDEF3: Процесс P2 — Загрузка медицинских данных

## Диаграмма процесса P2

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/IDEF3_P2.drawio}

### Mermaid версия (для справки)

```mermaid
flowchart LR
    Start([Начало]) --> UOB1["UOB-1: Выбор файлов"]
    UOB1 --> UOB2["UOB-2: Отправка POST запроса"]
    UOB2 --> UOB3["UOB-3: Валидация формата<br/>и размера"]
    UOB3 --> Junction1{XOR}
    Junction1 -->|Валидация успешна| UOB4["UOB-4: Сохранение в S3"]
    Junction1 -->|Ошибка валидации| UOBError["UOB-Error: Ошибка<br/>валидации"]
    UOB4 --> Junction2{AND}
    Junction2 --> UOB5["UOB-5: Сохранение<br/>метаданных"]
    Junction2 --> UOB6["UOB-6: Отправка сообщения<br/>в очередь"]
    UOB5 --> End([Конец])
    UOB6 --> End
    UOBError --> End
    
    style UOB1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB3 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB4 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB5 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB6 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOBError fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style Junction1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Junction2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#67c23a,stroke:#4a9428,stroke-width:3px
```

## Временные характеристики

| Этап | Среднее время | P95 |
|------|---------------|-----|
| Валидация формата | 10 мс | 25 мс |
| Загрузка в S3 (5MB) | 500 мс | 1200 мс |
| Сохранение метаданных | 50 мс | 120 мс |
| Отправка в RabbitMQ | 10 мс | 30 мс |
| **Итого** | **570 мс** | **1375 мс** |

