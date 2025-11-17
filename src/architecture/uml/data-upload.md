# UML Диаграммы: Загрузка данных

## Функция 2: Загрузка медицинских данных

### 1. Use Case Diagram (Диаграмма вариантов использования)

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_1_UseCase.drawio}

**Актёры:**
- **Пациент** (Patient)
- **Система хранения** (Storage System)

**Варианты использования:**
1. **Загрузка изображений**
   - Первичный актёр: Пациент
   - Предусловия: Пациент аутентифицирован
   - Постусловия: Изображение сохранено в S3
   
2. **Загрузка описания симптомов**
   - Первичный актёр: Пациент
   - Предусловия: Пациент аутентифицирован
   - Постусловия: Текст сохранён, отправлен в очередь
   
3. **Валидация файлов**
   - Первичный актёр: Система
   - Связь: `<<include>>` для обоих сценариев загрузки

**Связи:**
- `<<include>>`: Загрузка включает валидацию
- `<<extend>>`: Предпросмотр расширяет загрузку изображения

---

### 2. Activity Diagram (Диаграмма активностей)

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_2_Activity.drawio}

**Параллельные активности:**
- Fork: Разделение на параллельные потоки
- Join: Синхронизация потоков

---

### 3. Sequence Diagram (Диаграмма последовательности)

**Участники:**
- Patient (Пациент)
- WebUI (React)
- APIGateway (Spring Cloud)
- DataUploadController
- FileValidator
- S3Client
- PostgreSQL
- RabbitMQ

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_3_Sequence.drawio}

---

### 4. Class Diagram (Диаграмма классов)

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_4_Class.drawio}

---

### 5. State Diagram (Диаграмма состояний)

**Объект:** File Upload

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_5_State.drawio}

**Состояния:**
1. **Validating:** Проверка формата и размера
2. **Uploading:** Загрузка в S3
3. **Uploaded:** Файл сохранён в S3
4. **InQueue:** Сообщение в RabbitMQ
5. **Processing:** ML Service обрабатывает
6. **Completed:** Обработка завершена
7. **Failed:** Ошибка на любом этапе
8. **Archived:** Перемещён в долгосрочное хранилище

---

### 6. Component Diagram (Диаграмма компонентов)

@drawio{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/UML_DATA_UPLOAD_6_Component.drawio}

**Внешние зависимости:**
- AWS SDK (S3 Client)
- Spring AMQP (RabbitMQ)
- Spring Data JPA (PostgreSQL)

---

## Источники

- «Clean Architecture» Robert Martin
- [AWS S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/best-practices.html)
- [RabbitMQ Patterns](https://www.rabbitmq.com/getstarted.html)

