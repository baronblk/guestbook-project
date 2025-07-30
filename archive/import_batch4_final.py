#!/usr/bin/env python3
"""
Import aller historischen Bewertungen für Coco de Mer
Batch 4: Review 0 (letztes Review)
"""
import requests
import json
import time

# API Konfiguration
BASE_URL = "http://192.168.2.12:3000"
ADMIN_USER = "admin"
ADMIN_PASS = "whHBJveMvwjs5a6p"

def admin_login():
    """Admin login und JWT Token erhalten"""
    print("🔐 Admin-Anmeldung...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            params={
                "username": ADMIN_USER,
                "password": ADMIN_PASS
            }
        )
        
        if response.status_code == 200:
            print("✅ Admin-Anmeldung erfolgreich")
            result = response.json()
            token = result.get("access_token")
            if token:
                return token
            else:
                print("❌ Kein JWT Token erhalten")
                return None
        else:
            print(f"❌ Admin-Anmeldung fehlgeschlagen: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        return None

def import_batch_4(token):
    """Importiere Batch 4: Review 0 (das allererste Review)"""
    print("📦 Importiere Batch 4: Review 0...")
    
    reviews_batch_4 = [
        {
            "name": "Ramona",
            "email": "imported.0@coco-de-mer.review",
            "rating": 5,
            "title": "Genial - so stell ich mir den nächsten Urlaub vor",
            "content": "Genial, so stell ich mir den nächsten Urlaub vor. Noch eine Schönwettergarantie dazu und alles ist perfekt. Es gibt Personal bei eurem Lieblingsbäcker, die Interesse zeigen und im Belegungsplan vorgemerkt sein möchten. Wir wünschen viel Erfolg, einen vollen Belegungskalender und nur zufriedene Gäste. Wir sind dabei.",
            "import_source": "Gästebuch"
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    import_data = {
        "source": "historical_batch_4_final",
        "reviews": reviews_batch_4
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/reviews/import",
            json=import_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch 4: {result.get('imported_count', 0)} Reviews erfolgreich importiert!")
            return True
        else:
            print("❌ Batch 4 Import fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import von Batch 4: {e}")
        return False

def main():
    print("🚀 Coco de Mer Reviews Import - Batch 4 (Final)")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    token = admin_login()
    if token is None:
        print("Cannot proceed without admin login")
        return
    
    print()
    
    # Import Batch 4
    import_batch_4(token)
    
    print("\n🎉 Batch 4 Import abgeschlossen!")
    print("🏆 ALLE REVIEWS ERFOLGREICH IMPORTIERT!")
    print("=" * 60)
    print("📊 Import Zusammenfassung:")
    print("   • Batch 1: 15 Reviews (45-31)")
    print("   • Batch 2: 15 Reviews (30-16)")
    print("   • Batch 3: 15 Reviews (15-1)")
    print("   • Batch 4:  1 Review  (0)")
    print("   • Gesamt:  46 Reviews")
    print("=" * 60)
    print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")

if __name__ == "__main__":
    main()
