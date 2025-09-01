#!/usr/bin/env python3
"""
Quick Presentation Sync Script
Быстрый скрипт для синхронизации презентаций в утренней рутине
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулям проекта
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.main import PresentationAnalyzer

def quick_sync():
    """Быстрая синхронизация презентаций"""
    try:
        print("🔄 Запуск синхронизации презентаций...")
        
        analyzer = PresentationAnalyzer()
        
        # Только синхронизация (без полной обработки)
        downloaded_files = analyzer.sync_presentations()
        
        if downloaded_files:
            print(f"✅ Синхронизация завершена! Скачано файлов: {len(downloaded_files)}")
            
            # Краткий список скачанных файлов
            print("\n📥 Скачанные файлы:")
            for file_info in downloaded_files:
                print(f"  • {file_info['file_name']}")
            
            return True
        else:
            print("ℹ️ Нет новых файлов для синхронизации")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")
        return False

def quick_process():
    """Быстрая обработка уже скачанных файлов"""
    try:
        print("🔄 Запуск обработки презентаций...")
        
        analyzer = PresentationAnalyzer()
        
        # Обработка уже скачанных файлов
        results = analyzer.process_all()
        
        if results:
            print(f"✅ Обработка завершена! Обработано файлов: {len(results)}")
            
            # Краткий отчет
            print("\n📊 Результаты обработки:")
            for result in results:
                print(f"  • {result['file_name']}: {result['word_count']} слов, {len(result['keywords'])} ключевых слов")
            
            return True
        else:
            print("ℹ️ Нет файлов для обработки")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Быстрая синхронизация презентаций")
    parser.add_argument("--sync", action="store_true", help="Синхронизировать файлы из Google Drive")
    parser.add_argument("--process", action="store_true", help="Обработать уже скачанные файлы")
    parser.add_argument("--full", action="store_true", help="Полный анализ (синхронизация + обработка)")
    
    args = parser.parse_args()
    
    if args.full:
        # Полный анализ
        analyzer = PresentationAnalyzer()
        report = analyzer.run_full_analysis()
        
        if report['status'] == 'success':
            print(f"✅ Полный анализ завершен!")
            print(f"📥 Скачано: {report['downloaded_files']}, Обработано: {report['processed_files']}")
        else:
            print(f"❌ Ошибка: {report.get('error', 'Неизвестная ошибка')}")
    
    elif args.sync:
        quick_sync()
    
    elif args.process:
        quick_process()
    
    else:
        # По умолчанию - только синхронизация
        quick_sync()
