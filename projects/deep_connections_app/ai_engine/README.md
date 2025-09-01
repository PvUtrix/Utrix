# AI Engine - Deep Connections App

AI-движок для анализа совместимости, генерации контента и персонализации в приложении для знакомств.

## 🧠 Архитектура AI-системы

### Компоненты системы

```
ai_engine/
├── compatibility/          # Алгоритмы совместимости
│   ├── personality_match.py
│   ├── values_analysis.py
│   ├── communication_style.py
│   └── lifestyle_compatibility.py
├── content_gen/           # Генерация контента
│   ├── question_generator.py
│   ├── conversation_starters.py
│   ├── profile_suggestions.py
│   └── story_ideas.py
├── personality/           # Анализ личности
│   ├── big_five_analyzer.py
│   ├── mbti_classifier.py
│   ├── attachment_style.py
│   └── values_extractor.py
├── nlp/                   # NLP обработка
│   ├── text_analyzer.py
│   ├── sentiment_analysis.py
│   ├── topic_extraction.py
│   └── content_moderation.py
└── models/                # Обученные модели
    ├── compatibility_model.pkl
    ├── personality_model.pkl
    └── content_gen_model.pkl
```

## 🎯 Алгоритмы совместимости

### 1. Personality Matching (Совместимость личностей)

```python
class PersonalityMatcher:
    """
    Анализ совместимости на основе Big Five и MBTI
    """
    
    def calculate_compatibility(self, user1_profile, user2_profile):
        """
        Вычисляет совместимость двух пользователей
        Возвращает: score (0-100), explanation, areas_of_conflict
        """
        # Big Five совместимость
        big_five_score = self._big_five_compatibility(
            user1_profile.big_five, 
            user2_profile.big_five
        )
        
        # MBTI совместимость
        mbti_score = self._mbti_compatibility(
            user1_profile.mbti, 
            user2_profile.mbti
        )
        
        # Комбинированный скор
        final_score = (big_five_score * 0.6) + (mbti_score * 0.4)
        
        return {
            'score': final_score,
            'big_five_score': big_five_score,
            'mbti_score': mbti_score,
            'explanation': self._generate_explanation(final_score),
            'strengths': self._identify_strengths(user1_profile, user2_profile),
            'challenges': self._identify_challenges(user1_profile, user2_profile)
        }
```

### 2. Values Analysis (Анализ ценностей)

```python
class ValuesAnalyzer:
    """
    Анализ совместимости ценностей и жизненных целей
    """
    
    def analyze_values_compatibility(self, user1_values, user2_values):
        """
        Анализирует совместимость ценностей
        """
        # Ключевые области ценностей
        value_categories = {
            'family': ['children', 'marriage', 'family_tradition'],
            'career': ['ambition', 'work_life_balance', 'professional_growth'],
            'lifestyle': ['adventure', 'stability', 'social_life'],
            'spirituality': ['religion', 'philosophy', 'personal_growth'],
            'finances': ['saving', 'spending', 'investment_philosophy']
        }
        
        compatibility_scores = {}
        
        for category, values in value_categories.items():
            score = self._calculate_category_compatibility(
                user1_values, user2_values, values
            )
            compatibility_scores[category] = score
        
        return {
            'overall_score': np.mean(list(compatibility_scores.values())),
            'category_scores': compatibility_scores,
            'alignment_areas': self._find_alignment_areas(compatibility_scores),
            'conflict_areas': self._find_conflict_areas(compatibility_scores)
        }
```

### 3. Communication Style Matching

```python
class CommunicationMatcher:
    """
    Анализ совместимости стилей коммуникации
    """
    
    def analyze_communication_compatibility(self, user1_style, user2_style):
        """
        Анализирует совместимость стилей общения
        """
        styles = {
            'direct_vs_indirect': self._analyze_directness(user1_style, user2_style),
            'emotional_vs_rational': self._analyze_emotional_expression(user1_style, user2_style),
            'conflict_resolution': self._analyze_conflict_style(user1_style, user2_style),
            'communication_frequency': self._analyze_frequency_preference(user1_style, user2_style)
        }
        
        return {
            'overall_score': np.mean(list(styles.values())),
            'style_analysis': styles,
            'communication_tips': self._generate_communication_tips(styles)
        }
```

## 📝 Генерация контента

### 1. Question Generator (Генератор вопросов)

```python
class QuestionGenerator:
    """
    Генерирует персонализированные вопросы для знакомства
    """
    
    def generate_questions(self, user_profile, match_profile, context='initial'):
        """
        Генерирует вопросы на основе профилей и контекста
        """
        if context == 'initial':
            return self._generate_ice_breakers(user_profile, match_profile)
        elif context == 'deep':
            return self._generate_deep_questions(user_profile, match_profile)
        elif context == 'fun':
            return self._generate_fun_questions(user_profile, match_profile)
        
    def _generate_ice_breakers(self, user1, user2):
        """
        Генерирует вопросы для начала разговора
        """
        common_interests = self._find_common_interests(user1, user2)
        
        questions = []
        
        # Вопросы на основе общих интересов
        for interest in common_interests:
            questions.append(f"Что тебя больше всего привлекает в {interest}?")
        
        # Вопросы на основе различий
        differences = self._find_interesting_differences(user1, user2)
        for diff in differences:
            questions.append(f"Расскажи, как ты пришел к {diff}?")
        
        return questions[:5]  # Возвращаем топ-5 вопросов
```

### 2. Conversation Starters (Зачинщики разговоров)

