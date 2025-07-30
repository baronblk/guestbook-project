#!/usr/bin/env python3
"""
Datenbankmigrationsscript für Gästebuch-Moderation

Dieses Script:
1. Erstellt die nötigen Datenbankänderungen (falls nötig)
2. Setzt alle bestehenden Bewertungen auf is_approved=False, damit sie moderiert werden müssen
3. Optional: Setzt nur importierte Bewertungen auf is_approved=True

Verwendung:
    python migrate_moderation.py [--keep-existing-approved]
"""

import os
import sys
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database URL aus Umgebungsvariablen
DB_USER = os.getenv('DB_USER', 'guestuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'whHBJveMvwjs5a6p')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'guestbook')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def run_migration(keep_existing_approved=False):
    """Führt die Datenbankmigraton durch"""
    
    try:
        # Datenbankverbindung erstellen
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🔄 Starte Moderations-Migration...")
        
        # Prüfen ob die Spalte is_approved existiert (sollte sie bereits)
        try:
            result = session.execute(text("DESCRIBE reviews is_approved"))
            print("✅ Spalte 'is_approved' existiert bereits")
        except Exception as e:
            print(f"❌ Fehler beim Prüfen der Spalte: {e}")
            print("⚠️ Möglicherweise muss die Datenbank neu erstellt werden")
            return False
        
        if keep_existing_approved:
            # Nur neue Einträge (ohne import_source) auf unapproved setzen
            result = session.execute(text("""
                UPDATE reviews 
                SET is_approved = FALSE 
                WHERE import_source IS NULL OR import_source = ''
            """))
            affected_rows = result.rowcount
            print(f"✅ {affected_rows} neue Bewertungen als 'nicht genehmigt' markiert")
            print("ℹ️ Importierte Bewertungen bleiben genehmigt")
        else:
            # Alle bestehenden Bewertungen auf unapproved setzen für vollständige Moderation
            result = session.execute(text("""
                UPDATE reviews 
                SET is_approved = FALSE 
                WHERE is_approved = TRUE
            """))
            affected_rows = result.rowcount
            print(f"✅ {affected_rows} Bewertungen als 'nicht genehmigt' markiert")
            print("ℹ️ Alle Bewertungen müssen jetzt moderiert werden")
        
        # Statistiken anzeigen
        total_reviews = session.execute(text("SELECT COUNT(*) FROM reviews")).scalar()
        approved_reviews = session.execute(text("SELECT COUNT(*) FROM reviews WHERE is_approved = TRUE")).scalar()
        pending_reviews = total_reviews - approved_reviews
        
        print(f"\n📊 Aktuelle Statistiken:")
        print(f"   Gesamt: {total_reviews} Bewertungen")
        print(f"   Genehmigt: {approved_reviews}")
        print(f"   Ausstehend: {pending_reviews}")
        
        session.commit()
        session.close()
        
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("💡 Neue Bewertungen werden ab sofort standardmäßig versteckt und müssen freigegeben werden")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler bei der Migration: {e}")
        if 'session' in locals():
            session.rollback()
            session.close()
        return False

def main():
    parser = argparse.ArgumentParser(description='Gästebuch Moderations-Migration')
    parser.add_argument(
        '--keep-existing-approved',
        action='store_true',
        help='Bereits importierte Bewertungen bleiben genehmigt (empfohlen für bestehende Daten)'
    )
    
    args = parser.parse_args()
    
    print("🚀 Gästebuch Moderations-Migration")
    print("=" * 50)
    
    if args.keep_existing_approved:
        print("📋 Modus: Importierte Bewertungen bleiben genehmigt")
        print("⚠️ Nur neue (selbst erstellte) Bewertungen werden als 'nicht genehmigt' markiert")
    else:
        print("📋 Modus: Alle Bewertungen werden als 'nicht genehmigt' markiert")
        print("⚠️ Sie müssen alle bestehenden Bewertungen manuell freigeben")
    
    print(f"🔗 Datenbank: {DB_HOST}/{DB_NAME}")
    
    confirm = input("\nMöchten Sie fortfahren? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Migration abgebrochen")
        return
    
    success = run_migration(args.keep_existing_approved)
    
    if success:
        print("\n🎉 Migration erfolgreich!")
        print("👉 Sie können jetzt das Admin-Dashboard verwenden, um Bewertungen zu moderieren")
        sys.exit(0)
    else:
        print("\n💥 Migration fehlgeschlagen!")
        sys.exit(1)

if __name__ == "__main__":
    main()
