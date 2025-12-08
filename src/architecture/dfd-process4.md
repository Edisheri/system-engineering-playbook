# 3.1.4. DFD: Процесс P4 — Логирование и мониторинг

## Диаграмма потоков данных P4

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P4.drawio"></iframe>

## Декомпозиция процесса P4 (Logging Pipeline)

Подробная декомпозиция процесса логирования и мониторинга:

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=DFD%20P4%20Decomposition&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P4_DECOMPOSITION.drawio"></iframe>

### Подпроцессы:

**4.1 Сбор логов:**
- Filebeat собирает логи из всех сервисов
- Источники: P1, P2, P3, системные логи
- Формат: JSON structured logging
- Частота: real-time streaming

**4.2 Фильтрация и парсинг:**
- Logstash обрабатывает входящие логи
- Парсинг JSON, извлечение полей
- Фильтрация по уровню (INFO, WARN, ERROR)
- Обогащение метаданными (service, environment)

**4.3 Индексация в Elasticsearch:**
- Создание индексов по датам (logstash-YYYY.MM.DD)
- Индексация полей для поиска
- Retention: 30 дней
- Шардирование для производительности

**4.4 Генерация метрик:**
- Агрегация логов в метрики Prometheus
- Счетчики ошибок, время ответа, throughput
- Экспорт в Prometheus format

**4.5 Визуализация в Kibana:**
- Создание дашбордов для мониторинга
- Графики ошибок, производительности
- Поиск по логам через Kibana UI

**4.6 Генерация алертов:**
- Правила алертинга (error rate > threshold)
- Уведомления через Slack/Email
- Эскалация критических ошибок

## Потоки данных

| Поток | Источник | Назначение | Данные | Формат |
|-------|----------|------------|--------|--------|
| 4.1 | P1, P2, P3 | P4 | Логи приложений | JSON logs |
| 4.2 | Система | P4 | Системные метрики | Prometheus metrics |
| 4.3 | P4 | D4 | Индексированные логи | JSON (Elasticsearch) |
| 4.4 | P4 | Prometheus | Метрики | Prometheus format |
| 4.5 | P4 | DevOps | Алерты | Slack/Email |

## Хранилища данных

**D4: Elasticsearch**
- Тип: Поисковый движок (NoSQL)
- Данные: Логи и метрики за 30 дней
- Структура: Индексы по датам (logstash-YYYY.MM.DD)
- Доступ:
  - P4 → D4 (запись индексированных логов)
  - Kibana → D4 (чтение для визуализации)

## Структура лог записи

```json
{
  "timestamp": "2024-10-14T10:30:00Z",
  "level": "INFO",
  "service": "ml-inference",
  "message": "Inference completed",
  "taskId": "abc-123",
  "duration": 2300,
  "userId": 42,
  "gpuUtilization": 85.5,
  "memoryUsage": "2.3GB"
}
```

## Правила алертинга

| Правило | Условие | Действие |
|---------|---------|----------|
| Высокий error rate | > 5% за 5 минут | Slack alert + Email |
| Критическая ошибка | ERROR level | Immediate Slack + Phone call |
| GPU недоступен | GPU utilization = 0% | Slack alert |
| Высокая задержка | P95 latency > 5s | Slack warning |

## Внешние сущности
- **DevOps команда** — получатель алертов
- **Kibana** — визуализация логов (читает из D4)
- **Prometheus** — система мониторинга метрик

