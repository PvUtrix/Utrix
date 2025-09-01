# 🚀 Инструкция по настройке Presentation Analyzer

## 📋 Предварительные требования

### 1. Python 3.8+
```bash
python3 --version
```

### 2. Установка зависимостей
```bash
cd projects/presentation_analyzer
pip install -r requirements.txt
```

### 3. Установка Tesseract OCR (для распознавания текста)
#### macOS:
```bash
brew install tesseract tesseract-lang
```

#### Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-rus
```

#### Windows:
Скачайте с [официального сайта](https://github.com/UB-Mannheim/tesseract/wiki)

## 🔧 Настройка Google Drive API

### 1. Создание проекта в Google Cloud Console

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Запомните **Project ID**

### 2. Включение Google Drive API

1. В меню слева выберите **APIs & Services** → **Library**
2. Найдите **Google Drive API**
3. Нажмите **Enable**

### 3. Создание сервисного аккаунта

1. Перейдите в **APIs & Services** → **Credentials**
2. Нажмите **Create Credentials** → **Service Account**
3. Заполните форму:
   - **Name**: `presentation-analyzer`
   - **Description**: `Service account for presentation analysis`
4. Нажмите **Create and Continue**
5. Пропустите шаги 2 и 3, нажмите **Done**

### 4. Создание ключа

1. В списке сервисных аккаунтов найдите созданный
2. Нажмите на email аккаунта
3. Перейдите на вкладку **Keys**
4. Нажмите **Add Key** → **Create new key**
5. Выберите **JSON**
6. Нажмите **Create**
7. Файл `credentials.json` скачается автоматически

### 5. Настройка доступа к папке

1. Перейдите в Google Drive
2. Найдите папку с презентациями
3. Поделитесь папкой с email сервисного аккаунта (из файла credentials.json)
4. Дайте права **Viewer** или **Editor**

### 6. Получение ID папки

1. Откройте папку с презентациями в браузере
2. ID папки находится в URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Скопируйте `FOLDER_ID_HERE`

## ⚙️ Конфигурация проекта

### 1. Размещение credentials.json

```bash
# Скопируйте скачанный файл в папку config
cp ~/Downloads/credentials.json projects/presentation_analyzer/config/
```

### 2. Обновление настроек

Отредактируйте `config/settings.yaml`:

```yaml
google_drive:
  folder_id: "YOUR_ACTUAL_FOLDER_ID_HERE"  # Замените на реальный ID
  credentials_path: "config/credentials.json"
```

### 3. Создание необходимых директорий

```bash
mkdir -p data/raw data/processed data/database logs
```

## 🧪 Тестирование

### 1. Проверка подключения

```bash
cd projects/presentation_analyzer
python sync_presentations.py --sync
```

### 2. Полный тест

```bash
python sync_presentations.py --full
```

## 🔄 Интеграция в утреннюю рутину

### Автоматический запуск

Добавьте в `workflows/daily/morning_routine.md`:

```markdown
## 📚 Learning (7:20 AM)
- [ ] Read for 20 minutes
- [ ] Take 3 key notes
- [ ] Add to knowledge base
- [ ] Sync company presentations (5 min)
```

### Создание алиаса (опционально)

Добавьте в `~/.zshrc` или `~/.bashrc`:

```bash
alias sync-pres='cd ~/Downloads/personal_system/projects/presentation_analyzer && python sync_presentations.py --sync'
```

## 📊 Мониторинг

### Логи

Логи сохраняются в:
- `logs/presentation_analyzer.log` - основной лог
- Консольный вывод при запуске

### Результаты

- **Сырые файлы**: `data/raw/`
- **Обработанные данные**: `data/processed/`
- **Заметки в базе знаний**: `knowledge/notes/presentations/`

## 🔒 Безопасность

### Рекомендации:

1. **Не коммитьте** `credentials.json` в git
2. Добавьте в `.gitignore`:
   ```
   config/credentials.json
   token.json
   data/
   logs/
   ```
3. Регулярно ротируйте ключи API
4. Используйте минимальные права доступа

## 🐛 Устранение неполадок

### Ошибка аутентификации
```
Ошибка: invalid_grant
```
**Решение**: Удалите `token.json` и перезапустите

### Файлы не скачиваются
```
Ошибка: 403 Forbidden
```
**Решение**: Проверьте права доступа к папке

### OCR не работает
```
Tesseract OCR недоступен
```
**Решение**: Установите Tesseract и языковые пакеты

### Медленная работа
**Решение**: 
- Уменьшите `max_workers` в конфигурации
- Отключите OCR для быстрых тестов

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи в `logs/presentation_analyzer.log`
2. Убедитесь в корректности настроек
3. Проверьте доступность Google Drive API
4. Убедитесь в установке всех зависимостей
