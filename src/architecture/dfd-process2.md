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

## Потоки данных

| Поток | Источник | Назначение | Данные | Формат |
|-------|----------|------------|--------|--------|
| 2.1 | P1 | P2 | Файлы + метаданные | multipart/form-data |
| 2.2 | D2 (PostgreSQL) | P2 | Правила валидации | SQL SELECT |
| 2.3 | P2 | P3 | Валидированные данные | {fileId, s3Url, fileType} |
| 2.4 | P2 | Пациент | {error: "validation_failed", details: [...]} | JSON/HTTP 400 |

## Хранилища данных

**D2: PostgreSQL** (правила валидации)
- Доступ: P2 читает правила валидации из конфигурации

## Правила валидации

| Правило | Проверка | Действие при ошибке |
|---------|----------|---------------------|
| Формат файла | MIME-type in [image/jpeg, image/png, text/plain] | Reject: INVALID_FORMAT → Поток 2.4 |
| Размер | ≤ 10 MB | Reject: FILE_TOO_LARGE → Поток 2.4 |
| Текст | Valid JSON or Plain text | Reject: INVALID_TEXT → Поток 2.4 |
| Rate limit | ≤ 100 req/min per user | Reject: RATE_LIMIT_EXCEEDED → Поток 2.4 |

## Обработка ошибок

**Поток ошибки валидации (2.4):**
- Источник: P2 (после неуспешной валидации)
- Назначение: Пациент
- Данные: {error: "validation_failed", code: "INVALID_FORMAT" | "FILE_TOO_LARGE" | "INVALID_TEXT" | "RATE_LIMIT_EXCEEDED", message: "Описание ошибки", details: [...]}
- Формат: JSON/HTTP 400 Bad Request

**Успешная валидация:**
- Поток 2.3: Валидированные данные передаются в P3 для дальнейшей обработки

