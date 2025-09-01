"""
Presentation Analyzer - Main Module
Основной модуль для анализа презентаций из Google Drive
"""

import os
import logging
import yaml
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from connectors.google_drive import GoogleDriveConnector
from processors.text_extractor import TextExtractor

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/presentation_analyzer.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PresentationAnalyzer:
    """Основной класс для анализа презентаций"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Инициализация анализатора презентаций
        
        Args:
            config_path: Путь к конфигурационному файлу
        """
        self.config = self._load_config(config_path)
        self.drive_connector = None
        self.text_extractor = None
        self._initialize_components()
    
    def _load_config(self, config_path: str) -> Dict:
        """Загрузка конфигурации"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            logger.info("Конфигурация загружена успешно")
            return config
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            raise
    
    def _initialize_components(self):
        """Инициализация компонентов"""
        try:
            # Инициализация Google Drive коннектора
            credentials_path = self.config['google_drive']['credentials_path']
            folder_id = self.config['google_drive']['folder_id']
            
            if folder_id == "YOUR_FOLDER_ID_HERE":
                logger.warning("Необходимо указать ID папки в конфигурации")
                return
            
            self.drive_connector = GoogleDriveConnector(credentials_path, folder_id)
            
            # Инициализация экстрактора текста
            ocr_enabled = self.config['processing']['ocr_enabled']
            language = self.config['processing']['language']
            self.text_extractor = TextExtractor(ocr_enabled, language)
            
            logger.info("Компоненты инициализированы успешно")
            
        except Exception as e:
            logger.error(f"Ошибка инициализации компонентов: {e}")
            raise
    
    def sync_presentations(self) -> List[Dict]:
        """
        Синхронизация презентаций из Google Drive
        
        Returns:
            Список метаданных синхронизированных файлов
        """
        if not self.drive_connector:
            logger.error("Google Drive коннектор не инициализирован")
            return []
        
        try:
            # Получение списка презентаций
            file_types = self.config['google_drive']['file_types']
            presentations = self.drive_connector.list_presentations(file_types)
            
            if not presentations:
                logger.info("Презентации не найдены")
                return []
            
            # Создание директорий
            raw_data_path = self.config['storage']['raw_data_path']
            os.makedirs(raw_data_path, exist_ok=True)
            
            downloaded_files = []
            
            for presentation in presentations:
                file_id = presentation['id']
                file_name = presentation['name']
                
                # Определение расширения файла
                if presentation['mimeType'] == 'application/vnd.google-apps.presentation':
                    output_name = f"{file_name}.pdf"
                else:
                    output_name = file_name
                
                output_path = os.path.join(raw_data_path, output_name)
                
                # Скачивание файла
                if self.drive_connector.download_file(file_id, file_name, output_path):
                    downloaded_files.append({
                        'file_id': file_id,
                        'file_name': file_name,
                        'local_path': output_path,
                        'metadata': presentation
                    })
                    logger.info(f"Скачан файл: {file_name}")
                else:
                    logger.warning(f"Не удалось скачать: {file_name}")
            
            logger.info(f"Синхронизация завершена. Скачано файлов: {len(downloaded_files)}")
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Ошибка синхронизации: {e}")
            return []
    
    def process_all(self) -> List[Dict]:
        """
        Обработка всех скачанных презентаций
        
        Returns:
            Список результатов обработки
        """
        if not self.text_extractor:
            logger.error("Экстрактор текста не инициализирован")
            return []
        
        raw_data_path = self.config['storage']['raw_data_path']
        processed_data_path = self.config['storage']['processed_data_path']
        
        # Создание директории для обработанных данных
        os.makedirs(processed_data_path, exist_ok=True)
        
        results = []
        
        # Поиск всех PDF файлов
        pdf_files = list(Path(raw_data_path).glob("*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Обработка файла: {pdf_file.name}")
                
                # Извлечение текста
                text_data = self.text_extractor.extract_text_from_pdf(str(pdf_file))
                
                if text_data['full_text']:
                    # Очистка текста
                    cleaned_text = self.text_extractor.clean_text(text_data['full_text'])
                    
                    # Извлечение ключевых слов
                    keywords = self.text_extractor.extract_keywords(
                        cleaned_text, 
                        self.config['text_processing']['max_keywords_per_doc']
                    )
                    
                    # Генерация краткого содержания
                    summary = self.text_extractor.generate_summary(cleaned_text)
                    
                    # Формирование результата
                    result = {
                        'file_name': pdf_file.name,
                        'file_path': str(pdf_file),
                        'processed_at': datetime.now().isoformat(),
                        'total_pages': text_data['total_pages'],
                        'word_count': len(cleaned_text.split()),
                        'extraction_method': text_data['extraction_method'],
                        'ocr_used': text_data['ocr_used'],
                        'keywords': keywords,
                        'summary': summary,
                        'full_text': cleaned_text,
                        'pages': text_data['pages']
                    }
                    
                    results.append(result)
                    
                    # Сохранение результата
                    self._save_processed_data(result, processed_data_path)
                    
                    logger.info(f"Успешно обработан: {pdf_file.name}")
                else:
                    logger.warning(f"Не удалось извлечь текст из: {pdf_file.name}")
                    
            except Exception as e:
                logger.error(f"Ошибка обработки {pdf_file.name}: {e}")
        
        logger.info(f"Обработка завершена. Обработано файлов: {len(results)}")
        return results
    
    def _save_processed_data(self, result: Dict, output_path: str):
        """Сохранение обработанных данных"""
        try:
            # Создание имени файла для сохранения
            base_name = Path(result['file_name']).stem
            output_file = Path(output_path) / f"{base_name}_processed.json"
            
            # Сохранение в JSON
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Сохранен результат: {output_file}")
            
        except Exception as e:
            logger.error(f"Ошибка сохранения данных: {e}")
    
    def integrate_with_knowledge_base(self, results: List[Dict]):
        """
        Интеграция результатов в базу знаний
        
        Args:
            results: Результаты обработки презентаций
        """
        if not self.config['integration']['auto_tagging']:
            return
        
        knowledge_path = self.config['integration']['knowledge_base_path']
        os.makedirs(knowledge_path, exist_ok=True)
        
        for result in results:
            try:
                # Создание заметки для презентации
                note_content = self._create_knowledge_note(result)
                
                # Сохранение заметки
                note_filename = f"{Path(result['file_name']).stem}_notes.md"
                note_path = Path(knowledge_path) / note_filename
                
                with open(note_path, 'w', encoding='utf-8') as f:
                    f.write(note_content)
                
                logger.info(f"Создана заметка: {note_path}")
                
            except Exception as e:
                logger.error(f"Ошибка создания заметки: {e}")
    
    def _create_knowledge_note(self, result: Dict) -> str:
        """Создание заметки для базы знаний"""
        note_content = f"""# {result['file_name']}

