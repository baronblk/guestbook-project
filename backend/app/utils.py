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
    def export_reviews_json(reviews: list, include_comments: bool = True) -> dict:
        """Reviews als JSON exportieren mit optionalen Kommentaren"""
        export_data = {
            'exported_at': datetime.utcnow().isoformat(),
            'total_reviews': len(reviews),
            'include_comments': include_comments,
            'reviews': []
        }
        
        for review in reviews:
            review_data = {
                'id': review.id,
                'name': review.name,
                'email': review.email,
                'rating': review.rating,
                'title': review.title,
                'content': review.content,
                'created_at': review.created_at.isoformat() if review.created_at else None,
                'updated_at': review.updated_at.isoformat() if review.updated_at else None,
                'is_approved': review.is_approved,
                'is_featured': review.is_featured,
                'import_source': getattr(review, 'import_source', None),
                'external_id': getattr(review, 'external_id', None)
            }
            
            # Kommentare hinzufügen falls gewünscht
            if include_comments and hasattr(review, 'comments') and review.comments:
                review_data['comments'] = [
                    {
                        'id': comment.id,
                        'name': comment.name,
                        'email': comment.email,
                        'content': comment.content,
                        'created_at': comment.created_at.isoformat() if comment.created_at else None,
                        'updated_at': comment.updated_at.isoformat() if comment.updated_at else None,
                        'is_approved': comment.is_approved,
                        'admin_notes': comment.admin_notes,
                        'ip_address': comment.ip_address
                    }
                    for comment in review.comments
                ]
            else:
                review_data['comments'] = []
            
            export_data['reviews'].append(review_data)
        
        return export_data
    
    @staticmethod
    def convert_export_to_import_format(export_data: dict, import_source: str = "export_reimport") -> dict:
        """Konvertiert Export-Format zu Import-Format mit Kommentar-Support"""
        if 'reviews' not in export_data:
            raise ValueError("Invalid export format: missing 'reviews' key")
        
        import_reviews = []
        for review in export_data['reviews']:
            import_review = {
                'name': review['name'],
                'rating': review['rating'],
                'content': review['content'],
                'title': review.get('title'),
                'email': review.get('email'),
                'created_at': review.get('created_at'),
                'import_source': import_source,
                'external_id': review.get('external_id'),
                'comments': []
            }
            
            # Kommentare konvertieren falls vorhanden
            if 'comments' in review and review['comments']:
                import_review['comments'] = [
                    {
                        'name': comment['name'],
                        'email': comment.get('email'),
                        'content': comment['content'],
                        'created_at': comment.get('created_at'),
                        'is_approved': comment.get('is_approved', False),
                        'admin_notes': comment.get('admin_notes')
                    }
                    for comment in review['comments']
                ]
            
            import_reviews.append(import_review)
        
        return {
            'source': import_source,
            'reviews': import_reviews,
            'include_comments': export_data.get('include_comments', False)
        }

from io import BytesIO
from datetime import datetime
