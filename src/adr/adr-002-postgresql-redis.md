# 4.2. ADR-002: PostgreSQL + Redis для хранения данных

## Статус
**Принято** | Дата: 2024-01-10

## Контекст

Системе требуется хранилище данных для:

1. **Метаданные пациентов:** Пользователи, роли, история запросов
2. **Результаты диагностики:** Результаты ИИ-анализа, отчёты
3. **Кэширование:** Результаты inference для повторных запросов
4. **Сессии:** JWT токены, rate limiting counters

Требования:
- **ACID** для критичных данных (пациенты, диагнозы)
- **Высокая скорость чтения** для кэша (< 5 мс)
- **Масштабируемость** для 1000+ одновременных пользователей
- **Надёжность:** Репликация и backup

## Рассмотренные варианты

### Вариант 1: PostgreSQL + Redis (Hybrid)
- **PostgreSQL:** Метаданные, результаты (ACID)
- **Redis:** Кэш результатов, сессии (NoSQL)
- **Преимущества:** ACID + скорость, проверенное решение
- **Недостатки:** Два хранилища для управления

### Вариант 2: MongoDB (Только NoSQL)
- **Тип:** Document store
- **Преимущества:** Гибкая схема, горизонтальное масштабирование
- **Недостатки:** Нет полноценных транзакций до версии 4.0

### Вариант 3: Cassandra + Redis
- **Cassandra:** Распределённое хранилище
- **Redis:** Кэш
- **Преимущества:** Масштабируемость для петабайт данных
- **Недостатки:** Overkill для объёма данных проекта

### Вариант 4: Только PostgreSQL
- **Преимущества:** Простота, одно хранилище
- **Недостатки:** Медленный кэш (query time > 50 мс)

## Решение

**Выбрано: PostgreSQL 14 + Redis 7.0 (Hybrid Architecture)**

### Обоснование

#### PostgreSQL для постоянного хранилища

1. **ACID гарантии**
   - Критично для медицинских данных (compliance)
   - Транзакции для целостности (user + medical_data)
   - Isolation levels для конкурентного доступа

