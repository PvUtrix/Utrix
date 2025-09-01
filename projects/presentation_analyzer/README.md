# Presentation Analyzer

## 🎯 Цель
Автоматическое извлечение и анализ презентаций компании из Google Drive с последующей обработкой и структурированием данных.

## 🏗 Архитектура

### Компоненты:
1. **Google Drive Connector** - подключение к Google Drive API
2. **Document Downloader** - скачивание презентаций в PDF
3. **Text Extractor** - OCR и извлечение текста
4. **Data Processor** - обработка и структурирование
5. **Knowledge Integrator** - интеграция в систему знаний

### Технологии:
- Python 3.8+
- Google Drive API
- PyPDF2 / pdfplumber
- pytesseract (OCR)
- pandas (обработка данных)
- sqlite (локальное хранение)

## 📁 Структура проекта
```
presentation_analyzer/
├── src/
│   ├── connectors/
│   │   ├── google_drive.py
│   │   └── auth.py
│   ├── processors/
│   │   ├── downloader.py
│   │   ├── text_extractor.py
│   │   └── data_processor.py
│   ├── storage/
│   │   ├── database.py
│   │   └── file_manager.py
│   └── main.py
├── config/
│   ├── settings.yaml
│   └── credentials.json
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
├── requirements.txt
└── README.md
```

## 🔧 Установка и настройка

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка Google Drive API
1. Создать проект в Google Cloud Console
2. Включить Google Drive API
3. Создать сервисный аккаунт
4. Скачать credentials.json

### 3. Конфигурация
```yaml
# config/settings.yaml
google_drive:
  folder_id: "YOUR_FOLDER_ID"
  credentials_path: "config/credentials.json"

processing:
  download_pdf: true
  extract_text: true
  ocr_enabled: true
  language: "ru"

storage:
  raw_data_path: "data/raw"
  processed_data_path: "data/processed"
  database_path: "data/database/presentations.db"
```

## 🚀 Использование

### Базовое использование:
```python
from src.main import PresentationAnalyzer

analyzer = PresentationAnalyzer()
analyzer.sync_presentations()
analyzer.process_all()
```

### Интеграция в утреннюю рутину:
```python
# Добавить в workflows/daily/morning_routine.md
- [ ] Sync company presentations (5 min)
- [ ] Review new insights (3 min)
```

## 📊 Выходные данные

### Структурированные данные:
- Текст презентаций
- Метаданные (дата, автор, тема)
- Ключевые слова и темы
- Извлеченные инсайты

### Интеграция с системой знаний:
- Автоматическое добавление в `knowledge/notes/`
- Связи с существующими темами
- Обновление базы знаний

## 🔒 Безопасность
- Локальное хранение данных
- Шифрование чувствительной информации
- Приватные маркеры для конфиденциальных презентаций

## 📈 Возможности расширения
- Анализ трендов в презентациях
- Автоматическое создание отчетов
- Интеграция с другими источниками данных
- AI-анализ контента