```python
class ConversationStarter:
    """
    Генерирует зачинщики разговоров на основе контекста
    """
    
    def generate_starters(self, user_profile, current_time, location=None):
        """
        Генерирует зачинщики разговоров
        """
        starters = []
        
        # Временные зачинщики
        if current_time.hour < 12:
            starters.append("Как прошел твой утренний ритуал?")
        elif current_time.hour < 18:
            starters.append("Чем занимаешься в этот прекрасный день?")
        else:
            starters.append("Как прошел твой день?")
        
        # Локационные зачинщики
        if location:
            starters.append(f"Что тебя привело в {location}?")
        
        # Персональные зачинщики
        starters.extend(self._generate_personal_starters(user_profile))
        
        return starters
```

## 🧠 Анализ личности

### 1. Big Five Analyzer

```python
class BigFiveAnalyzer:
    """
    Анализ личности по модели Big Five
    """
    
    def analyze_personality(self, text_content, test_responses):
        """
        Анализирует личность на основе контента и тестов
        """
        # Анализ текстового контента
        text_scores = self._analyze_text_content(text_content)
        
        # Анализ результатов тестов
        test_scores = self._analyze_test_responses(test_responses)
        
        # Комбинированный анализ
        final_scores = self._combine_scores(text_scores, test_scores)
        
        return {
            'openness': final_scores['openness'],
            'conscientiousness': final_scores['conscientiousness'],
            'extraversion': final_scores['extraversion'],
            'agreeableness': final_scores['agreeableness'],
            'neuroticism': final_scores['neuroticism'],
            'confidence': self._calculate_confidence(final_scores)
        }
```

### 2. Values Extractor

```python
class ValuesExtractor:
    """
    Извлекает ценности из текстового контента
    """
    
    def extract_values(self, text_content):
        """
        Извлекает ценности из текста
        """
        # Предопределенные категории ценностей
        value_categories = {
            'family': ['семья', 'дети', 'брак', 'традиции'],
            'career': ['карьера', 'работа', 'успех', 'развитие'],
            'adventure': ['путешествия', 'приключения', 'новый опыт'],
            'stability': ['стабильность', 'безопасность', 'порядок'],
            'creativity': ['творчество', 'искусство', 'самовыражение'],
            'learning': ['обучение', 'знания', 'образование'],
            'health': ['здоровье', 'спорт', 'питание'],
            'spirituality': ['духовность', 'религия', 'философия']
        }
        
        extracted_values = {}
        
        for category, keywords in value_categories.items():
            score = self._calculate_category_score(text_content, keywords)
            if score > 0.3:  # Порог значимости
                extracted_values[category] = score
        
        return extracted_values
```

## 🔍 NLP обработка

### 1. Text Analyzer

```python
class TextAnalyzer:
    """
    Анализ текстового контента
    """
    
    def analyze_text(self, text):
        """
        Комплексный анализ текста
        """
        return {
            'sentiment': self._analyze_sentiment(text),
            'topics': self._extract_topics(text),
            'writing_style': self._analyze_writing_style(text),
            'emotional_tone': self._analyze_emotional_tone(text),
            'complexity': self._analyze_complexity(text)
        }
    
    def _analyze_sentiment(self, text):
        """
        Анализ эмоционального тона
        """
        # Использование предобученной модели
        sentiment_model = self._load_sentiment_model()
        return sentiment_model.predict(text)
    
    def _extract_topics(self, text):
        """
        Извлечение тем из текста
        """
        # LDA модель для извлечения тем
        lda_model = self._load_lda_model()
        return lda_model.extract_topics(text)
```

## 📊 Метрики качества

### Оценка алгоритмов

```python
class AlgorithmEvaluator:
    """
    Оценка качества AI алгоритмов
    """
    
    def evaluate_compatibility_algorithm(self, predictions, actual_outcomes):
        """
        Оценивает точность алгоритма совместимости
        """
        # Метрики для оценки
        metrics = {
            'accuracy': accuracy_score(actual_outcomes, predictions),
            'precision': precision_score(actual_outcomes, predictions, average='weighted'),
            'recall': recall_score(actual_outcomes, predictions, average='weighted'),
            'f1_score': f1_score(actual_outcomes, predictions, average='weighted'),
            'auc': roc_auc_score(actual_outcomes, predictions)
        }
        
        return metrics
    
    def evaluate_content_generation(self, generated_content, user_feedback):
        """
        Оценивает качество сгенерированного контента
        """
        return {
            'relevance_score': np.mean([feedback['relevance'] for feedback in user_feedback]),
            'engagement_score': np.mean([feedback['engagement'] for feedback in user_feedback]),
            'conversation_start_rate': self._calculate_conversation_rate(generated_content)
        }
```

## 🚀 Развертывание

### Docker контейнеризация

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### API Endpoints

```python
# Основные эндпоинты AI-движка
@app.post("/api/v1/compatibility/calculate")
async def calculate_compatibility(user1_id: int, user2_id: int):
    """Вычисляет совместимость двух пользователей"""

@app.post("/api/v1/content/generate-questions")
async def generate_questions(user_id: int, context: str):
    """Генерирует персонализированные вопросы"""

@app.post("/api/v1/personality/analyze")
async def analyze_personality(user_id: int):
    """Анализирует личность пользователя"""

@app.post("/api/v1/values/extract")
async def extract_values(text_content: str):
    """Извлекает ценности из текста"""
```

## 📈 Мониторинг и аналитика

### Логирование

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_engine.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Метрики производительности

```python
from prometheus_client import Counter, Histogram, Gauge

# Метрики
compatibility_requests = Counter('compatibility_requests_total', 'Total compatibility requests')
compatibility_duration = Histogram('compatibility_duration_seconds', 'Compatibility calculation duration')
active_users = Gauge('active_users', 'Number of active users')
```

---

*AI-движок создан для построения более глубоких и осмысленных связей между людьми*
