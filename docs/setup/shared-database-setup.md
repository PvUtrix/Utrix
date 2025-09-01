# 🗄️ Настройка единой базы данных для всех сервисов

## Обзор
Это руководство описывает настройку **единой базы данных PostgreSQL** для всех сервисов персональной системы, включая Gitea, Coolify и другие приложения.

## 🎯 Преимущества единой базы данных

✅ **Экономия ресурсов** - меньше памяти и CPU  
✅ **Простота управления** - одна точка резервного копирования  
✅ **Единый мониторинг** - все метрики в одном месте  
✅ **Кросс-сервисные запросы** - возможность объединения данных  
✅ **Простота развертывания** - меньше контейнеров для управления  

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Gitea      │    │    Coolify      │    │   Другие       │
│   (Git-сервер) │    │  (Деплой)       │    │   Сервисы      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Единая PostgreSQL      │
                    │   База данных            │
                    │   ┌─────────────────────┐ │
                    │   │ Схема: gitea        │ │
                    │   │ Схема: coolify      │ │
                    │   │ Схема: monitoring   │ │
                    │   │ Схема: logs         │ │
                    │   └─────────────────────┘ │
                    └───────────────────────────┘
```

## 🚀 Быстрая настройка

### 1. Создайте единую базу данных PostgreSQL

```bash
# В Coolify создайте новый сервис PostgreSQL
docker run -d \
  --name shared-postgres \
  --network personal-system-network \
  -e POSTGRES_DB=personal_system_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secure_password_123 \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine
```

### 2. Создайте схемы для разных сервисов

```sql
-- Подключитесь к базе данных
psql -h localhost -U postgres -d personal_system_db

-- Создайте схемы для изоляции данных
CREATE SCHEMA IF NOT EXISTS gitea;
CREATE SCHEMA IF NOT EXISTS coolify;
CREATE SCHEMA IF NOT EXISTS monitoring;
CREATE SCHEMA IF NOT EXISTS logs;

-- Создайте пользователей для каждого сервиса
CREATE USER gitea_user WITH PASSWORD 'gitea_password';
CREATE USER coolify_user WITH PASSWORD 'coolify_password';

-- Назначьте права на схемы
GRANT USAGE ON SCHEMA gitea TO gitea_user;
GRANT ALL PRIVILEGES ON SCHEMA gitea TO gitea_user;

GRANT USAGE ON SCHEMA coolify TO coolify_user;
GRANT ALL PRIVILEGES ON SCHEMA coolify TO coolify_user;
```

### 3. Настройте Gitea для использования единой базы

```yaml
# В переменных окружения Gitea
GITEA__database__DB_TYPE: postgres
GITEA__database__HOST: shared-postgres
GITEA__database__NAME: personal_system_db
GITEA__database__USER: gitea_user
GITEA__database__PASSWD: gitea_password
GITEA__database__PORT: 5432
GITEA__database__SCHEMA: gitea
```

## ⚙️ Детальная настройка

### Переменные окружения

Создайте файл `.env` в корне проекта:

```bash
# Основные настройки базы данных
SHARED_DB_HOST=localhost
SHARED_DB_PORT=5432
SHARED_DB_NAME=personal_system_db
SHARED_DB_USER=postgres
SHARED_DB_PASSWORD=secure_password_123

# Настройки Redis
SHARED_REDIS_HOST=localhost
SHARED_REDIS_PORT=6379
SHARED_REDIS_PASSWORD=redis_password_123

# Настройки Gitea
GITEA_DOMAIN=git.yourdomain.com
GITEA_SECRET_KEY=your-secret-key-here
GITEA_INTERNAL_TOKEN=your-internal-token-here
```

### Настройка в Coolify

1. **Создайте сервис PostgreSQL:**
   - Имя: `shared-postgres`
   - Порт: `5432`
   - База данных: `personal_system_db`
   - Пользователь: `postgres`
   - Пароль: `secure_password_123`

2. **Создайте сервис Redis (опционально):**
   - Имя: `shared-redis`
   - Порт: `6379`
   - Пароль: `redis_password_123`

3. **Создайте сервис Gitea:**
   - Используйте конфигурацию из `config/automation/gitea-shared-db.yaml`
   - Подключите к общей базе данных

## 🔧 Конфигурация сервисов

### Gitea

```yaml
# config/automation/gitea-shared-db.yaml
gitea:
  container:
    environment:
      # Настройки базы данных - ИСПОЛЬЗУЕМ ЕДИНУЮ БАЗУ
      GITEA__database__DB_TYPE: postgres
      GITEA__database__HOST: shared-postgres
      GITEA__database__NAME: personal_system_db
      GITEA__database__USER: gitea_user
      GITEA__database__PASSWD: gitea_password
      GITEA__database__PORT: 5432
      GITEA__database__SCHEMA: gitea
      
      # Настройки Redis
      GITEA__cache__ADAPTER: redis
      GITEA__cache__HOST: shared-redis
      GITEA__cache__PORT: 6379
      GITEA__cache__PASSWORD: redis_password_123
```

### Coolify

```yaml
# В настройках Coolify
database:
  type: postgres
  host: shared-postgres
  port: 5432
  name: personal_system_db
  user: coolify_user
  password: coolify_password
  schema: coolify
```

## 📊 Мониторинг и метрики

### Prometheus метрики

```yaml
# postgres-exporter для мониторинга базы данных
postgres-exporter:
  image: prometheuscommunity/postgres-exporter:latest
  environment:
    DATA_SOURCE_NAME: "postgresql://postgres:password@shared-postgres:5432/personal_system_db?sslmode=disable"
  ports:
    - "9187:9187"
