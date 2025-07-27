import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from PIL import Image
import aiofiles

class FileManager:
    
    UPLOAD_DIR = "/app/uploads"
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_IMAGE_SIZE = (1200, 1200)  # Max Bildgröße nach Resize
    
    @classmethod
    async def save_image(cls, file: UploadFile) -> str:
        """Bild speichern und verarbeiten"""
        # Validierung
        if not file.filename:
            raise HTTPException(status_code=400, detail="Keine Datei ausgewählt")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Dateiformat nicht unterstützt. Erlaubt: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        
        # Dateigröße prüfen
        content = await file.read()
        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail="Datei zu groß. Maximum: 5MB"
            )
        
        # Unique filename generieren
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)
        
        # Upload-Ordner erstellen falls nicht vorhanden
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        
        # Bild verarbeiten und speichern
        try:
            # Bild öffnen und validieren
            image = Image.open(BytesIO(content))
            
            # Bild auf maximal erlaubte Größe reduzieren
            image.thumbnail(cls.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            
            # EXIF-Daten entfernen (Datenschutz)
            if hasattr(image, '_getexif'):
                image = image._getexif() and image.copy() or image
            
            # Als JPEG speichern (kleinere Dateigröße)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            
            image.save(file_path, "JPEG", quality=85, optimize=True)
            
            return f"/uploads/{unique_filename}"
            
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail="Bild konnte nicht verarbeitet werden"
            )
    
    @classmethod
    def delete_image(cls, image_path: str) -> bool:
        """Bild löschen"""
        if not image_path or not image_path.startswith("/uploads/"):
            return False
        
        filename = image_path.replace("/uploads/", "")
        file_path = os.path.join(cls.UPLOAD_DIR, filename)
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception:
            pass
        
        return False

# Text-Utilities
class TextUtils:
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Text bereinigen"""
        # HTML-Tags entfernen (basic)
        import re
        text = re.sub(r'<[^>]+>', '', text)
        
        # Mehrfache Leerzeichen/Zeilenumbrüche normalisieren
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 200) -> str:
        """Text auf maximale Länge kürzen"""
        if len(text) <= max_length:
            return text
        
        # An Wortgrenze kürzen
        truncated = text[:max_length].rsplit(' ', 1)[0]
        return f"{truncated}..."
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 5) -> list:
        """Einfache Keyword-Extraktion"""
        import re
        from collections import Counter
        
        # Stopwörter (erweiterte Liste für Deutsch und Englisch)
        stopwords = {
            'der', 'die', 'das', 'und', 'oder', 'aber', 'ist', 'war', 'hat', 'haben',
            'the', 'and', 'or', 'but', 'is', 'was', 'has', 'have', 'a', 'an', 'in',
            'on', 'at', 'to', 'for', 'of', 'with', 'by', 'very', 'really', 'so'
        }
        
        # Text in Wörter aufteilen
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Stopwörter und kurze Wörter entfernen
        keywords = [word for word in words if len(word) > 3 and word not in stopwords]
        
        # Häufigste Wörter zurückgeben
        return [word for word, count in Counter(keywords).most_common(max_keywords)]

# Import/Export Utilities
class ImportExportUtils:
    
    @staticmethod
    def parse_google_reviews_json(json_data: dict) -> list:
        """Google Reviews JSON parsen"""
        reviews = []
        
        # Annahme: Google Reviews haben ein bestimmtes Format
        # Dies müsste an das tatsächliche Google Reviews Format angepasst werden
        for item in json_data.get('reviews', []):
            review = {
                'name': item.get('author_name', 'Anonym'),
                'rating': item.get('rating', 5),
                'content': item.get('text', ''),
                'title': None,
                'external_id': item.get('id'),
                'created_at': item.get('time'),  # Ggf. Datetime-Parsing
                'import_source': 'google_reviews'
            }
            reviews.append(review)
        
        return reviews
    
    @staticmethod
    def export_reviews_json(reviews: list) -> dict:
        """Reviews als JSON exportieren"""
        export_data = {
            'exported_at': datetime.utcnow().isoformat(),
            'total_reviews': len(reviews),
            'reviews': [
                {
                    'id': review.id,
                    'name': review.name,
                    'rating': review.rating,
                    'title': review.title,
                    'content': review.content,
                    'created_at': review.created_at.isoformat(),
                    'is_featured': review.is_featured
                }
                for review in reviews
            ]
        }
        return export_data

from io import BytesIO
from datetime import datetime