## 📊 Метаданные
- **Дата обработки:** {result['processed_at']}
- **Количество страниц:** {result['total_pages']}
- **Количество слов:** {result['word_count']}
- **Метод извлечения:** {result['extraction_method']}
- **OCR использован:** {'Да' if result['ocr_used'] else 'Нет'}

## 🔑 Ключевые слова
{', '.join(result['keywords'])}

## 📝 Краткое содержание
{result['summary']}

## 📄 Полный текст
{result['full_text'][:1000]}...

---
*Автоматически создано системой анализа презентаций*
"""
        return note_content
    
    def run_full_analysis(self) -> Dict:
        """
        Запуск полного анализа презентаций
        
        Returns:
            Словарь с результатами анализа
        """
        logger.info("Запуск полного анализа презентаций")
        
        try:
            # Синхронизация
            downloaded_files = self.sync_presentations()
            
            if not downloaded_files:
                logger.warning("Нет файлов для обработки")
                return {'status': 'no_files'}
            
            # Обработка
            results = self.process_all()
            
            # Интеграция с базой знаний
            self.integrate_with_knowledge_base(results)
            
            # Формирование отчета
            report = {
                'status': 'success',
                'downloaded_files': len(downloaded_files),
                'processed_files': len(results),
                'timestamp': datetime.now().isoformat(),
                'results': results
            }
            
            logger.info(f"Анализ завершен успешно. Обработано: {len(results)} файлов")
            return report
            
        except Exception as e:
            logger.error(f"Ошибка полного анализа: {e}")
            return {'status': 'error', 'error': str(e)}


def main():
    """Основная функция для запуска анализатора"""
    try:
        analyzer = PresentationAnalyzer()
        report = analyzer.run_full_analysis()
        
        if report['status'] == 'success':
            print(f"✅ Анализ завершен успешно!")
            print(f"📥 Скачано файлов: {report['downloaded_files']}")
            print(f"📊 Обработано файлов: {report['processed_files']}")
        else:
            print(f"❌ Ошибка анализа: {report.get('error', 'Неизвестная ошибка')}")
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()
