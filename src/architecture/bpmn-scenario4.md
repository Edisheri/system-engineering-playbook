# BPMN Сценарий 4: Интеграция с MIS (Clinic Management Information System)

## Участники
- **Система диагностики**
- **Report Generator**
- **Clinic MIS**
- **Администратор**

## BPMN Диаграмма

```mermaid
graph TB
    Start([Начало])
    
    subgraph "Пул: Система"
        S1[Результаты готовы]
        S2[Генерация PDF]
        S3[Формирование JSON]
        S4{Доступен MIS?}
        S5[Сохранение в очередь]
        S6[Уведомление админа]
    end
    
    subgraph "Пул: Report Generator"
        R1[Создание PDF]
        R2[Подготовка JSON]
    end
    
    subgraph "Пул: Clinic MIS"
        M1[Получение POST]
        M2[Обработка отчёта]
        M3[Возврат 200 OK]
        M4[Возврат ошибки]
    end
    
    subgraph "Пул: Админ"
        A1[Получение уведомления]
    end
    
    Start --> S1
    S1 --> S2
    S2 --> R1
    R1 --> S3
    S3 --> R2
    R2 --> S4
    S4 -->|Да| M1
    S4 -->|Нет| S5
    S5 --> S4
    M1 --> M2
    M2 --> M3
    M2 --> M4
    M3 --> End([Конец])
    M4 --> S6
    S6 --> A1
    A1 --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style S4 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style R1 fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style M1 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style A1 fill:#9966ff,stroke:#7744cc,stroke-width:2px,color:#fff
```

## Процесс

1. **Старт:** Результаты ИИ-анализа готовы
2. **Задача:** Генерация PDF-отчёта (PDFKit)
3. **Задача:** Формирование JSON для API
4. **Шлюз (XOR):** Проверка доступности MIS
   - **Доступен:** Отправить отчёт
   - **Недоступен:** Сохранить в очередь ожидания
5. **Задача:** POST запрос к MIS API
6. **Шлюз (XOR):** Проверка ответа
   - **200 OK:** Успешная отправка
   - **4xx/5xx:** Повтор через 5 минут
7. **Событие (таймер):** Ожидание перед повтором
8. **Задача:** Уведомление администратора (если 3 неудачи)
9. **Конец:** Отчёт доставлен

## Особенности
- **Обработка ошибок:** Retry mechanism с экспоненциальной задержкой
- **Таймер-события:** Автоматический повтор
- **Эскалация:** Уведомление администратора при критических ошибках
