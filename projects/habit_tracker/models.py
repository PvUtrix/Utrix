from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Habit(db.Model):
    """Модель привычки"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # morning, evening, daily, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Связи
    checklist_items = db.relationship('ChecklistItem', backref='habit', lazy=True, cascade='all, delete-orphan')
    completions = db.relationship('HabitCompletion', backref='habit', lazy=True, cascade='all, delete-orphan')

class ChecklistItem(db.Model):
    """Элементы чек-листа для привычки"""
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    is_required = db.Column(db.Boolean, default=True)
    
class HabitCompletion(db.Model):
    """Записи о выполнении привычек"""
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    completion_date = db.Column(db.Date, nullable=False, default=date.today)
    completed_items = db.Column(db.Integer, default=0)
    total_items = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальный индекс для предотвращения дублирования
    __table_args__ = (db.UniqueConstraint('habit_id', 'completion_date', name='unique_habit_date'),)

class HabitStreak(db.Model):
    """Отслеживание последовательных дней выполнения"""
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_completion_date = db.Column(db.Date)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
