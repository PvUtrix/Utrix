# Настройка Gitea через Coolify для персональной системы

## Обзор
Это руководство описывает настройку Gitea (Git-сервера) через Coolify для управления всеми персональными проектами и автоматического деплоя.

## Предварительные требования
- Работающий Coolify сервер
- Доступ к домену (опционально, но рекомендуется)
- SSH ключи для аутентификации

## Шаг 1: Настройка Gitea в Coolify

### 1.1 Установка Gitea через Coolify
1. Войдите в панель управления Coolify
2. Перейдите в раздел "Services" → "New Service"
3. Выберите "Gitea" из списка доступных сервисов
4. Настройте параметры:
   - **Service Name**: `gitea-personal`
   - **Port**: `3000` (стандартный порт Gitea)
   - **Database**: Используйте ЕДИНУЮ базу данных PostgreSQL (см. раздел "Единая база данных")
   - **Domain**: `git.yourdomain.com` (если есть домен)

**ВАЖНО:** Для экономии ресурсов рекомендуется использовать единую базу данных PostgreSQL для всех сервисов. Подробности в разделе "Единая база данных" ниже.

### 1.2 Конфигурация Gitea
После установки настройте:
- **Site Title**: "Personal System Gitea"
- **Repository Root Path**: `/data/git/repositories`
- **Git LFS**: Включить для больших файлов
- **SSH Server Domain**: `git.yourdomain.com` (или IP сервера)

## Шаг 1.5: Настройка единой базы данных (Рекомендуется)

### 1.5.1 Создание единой базы данных PostgreSQL
Для экономии ресурсов и упрощения управления рекомендуется использовать одну базу данных PostgreSQL для всех сервисов:

```bash
# В Coolify создайте сервис PostgreSQL
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

### 1.5.2 Создание схем для изоляции данных
```sql
-- Подключитесь к базе данных
psql -h localhost -U postgres -d personal_system_db

-- Создайте схемы для разных сервисов
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

### 1.5.3 Преимущества единой базы данных
✅ **Экономия ресурсов** - меньше памяти и CPU  
✅ **Простота управления** - одна точка резервного копирования  
✅ **Единый мониторинг** - все метрики в одном месте  
✅ **Кросс-сервисные запросы** - возможность объединения данных  

**Подробное руководство:** [Настройка единой базы данных](shared-database-setup.md)

## Шаг 2: Настройка SSH ключей

### 2.1 Генерация SSH ключа (если нет)
```bash
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/gitea_key
```

### 2.2 Добавление ключа в Gitea
1. Скопируйте публичный ключ:
   ```bash
   cat ~/.ssh/gitea_key.pub
   ```
2. В Gitea: Settings → SSH Keys → Add Key
3. Вставьте публичный ключ

### 2.3 Настройка SSH конфигурации
Создайте/отредактируйте `~/.ssh/config`:
```
Host gitea-personal
    HostName YOUR_COOLIFY_SERVER_IP
    Port 22
    User git
    IdentityFile ~/.ssh/gitea_key
    IdentitiesOnly yes
```

## Шаг 3: Настройка персональной системы

### 3.1 Создание репозитория в Gitea
1. В Gitea создайте новый репозиторий:
   - **Repository Name**: `personal-system`
   - **Description**: "Персональная система управления жизнью и проектами"
   - **Visibility**: Private (рекомендуется)
   - **Initialize with README**: Да

### 3.2 Настройка Git remote
```bash
# Добавить удаленный репозиторий
git remote add origin git@gitea-personal:username/personal-system.git

# Проверить настройки
git remote -v

# Первый push
git push -u origin main
```

### 3.3 Настройка переменных окружения для единой базы данных
Если вы используете единую базу данных, настройте переменные окружения в Gitea:

```bash
# В переменных окружения Gitea
GITEA__database__DB_TYPE=postgres
GITEA__database__HOST=shared-postgres
GITEA__database__NAME=personal_system_db
GITEA__database__USER=gitea_user
GITEA__database__PASSWD=gitea_password
GITEA__database__PORT=5432
GITEA__database__SCHEMA=gitea
```

## Шаг 4: Настройка автоматического деплоя

### 4.1 Webhook для автоматического деплоя
1. В репозитории Gitea: Settings → Webhooks → Add Webhook
2. Настройте webhook:
   - **Target URL**: `https://your-coolify-server.com/api/v1/webhooks/deploy`
   - **HTTP Method**: POST
   - **Content Type**: application/json
   - **Secret**: Сгенерируйте секретный ключ

### 4.2 Настройка CI/CD в Coolify
1. Создайте новый проект в Coolify
2. Подключите репозиторий Gitea
3. Настройте автоматический деплой при push в main ветку

## Шаг 5: Настройка .gitignore

### 5.1 Создание .gitignore
Создайте файл `.gitignore` в корне проекта:
```
# Логи
logs/
*.log

# Конфиденциальные данные
privacy/
config/global/preferences.yaml

# Временные файлы
*.tmp
*.temp
.DS_Store

# Автоматизация
automation/scripts/custom/*.pyc
__pycache__/

# Локальные настройки
.env
.env.local
```

## Шаг 6: Настройка веток и workflow

### 6.1 Структура веток
- **main**: Основная ветка, всегда стабильная
- **develop**: Ветка разработки
- **feature/***: Ветки для новых функций
- **hotfix/***: Срочные исправления

### 6.2 Workflow
1. Создайте feature ветку: `git checkout -b feature/new-feature`
2. Разрабатывайте и коммитьте изменения
3. Создайте Pull Request в Gitea
4. После ревью мержите в develop
5. Периодически мержите develop в main

## Шаг 7: Автоматизация и мониторинг

### 7.1 Автоматические задачи
- Автоматический деплой при push в main
- Автоматические тесты (если есть)
- Уведомления о статусе деплоя

### 7.2 Мониторинг
- Статус сервисов в Coolify
- Логи Gitea
- Статистика репозитория

## Полезные команды

### Git команды
```bash
# Проверить статус
git status

# Добавить все изменения
git add .

# Коммит
git commit -m "Описание изменений"

# Push
git push origin main

# Pull последних изменений
git pull origin main
```

### SSH команды
```bash
# Тест SSH соединения
ssh -T git@gitea-personal

# Клонирование репозитория
git clone git@gitea-personal:username/repository-name.git
```

## Troubleshooting

### Проблемы с SSH
- Проверьте права на SSH ключ: `chmod 600 ~/.ssh/gitea_key`
- Проверьте SSH конфигурацию: `ssh -vT git@gitea-personal`

### Проблемы с доступом
- Убедитесь, что IP адрес Coolify сервера доступен
- Проверьте настройки файрвола
- Убедитесь, что порт 22 открыт для SSH

## Следующие шаги
1. Настройте Gitea в Coolify
2. Создайте репозиторий
3. Настройте SSH ключи
4. Перенесите код в Gitea
5. Настройте автоматический деплой
6. Настройте workflow для командной работы

## Полезные ссылки
- [Gitea Documentation](https://docs.gitea.io/)
- [Coolify Documentation](https://coolify.io/docs)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Настройка единой базы данных](shared-database-setup.md) - руководство по использованию одной PostgreSQL для всех сервисов
