# Публичный API (Swagger Documentation)

## Интерактивная документация

<iframe src="swagger/swagger.html" width="100%" height="1500px" style="border:0;" allowfullscreen="allowfullscreen"></iframe>

---

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

## Источники

1. [OpenAPI 3.0 Specification](https://swagger.io/specification/)
2. [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
3. «RESTful API Design» Leonard Richardson

