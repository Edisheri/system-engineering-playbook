# 3.1.4. DFD: Процесс P2 — Валидация данных

## Диаграмма потоков данных P2

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P2.drawio"></iframe>

## Декомпозиция процесса P2

Подробная декомпозиция процесса валидации данных на подпроцессы:

<iframe class="drawio-viewer" style="width: 100%; height: 2000px; min-height: 1500px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=DFD%20P2%20Decomposition&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/DFD_P2_DECOMPOSITION.drawio"></iframe>

### Подпроцессы:

**2.1 Валидация файла:**
- Проверка MIME-type
- Проверка размера файла (≤10MB)
- Проверка формата (JPEG/PNG)

**2.2 Загрузка в S3:**
- Генерация уникального fileId
- Шифрование AES-256
- Сохранение в бакет `medical-images-raw`

**2.3 Сохранение метаданных:**
- INSERT в PostgreSQL таблицу `medical_data`
- Сохранение userId, fileId, s3Url, timestamp

**2.4 Отправка в очередь:**
- PUBLISH сообщения в RabbitMQ
- Очередь `ml_inference`
- Формат: {fileId, userId, s3Url, fileType}

## Правила валидации

| Правило | Проверка | Действие при ошибке |
|---------|----------|---------------------|
| Формат файла | MIME-type in [image/jpeg, image/png] | Reject: INVALID_FORMAT |
| Размер | ≤ 10 MB | Reject: FILE_TOO_LARGE |
| Текст | Valid JSON or Plain text | Reject: INVALID_TEXT |
| Rate limit | ≤ 100 req/min per user | Reject: RATE_LIMIT_EXCEEDED |

