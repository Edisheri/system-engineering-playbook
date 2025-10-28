# UML Диаграммы: Регистрация пользователя

## Функция 1: Регистрация пользователя

### 1. Use Case Diagram (Диаграмма вариантов использования)

![Use Case - Registration](../img/diagrams/uml-registration-1.png)

**Актёры:**
- **Пациент** (Patient)
- **Администратор** (Administrator)
- **Email Service** (система)

**Варианты использования:**
1. **Регистрация в системе**
   - Первичный актёр: Пациент
   - Предусловия: Нет
   - Постусловия: Пациент зарегистрирован, письмо отправлено
   
2. **Подтверждение email**
   - Первичный актёр: Пациент
   - Предусловия: Регистрация завершена
   - Постусловия: Аккаунт активирован
   
3. **Управление ролями**
   - Первичный актёр: Администратор
   - Предусловия: Администратор аутентифицирован
   - Постусловия: Роли пользователя обновлены

**Связи:**
- `<<include>>`: Регистрация включает валидацию данных
- `<<extend>>`: Подтверждение email расширяет регистрацию

---

### 2. Activity Diagram (Диаграмма активностей)

![Диаграмма](../img/diagrams/uml-registration-2.png)

**Элементы:**
- **Начальная точка:** Круг с заливкой
- **Активности:** Прямоугольники со скруглёнными углами
- **Условия:** Ромб (decision node)
- **Конечная точка:** Круг с кругом внутри

---

### 3. Sequence Diagram (Диаграмма последовательности)

![Диаграмма](../img/diagrams/uml-registration-3.png)

**Ключевые сообщения:**
- Синхронные вызовы: сплошная линия со стрелкой
- Возвраты: пунктирная линия
- Активация: вертикальный прямоугольник на lifeline

---

### 4. Class Diagram (Диаграмма классов)

![Диаграмма](../img/diagrams/uml-registration-4.png)

**Связи:**
- **Ассоциация:** `AuthController` использует `AuthService`
- **Зависимость:** `AuthService` зависит от `UserRepository`
- **Реализация:** `UserRepositoryImpl` реализует `UserRepository`
- **Наследование:** `User` наследуется от `BaseEntity`

---

### 5. State Diagram (Диаграмма состояний)

![Диаграмма](../img/diagrams/uml-registration-5.png)

**Состояния:**
1. **New:** Пользователь создан, письмо не отправлено
2. **Pending:** Письмо отправлено, ожидание активации
3. **Activated:** Аккаунт активирован, может использовать систему
4. **Dormant:** Неактивен более 30 дней
5. **Blocked:** Заблокирован администратором

**Переходы:**
- `sendActivationEmail()`: New → Pending
- `activate(token)`: Pending → Activated
- `after 30 days no login`: Activated → Dormant
- `admin blocks`: * → Blocked

---

### 6. Component Diagram (Диаграмма компонентов)

```mermaid
graph TB
    subgraph "Auth Module"
        AuthController[AuthController]
        AuthService[AuthService]
        UserRepository[UserRepository JPA]
        RESTAPI[REST API<br/>/api/register<br/>/api/activate]
    end
    
    subgraph "Email Module"
        EmailService[EmailService]
        EmailTemplate[EmailTemplate Engine]
        JavaMailSender[JavaMailSender<br/>Spring Mail]
    end
    
    subgraph "Security Module"
        Keycloak[Keycloak Identity]
        JWTFilter[JWT Filter]
        SecurityContext[SecurityContext Spring]
    end
    
    subgraph "Database"
        PostgreSQL[(PostgreSQL Database)]
    end
    
    subgraph "External Services"
        EmailProvider[Email Provider<br/>SendGrid/SES]
    end
    
    AuthController --> AuthService
    AuthController --> RESTAPI
    AuthService --> UserRepository
    AuthService --> EmailService
    UserRepository --> PostgreSQL
    
    EmailService --> EmailTemplate
    EmailService --> JavaMailSender
    JavaMailSender --> EmailProvider
    
    Keycloak --> JWTFilter
    JWTFilter --> SecurityContext
    
    style AuthController fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style AuthService fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style EmailService fill:#6db33f,stroke:#4a7c2f,stroke-width:2px
    style Keycloak fill:#ff6f00,stroke:#c43e00,stroke-width:2px,color:#fff
    style PostgreSQL fill:#336791,stroke:#1a3a5c,stroke-width:2px,color:#fff
    style EmailProvider fill:#e6a23c,stroke:#b8821e,stroke-width:2px
```

**Компоненты:**
- **Auth Module:** Управление пользователями
- **Email Module:** Отправка писем
- **Security Module:** Аутентификация и авторизация

**Интерфейсы:**
- REST API: `/api/register`, `/api/activate`
- SMTP: Протокол отправки email
- JDBC: Подключение к PostgreSQL

---

## Источники

- «UML Distilled» Martin Fowler
- [Spring Security Documentation](https://spring.io/projects/spring-security)
- «Design Patterns» Gang of Four

