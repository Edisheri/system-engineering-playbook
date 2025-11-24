# UML Диаграммы: Система продажи железнодорожных билетов

## Полный набор UML диаграмм

### 1. Use Case Diagram (Диаграмма вариантов использования)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_1_UseCase.drawio"></iframe>

**Актёры:**
- **Гость** - неавторизованный пользователь
- **Пользователь** - авторизованный пользователь (наследует от Гостя)
- **Администратор** - администратор системы (наследует от Пользователя)

**Основные варианты использования:**

**Для Гостя:**
- Регистрация (включает: ввод ФИО, логина, пароля, телефона; расширяет: ввод паспортных данных)
- Просмотр расписания поездов
- Просмотр тарифов и акций

**Для Пользователя:**
- Все функции Гостя +
- Управление аккаунтом (удаление, редактирование)
- Создание пассажиров
- Купить билет (включает: ввод даты, места отправления/прибытия, выбор поезда, вагона, места, добавление пассажиров, оплату; расширяет: добавление РЖД бонус)

**Для Администратора:**
- Все функции Пользователя +
- Управление маршрутами (добавление, удаление, редактирование)

---

### 2. Activity Diagram (Диаграмма активностей)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_2_Activity.drawio"></iframe>

**Процесс покупки билета:**

1. **Вход в систему** - пользователь заходит на сайт/приложение
2. **Поиск маршрута** - ввод данных о поездке
3. **Decision: Маршрут найден?**
   - Да → продолжить
   - Нет → сообщение об отсутствии маршрута → конец
4. **Выбор поезда** - из списка доступных
5. **Выбор места** - выбор вагона и конкретного места
6. **Decision: Есть аккаунт?**
   - Да → аутентификация пользователя
   - Нет → регистрация
7. **Ввод данных о пасажирах** - ФИО, паспортные данные
8. **Ввод дополнительных услуг** - питание, постельное белье и т.д.
9. **Оплата** - обработка платежа
10. **Fork (параллельные процессы):**
    - Формирование электронного билета
    - Отправка чека
11. **Конец процесса**

---

### 3. Sequence Diagram (Диаграмма последовательности)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_3_Sequence.drawio"></iframe>

**Участники:**
- Пользователь
- WebUI (пользовательский интерфейс)
- APIGateway (шлюз API)
- TicketService (сервис билетов)
- RouteService (сервис маршрутов)
- PaymentService (сервис оплаты)
- PostgreSQL (база данных)
- EmailService (сервис email)

**Последовательность взаимодействий:**

1. Поиск маршрута: UI → API → RouteService → DB → возврат списка маршрутов
2. Проверка авторизации (если не авторизован): вход/регистрация через API
3. Создание бронирования: UI → API → TicketService → DB (транзакция: INSERT booking, UPDATE seat status)
4. Обработка платежа: UI → API → PaymentService → проверка карты → UPDATE booking status
5. Параллельная отправка: email с билетом и чеком
6. Возврат результата пользователю

---

### 4. Class Diagram (Диаграмма классов)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_4_Class.drawio"></iframe>

**Основные классы:**

**User (Пользователь)**
- id, email, password, phone, fio, passportData
- login(), register(), updateProfile()

**Passenger (Пассажир)**
- id, userId, fio, passportNumber, birthDate
- create(), update()

**Route (Маршрут)**
- id, trainNumber, departure, arrival, departureTime, arrivalTime, duration
- search(), getAvailableSeats()

**Train (Поезд)**
- id, number, type, wagons
- getWagons()

**Wagon (Вагон)**
- id, number, type, seats
- getAvailableSeats()

**Seat (Место)**
- id, number, wagonId, status, price
- reserve(), release()

**Booking (Бронирование)**
- id, userId, routeId, passengers, seats, totalPrice, status, createdAt
- create(), cancel(), confirm()

**Payment (Платеж)**
- id, bookingId, amount, status, method, transactionId
- process(), refund()

**Ticket (Билет)**
- id, bookingId, passengerId, seatId, ticketNumber, qrCode
- generate(), send()

**Связи:**
- User 1 --- 0..* Passenger
- User 1 --- 0..* Booking
- Route 1 --- 1 Train
- Train 1 --- 1..* Wagon
- Wagon 1 --- 1..* Seat
- Booking 1 --- 1..* Passenger
- Booking 1 --- 1..* Seat
- Booking 1 --- 1 Payment
- Booking 1 --- 1..* Ticket

---

### 5. State Diagram (Диаграмма состояний)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_5_State.drawio"></iframe>

**Состояния процесса покупки билета:**

1. **Поиск** - пользователь ищет маршрут
2. **Выбор Маршрута** - выбор поезда и места
3. **Аутентификация** - вход или регистрация
4. **Ввод Данных** - ввод данных пассажиров
5. **Выбор Услуг** - выбор дополнительных услуг
6. **Оплата** - обработка платежа
7. **Ожидание Подтверждения** - ожидание ответа от платежной системы
8. **Ошибка Оплаты** - платеж отклонен (возможность повторить или отменить)
9. **Формирование Билета** - генерация и отправка билета
10. **Завершено** - процесс успешно завершен

**Переходы:**
- Из любого состояния возможен возврат к предыдущему
- При ошибке оплаты - возможность повторить или полностью отменить
- Успешный путь: Поиск → Выбор → Аутентификация → Данные → Услуги → Оплата → Ожидание → Билет → Завершено

---

### 6. Component Diagram (Диаграмма компонентов)

<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url=https://raw.githubusercontent.com/Edisheri/system-engineering-playbook/main/diagrams-codes/UML_REGISTRATION_6_Component.drawio"></iframe>

**Архитектура системы:**

**Frontend:**
- WebUI (React) - веб-приложение
- MobileApp (React Native) - мобильное приложение

**API Gateway:**
- Kong Gateway - единая точка входа
- Authentication (JWT) - аутентификация

**Backend Services (микросервисы):**
- User Service (Spring Boot) - управление пользователями
- Route Service (Spring Boot) - управление маршрутами
- Booking Service (Spring Boot) - управление бронированиями
- Payment Service (Spring Boot) - обработка платежей
- Notification Service (Node.js) - отправка уведомлений

**External Services:**
- Payment Gateway (Sberbank API) - платежный шлюз
- Email Service (SMTP) - отправка email
- SMS Service (Twilio) - отправка SMS

**Data Storage:**
- PostgreSQL - основная БД (пользователи, бронирования, маршруты)
- Redis - кеш и сессии
- MongoDB - логи системы

**Message Queue:**
- RabbitMQ - очередь сообщений для асинхронной обработки

---

## Источники

- PlantUML Documentation
- UML 2.5 Specification
- Domain-Driven Design Patterns
- Microservices Architecture Patterns
