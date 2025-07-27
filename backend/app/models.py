from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Review(Base):
    """Gästebuch-Bewertung Model"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=True)  # Optional, für Benachrichtigungen
    rating = Column(Integer, nullable=False)  # 1-5 Sterne
    title = Column(String(200), nullable=True)  # Optionaler Titel
    content = Column(Text, nullable=False)  # Bewertungstext (max 5000 Zeichen)
    image_path = Column(String(500), nullable=True)  # Pfad zum hochgeladenen Bild
    
    # Metadaten
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Admin-Features
    is_approved = Column(Boolean, default=True, nullable=False)  # Moderation
    is_featured = Column(Boolean, default=False, nullable=False)  # Hervorheben
    admin_notes = Column(Text, nullable=True)  # Interne Notizen
    
    # Import-Tracking
    import_source = Column(String(100), nullable=True)  # z.B. "google_reviews"
    external_id = Column(String(255), nullable=True)  # Original-ID aus Import
    
    # IP-Adresse für Anti-Spam (optional)
    ip_address = Column(String(45), nullable=True)
    
    def __repr__(self):
        return f"<Review(id={self.id}, name='{self.name}', rating={self.rating})>"

class AdminUser(Base):
    """Admin-Benutzer für Verwaltung"""
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<AdminUser(id={self.id}, username='{self.username}')>"
