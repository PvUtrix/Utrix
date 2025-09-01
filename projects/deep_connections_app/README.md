# Deep Connections App

Мобильное приложение для глубокого и осмысленного знакомства людей, использующее AI и психологические тесты для лучшего матчинга.

## 🎯 Концепция

Приложение фокусируется на качественном контенте, психологической совместимости и постепенном построении отношений, в отличие от быстрых свиданий.

## 🚀 Быстрый старт

### Предварительные требования
- Node.js 18+
- React Native CLI
- Python 3.9+ (для AI компонентов)
- PostgreSQL 14+
- Redis 6+

### Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd deep_connections_app

# Установка зависимостей
npm install
cd backend && pip install -r requirements.txt

# Настройка базы данных
npm run db:setup

# Запуск разработки
npm run dev
```

## 📁 Структура проекта

```
deep_connections_app/
├── mobile/                 # React Native приложение
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── screens/        # Экраны приложения
│   │   ├── navigation/     # Навигация
│   │   ├── store/          # Redux store
│   │   ├── services/       # API сервисы
│   │   └── utils/          # Утилиты
│   ├── android/            # Android конфигурация
│   └── ios/                # iOS конфигурация
├── backend/                # Backend API
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Модели данных
│   │   ├── services/       # Бизнес логика
│   │   ├── ml/             # AI/ML компоненты
│   │   └── utils/          # Утилиты
│   └── tests/              # Тесты
├── ai_engine/              # AI сервисы
│   ├── compatibility/      # Алгоритмы совместимости
│   ├── content_gen/        # Генерация контента
│   └── personality/        # Анализ личности
└── docs/                   # Документация
```

## 🔧 Технологический стек

### Frontend (Mobile)
- **React Native** - кроссплатформенная разработка
- **TypeScript** - типобезопасность
- **Redux Toolkit** - управление состоянием
- **React Navigation** - навигация
- **React Native Elements** - UI компоненты
- **React Native Camera** - работа с камерой
- **React Native Video** - видео функциональность

### Backend
- **FastAPI** - высокопроизводительный API
- **SQLAlchemy** - ORM
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и сессии
- **Celery** - фоновые задачи
- **JWT** - аутентификация

### AI/ML
- **OpenAI API** - генерация контента
- **TensorFlow** - анализ совместимости
- **spaCy** - NLP анализ
- **scikit-learn** - машинное обучение

### Инфраструктура
- **Docker** - контейнеризация
- **AWS** - облачная инфраструктура
- **GitHub Actions** - CI/CD
- **Sentry** - мониторинг ошибок

## 🎨 Основные функции

### 1. Расширенные профили
- Многослойная информация о пользователе
- Интересы, ценности, жизненные цели
- Фотографии в разных контекстах
- Видео-интервью

### 2. Stories и контент
- Ежедневные stories о жизни
- Длинные посты о важных темах
- Видео-контент
- Совместные активности

### 3. AI-функции
- Генерация вопросов для знакомства
- Анализ совместимости
- Персонализированные рекомендации
- Анализ контента

### 4. Психологические тесты
- Big Five личностный тест
- Тест ценностей
- Тест стиля отношений
- Тест коммуникации

### 5. Система матчинга
- Алгоритм совместимости
- Временные ограничения
- Фильтры по критериям
- Качественные рекомендации

## 🔐 Безопасность

- **Шифрование** всех персональных данных
- **GDPR** соответствие
- **Двухфакторная аутентификация**
- **Модерация контента**
- **Защита от ботов**

## 📊 Метрики и аналитика

- **Retention rate** - удержание пользователей
- **Engagement** - вовлеченность
- **Match quality** - качество матчей
- **Conversion** - конверсия в премиум
- **User satisfaction** - удовлетворенность

## 🚀 Развертывание

### Development
```bash
npm run dev
```

### Staging
```bash
npm run build:staging
npm run deploy:staging
```

### Production
```bash
npm run build:prod
npm run deploy:prod
```

## 🧪 Тестирование

```bash
# Unit тесты
npm run test

# Integration тесты
npm run test:integration

# E2E тесты
npm run test:e2e
```

## 📝 Документация API

API документация доступна по адресу: `http://localhost:8000/docs`

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Контакты

- **Email**: team@deepconnections.app
- **Telegram**: @deepconnections_support
- **Discord**: [Deep Connections Community](https://discord.gg/deepconnections)

---

*Создано с ❤️ для построения подлинных связей*
