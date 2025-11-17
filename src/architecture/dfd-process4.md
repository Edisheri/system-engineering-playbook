# 3.1.4. DFD: Процесс P4 — Логирование

## Диаграмма потоков данных P4

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/DFD_P4.drawio}

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

