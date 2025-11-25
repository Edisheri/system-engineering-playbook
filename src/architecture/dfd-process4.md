# 3.1.4. DFD: Процесс P4 — Логирование

## Диаграмма потоков данных P4

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P4.drawio"></iframe>

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

