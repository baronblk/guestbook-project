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
        admin_is_superuser = os.getenv("ADMIN_IS_SUPERUSER", "true").lower() == "true"

        # Prüfen ob bereits Admin-Benutzer existiert
        existing_admin = db.query(AdminUser).filter(AdminUser.username == admin_username).first()

        if existing_admin:
            print(f"ℹ️  Admin-User '{existing_admin.username}' existiert bereits")

            # Passwort aktualisieren falls es sich geändert hat
            from app.auth import SecurityUtils
            new_password_hash = SecurityUtils.hash_password(admin_password)

            updated = False
            if existing_admin.hashed_password != new_password_hash:
                existing_admin.hashed_password = new_password_hash
                updated = True
                print(f"🔑 Passwort aktualisiert")

            if existing_admin.email != admin_email:
                existing_admin.email = admin_email
                updated = True
                print(f"📧 E-Mail aktualisiert: {admin_email}")

            if existing_admin.is_superuser != admin_is_superuser:
                existing_admin.is_superuser = admin_is_superuser
                updated = True
                status = "aktiviert" if admin_is_superuser else "deaktiviert"
                print(f"👑 Superuser-Status {status}")

            if not existing_admin.is_active:
                existing_admin.is_active = True
                updated = True
                print(f"✅ Benutzer aktiviert")

            if updated:
                db.commit()
                print(f"✅ Admin-Benutzer '{admin_username}' erfolgreich aktualisiert!")
            else:
                print(f"ℹ️  Alle Admin-Einstellungen sind bereits aktuell")
            return

        # Neuen Admin-Benutzer erstellen
        admin_data = AdminUserCreate(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )

        admin_user = admin_user_crud.create_admin_user(db, admin_data)
        admin_user.is_superuser = admin_is_superuser
        admin_user.is_active = True
        db.commit()

        superuser_status = "mit Superuser-Rechten" if admin_is_superuser else "ohne Superuser-Rechte"
        print(f"✅ Admin-Benutzer '{admin_user.username}' erfolgreich erstellt {superuser_status}!")
        print(f"📧 E-Mail: {admin_user.email}")
        print(f"👑 Superuser: {'Ja' if admin_is_superuser else 'Nein'}")
        print("⚠️  Bitte Passwort nach dem ersten Login ändern!")

    except Exception as e:
        print(f"❌ Fehler beim Erstellen/Aktualisieren des Admin-Benutzers: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
