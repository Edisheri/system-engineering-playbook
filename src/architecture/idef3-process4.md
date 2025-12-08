# 3.1.3. IDEF3: Процесс P4 — Логирование и мониторинг

## Диаграмма процесса P4

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/IDEF3_P4.drawio"></iframe>

## Описание процесса P4

**Важно:** Логирование происходит параллельно всем процессам (P1, P2, P3) как непрерывный фоновый процесс!

### Участники
- **Все сервисы** (P1, P2, P3) — источники логов
- **Filebeat** — сбор логов
- **Logstash** — обработка и фильтрация
- **Elasticsearch** — хранилище логов
- **Kibana** — визуализация
- **DevOps команда** — получатель алертов

### Временные связи

| Событие | Последующее событие | Условие | Задержка |
|---------|---------------------|---------|----------|
| E1 → E2 | Логи собраны | Filebeat успешно собрал | Real-time (непрерывно) |
| E2 → E3 | Логи обработаны | Logstash фильтрация успешна | 10-50 мс |
| E3 → E4 | Логи проиндексированы | Elasticsearch индексация успешна | 50-200 мс |
| E4 → E5 | Метрики визуализированы | Kibana дашборд обновлён | 100-500 мс |
| E4 → E6 | Алерты проверены | Критическая ошибка обнаружена | 10-100 мс |
| E6 → E7 | Алерт отправлен | Условие алерта выполнено | 50-200 мс |

### Точки синхронизации
- **После E4**: Параллельное выполнение визуализации (E5) и проверки алертов (E6) (AND junction)
- **Процесс непрерывный**: Выполняется параллельно всем процессам P1, P2, P3

### UOB (Unit of Behavior)

**UOB-1: Генерация логов**
- Input: События от всех сервисов (P1, P2, P3)
- Process: Structured logging (JSON format), добавление метаданных
- Output: Log entries (JSON)

**UOB-2: Сбор логов**
- Input: Log files от всех сервисов
- Process: Filebeat tailing log files, отправка в Logstash
- Output: Log streams → Logstash

**UOB-3: Обработка и фильтрация**
- Input: Raw log streams
- Process: Парсинг JSON, фильтрация по уровню (INFO, WARN, ERROR), обогащение метаданными
- Output: Обработанные логи

**UOB-4: Индексация данных**
- Input: Обработанные логи
- Process: Создание индексов в Elasticsearch по датам, индексация полей
- Output: Индексированные логи в Elasticsearch

**UOB-5: Визуализация метрик**
- Input: Данные из Elasticsearch
- Process: Обновление Kibana дашбордов, графики, таблицы
- Output: Визуализированные метрики в Kibana

**UOB-6: Генерация алертов**
- Input: Данные из Elasticsearch (error rate, критичные ошибки)
- Process: Проверка правил алертинга, определение критичности
- Output: Alert events (если условия выполнены)

**UOB-7: Отправка алертов**
- Input: Alert events
- Process: Отправка через Slack webhook или Email SMTP
- Output: Уведомления → DevOps команда

### Junction
- **После UOB-4**: AND junction (параллельное выполнение визуализации UOB-5 и генерации алертов UOB-6)
- **После UOB-6**: OR junction (алерты генерируются только при критических ошибках)

### Референсы
- Референс на P1, P2, P3: Непрерывное выполнение параллельно всем процессам (concurrent process)

### Временная диаграмма

**Непрерывный процесс (выполняется параллельно P1, P2, P3):**
```
t=0s      Генерация логов от всех сервисов (UOB-1) [непрерывно]
t=0.01s   Сбор логов Filebeat (UOB-2) [real-time streaming]
t=0.06s   Обработка и фильтрация Logstash (UOB-3) (10-50 мс)
t=0.26s   Индексация в Elasticsearch (UOB-4) (50-200 мс)
t=0.36s   Визуализация метрик Kibana (UOB-5) (100-500 мс) [параллельно]
t=0.16s   Генерация алертов (UOB-6) (10-100 мс) [параллельно, если есть ошибки]
t=0.36s   Отправка алертов DevOps (UOB-7) (50-200 мс) [если условия выполнены]
...       Процесс повторяется непрерывно
```

**Сценарий с критической ошибкой:**
```
t=X       Критическая ошибка обнаружена в логах P3
t=X+0.01s Сбор логов (UOB-2)
t=X+0.06s Обработка и фильтрация (UOB-3)
t=X+0.26s Индексация в Elasticsearch (UOB-4)
t=X+0.16s Генерация алертов: условие выполнено (UOB-6)
t=X+0.36s Отправка алерта DevOps (UOB-7)
t=X+0.56s Алерт доставлен
```

### Компоненты
- Filebeat (сбор логов, версия 7.x)
- Logstash (обработка, версия 7.x)
- Elasticsearch (хранилище, версия 7.x)
- Kibana (визуализация, версия 7.x)

### Правила алертинга

| Правило | Условие | Действие |
|---------|---------|----------|
| Высокий error rate | > 5% за 5 минут | Slack alert + Email |
| Критическая ошибка | ERROR level с критическими тегами | Immediate Slack + Phone call |
| GPU недоступен | GPU utilization = 0% более 1 минуты | Slack alert |
| Высокая задержка | P95 latency > 5s более 2 минут | Slack warning |
| Диск заполнен | Disk usage > 90% | Slack alert + Email |

## Источники
- IDEF3 Process Description Capture Method
- ELK Stack Documentation
- Logging Best Practices

