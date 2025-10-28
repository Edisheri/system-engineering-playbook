# 4.3. ADR-003: RabbitMQ для асинхронной обработки

## Статус
**Принято** | Дата: 2024-01-12

## Контекст

Система требует асинхронной обработки медицинских данных для:

1. **Долгие операции:** ИИ-анализ изображений (2 секунды)
2. **Отказоустойчивость:** Повторная обработка при сбоях
3. **Масштабируемость:** Обработка 1000+ одновременных запросов
4. **Разделение ответственности:** Data Upload Service ≠ ML Inference Service

Требования:
- **Гарантия доставки:** At-least-once delivery
- **Retry механизм:** Повторная обработка неудачных задач
- **Dead Letter Queue:** Изоляция проблемных сообщений
- **Throughput:** ≥ 100 сообщений/секунду

## Рассмотренные варианты

### Вариант 1: RabbitMQ
- **Тип:** Message broker (AMQP 0.9.1)
- **Преимущества:** Гарантии доставки, DLQ, простота
- **Недостатки:** Меньший throughput, чем Kafka

### Вариант 2: Apache Kafka
- **Тип:** Distributed streaming platform
- **Преимущества:** Высокий throughput (1M msg/sec), persistence
- **Недостатки:** Сложность, overkill для проекта

### Вариант 3: AWS SQS
- **Тип:** Managed queue service
- **Преимущества:** Serverless, автомасштабирование
- **Недостатки:** Vendor lock-in, задержки (visibility timeout)

### Вариант 4: Redis Pub/Sub
- **Тип:** In-memory messaging
- **Преимущества:** Скорость, простота
- **Недостатки:** Нет гарантий доставки, нет persistence

## Решение

**Выбрано: RabbitMQ 3.9**

### Обоснование

1. **AMQP протокол**
   - Стандартизированный протокол (ISO/IEC 19464)
   - Гарантии доставки: At-least-once (acknowledgments)
   - Publisher confirms для надёжности

2. **Гибкие паттерны маршрутизации**
   - **Direct exchange:** Для специфичных задач (medical_data)
   - **Topic exchange:** Для разных типов данных (image.xray, text.symptoms)
   - **Dead Letter Exchange:** Автоматическая изоляция проблемных сообщений

3. **Зрелость и надёжность**
   - 13+ лет в production
   - Используется Uber, Reddit, NASA
   - [RabbitMQ Case Studies](https://www.rabbitmq.com/case-studies.html)

4. **Throughput достаточен**
   - 10k-50k msg/sec на стандартном сервере
   - Наше требование: ~100-200 msg/sec
   - Запас производительности: 50x

5. **Retry механизм из коробки**
   - TTL (Time-To-Live) для сообщений
   - Dead Letter Queue для неудачных попыток
   - Exponential backoff через TTL

6. **Management UI**
   - Встроенный веб-интерфейс для мониторинга
   - Метрики: queue size, publish rate, ack rate
   - Визуализация топологии exchanges/queues

7. **Простота vs Kafka**
   - Не требуется Zookeeper/KRaft
   - Меньше ресурсов (CPU, RAM)
   - Быстрее setup и maintenance

### Почему не Kafka?

| Критерий | RabbitMQ | Kafka | Победитель |
|----------|----------|-------|------------|
| Throughput | 50k msg/sec | 1M msg/sec | Kafka |
| Latency | 1-5 мс | 5-10 мс | RabbitMQ |
| Гарантии доставки | At-least-once | At-least-once | Ничья |
| Complexity | Низкая | Высокая | RabbitMQ |
| Retention | Не нужен | Долгосрочное хранение | Kafka |
| **Наши требования** | ✅ Достаточно | ❌ Overkill | **RabbitMQ** |

**Вывод:** Kafka избыточен для throughput 100-200 msg/sec и не требуется event sourcing.

## Последствия

### Позитивные

- ✅ **Отказоустойчивость:** Сообщения не теряются при сбое consumer
- ✅ **Масштабируемость:** Multiple consumers для параллельной обработки
- ✅ **Разделение:** Data Upload Service не ждёт ML Inference
- ✅ **Retry:** Автоматическая повторная обработка неудачных задач
- ✅ **Monitoring:** Prometheus exporter для метрик

### Негативные

- ⚠️ **Single point of failure:** Без HA кластера
- ⚠️ **Ordering:** Не гарантирует порядок при multiple consumers
- ⚠️ **Memory:** In-memory queue может заполниться при высокой нагрузке

### Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| RabbitMQ падает | Низкая | Высокое | Кластер (3 ноды), Quorum queues |
| Queue переполнена | Средняя | Среднее | Max-length + TTL, dead letter queue |
| Consumer медленный | Средняя | Среднее | Autoscaling consumers (KEDA) |
| Сообщение застревает | Низкая | Низкое | Message TTL = 24 часа |

## Технические детали

### Архитектура очередей

```
┌──────────────────────────────────────────────────────┐
│           RabbitMQ Cluster (3 nodes)                 │
│                                                      │
│  ┌─────────────────┐         ┌─────────────────┐   │
│  │  medical_exchange│────────>│ medical_data    │   │
│  │   (Direct)      │         │   (Queue)       │   │
│  └─────────────────┘         └─────────────────┘   │
│         │                            │              │
│         │ routing_key:               │ consumers    │
│         │ "medical.data"             ↓              │
│         │                    ┌─────────────────┐   │
│         │                    │  ML Inference   │   │
│         │                    │   Service       │   │
│         │                    │  (3 replicas)   │   │
│         │                    └─────────────────┘   │
│         │                                           │
│         │ DLX                                       │
│         ↓                                           │
│  ┌─────────────────┐         ┌─────────────────┐   │
│  │  dlx_exchange   │────────>│    dlq          │   │
│  │   (Fanout)      │         │ (Dead Letter)   │   │
│  └─────────────────┘         └─────────────────┘   │
│                                      │              │
│                                      │ manual review│
│                                      ↓              │
│                              ┌─────────────────┐   │
│                              │  Alert Service  │   │
│                              └─────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Queue Configuration

```python
# Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq-cluster',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials('user', 'password'),
        heartbeat=600,
        blocked_connection_timeout=300
    )
)
channel = connection.channel()

