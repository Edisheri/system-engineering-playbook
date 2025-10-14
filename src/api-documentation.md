# Публичный API (Swagger Documentation)

## Обзор

Medical Diagnosis Platform предоставляет RESTful API для интеграции с внешними системами и клиентскими приложениями.

### Базовый URL

- **Production:** `https://api.med-diagnosis.com/v1`
- **Staging:** `https://staging-api.med-diagnosis.com/v1`
- **Development:** `http://localhost:8080/api/v1`

### Аутентификация

API использует **JWT (JSON Web Tokens)** для аутентификации:

```http
Authorization: Bearer {your_jwt_token}
```

Получить токен можно через эндпоинт `/auth/login`.

### Rate Limiting

- **Аутентифицированные пользователи:** 100 запросов/минуту
- **Неаутентифицированные:** 10 запросов/минуту

Информация о лимитах возвращается в заголовках ответа:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642512000
```

## Интерактивная документация

<iframe src="swagger/swagger.html" width="100%" height="1500px" style="border:0;" allowfullscreen="allowfullscreen"></iframe>

---

## Основные эндпоинты

### 1. Регистрация пользователя

```http
POST /auth/register
Content-Type: application/json

{
  "email": "patient@example.com",
  "password": "SecurePass123!",
  "firstName": "Иван",
  "lastName": "Петров"
}
```

**Ответ (201 Created):**
```json
{
  "message": "Регистрация успешна. Проверьте email для активации.",
  "userId": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 2. Вход в систему

```http
POST /auth/login
Content-Type: application/json

{
  "email": "patient@example.com",
  "password": "SecurePass123!"
}
```

**Ответ (200 OK):**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer",
  "expiresIn": 3600,
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 3. Загрузка медицинских данных

```http
POST /upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

image: <binary file>
symptoms: {"symptoms": ["головная боль", "температура 38.5"], "duration": "3 дня"}
```

**Ответ (202 Accepted):**
```json
{
  "taskId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Данные загружены и отправлены на обработку",
  "estimatedTime": 5
}
```

---

### 4. Проверка статуса обработки

```http
GET /analysis/{taskId}/status
Authorization: Bearer {token}
```

**Ответ (200 OK) - Обработка:**
```json
{
  "taskId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "processing",
  "progress": 65,
  "message": "Анализ изображения ResNet-50"
}
```

---

### 5. Получение результатов анализа

```http
GET /analysis/{taskId}/result
Authorization: Bearer {token}
```

**Ответ (200 OK):**
```json
{
  "taskId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "imagePredictions": [
    {
      "disease": "Пневмония",
      "probability": 0.952,
      "confidence": "высокая"
    }
  ],
  "textPredictions": [
    {
      "disease": "Грипп",
      "probability": 0.782,
      "symptoms": ["температура", "головная боль"]
    }
  ],
  "heatmapUrl": "https://cdn.med-diagnosis.com/heatmaps/a1b2c3d4.png",
  "combinedDiagnosis": [
    {
      "disease": "Пневмония",
      "overallProbability": 0.867,
      "recommendation": "Требуется консультация пульмонолога"
    }
  ],
  "processingTime": 2.3
}
```

---

### 6. Скачивание PDF отчёта

```http
GET /reports/{taskId}?format=pdf
Authorization: Bearer {token}
```

**Ответ (200 OK):**
- Content-Type: `application/pdf`
- Binary PDF file

---

## Коды ошибок

| HTTP Code | Код ошибки | Описание |
|-----------|------------|----------|
| 400 | `INVALID_REQUEST` | Невалидные данные в запросе |
| 401 | `UNAUTHORIZED` | Требуется аутентификация |
| 403 | `FORBIDDEN` | Недостаточно прав доступа |
| 404 | `NOT_FOUND` | Ресурс не найден |
| 409 | `EMAIL_EXISTS` | Email уже зарегистрирован |
| 413 | `FILE_TOO_LARGE` | Файл превышает 10 МБ |
| 425 | `PROCESSING_NOT_COMPLETE` | Обработка ещё не завершена |
| 429 | `RATE_LIMIT_EXCEEDED` | Превышен лимит запросов |
| 500 | `INTERNAL_ERROR` | Внутренняя ошибка сервера |
| 502 | `MIS_UNAVAILABLE` | MIS система недоступна |

---

## Примеры интеграции

### Python (requests)

```python
import requests

BASE_URL = "https://api.med-diagnosis.com/v1"

# Вход
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "patient@example.com", "password": "SecurePass123!"}
)
token = response.json()["accessToken"]

# Загрузка данных
files = {"image": open("xray.jpg", "rb")}
data = {"symptoms": '{"symptoms": ["головная боль"]}'}
headers = {"Authorization": f"Bearer {token}"}

response = requests.post(
    f"{BASE_URL}/upload",
    files=files,
    data=data,
    headers=headers
)
task_id = response.json()["taskId"]
```

### JavaScript (fetch)

```javascript
const BASE_URL = "https://api.med-diagnosis.com/v1";

async function login(email, password) {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return (await response.json()).accessToken;
}

async function uploadData(token, imageFile, symptoms) {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('symptoms', JSON.stringify(symptoms));
  
  const response = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  
  return await response.json();
}
```

---

## Источники

1. [OpenAPI 3.0 Specification](https://swagger.io/specification/)
2. [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
3. «RESTful API Design» Leonard Richardson

