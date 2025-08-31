#!/bin/bash

# Скрипт настройки синхронизации с Gitea через Coolify
# Использование: ./setup_gitea_sync.sh [COOLIFY_SERVER_IP] [USERNAME]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка аргументов
if [ $# -lt 2 ]; then
    error "Использование: $0 <COOLIFY_SERVER_IP> <USERNAME>"
    echo "Пример: $0 192.168.1.100 pvutrix"
    exit 1
fi

COOLIFY_SERVER_IP=$1
USERNAME=$2
REPO_NAME="personal-system"

log "Настройка синхронизации с Gitea на сервере $COOLIFY_SERVER_IP для пользователя $USERNAME"

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    error "Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

# Проверка SSH ключей
log "Проверка SSH ключей..."
if [ ! -f ~/.ssh/gitea_key ]; then
    warn "SSH ключ для Gitea не найден. Создаю новый ключ..."
    ssh-keygen -t ed25519 -C "$USERNAME@$COOLIFY_SERVER_IP" -f ~/.ssh/gitea_key -N ""
    chmod 600 ~/.ssh/gitea_key
    log "SSH ключ создан: ~/.ssh/gitea_key"
    echo ""
    echo "Добавьте следующий публичный ключ в Gitea:"
    echo "=========================================="
    cat ~/.ssh/gitea_key.pub
    echo "=========================================="
    echo ""
    read -p "Нажмите Enter после добавления ключа в Gitea..."
else
    log "SSH ключ найден: ~/.ssh/gitea_key"
fi

# Настройка SSH конфигурации
log "Настройка SSH конфигурации..."
SSH_CONFIG="$HOME/.ssh/config"
SSH_HOST="gitea-personal"

# Создание SSH конфигурации
if [ ! -f "$SSH_CONFIG" ]; then
    touch "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
fi

# Проверка существующей конфигурации
if grep -q "Host $SSH_HOST" "$SSH_CONFIG"; then
    warn "SSH хост $SSH_HOST уже настроен. Обновляю конфигурацию..."
    # Удаляем существующую конфигурацию
    sed -i.bak "/Host $SSH_HOST/,/^$/d" "$SSH_CONFIG"
fi

# Добавляем новую конфигурацию
cat >> "$SSH_CONFIG" << EOF

Host $SSH_HOST
    HostName $COOLIFY_SERVER_IP
    Port 22
    User git
    IdentityFile ~/.ssh/gitea_key
    IdentitiesOnly yes
    StrictHostKeyChecking no
EOF

log "SSH конфигурация обновлена"

# Тест SSH соединения
log "Тестирование SSH соединения..."
if ssh -o ConnectTimeout=10 -T git@$SSH_HOST 2>&1 | grep -q "successfully authenticated"; then
    log "SSH соединение успешно установлено!"
else
    warn "SSH соединение не удалось установить. Проверьте настройки сервера."
    warn "Убедитесь, что:"
    warn "1. SSH ключ добавлен в Gitea"
    warn "2. Сервер доступен по IP $COOLIFY_SERVER_IP"
    warn "3. Порт 22 открыт"
fi

# Настройка Git remote
log "Настройка Git remote..."
if git remote get-url origin &> /dev/null; then
    warn "Remote origin уже настроен. Обновляю..."
    git remote set-url origin git@$SSH_HOST:$USERNAME/$REPO_NAME.git
else
    log "Добавляю remote origin..."
    git remote add origin git@$SSH_HOST:$USERNAME/$REPO_NAME.git
fi

# Проверка remote
log "Проверка настроек remote..."
git remote -v

# Создание .gitignore если не существует
if [ ! -f .gitignore ]; then
    warn "Файл .gitignore не найден. Создаю базовый .gitignore..."
    cat > .gitignore << 'EOF'
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
Thumbs.db

# Автоматизация
automation/scripts/custom/*.pyc
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Локальные настройки
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Системные файлы
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Временные файлы
*.tmp
*.temp
*.bak
*.backup

# Локальные конфигурации
config/local/
*.local.yaml
*.local.yml
EOF
    log "Файл .gitignore создан"
fi

# Проверка статуса Git
log "Проверка статуса Git..."
git status

# Инструкции по первому push
echo ""
echo "=========================================="
echo "НАСТРОЙКА ЗАВЕРШЕНА!"
echo "=========================================="
echo ""
echo "Следующие шаги:"
echo "1. Создайте репозиторий '$REPO_NAME' в Gitea"
echo "2. Добавьте и закоммитьте изменения:"
echo "   git add ."
echo "   git commit -m 'Initial commit'"
echo "3. Сделайте первый push:"
echo "   git push -u origin main"
echo ""
echo "Для автоматического деплоя настройте webhook в Gitea:"
echo "Target URL: https://$COOLIFY_SERVER_IP/api/v1/webhooks/deploy"
echo ""

# Проверка готовности к push
if [ -n "$(git status --porcelain)" ]; then
    warn "У вас есть незакоммиченные изменения. Рекомендуется их закоммитить перед push."
    echo "Незакоммиченные файлы:"
    git status --porcelain
else
    log "Все изменения закоммичены. Готово к push!"
fi