# Main exchange
channel.exchange_declare(
    exchange='medical_exchange',
    exchange_type='direct',
    durable=True
)

# Dead Letter Exchange
channel.exchange_declare(
    exchange='dlx_exchange',
    exchange_type='fanout',
    durable=True
)

# Main queue with DLX
channel.queue_declare(
    queue='medical_data',
    durable=True,
    arguments={
        'x-dead-letter-exchange': 'dlx_exchange',
        'x-message-ttl': 86400000,  # 24 hours
        'x-max-length': 10000,       # Max 10k messages
        'x-max-priority': 10,        # Priority queue
        'x-queue-type': 'quorum'     # Quorum queue (HA)
    }
)

# Dead Letter Queue
channel.queue_declare(
    queue='dlq',
    durable=True
)

# Bindings
channel.queue_bind(
    exchange='medical_exchange',
    queue='medical_data',
    routing_key='medical.data'
)

channel.queue_bind(
    exchange='dlx_exchange',
    queue='dlq'
)
```

### Producer (Data Upload Service)

```java
@Service
public class MessageProducer {
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public void sendToMLService(MedicalData data) {
        MessageProperties props = new MessageProperties();
        props.setDeliveryMode(MessageDeliveryMode.PERSISTENT);
        props.setPriority(data.isUrgent() ? 10 : 5);
        props.setExpiration("86400000"); // 24h TTL
        
        Message message = new Message(
            objectMapper.writeValueAsBytes(data),
            props
        );
        
        // Publisher confirms enabled
        rabbitTemplate.convertAndSend(
            "medical_exchange",
            "medical.data",
            message
        );
    }
}
```

### Consumer (ML Inference Service)

```python
def callback(ch, method, properties, body):
    try:
        # Parse message
        data = json.loads(body)
        medical_data_id = data['medical_data_id']
        
        # Process (ML inference)
        result = ml_service.process(medical_data_id)
        
        # Save result
        result_repository.save(result)
        
        # Acknowledge
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        
        # Retry logic
        retry_count = properties.headers.get('x-retry-count', 0)
        
        if retry_count < 3:
            # Requeue with delay (exponential backoff)
            delay = 2 ** retry_count * 1000  # 1s, 2s, 4s
            
            ch.basic_publish(
                exchange='medical_exchange',
                routing_key='medical.data',
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={'x-retry-count': retry_count + 1},
                    expiration=str(delay)
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Max retries reached -> DLQ
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False  # Send to DLX
            )

