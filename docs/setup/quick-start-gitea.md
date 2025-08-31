# 🚀 Быстрый старт: Gitea + Coolify

## Что это?
Настройка персонального Git-сервера (Gitea) через Coolify для управления всеми проектами с автоматическим деплоем.

## ⚡ Быстрая настройка (5 минут)

### 1. Запустите скрипт настройки
```bash
cd /path/to/personal-system
./automation/scripts/custom/setup_gitea_sync.sh YOUR_COOLIFY_IP YOUR_USERNAME
```

**Пример:**
```bash
./automation/scripts/custom/setup_gitea_sync.sh 192.168.1.100 pvutrix
```

### 2. Следуйте инструкциям скрипта
- Скрипт создаст SSH ключ (если нужно)
- Настроит Git remote
- Покажет публичный ключ для добавления в Gitea

### 3. Создайте репозиторий в Gitea
- Войдите в Gitea через Coolify
- Создайте репозиторий `personal-system`
- Добавьте SSH ключ (показан скриптом)

### 4. Первый push
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

## 🔧 Что происходит автоматически?

✅ **SSH настройка** - создание ключей и конфигурации  
✅ **Git remote** - подключение к Gitea  
✅ **Безопасность** - исключение конфиденциальных файлов  
✅ **Автодеплой** - настройка webhook для Coolify  

## 📁 Структура после настройки

```
personal-system/
├── .git/                    # Git репозиторий
├── .gitignore              # Исключения (создается автоматически)
├── automation/              # Скрипты автоматизации
├── config/                  # Конфигурации
├── core/                    # Основная система
├── domains/                 # Домены жизни
└── docs/                    # Документация
```

## 🚨 Важные моменты

### Безопасность
- Файлы в `privacy/` автоматически исключены
- Конфиденциальные конфиги не попадут в Git
- SSH ключи хранятся локально

### Автоматизация
- При каждом push в `main` - автоматический деплой
- Webhook настроен для Coolify
- Мониторинг и уведомления включены

## 🔄 Ежедневное использование

### Добавление изменений
```bash
git add .
git commit -m "Описание изменений"
git push origin main
```

### Получение обновлений
```bash
git pull origin main
```

### Создание новой функции
```bash
git checkout -b feature/new-feature
# ... работа ...
git push origin feature/new-feature
# Создать Pull Request в Gitea
```

## 🆘 Если что-то пошло не так

### Проверка SSH
```bash
ssh -T git@gitea-personal
```

### Проверка Git remote
```bash
git remote -v
```

### Сброс настроек
```bash
git remote remove origin
./automation/scripts/custom/setup_gitea_sync.sh IP USERNAME
```

## 📚 Дополнительные ресурсы

- [Полное руководство](gitea-coolify-setup.md) - детальная настройка
- [Конфигурация Coolify](../config/automation/coolify-deploy.yaml)
- [Скрипт настройки](../automation/scripts/custom/setup_gitea_sync.sh)

## 🎯 Следующие шаги

1. ✅ Настройте Gitea через Coolify
2. ✅ Запустите скрипт настройки
3. ✅ Создайте репозиторий в Gitea
4. ✅ Сделайте первый push
5. 🔄 Настройте автоматический деплой
6. 🔄 Настройте мониторинг и уведомления

---

**Время настройки:** ~5 минут  
**Уровень сложности:** 🟢 Легко  
**Автоматизация:** 🟢 Полная
