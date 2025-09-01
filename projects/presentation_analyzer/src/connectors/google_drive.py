"""
Google Drive Connector
Подключение к Google Drive API и работа с презентациями
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Если изменяете эти области, удалите файл token.json
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

class GoogleDriveConnector:
    """Класс для работы с Google Drive API"""
    
    def __init__(self, credentials_path: str, folder_id: str):
        """
        Инициализация подключения к Google Drive
        
        Args:
            credentials_path: Путь к файлу credentials.json
            folder_id: ID папки с презентациями
        """
        self.credentials_path = credentials_path
        self.folder_id = folder_id
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в Google Drive API"""
        creds = None
        
        # Файл token.json хранит токены доступа и обновления пользователя
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # Если нет валидных (доступных) учетных данных, попросите пользователя войти в систему
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Сохраните учетные данные для следующего запуска
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Успешное подключение к Google Drive API")
        except Exception as e:
            logger.error(f"Ошибка подключения к Google Drive API: {e}")
            raise
    
    def list_presentations(self, file_types: List[str] = None) -> List[Dict]:
        """
        Получение списка презентаций из указанной папки
        
        Args:
            file_types: Список MIME типов файлов для фильтрации
            
        Returns:
            Список метаданных файлов
        """
        if not self.service:
            raise Exception("Google Drive API не инициализирован")
        
        if file_types is None:
            file_types = [
                'application/vnd.google-apps.presentation',
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            ]
        
        try:
            # Построение запроса для поиска файлов
            query_parts = [f"'{self.folder_id}' in parents"]
            
            # Добавление фильтра по типам файлов
            mime_types = " or ".join([f"mimeType='{mime_type}'" for mime_type in file_types])
            query_parts.append(f"({mime_types})")
            
            query = " and ".join(query_parts)
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size, owners)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"Найдено {len(files)} презентаций в папке")
            
            return files
            
        except HttpError as error:
            logger.error(f"Ошибка при получении списка файлов: {error}")
            return []
    
    def download_file(self, file_id: str, file_name: str, output_path: str) -> bool:
        """
        Скачивание файла из Google Drive
        
        Args:
            file_id: ID файла в Google Drive
            file_name: Имя файла
            output_path: Путь для сохранения
            
        Returns:
            True если скачивание успешно, False иначе
        """
        if not self.service:
            raise Exception("Google Drive API не инициализирован")
        
        try:
            # Получение метаданных файла
            file_metadata = self.service.files().get(fileId=file_id).execute()
            mime_type = file_metadata.get('mimeType', '')
            
            # Для Google Slides экспортируем в PDF
            if mime_type == 'application/vnd.google-apps.presentation':
                return self._export_google_slides_to_pdf(file_id, file_name, output_path)
            
            # Для других файлов скачиваем напрямую
            else:
                return self._download_direct_file(file_id, file_name, output_path)
                
        except HttpError as error:
            logger.error(f"Ошибка при скачивании файла {file_name}: {error}")
            return False
    
    def _export_google_slides_to_pdf(self, file_id: str, file_name: str, output_path: str) -> bool:
        """Экспорт Google Slides в PDF"""
        try:
            # Экспорт в PDF
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType='application/pdf'
            )
            
            # Создание директории если не существует
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Скачивание файла
            with open(output_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        logger.info(f"Скачивание {file_name}: {int(status.progress() * 100)}%")
            
            logger.info(f"Успешно экспортирован в PDF: {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка экспорта Google Slides в PDF: {e}")
            return False
    
    def _download_direct_file(self, file_id: str, file_name: str, output_path: str) -> bool:
        """Прямое скачивание файла"""
        try:
            request = self.service.files().get_media(fileId=file_id)
            
            # Создание директории если не существует
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Скачивание файла
            with open(output_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        logger.info(f"Скачивание {file_name}: {int(status.progress() * 100)}%")
            
            logger.info(f"Успешно скачан: {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка скачивания файла: {e}")
            return False
    
    def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        """
        Получение метаданных файла
        
        Args:
            file_id: ID файла
            
        Returns:
            Метаданные файла или None
        """
        if not self.service:
            raise Exception("Google Drive API не инициализирован")
        
        try:
            metadata = self.service.files().get(
                fileId=file_id,
                fields="id,name,mimeType,createdTime,modifiedTime,size,owners,description"
            ).execute()
            
            return metadata
            
        except HttpError as error:
            logger.error(f"Ошибка при получении метаданных файла {file_id}: {error}")
            return None

