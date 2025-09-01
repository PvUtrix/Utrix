from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date
import json
from models import db, Habit, ChecklistItem, HabitCompletion, HabitStreak
from database import init_database, get_habit_stats, mark_habit_completed, get_today_completion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
init_database(app)

@app.route('/')
def index():
    """Главная страница с обзором привычек"""
    habits = Habit.query.filter_by(is_active=True).all()
    
    # Получаем статистику для каждой привычки
    for habit in habits:
        streak = HabitStreak.query.filter_by(habit_id=habit.id).first()
        habit.current_streak = streak.current_streak if streak else 0
        habit.longest_streak = streak.longest_streak if streak else 0
        
        # Проверяем выполнение на сегодня
        today_completion = get_today_completion(habit.id)
        habit.today_completed = today_completion is not None and today_completion.completion_percentage > 0
    
    return render_template('index.html', habits=habits)

@app.route('/habit/<int:habit_id>')
def habit_detail(habit_id):
    """Детальная страница привычки"""
    habit = Habit.query.get_or_404(habit_id)
    checklist_items = ChecklistItem.query.filter_by(habit_id=habit_id).order_by(ChecklistItem.order_index).all()
    
    # Получаем выполнение на сегодня
    today_completion = get_today_completion(habit_id)
    completed_items = []
    if today_completion:
        # Здесь можно добавить логику для определения выполненных элементов
        pass
    
    # Получаем статистику
    stats = get_habit_stats(habit_id, days=30)
    
    return render_template('habit_detail.html', 
                         habit=habit, 
                         checklist_items=checklist_items,
                         stats=stats,
                         today_completion=today_completion)

@app.route('/habit/<int:habit_id>/complete', methods=['POST'])
def complete_habit(habit_id):
    """Отметить выполнение привычки"""
    data = request.get_json()
    completed_items = data.get('completed_items', [])
    notes = data.get('notes', '')
    
    habit = Habit.query.get_or_404(habit_id)
    total_items = len(habit.checklist_items)
    
    completion = mark_habit_completed(habit_id, len(completed_items), total_items, notes)
    
    return jsonify({
        'success': True,
        'completion_percentage': completion.completion_percentage,
        'message': 'Привычка отмечена как выполненная!'
    })

@app.route('/habit/new', methods=['GET', 'POST'])
def new_habit():
    """Создание новой привычки"""
    if request.method == 'POST':
        data = request.get_json()
        
        habit = Habit(
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', 'daily')
        )
        db.session.add(habit)
        db.session.flush()
        
        # Добавляем элементы чек-листа
        for i, item_text in enumerate(data.get('checklist_items', [])):
            item = ChecklistItem(
                habit_id=habit.id,
                text=item_text,
                order_index=i,
                is_required=True
            )
            db.session.add(item)
        
        db.session.commit()
        
        return jsonify({'success': True, 'habit_id': habit.id})
    
    return render_template('new_habit.html')

@app.route('/habit/<int:habit_id>/edit', methods=['GET', 'POST'])
def edit_habit(habit_id):
    """Редактирование привычки"""
    habit = Habit.query.get_or_404(habit_id)
    
    if request.method == 'POST':
        data = request.get_json()
        
        habit.name = data['name']
        habit.description = data.get('description', '')
        habit.category = data.get('category', 'daily')
        
        # Обновляем элементы чек-листа
        ChecklistItem.query.filter_by(habit_id=habit_id).delete()
        
        for i, item_text in enumerate(data.get('checklist_items', [])):
            item = ChecklistItem(
                habit_id=habit.id,
                text=item_text,
                order_index=i,
                is_required=True
            )
            db.session.add(item)
        
        db.session.commit()
        
        return jsonify({'success': True})
    
    checklist_items = ChecklistItem.query.filter_by(habit_id=habit_id).order_by(ChecklistItem.order_index).all()
    return render_template('edit_habit.html', habit=habit, checklist_items=checklist_items)

@app.route('/stats')
def stats():
    """Страница статистики"""
    habits = Habit.query.filter_by(is_active=True).all()
    
    # Получаем общую статистику
    total_habits = len(habits)
    total_completions_today = 0
    total_streaks = 0
    
    for habit in habits:
        today_completion = get_today_completion(habit.id)
        if today_completion and today_completion.completion_percentage > 0:
            total_completions_today += 1
        
        streak = HabitStreak.query.filter_by(habit_id=habit.id).first()
        if streak:
            total_streaks += streak.current_streak
    
    return render_template('stats.html', 
                         habits=habits,
                         total_habits=total_habits,
                         total_completions_today=total_completions_today,
                         total_streaks=total_streaks)

@app.route('/api/habit/<int:habit_id>/stats')
def api_habit_stats(habit_id):
    """API для получения статистики привычки"""
    stats = get_habit_stats(habit_id, days=30)
    return jsonify(stats)

@app.route('/api/habits')
def api_habits():
    """API для получения списка привычек"""
    habits = Habit.query.filter_by(is_active=True).all()
    habits_data = []
    
    for habit in habits:
        streak = HabitStreak.query.filter_by(habit_id=habit.id).first()
        today_completion = get_today_completion(habit.id)
        
        habits_data.append({
            'id': habit.id,
            'name': habit.name,
            'category': habit.category,
            'current_streak': streak.current_streak if streak else 0,
            'longest_streak': streak.longest_streak if streak else 0,
            'today_completed': today_completion is not None and today_completion.completion_percentage > 0
        })
    
    return jsonify(habits_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
