# IDEF3: Процесс P1 — Регистрация пациента

## Диаграмма процесса P1

```mermaid
graph TB
    Start([Начало])
    
    E1[Пациент открывает<br/>форму регистрации]
    E2[Заполняет поля<br/>Email, Пароль, ФИО]
    
    J1{Email<br/>валиден?}
    
    E3[Система проверяет<br/>уникальность email]
    
    J2{Email уже<br/>существует?}
    
    E4[Хеширование<br/>пароля BCrypt]
    E5[Сохранение в<br/>PostgreSQL]
    E6[Генерация токена<br/>активации]
    E7[Отправка письма<br/>с токеном]
    
    E8[Показать ошибку:<br/>"Невалидный email"]
    E9[Показать ошибку:<br/>"Email занят"]
    
    E10[Показать сообщение:<br/>"Проверьте почту"]
    
    E11[Пациент кликает<br/>по ссылке в письме]
    E12[Система активирует<br/>аккаунт]
    
    End([Конец])
    
    Start --> E1
    E1 --> E2
    E2 --> J1
    
    J1 -->|Нет| E8
    E8 --> E2
    
    J1 -->|Да| E3
    E3 --> J2
    
    J2 -->|Да| E9
    E9 --> End
    
    J2 -->|Нет| E4
    E4 --> E5
    E5 --> E6
    E6 --> E7
    E7 --> E10
    E10 --> E11
    E11 --> E12
    E12 --> End
    
    style Start fill:#67c23a,stroke:#4a9428,stroke-width:2px
    style End fill:#f56c6c,stroke:#c94545,stroke-width:2px
    style J1 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style J2 fill:#e6a23c,stroke:#b8821e,stroke-width:2px
    style E4 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style E5 fill:#4a90e2,stroke:#2e5c8a,stroke-width:2px,color:#fff
    style E12 fill:#67c23a,stroke:#4a9428,stroke-width:2px
```

## Описание процесса P1

### Участники
- **Пациент** — инициирует регистрацию
- **Web UI (React)** — отображает форму
- **Auth Service** — обрабатывает регистрацию
- **PostgreSQL** — хранит данные пользователей
- **Email Service** — отправляет письмо

### Временные связи

| Событие | Последующее событие | Условие | Задержка |
|---------|---------------------|---------|----------|
| E2 → E3 | Валидация успешна | Email корректен | 50 мс |
| E3 → E4 | Email уникален | Нет дубликатов | 100 мс |
| E4 → E5 | Пароль захеширован | BCrypt | 200 мс |
| E7 → E11 | Письмо доставлено | SMTP успех | 5-30 сек |
| E11 → E12 | Токен валиден | Не истёк | 100 мс |

### Точки синхронизации
- **После E3**: Обязательна проверка уникальности
- **После E7**: Асинхронное ожидание действия пользователя
- **После E11**: Проверка валидности токена

### UOB (Unit of Behavior)

**UOB-1: Валидация данных**
- Input: Email, Password
- Process: Regex validation
- Output: Валидированные данные или ошибка

**UOB-2: Проверка уникальности**
- Input: Email
- Process: SELECT FROM users WHERE email=?
- Output: Boolean (exists/not exists)

**UOB-3: Создание пользователя**
- Input: User data
- Process: Hash password, INSERT INTO users
- Output: User ID

**UOB-4: Отправка письма**
- Input: Email, Token
- Process: SMTP send
- Output: Message ID

### Временная диаграмма

```
t=0s    Начало регистрации
t=0.5s  Валидация email
t=0.6s  Проверка уникальности
t=0.8s  Хеширование пароля
t=1.0s  Сохранение в БД
t=1.1s  Генерация токена
t=1.2s  Отправка письма
t=5-30s Доставка письма (асинхронно)
...     Ожидание действия пользователя
t=X     Клик по ссылке
t=X+0.1s Активация аккаунта
t=X+0.2s Конец процесса
```

## Источники
- IDEF3 Process Description Capture Method
- Spring Security Documentation

