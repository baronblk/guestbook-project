#!/usr/bin/env python3
"""
Script zum Erstellen eines Admin-Benutzers
"""
import sys
import os
import asyncio
from sqlalchemy.orm import Session

# Path für Import hinzufügen
sys.path.append('/app')

from app.database import SessionLocal, engine
from app.models import Base, AdminUser
from app.crud import admin_user_crud
from app.schemas import AdminUserCreate

def create_admin_user():
    """Erstellt einen Admin-Benutzer oder aktualisiert das Passwort"""
    # Tabellen erstellen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Umgebungsvariablen lesen
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@guestbook.local")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
        
        # Prüfen ob bereits Admin-Benutzer existiert
        existing_admin = db.query(AdminUser).filter(AdminUser.username == admin_username).first()
        
        if existing_admin:
            print(f"Admin-Benutzer '{existing_admin.username}' existiert bereits.")
            
            # Passwort aktualisieren falls es sich geändert hat
            from app.core.security import get_password_hash
            new_password_hash = get_password_hash(admin_password)
            
            if existing_admin.hashed_password != new_password_hash:
                existing_admin.hashed_password = new_password_hash
                existing_admin.email = admin_email  # E-Mail auch aktualisieren
                db.commit()
                print(f"✅ Admin-Passwort und E-Mail für '{admin_username}' erfolgreich aktualisiert!")
            else:
                print(f"ℹ️  Admin-Passwort ist bereits aktuell.")
            return
        
        # Neuen Admin-Benutzer erstellen
        admin_data = AdminUserCreate(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        
        admin_user = admin_user_crud.create_admin_user(db, admin_data)
        admin_user.is_superuser = True
        db.commit()
        
        print(f"✅ Admin-Benutzer '{admin_user.username}' erfolgreich erstellt!")
        print(f"E-Mail: {admin_user.email}")
        print("⚠️  Bitte Passwort nach dem ersten Login ändern!")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen/Aktualisieren des Admin-Benutzers: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
