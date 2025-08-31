#!/usr/bin/env python3
"""
Скрипт-напоминание для обновления интро
Запускается еженедельно для актуализации информации
"""

import os
import datetime
from pathlib import Path

def check_intro_file():
    """Проверяет файл интро и предлагает обновления"""
    
    # Путь к файлу интро
    intro_path = Path("core/identity/intro.md")
    
    if not intro_path.exists():
        print("❌ Файл intro.md не найден!")
        return
    
    # Читаем файл
    with open(intro_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем дату последнего обновления
    today = datetime.datetime.now()
    
    # Ищем строку с датой обновления
    if "обновлено:" in content:
        # Извлекаем дату из строки
        for line in content.split('\n'):
            if "обновлено:" in line:
                try:
                    # Ищем дату в формате YYYY-MM-DD
                    import re
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                    if date_match:
                        date_str = date_match.group(1)
                        last_update = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                        days_since = (today - last_update).days
                        
                        if days_since > 30:
                            print(f"⚠️  Интро не обновлялось {days_since} дней!")
                            print("💡 Рекомендуется обновить:")
                            print("   - Текущие проекты и достижения")
                            print("   - Новые технологические интересы")
                            print("   - Изменения в карьерном пути")
                            print("   - Обновить дату в файле")
                        elif days_since > 14:
                            print(f"📝 Интро обновлялось {days_since} дней назад")
                            print("💡 Можно рассмотреть обновление")
                        else:
                            print(f"✅ Интро актуально! Обновлялось {days_since} дней назад")
                    else:
                        print("⚠️  Дата в строке не найдена")
                        
                except ValueError:
                    print("⚠️  Не удалось распарсить дату обновления")
                break
    else:
        print("⚠️  Дата обновления не найдена в файле")
    
    # Проверяем наличие ключевых разделов
    sections = [
        "## Текущее интро",
        "## Ключевые теги для поиска", 
        "## Структура для обновления",
        "## История обновлений",
        "## Планы по развитию"
    ]
    
    missing_sections = []
    for section in sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"\n⚠️  Отсутствуют разделы: {', '.join(missing_sections)}")
        print("💡 Рекомендуется добавить недостающие разделы")
    
    # Предложения по обновлению
    print(f"\n📅 Сегодня: {today.strftime('%Y-%m-%d')}")
    print("\n💡 Что можно обновить в интро:")
    print("   1. Новые проекты и достижения")
    print("   2. Изменения в технологических интересах")
    print("   3. Обновление карьерного пути")
    print("   4. Новые хобби и увлечения")
    print("   5. Изменения в географическом положении")
    print("   6. Обновление социальных сетей")

def main():
    """Основная функция"""
    print("🔍 Проверка файла интро...")
    print("=" * 50)
    
    check_intro_file()
    
    print("\n" + "=" * 50)
    print("✅ Проверка завершена!")

if __name__ == "__main__":
    main()

