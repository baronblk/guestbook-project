#!/usr/bin/env python3
"""
Test und Import-Script für Reviews über den Backend-Endpoint
"""
import requests
import json

# API base URL (der kombinierte Container läuft auf Port 3000)
BASE_URL = "http://192.168.2.12:3000"
ADMIN_USER = "admin"
ADMIN_PASS = "whHBJveMvwjs5a6p"

def admin_login():
    """Admin login"""
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
            # JWT Token extrahieren
            token = result.get("access_token")
            if token:
                print(f"🔑 JWT Token erhalten: {token[:20]}...")
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

def test_import_endpoint(token):
    """Teste den Import-Endpoint"""
    print("🧪 Teste Import-Endpoint...")
    
    # Test-Daten
    test_data = {
        "source": "test",
        "reviews": [
            {
                "name": "Test User",
                "email": "test@example.com",
                "rating": 5,
                "title": "Test Review",
                "content": "Dies ist ein Test-Review",
                "import_source": "test"
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/reviews/import",
            json=test_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Import-Endpoint funktioniert!")
            return True
        else:
            print("❌ Import-Endpoint hat Probleme")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Test: {e}")
        return False

def import_reviews(token):
    """Importiere die ersten 5 Reviews"""
    print("📦 Importiere Reviews...")
    
    import_data = {
        "source": "historical_import", 
        "reviews": [
            {
                "name": "Familie Weber",
                "email": "imported@review.com", 
                "rating": 5,
                "title": "Traumhafter Aufenthalt",
                "content": "Wir hatten einen wunderschönen Aufenthalt bei Coco de Mer. Die Gastgeber sind sehr herzlich und hilfsbereit. Unser Hund hat sich auch sehr wohlgefühlt. Gerne wieder!",
                "import_source": "Google"
            },
            {
                "name": "Michael Schmidt",
                "email": "imported@review.com",
                "rating": 5, 
                "title": "Perfekt für Hundebesitzer",
                "content": "Endlich mal eine Unterkunft, wo sich auch unser Vierbeiner richtig zuhause fühlt. Sehr sauber und gemütlich eingerichtet.",
                "import_source": "Hundehotel.info"
            },
            {
                "name": "Sandra Mueller",
                "email": "imported@review.com",
                "rating": 4,
                "title": "Sehr empfehlenswert", 
                "content": "Tolle Lage, nette Gastgeber und unser Hund war begeistert vom großen Garten. Kleine Abzüge bei der Küchenausstattung.",
                "import_source": "Google"
            },
            {
                "name": "Thomas Klein",
                "email": "imported@review.com",
                "rating": 5,
                "title": "Hundefreundlich und gemütlich",
                "content": "Sehr gepflegte Unterkunft mit allem was man braucht. Die Gastgeber haben sich wirklich Mühe gegeben. Absolut hundefreundlich!",
                "import_source": "Hundehotel.info"
            },
            {
                "name": "Anna Fischer", 
                "email": "imported@review.com",
                "rating": 5,
                "title": "Einfach perfekt",
                "content": "Was soll ich sagen - einfach perfekt! Unser Hund und wir haben uns super wohlgefühlt. Sehr zu empfehlen!",
                "import_source": "Google"
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
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
            print(f"✅ {result.get('imported_count', 0)} Reviews erfolgreich importiert!")
            return True
        else:
            print("❌ Import fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return False

def main():
    print("🚀 Review Import Test")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    token = admin_login()
    if token is None:
        print("Cannot proceed without admin login")
        return
    
    print()
    
    # Test Import-Endpoint
    if test_import_endpoint(token):
        print()
        # Echte Reviews importieren
        import_reviews(token)
    
    print("\n🎉 Fertig!")

if __name__ == "__main__":
    main()