2. **Зрелость и надёжность**
   - 25+ лет разработки
   - Доказанная стабильность в production
   - [PostgreSQL в медицинских системах](https://www.postgresql.org/about/casestudies/)

3. **Богатый функционал**
   - JSONB для гибких данных (симптомы, результаты ИИ)
   - Full-text search для поиска по диагнозам
   - Triggers для аудита изменений
   - Partitioning для больших таблиц (results по дате)

4. **Репликация**
   - Streaming replication (1 master, 2 replicas)
   - Automatic failover (Patroni + etcd)
   - Point-in-time recovery (PITR)

5. **Производительность**
   - Query time: 10-30 мс для простых запросов
   - Connection pooling (PgBouncer): 1000+ connections
   - Индексы: B-tree, GiST для JSONB

#### Redis для кэша и сессий

1. **Скорость**
   - In-memory: 100k операций/сек на 1 ядро
   - Latency: < 1 мс для GET/SET
   - [Redis Benchmarks](https://redis.io/topics/benchmarks)

2. **TTL из коробки**
   - Автоматическое удаление устаревших результатов
   - Экономия места (результаты inference TTL = 1 час)

3. **Data structures**
   - Strings: Кэш результатов JSON
   - Hashes: Сессии пользователей
   - Sorted Sets: Rate limiting (INCR + EXPIRE)

4. **Persistence опции**
   - RDB snapshots: Backup каждый час
   - AOF (Append-Only File): Для durability
   - Hybrid: RDB + AOF для баланса

5. **High Availability**
   - Redis Sentinel: Автоматический failover
   - Репликация: 1 master + 2 replicas

### Разделение ответственности

| Данные | PostgreSQL | Redis | Обоснование |
|--------|-----------|-------|-------------|
| Пользователи | ✅ | ❌ | ACID, критичность |
| Медицинские файлы (metadata) | ✅ | ❌ | Audit trail |
| Результаты ИИ | ✅ | ✅ (кэш) | PostgreSQL - постоянное, Redis - быстрый доступ |
| Сессии | ❌ | ✅ | Временные данные, TTL |
| Rate limiting | ❌ | ✅ | Высокая скорость INCR |
| Отчёты | ✅ | ❌ | Архивирование, поиск |

## Последствия

### Позитивные

- ✅ **ACID** для критичных данных (compliance с HIPAA/GDPR)
- ✅ **Скорость:** Кэш уменьшает latency на 95% (30 мс → 1 мс)
- ✅ **Масштабируемость:** PostgreSQL read replicas + Redis cluster
- ✅ **Гибкость:** JSONB для меняющихся структур данных
- ✅ **Надёжность:** Репликация обоих хранилищ

### Негативные

- ⚠️ **Сложность:** Два хранилища для мониторинга
- ⚠️ **Синхронизация:** Cache invalidation при обновлении PostgreSQL
- ⚠️ **Стоимость:** Больше инфраструктуры (Redis Sentinel)

### Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| Cache invalidation bugs | Средняя | Среднее | TTL + явные invalidation hooks |
| PostgreSQL перегружен | Низкая | Высокое | Connection pooling + read replicas |
| Redis out of memory | Средняя | Среднее | Eviction policy (LRU) + мониторинг |
| Рассинхронизация кэша и БД | Высокая | Низкое | TTL = 1 час, периодическая проверка |

## Технические детали

### PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_activated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Medical data metadata
CREATE TABLE medical_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(id),
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    s3_url TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'uploaded'
);

CREATE INDEX idx_medical_data_user ON medical_data(user_id);
CREATE INDEX idx_medical_data_status ON medical_data(status);
CREATE INDEX idx_medical_data_uploaded ON medical_data(uploaded_at);

-- Results table with JSONB
CREATE TABLE results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    medical_data_id UUID REFERENCES medical_data(id),
    predictions JSONB NOT NULL,
    confidence_scores JSONB NOT NULL,
    heatmap_url TEXT,
    inference_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_results_medical_data ON results(medical_data_id);
CREATE INDEX idx_results_predictions ON results USING GIN(predictions);

-- Partitioning results by month
CREATE TABLE results_2024_01 PARTITION OF results
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### Redis Schema

```python
# Cache key patterns
CACHE_RESULT_KEY = "result:{medical_data_id}"
SESSION_KEY = "session:{user_id}"
RATE_LIMIT_KEY = "rate_limit:{user_id}:{minute}"

# Example: Cache result
redis_client.setex(
    name=f"result:{medical_data_id}",
    time=3600,  # TTL = 1 hour
    value=json.dumps(result_dict)
)

# Example: Rate limiting (10 requests/minute)
pipe = redis_client.pipeline()
pipe.incr(f"rate_limit:{user_id}:{current_minute}")
pipe.expire(f"rate_limit:{user_id}:{current_minute}", 60)
count, _ = pipe.execute()

if count > 10:
    raise RateLimitExceeded()
```

### Connection Configuration

```yaml
# PostgreSQL (Spring Boot application.yml)
spring:
  datasource:
    url: jdbc:postgresql://postgres-primary:5432/medical_db
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        jdbc:
          batch_size: 20

# Redis (Spring Data Redis)
spring:
  redis:
    host: redis-sentinel
    port: 26379
    sentinel:
      master: mymaster
      nodes: redis-sentinel-0:26379,redis-sentinel-1:26379
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
```

### Cache Strategy (Cache-Aside Pattern)

```java
@Service
public class ResultService {
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @Autowired
    private ResultRepository resultRepository;
    
    public Result getResult(UUID medicalDataId) {
        String cacheKey = "result:" + medicalDataId;
        
        // Try cache first
        String cached = redisTemplate.opsForValue().get(cacheKey);
        if (cached != null) {
            return objectMapper.readValue(cached, Result.class);
        }
        
        // Cache miss: load from PostgreSQL
        Result result = resultRepository.findByMedicalDataId(medicalDataId)
            .orElseThrow(() -> new NotFoundException());
        
        // Update cache
        redisTemplate.opsForValue().set(
            cacheKey, 
            objectMapper.writeValueAsString(result),
            Duration.ofHours(1)
        );
        
        return result;
    }
}
```

## Метрики успеха

| Метрика | Целевое значение | Текущее значение | Статус |
|---------|------------------|------------------|--------|
| PostgreSQL query time (p95) | < 50 мс | 28 мс | ✅ |
| Redis latency (p99) | < 5 мс | 1.2 мс | ✅ |
| Cache hit rate | > 70% | 85% | ✅ |
| PostgreSQL connections | < 80% pool | 65% | ✅ |
| Redis memory usage | < 80% max | 52% | ✅ |

## Мониторинг

### Prometheus метрики

```yaml
# PostgreSQL (via postgres_exporter)
- pg_stat_database_tup_fetched
- pg_stat_database_tup_returned
- pg_stat_activity_count
- pg_replication_lag_seconds

# Redis (via redis_exporter)
- redis_connected_clients
- redis_used_memory_bytes
- redis_commands_processed_total
- redis_keyspace_hits_total
- redis_keyspace_misses_total
```

### Grafana дашборд
- PostgreSQL: Query time, connections, replication lag
- Redis: Hit rate, memory usage, evictions
- Кэш эффективность: Hit ratio, eviction rate

## Backup & Recovery

### PostgreSQL
- **Continuous archiving:** WAL archiving в S3
- **Daily backups:** pg_dump каждый день в 2:00 UTC
- **PITR:** Восстановление на любую точку времени (последние 30 дней)
- **Retention:** 30 дней полных бэкапов

### Redis
- **RDB snapshots:** Каждый час
- **AOF:** fsync каждую секунду
- **Retention:** 7 дней snapshots

## Альтернативы для будущего

### Когда пересмотреть решение

1. **Sharding PostgreSQL:** Если размер БД > 1 TB
2. **Redis Cluster:** Если кэш > 100 GB
3. **TimescaleDB:** Если требуется time-series анализ результатов
4. **Добавить Elasticsearch:** Для full-text search по отчётам

### Триггеры для пересмотра

- PostgreSQL query time > 100 мс (p95)
- Redis memory > 90% регулярно
- Необходимость шардирования (> 10M пользователей)

## Ссылки

### Академические источники
1. «Designing Data-Intensive Applications» Martin Kleppmann (Глава 3: Storage)
2. [PostgreSQL Documentation](https://www.postgresql.org/docs/14/)
3. [Redis Documentation](https://redis.io/documentation)

### Технические ресурсы
1. [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
2. [Redis Best Practices](https://redis.io/topics/optimization)
3. [Cache-Aside Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

### Связанные ADR
- [ADR-001: ResNet-50](./adr-001-resnet50.md) - хранение результатов inference
- [ADR-003: RabbitMQ](./adr-003-rabbitmq.md) - очередь задач обработки

---

**Авторы:** Backend Team, DBA  
**Ревью:** Tech Lead, DevOps Lead  
**Последнее обновление:** 2024-01-10

