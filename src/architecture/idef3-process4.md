# 3.1.3. IDEF3: Процесс P4 — Логирование и мониторинг

## Диаграмма процесса P4

```mermaid
flowchart LR
    Start([Начало]) --> UOB1["UOB-1: Генерация логов<br/>(все сервисы)"]
    UOB1 --> UOB2["UOB-2: Сбор логов<br/>(Filebeat)"]
    UOB2 --> UOB3["UOB-3: Обработка и фильтрация<br/>(Logstash)"]
    UOB3 --> UOB4["UOB-4: Индексация данных<br/>(Elasticsearch)"]
    UOB4 --> Junction1{AND}
    Junction1 --> UOB5["UOB-5: Визуализация метрик<br/>(Kibana)"]
    Junction1 --> UOB6["UOB-6: Генерация алертов<br/>(при критических ошибках)"]
    UOB5 --> End([Конец])
    UOB6 --> End
    
    style UOB1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB3 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB4 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB5 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style UOB6 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style Junction1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:3px
    style End fill:#67c23a,stroke:#4a9428,stroke-width:3px
```

## Логирование происходит параллельно всем процессам!

