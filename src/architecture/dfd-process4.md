# DFD: Процесс P4 — Логирование

## Диаграмма потоков данных P4

```mermaid
graph TB
    P1[P1 Приём]
    P2[P2 Валидация]
    P3[P3 ИИ-анализ]
    
    P4[P4<br/>Логирование]
    
    D4[(D4<br/>Elasticsearch<br/>Logs)]
    
    Kibana[Kibana<br/>Dashboard]
    DevOps[👨‍💻 DevOps]
    
    P1 -->|Логи<br/>INFO/ERROR| P4
    P2 -->|Логи<br/>WARN/ERROR| P4
    P3 -->|Логи<br/>DEBUG/INFO| P4
    
    P4 -->|Индексация<br/>логов| D4
    D4 -->|Запросы<br/>поиска| Kibana
    Kibana -->|Визуализация| DevOps
    
    style P4 fill:#005571,stroke:#00394d,stroke-width:3px,color:#fff
    style D4 fill:#005571,stroke:#00394d,stroke-width:2px,color:#fff
```

## Структура лог записи

```json
{
  "timestamp": "2024-10-14T10:30:00Z",
  "level": "INFO",
  "service": "ml-inference",
  "message": "Inference completed",
  "taskId": "abc-123",
  "duration": 2300,
  "userId": 42
}
```