```

### Проверки здоровья

```yaml
healthcheck:
  database:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 30s
    timeout: 10s
    retries: 3
```

## 🛡️ Безопасность

### Изоляция данных

```sql
-- Каждый сервис использует свою схему
-- Gitea: схема 'gitea'
-- Coolify: схема 'coolify'
-- Мониторинг: схема 'monitoring'

-- Пользователи имеют доступ только к своим схемам
GRANT USAGE ON SCHEMA gitea TO gitea_user;
GRANT ALL PRIVILEGES ON SCHEMA gitea TO gitea_user;
```

### Шифрование соединений

```yaml
# Для продакшена включите SSL
GITEA__database__SSL_MODE: require
GITEA__database__SSL_CERT: /path/to/cert
GITEA__database__SSL_KEY: /path/to/key
GITEA__database__SSL_CA: /path/to/ca
```

## 💾 Резервное копирование

### Автоматическое резервное копирование

```bash
#!/bin/bash
# backup-database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/database"

# Резервное копирование всей базы данных
pg_dump -h localhost -U postgres -d personal_system_db \
  --format=custom --verbose \
  --file="$BACKUP_DIR/full_backup_$DATE.dump"

# Резервное копирование отдельных схем
pg_dump -h localhost -U postgres -d personal_system_db \
  --schema=gitea --format=custom \
  --file="$BACKUP_DIR/gitea_schema_$DATE.dump"

pg_dump -h localhost -U postgres -d personal_system_db \
  --schema=coolify --format=custom \
  --file="$BACKUP_DIR/coolify_schema_$DATE.dump"

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "*.dump" -mtime +30 -delete
```

### Cron задача

```bash
# Добавьте в crontab
0 2 * * * /path/to/backup-database.sh >> /var/log/backup.log 2>&1
```

## 🔄 Миграция существующих данных

### Если у вас уже есть отдельные базы данных

```bash
# 1. Создайте резервные копии
pg_dump -h old_gitea_host -U old_user -d old_gitea_db > gitea_backup.sql
pg_dump -h old_coolify_host -U old_user -d old_coolify_db > coolify_backup.sql

# 2. Восстановите в новую единую базу
psql -h localhost -U postgres -d personal_system_db -c "CREATE SCHEMA gitea;"
psql -h localhost -U postgres -d personal_system_db -c "CREATE SCHEMA coolify;"

# 3. Восстановите данные в соответствующие схемы
psql -h localhost -U postgres -d personal_system_db -f gitea_backup.sql
psql -h localhost -U postgres -d personal_system_db -f coolify_backup.sql
```

## 📈 Производительность

### Настройки PostgreSQL

```sql
-- Оптимизация для единой базы данных
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Перезапустите PostgreSQL для применения изменений
SELECT pg_reload_conf();
```

### Мониторинг производительности

```sql
-- Проверка размера схем
SELECT 
  schemaname,
  pg_size_pretty(pg_total_relation_size(schemaname||'.*')) as size
FROM pg_schema
WHERE schemaname IN ('gitea', 'coolify', 'monitoring', 'logs');

-- Проверка активных соединений
SELECT 
  datname,
  usename,
  application_name,
  client_addr,
  state
FROM pg_stat_activity
WHERE datname = 'personal_system_db';
```

## 🆘 Troubleshooting

### Проблемы с подключением

```bash
# Проверка доступности базы данных
pg_isready -h localhost -p 5432 -U postgres

# Проверка соединения
psql -h localhost -U postgres -d personal_system_db -c "SELECT version();"

# Проверка логов PostgreSQL
docker logs shared-postgres
```

### Проблемы с правами доступа

```sql
-- Проверка прав пользователя
SELECT 
  schemaname,
  tablename,
  tableowner,
  hasinsert,
  hasselect,
  hasupdate,
  hasdelete
FROM pg_tables
WHERE schemaname IN ('gitea', 'coolify');

-- Назначение прав
GRANT ALL PRIVILEGES ON SCHEMA gitea TO gitea_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA gitea TO gitea_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA gitea TO gitea_user;
```

## 📚 Полезные команды

### Управление базой данных

```bash
# Подключение к базе данных
psql -h localhost -U postgres -d personal_system_db

# Создание резервной копии
pg_dump -h localhost -U postgres -d personal_system_db > backup.sql

# Восстановление из резервной копии
psql -h localhost -U postgres -d personal_system_db < backup.sql

# Проверка размера базы данных
psql -h localhost -U postgres -d personal_system_db -c "SELECT pg_size_pretty(pg_database_size('personal_system_db'));"
```

### Управление Docker

```bash
# Запуск всех сервисов
docker-compose -f docker-compose.shared-db.yml up -d

# Остановка всех сервисов
docker-compose -f docker-compose.shared-db.yml down

# Просмотр логов
docker-compose -f docker-compose.shared-db.yml logs -f

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.shared-db.yml restart gitea
```

## 🎯 Следующие шаги

1. ✅ Создайте единую базу данных PostgreSQL
2. ✅ Настройте схемы для разных сервисов
3. ✅ Обновите конфигурации сервисов
4. ✅ Настройте мониторинг и метрики
5. ✅ Настройте автоматическое резервное копирование
6. 🔄 Мигрируйте существующие данные (если есть)
7. 🔄 Оптимизируйте производительность

---

**Результат:** Единая база данных для всех сервисов с изоляцией данных по схемам, упрощенным управлением и мониторингом.
