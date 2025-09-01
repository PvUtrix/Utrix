"""
Text Extractor
Извлечение текста из PDF файлов с поддержкой OCR
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
import re
from pathlib import Path

import pdfplumber
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import numpy as np
import io

logger = logging.getLogger(__name__)

class TextExtractor:
    """Класс для извлечения текста из PDF файлов"""
    
    def __init__(self, ocr_enabled: bool = True, language: str = "rus"):
        """
        Инициализация экстрактора текста
        
        Args:
            ocr_enabled: Включить OCR для изображений
            language: Язык для OCR (rus, eng, etc.)
        """
        self.ocr_enabled = ocr_enabled
        self.language = language
        
        # Настройка tesseract для русского языка
        if self.ocr_enabled:
            try:
                # Проверка доступности tesseract
                pytesseract.get_tesseract_version()
                logger.info("Tesseract OCR доступен")
            except Exception as e:
                logger.warning(f"Tesseract OCR недоступен: {e}")
                self.ocr_enabled = False
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """
        Извлечение текста из PDF файла
        
        Args:
            pdf_path: Путь к PDF файлу
            
        Returns:
            Словарь с извлеченным текстом и метаданными
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF файл не найден: {pdf_path}")
        
        result = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'total_pages': 0,
            'pages': [],
            'full_text': '',
            'extraction_method': 'pdfplumber',
            'ocr_used': False
        }
        
        try:
            # Попытка извлечения с помощью pdfplumber
            text_data = self._extract_with_pdfplumber(pdf_path)
            if text_data['success']:
                result.update(text_data['data'])
                logger.info(f"Успешно извлечен текст из {pdf_path} с помощью pdfplumber")
                return result
            
            # Если pdfplumber не сработал, пробуем PyPDF2
            text_data = self._extract_with_pypdf2(pdf_path)
            if text_data['success']:
                result.update(text_data['data'])
                result['extraction_method'] = 'pypdf2'
                logger.info(f"Успешно извлечен текст из {pdf_path} с помощью PyPDF2")
                return result
            
            # Если и PyPDF2 не сработал, используем OCR
            if self.ocr_enabled:
                text_data = self._extract_with_ocr(pdf_path)
                if text_data['success']:
                    result.update(text_data['data'])
                    result['extraction_method'] = 'ocr'
                    result['ocr_used'] = True
                    logger.info(f"Успешно извлечен текст из {pdf_path} с помощью OCR")
                    return result
            
            logger.warning(f"Не удалось извлечь текст из {pdf_path}")
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении текста из {pdf_path}: {e}")
            return result
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> Dict:
        """Извлечение текста с помощью pdfplumber"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages = []
                full_text = ""
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        page_data = {
                            'page_number': page_num,
                            'text': page_text.strip(),
                            'word_count': len(page_text.split()),
                            'extraction_method': 'pdfplumber'
                        }
                        pages.append(page_data)
                        full_text += page_text + "\n"
                
                return {
                    'success': True,
                    'data': {
                        'total_pages': len(pdf.pages),
                        'pages': pages,
                        'full_text': full_text.strip()
                    }
                }
                
        except Exception as e:
            logger.debug(f"pdfplumber не смог извлечь текст: {e}")
            return {'success': False}
    
    def _extract_with_pypdf2(self, pdf_path: str) -> Dict:
        """Извлечение текста с помощью PyPDF2"""
        try:
            pages = []
            full_text = ""
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        page_data = {
                            'page_number': page_num + 1,
                            'text': page_text.strip(),
                            'word_count': len(page_text.split()),
                            'extraction_method': 'pypdf2'
                        }
                        pages.append(page_data)
                        full_text += page_text + "\n"
                
                return {
                    'success': True,
                    'data': {
                        'total_pages': total_pages,
                        'pages': pages,
                        'full_text': full_text.strip()
                    }
                }
                
        except Exception as e:
            logger.debug(f"PyPDF2 не смог извлечь текст: {e}")
            return {'success': False}
    
    def _extract_with_ocr(self, pdf_path: str) -> Dict:
        """Извлечение текста с помощью OCR"""
        if not self.ocr_enabled:
            return {'success': False}
        
        try:
            pages = []
            full_text = ""
            
            # Открываем PDF с помощью PyMuPDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                
                # Получаем изображение страницы
                mat = fitz.Matrix(2, 2)  # Увеличиваем разрешение для лучшего OCR
                pix = page.get_pixmap(matrix=mat)
                
                # Конвертируем в PIL Image
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # OCR
                page_text = pytesseract.image_to_string(
                    img, 
                    lang=self.language,
                    config='--psm 6'  # Предполагаем единый блок текста
                )
                
                if page_text.strip():
                    page_data = {
                        'page_number': page_num + 1,
                        'text': page_text.strip(),
                        'word_count': len(page_text.split()),
                        'extraction_method': 'ocr'
                    }
                    pages.append(page_data)
                    full_text += page_text + "\n"
            
            doc.close()
            
            return {
                'success': True,
                'data': {
                    'total_pages': total_pages,
                    'pages': pages,
                    'full_text': full_text.strip()
                }
            }
            
        except Exception as e:
            logger.error(f"Ошибка OCR: {e}")
            return {'success': False}
    
    def clean_text(self, text: str) -> str:
        """
        Очистка извлеченного текста
        
        Args:
            text: Исходный текст
            
        Returns:
            Очищенный текст
        """
        if not text:
            return ""
        
        # Удаление лишних пробелов и переносов строк
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Удаление специальных символов (но оставляем кириллицу и латиницу)
        text = re.sub(r'[^\w\sа-яёА-ЯЁ.,!?;:()\-–—""''\n]', '', text)
        
        # Нормализация кавычек
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()
    
    def extract_keywords(self, text: str, max_keywords: int = 20) -> List[str]:
        """
        Извлечение ключевых слов из текста
        
        Args:
            text: Исходный текст
            max_keywords: Максимальное количество ключевых слов
            
        Returns:
            Список ключевых слов
        """
        if not text:
            return []
        
        # Простое извлечение ключевых слов (можно улучшить с помощью NLP)
        words = re.findall(r'\b[а-яёА-ЯЁ]{3,}\b', text.lower())
        
        # Подсчет частоты
        word_freq = {}
        for word in words:
            if word not in word_freq:
                word_freq[word] = 0
            word_freq[word] += 1
        
        # Сортировка по частоте и выбор топ ключевых слов
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in keywords[:max_keywords]]
        
        return keywords
    
    def generate_summary(self, text: str, max_length: int = 500) -> str:
        """
        Генерация краткого содержания
        
        Args:
            text: Исходный текст
            max_length: Максимальная длина краткого содержания
            
        Returns:
            Краткое содержание
        """
        if not text:
            return ""
        
        # Простое извлечение первых предложений
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        summary = ""
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + ". "
            else:
                break
        
        return summary.strip()