# Consumer setup
channel.basic_qos(prefetch_count=1)  # Fair dispatch
channel.basic_consume(
    queue='medical_data',
    on_message_callback=callback,
    auto_ack=False  # Manual ack
)

channel.start_consuming()
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: rabbitmq
spec:
  serviceName: rabbitmq
  replicas: 3
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
    spec:
      containers:
      - name: rabbitmq
        image: rabbitmq:3.9-management
        ports:
        - containerPort: 5672
          name: amqp
        - containerPort: 15672
          name: management
        env:
        - name: RABBITMQ_DEFAULT_USER
          valueFrom:
            secretKeyRef:
              name: rabbitmq-secret
              key: username
        - name: RABBITMQ_DEFAULT_PASS
          valueFrom:
            secretKeyRef:
              name: rabbitmq-secret
              key: password
        - name: RABBITMQ_ERLANG_COOKIE
          value: "secret-cookie"
        volumeMounts:
        - name: data
          mountPath: /var/lib/rabbitmq
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

## Метрики успеха

| Метрика | Целевое значение | Текущее значение | Статус |
|---------|------------------|------------------|--------|
| Message throughput | ≥ 100 msg/sec | 150 msg/sec | ✅ |
| Publish latency (p95) | < 10 мс | 3 мс | ✅ |
| Consumer latency | < 5 секунд | 2.1 секунды | ✅ |
| Message loss rate | 0% | 0% | ✅ |
| DLQ rate | < 1% | 0.2% | ✅ |

## Мониторинг

### Prometheus метрики (rabbitmq_exporter)

```yaml
# Queue metrics
- rabbitmq_queue_messages_ready
- rabbitmq_queue_messages_unacknowledged
- rabbitmq_queue_consumers

# Message rates
- rabbitmq_queue_messages_published_total
- rabbitmq_queue_messages_delivered_total
- rabbitmq_queue_messages_redelivered_total

# Cluster health
- rabbitmq_up
- rabbitmq_node_disk_free_bytes
- rabbitmq_node_mem_used_bytes
```

### Grafana дашборд
- Queue size (ready, unacked)
- Publish/consume rate
- Consumer lag
- DLQ size (alarm if > 10)

### Alerting

```yaml
# AlertManager rules
groups:
- name: rabbitmq
  rules:
  - alert: RabbitMQDown
    expr: rabbitmq_up == 0
    for: 1m
    annotations:
      summary: "RabbitMQ is down"
      
  - alert: RabbitMQQueueOverflow
    expr: rabbitmq_queue_messages_ready > 5000
    for: 5m
    annotations:
      summary: "Queue overflow: {{ $value }} messages"
      
  - alert: RabbitMQHighDLQ
    expr: rabbitmq_queue_messages{queue="dlq"} > 50
    for: 10m
    annotations:
      summary: "High DLQ rate: {{ $value }} failed messages"
```

## Disaster Recovery

### Backup
- **Queue definitions:** Export via management API (daily)
- **Messages:** Persistence на диске (durable queues)
- **Cluster state:** Etcd backup (hourly)

### Recovery
1. **Single node failure:** Автоматический failover (quorum queues)
2. **Cluster failure:** Restore от последнего backup
3. **Data loss:** Reprocess от последнего checkpoint в PostgreSQL

## Альтернативы для будущего

### Когда пересмотреть решение

1. **Apache Kafka**: Если throughput > 10k msg/sec
2. **AWS SQS**: Если миграция в AWS и не требуется on-premise
3. **NATS**: Если требуется ultra-low latency (< 1 мс)

### Триггеры для пересмотра

- Throughput требование > 50k msg/sec
- Требуется event sourcing (long retention)
- Требуется exactly-once delivery semantics

## Ссылки

### Академические источники
1. [AMQP 0.9.1 Specification](https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf)
2. «Enterprise Integration Patterns» Gregor Hohpe

### Технические ресурсы
1. [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
2. [RabbitMQ Best Practices](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)
3. [Quorum Queues](https://www.rabbitmq.com/quorum-queues.html)

### Связанные ADR
- [ADR-001: ResNet-50](./adr-001-resnet50.md) - асинхронная обработка изображений
- [ADR-002: PostgreSQL + Redis](./adr-002-postgresql-redis.md) - хранение результатов

---

**Авторы:** Backend Team, DevOps  
**Ревью:** Tech Lead, Solutions Architect  
**Последнее обновление:** 2024-01-12

