# 3.1.4. DFD: Процесс P4 — Логирование

## Диаграмма потоков данных P4

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://cdn.jsdelivr.net/gh/Edisheri/system-engineering-playbook@main/diagrams-codes/DFD_P4.drawio"></iframe>

## Декомпозиция процесса P4 (Text Analysis Pipeline)

Подробная декомпозиция анализа текстовых данных (симптомов):

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=DFD%20P4%20Decomposition&url=https://cdn.jsdelivr.net/gh/Edisheri/system-engineering-playbook@main/diagrams-codes/DFD_P4_DECOMPOSITION.drawio"></iframe>

### Подпроцессы:

**4.1 Извлечение симптомов:**
- Парсинг JSON с текстовыми данными
- Извлечение поля "symptoms"
- Очистка от HTML-тегов и спецсимволов

**4.2 Токенизация текста:**
- HuggingFace Tokenizer (BERT)
- Разбиение на токены
- Обработка OOV (Out-Of-Vocabulary) слов

**4.3 Генерация input_ids:**
- Маппинг токенов → IDs
- Добавление [CLS], [SEP] токенов
- Padding до max_length=512

**4.4 Генерация attention_mask:**
- 1 для реальных токенов
- 0 для padding токенов
- Длина = max_length

**4.5 Объединение токенов:**
- Формирование словаря {input_ids, attention_mask}
- Кэширование в Redis (TTL=10 min)
- Передача в BERT модель

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

