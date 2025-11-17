# 3.1.4. DFD: Процесс P2 — Валидация данных

## Диаграмма потоков данных P2

```mermaid
flowchart LR
    P1(("P1: Приём данных")) -->|"Поток 2.1: Данные<br/>(multipart/form-data)"| P2(("P2: Валидация данных"))
    D2[("D2: PostgreSQL<br/>Хранилище данных")] -->|"Поток 2.2: Правила валидации"| P2
    P2 -->|"Поток 2.3: Валидированные данные"| P3(("P3: ИИ-анализ"))
    P2 -->|"Поток 2.4: Ошибки валидации<br/>(JSON)"| Patient[Пациент<br/>Внешняя сущность]
    
    style P1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style P2 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style P3 fill:#4a90e2,stroke:#2e5c8a,stroke-width:3px,color:#fff
    style Patient fill:#ff9800,stroke:#e68900,stroke-width:2px
    style D2 fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px,color:#fff
```

## Правила валидации

| Правило | Проверка | Действие при ошибке |
|---------|----------|---------------------|
| Формат файла | MIME-type in [image/jpeg, image/png] | Reject: INVALID_FORMAT |
| Размер | ≤ 10 MB | Reject: FILE_TOO_LARGE |
| Текст | Valid JSON or Plain text | Reject: INVALID_TEXT |
| Rate limit | ≤ 100 req/min per user | Reject: RATE_LIMIT_EXCEEDED |

