# IDEF3: Процесс P2 — Загрузка медицинских данных

## Диаграмма процесса P2

```mermaid
graph TB
    Start([Начало])
    E1[Выбор файлов<br/>изображения и текста]
    J1{Формат<br/>корректен?}
    J2{Размер<br/>≤10МБ?}
    E2[Показать ошибку<br/>формата]
    E3[Показать ошибку<br/>размера]
    E4[Загрузка в S3]
    E5[Сохранение метаданных<br/>в PostgreSQL]
    E6[Отправка сообщения<br/>в RabbitMQ]
    E7[Возврат taskId<br/>пациенту]
    End([Конец])
    
    Start --> E1
    E1 --> J1
    J1 -->|Нет| E2
    E2 --> E1
    J1 -->|Да| J2
    J2 -->|Нет| E3
    E3 --> E1
    J2 -->|Да| E4
    E4 --> E5
    E5 --> E6
    E6 --> E7
    E7 --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style E4 fill:#ff9900,stroke:#cc7700,stroke-width:2px
    style E5 fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style E6 fill:#ff6600,stroke:#cc5200,stroke-width:2px,color:#fff
```

## Временные характеристики

| Этап | Среднее время | P95 |
|------|---------------|-----|
| Валидация формата | 10 мс | 25 мс |
| Загрузка в S3 (5MB) | 500 мс | 1200 мс |
| Сохранение метаданных | 50 мс | 120 мс |
| Отправка в RabbitMQ | 10 мс | 30 мс |
| **Итого** | **570 мс** | **1375 мс** |

