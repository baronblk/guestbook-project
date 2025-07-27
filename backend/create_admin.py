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
    """Erstellt einen Admin-Benutzer"""
    # Tabellen erstellen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Prüfen ob bereits Admin-Benutzer existiert
        existing_admin = db.query(AdminUser).first()
        if existing_admin:
            print(f"Admin-Benutzer '{existing_admin.username}' existiert bereits.")
            return
        
        # Standard-Admin erstellen
        admin_data = AdminUserCreate(
            username=os.getenv("ADMIN_USERNAME", "admin"),
            email=os.getenv("ADMIN_EMAIL", "admin@guestbook.local"),
            password=os.getenv("ADMIN_PASSWORD", "admin123")
        )
        
        admin_user = admin_user_crud.create_admin_user(db, admin_data)
        admin_user.is_superuser = True
        db.commit()
        
        print(f"Admin-Benutzer '{admin_user.username}' erfolgreich erstellt!")
        print(f"E-Mail: {admin_user.email}")
        print("⚠️  Bitte Passwort nach dem ersten Login ändern!")
        
    except Exception as e:
        print(f"Fehler beim Erstellen des Admin-Benutzers: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
