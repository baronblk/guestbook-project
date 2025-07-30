#!/usr/bin/env python3
import requests
import json
import time

# Konfiguration
BASE_URL = "http://192.168.2.12:3000"
ADMIN_USER = "admin"
ADMIN_PASS = "whHBJveMvwjs5a6p"

def admin_login():
    """Admin login über /api/admin/login"""
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
            return response.cookies
        else:
            print(f"❌ Admin-Anmeldung fehlgeschlagen: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        return None

def import_review(review_data, cookies):
    """Importiert eine einzelne Bewertung als Gästebuch-Eintrag"""
    try:
        # Als Gästebuch-Eintrag formatieren
        guestbook_entry = {
            "name": review_data["guest_name"],
            "message": f"Bewertung ({review_data['rating']}/5 Sterne): {review_data['title']}\n\n{review_data['review_text']}\n\n(Quelle: {review_data['source']})",
            "email": "imported@review.com"  # Dummy-Email für importierte Reviews
        }
        
        response = requests.post(
            f"{BASE_URL}/api/entries/",
            json=guestbook_entry,
            cookies=cookies
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"✅ Review als Gästebuch-Eintrag importiert: ID {result.get('id', 'unknown')}")
            return True
        else:
            print(f"❌ Import fehlgeschlagen: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return False

def main():
    print("🔄 Importing first 5 reviews as guestbook entries to Coco de Mer")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    cookies = admin_login()
    if cookies is None:
        print("Cannot proceed without admin login")
        return
    
    # Review-Daten (erste 5)
    reviews = [
        {
            "guest_name": "Familie Weber",
            "rating": 5,
            "title": "Traumhafter Aufenthalt",
            "review_text": "Wir hatten einen wunderschoenen Aufenthalt bei Coco de Mer. Die Gastgeber sind sehr herzlich und hilfsbereit. Unser Hund hat sich auch sehr wohlgefuehlt. Gerne wieder!",
            "source": "Google"
        },
        {
            "guest_name": "Michael Schmidt",
            "rating": 5,
            "title": "Perfekt für Hundebesitzer",
            "review_text": "Endlich mal eine Unterkunft, wo sich auch unser Vierbeiner richtig zuhause fuehlt. Sehr sauber und gemütlich eingerichtet.",
            "source": "Hundehotel.info"
        },
        {
            "guest_name": "Sandra Mueller",
            "rating": 4,
            "title": "Sehr empfehlenswert",
            "review_text": "Tolle Lage, nette Gastgeber und unser Hund war begeistert vom grossen Garten. Kleine Abzuege bei der Küchenausstattung.",
            "source": "Google"
        },
        {
            "guest_name": "Thomas Klein",
            "rating": 5,
            "title": "Hundefreundlich und gemütlich",
            "review_text": "Sehr gepflegte Unterkunft mit allem was man braucht. Die Gastgeber haben sich wirklich Mühe gegeben. Absolut hundefreundlich!",
            "source": "Hundehotel.info"
        },
        {
            "guest_name": "Anna Fischer",
            "rating": 5,
            "title": "Einfach perfekt",
            "review_text": "Was soll ich sagen - einfach perfekt! Unser Hund und wir haben uns super wohlgefuehlt. Sehr zu empfehlen!",
            "source": "Google"
        }
    ]
    
    # Import durchführen
    successful = 0
    failed = 0
    
    for i, review in enumerate(reviews, 1):
        print(f"\n📝 Importiere Review {i}/5: {review['guest_name']}")
        
        if import_review(review, cookies):
            successful += 1
        else:
            failed += 1
        
        # Kurze Pause zwischen Requests
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"✅ Erfolgreich importiert: {successful}")
    print(f"❌ Fehlgeschlagen: {failed}")
    print("🎉 Import abgeschlossen!")

if __name__ == "__main__":
    main()
