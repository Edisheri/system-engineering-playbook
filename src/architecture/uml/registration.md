# UML Диаграммы: Регистрация пользователя

## Функция 1: Регистрация пользователя

### 1. Use Case Diagram (Диаграмма вариантов использования)

```plantuml
left to right direction

actor Пациент
actor Администратор
actor "Email Service" as EmailService

Пациент --> (Регистрация в системе)
Пациент --> (Подтверждение email)
Администратор --> (Управление ролями)

(Регистрация в системе) ..> (Валидация данных): <<include>>
(Регистрация в системе) ..> (Создание пользователя): <<include>>
(Регистрация в системе) ..> (Генерация токена): <<include>>
(Регистрация в системе) <.. (Подтверждение email): <<extend>>

(Подтверждение email) ..> (Отправка письма активации): <<include>>
EmailService --> (Отправка письма активации)

(Управление ролями) ..> (Назначение ролей): <<include>>
(Управление ролями) ..> (Удаление ролей): <<include>>

note right of (Регистрация в системе)
  Обязательные шаги:
  - Валидация данных
  - Создание пользователя
  - Генерация токена
end note

note right of (Подтверждение email)
  Опциональный шаг:
  Выполняется только если
  пользователь переходит
  по ссылке из письма
end note
```

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

```plantuml
start

:Заполнение формы регистрации;

:Валидация данных;

if (Данные корректны?) then (Да)
  :Проверка уникальности email;
  
  if (Email уникален?) then (Да)
    fork
      :Создание пользователя;
      :Генерация токена активации;
    fork again
      :Хеширование пароля (BCrypt);
    end fork
    
    :Отправка письма;
    
    fork
      :Сохранение в PostgreSQL;
    fork again
      :Логирование события;
    end fork
    
    :Активация аккаунта;
    stop
  else (Нет)
    :Ошибка: Email уже существует;
    stop
  endif
  
else (Нет)
  :Ошибка валидации;
  stop
endif
```

**Элементы:**
- **Начальная точка:** Круг с заливкой
- **Активности:** Прямоугольники со скруглёнными углами
- **Условия:** Ромб (decision node)
- **Конечная точка:** Круг с кругом внутри

---

### 3. Sequence Diagram (Диаграмма последовательности)

```plantuml
actor Пациент
participant "WebUI
(React)" as WebUI
participant "APIGateway
(Spring Cloud)" as Gateway
participant "RegistrationController" as Controller
participant "UserService" as Service
participant "EmailService" as Email
database "PostgreSQL" as DB

Пациент -> WebUI: Заполнение формы
activate WebUI

WebUI -> Gateway: POST /api/register
activate Gateway
Gateway -> Controller: registerUser()
activate Controller

Controller -> Service: validateData()
activate Service
Service -> Service: Проверка формата email
Service -> Service: Проверка сложности пароля
Service --> Controller: ValidationResult
deactivate Service

Controller -> Service: checkEmailUnique()
activate Service
Service -> DB: SELECT email WHERE email=?
activate DB
DB --> Service: Result
deactivate DB
Service --> Controller: EmailUnique
deactivate Service

alt Email уникален
    Controller -> Service: createUser()
    activate Service
    Service -> Service: Хеширование пароля (BCrypt)
    Service -> DB: INSERT user
    activate DB
    DB --> Service: User
    deactivate DB
    Service --> Controller: UserCreated
    deactivate Service
    
    Controller -> Service: generateActivationToken()
    activate Service
    Service --> Controller: Token
    deactivate Service
    
    Controller -> Email: sendActivationEmail()
    activate Email
    Email -> Email: Формирование письма
    Email -> Email: Отправка через SMTP
    Email --> Controller: EmailSent
    deactivate Email
    
    Controller --> Gateway: UserCreated
    deactivate Controller
    Gateway --> WebUI: 201 Created
    deactivate Gateway
    WebUI --> Пациент: Подтверждение регистрации
else Email существует
    Controller --> Gateway: 409 Conflict
    deactivate Controller
    Gateway --> WebUI: 409 Conflict
    deactivate Gateway
    WebUI --> Пациент: Ошибка: Email уже существует
end

deactivate WebUI
```

**Ключевые сообщения:**
- Синхронные вызовы: сплошная линия со стрелкой
- Возвраты: пунктирная линия
- Активация: вертикальный прямоугольник на lifeline

---

### 4. Class Diagram (Диаграмма классов)

```plantuml
class RegistrationController {
  -userService: UserService
  -emailService: EmailService
  +registerUser(request): ResponseEntity
  +activateAccount(token): ResponseEntity
}

class UserService {
  -userRepository: UserRepository
  -passwordEncoder: PasswordEncoder
  +validateData(data): ValidationResult
  +checkEmailUnique(email): boolean
  +createUser(data): User
  +activateUser(token): User
}

class User {
  -id: UUID
  -email: String
  -password: String
  -enabled: boolean
  -activationToken: String
  +isEnabled(): boolean
  +activate(): void
}

class EmailService {
  -mailSender: JavaMailSender
  +sendActivationEmail(user): void
}

class UserRepository {
  +findByEmail(email): Optional<User>
  +save(user): User
}

RegistrationController --> UserService
RegistrationController --> EmailService
UserService --> UserRepository
UserService --> User
EmailService --> User
```

**Связи:**
- **Ассоциация:** `AuthController` использует `AuthService`
- **Зависимость:** `AuthService` зависит от `UserRepository`
- **Реализация:** `UserRepositoryImpl` реализует `UserRepository`
- **Наследование:** `User` наследуется от `BaseEntity`

---

### 5. State Diagram (Диаграмма состояний)

```plantuml
[*] --> Unregistered: Начало
Unregistered --> RegistrationForm: Заполнение формы
RegistrationForm --> Validating: Отправка формы
Validating --> EmailChecking: Валидация успешна
Validating --> RegistrationForm: Ошибка валидации
EmailChecking --> UserCreated: Email уникален
EmailChecking --> RegistrationForm: Email существует
UserCreated --> EmailSent: Письмо отправлено
EmailSent --> PendingActivation: Ожидание активации
PendingActivation --> Activated: Переход по ссылке
PendingActivation --> Expired: Токен истёк
Expired --> RegistrationForm: Повторная регистрация
Activated --> [*]: Аккаунт активен
```

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

```plantuml
package "Registration Module" {
  [RegistrationController] as Controller
  [UserService] as Service
  [EmailService] as Email
  [UserRepository] as Repo
}

package "Database" {
  database "PostgreSQL" as DB
}

package "External" {
  [Email Server
(SMTP)] as SMTP
}

Controller --> Service
Service --> Repo
Repo --> DB
Email --> SMTP
Service --> Email
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

