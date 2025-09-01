import os
from datetime import datetime, date, timedelta
from models import db, Habit, ChecklistItem, HabitCompletion, HabitStreak

def init_database(app):
    """Инициализация базы данных"""
    db.init_app(app)
    
    # Создаем директорию для данных если её нет
    os.makedirs('data', exist_ok=True)
    
    with app.app_context():
        db.create_all()
        create_sample_data()

def create_sample_data():
    """Создание образцовых данных для демонстрации"""
    # Проверяем, есть ли уже данные
    if Habit.query.first():
        return
    
    # Создаем утреннюю рутину
    morning_habit = Habit(
        name="Утренняя рутина",
        description="Ежедневная утренняя рутина для продуктивного дня",
        category="morning"
    )
    db.session.add(morning_habit)
    db.session.flush()  # Получаем ID
    
    morning_items = [
        "Проснуться без откладывания",
        "Выпить стакан воды",
        "10 минут медитации",
        "5 минут растяжки",
        "Принять холодный душ",
        "Здоровый завтрак",
        "Планирование дня"
    ]
    
    for i, item_text in enumerate(morning_items):
        item = ChecklistItem(
            habit_id=morning_habit.id,
            text=item_text,
            order_index=i,
            is_required=True
        )
        db.session.add(item)
    
    # Создаем вечернюю рутину
    evening_habit = Habit(
        name="Вечерняя рутина",
        description="Рутина для подготовки ко сну и рефлексии",
        category="evening"
    )
    db.session.add(evening_habit)
    db.session.flush()
    
    evening_items = [
        "Завершить рабочие задачи",
        "Подготовить одежду на завтра",
        "10 минут чтения",
        "Записать 3 благодарности",
        "Отключить уведомления",
        "Подготовиться ко сну"
    ]
    
    for i, item_text in enumerate(evening_items):
        item = ChecklistItem(
            habit_id=evening_habit.id,
            text=item_text,
            order_index=i,
            is_required=True
        )
        db.session.add(item)
    
    db.session.commit()

def get_habit_stats(habit_id, days=30):
    """Получение статистики привычки за последние дни"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    completions = HabitCompletion.query.filter(
        HabitCompletion.habit_id == habit_id,
        HabitCompletion.completion_date >= start_date,
        HabitCompletion.completion_date <= end_date
    ).order_by(HabitCompletion.completion_date).all()
    
    # Создаем полный список дат
    dates = []
    completion_data = []
    
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        
        # Ищем выполнение для этой даты
        completion = next((c for c in completions if c.completion_date == current_date), None)
        if completion:
            completion_data.append(completion.completion_percentage)
        else:
            completion_data.append(0)
        
        current_date += timedelta(days=1)
    
    return {
        'dates': dates,
        'completion_data': completion_data,
        'total_completions': len([c for c in completions if c.completion_percentage > 0]),
        'average_completion': sum(c.completion_percentage for c in completions) / len(completions) if completions else 0
    }

def update_streak(habit_id):
    """Обновление streak для привычки"""
    streak = HabitStreak.query.filter_by(habit_id=habit_id).first()
    if not streak:
        streak = HabitStreak(habit_id=habit_id)
        db.session.add(streak)
    
    # Получаем последние выполнения
    completions = HabitCompletion.query.filter(
        HabitCompletion.habit_id == habit_id,
        HabitCompletion.completion_percentage > 0
    ).order_by(HabitCompletion.completion_date.desc()).all()
    
    if not completions:
        streak.current_streak = 0
        streak.last_completion_date = None
    else:
        last_completion = completions[0]
        streak.last_completion_date = last_completion.completion_date
        
        # Подсчитываем текущий streak
        current_streak = 1
        current_date = last_completion.completion_date - timedelta(days=1)
        
        for completion in completions[1:]:
            if completion.completion_date == current_date:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        streak.current_streak = current_streak
        streak.longest_streak = max(streak.longest_streak, current_streak)
    
    db.session.commit()
    return streak

def get_today_completion(habit_id):
    """Получение выполнения привычки на сегодня"""
    today = date.today()
    return HabitCompletion.query.filter_by(
        habit_id=habit_id,
        completion_date=today
    ).first()

def mark_habit_completed(habit_id, completed_items, total_items, notes=""):
    """Отметить выполнение привычки"""
    today = date.today()
    completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0
    
    # Проверяем, есть ли уже запись на сегодня
    completion = get_today_completion(habit_id)
    
    if completion:
        # Обновляем существующую запись
        completion.completed_items = completed_items
        completion.total_items = total_items
        completion.completion_percentage = completion_percentage
        completion.notes = notes
    else:
        # Создаем новую запись
        completion = HabitCompletion(
            habit_id=habit_id,
            completion_date=today,
            completed_items=completed_items,
            total_items=total_items,
            completion_percentage=completion_percentage,
            notes=notes
        )
        db.session.add(completion)
    
    db.session.commit()
    
    # Обновляем streak
    update_streak(habit_id)
    
    return completion
