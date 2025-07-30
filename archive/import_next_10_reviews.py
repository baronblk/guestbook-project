#!/usr/bin/env python3
"""
Import next 10 reviews with original dates in controlled steps
"""
import requests
import time
from datetime import datetime

# API base URL - using production container
API_BASE_URL = "http://192.168.2.12:3000/api"

def get_admin_token():
    """Get admin JWT token"""
    try:
        response = requests.post(f"{API_BASE_URL}/admin/login?username=admin&password=whHBJveMvwjs5a6p")
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def parse_date(date_str):
    """Parse date string DD.MM.YYYY to datetime"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print(f"⚠️ Invalid date format: {date_str}")
        return None

def create_review(token, review_data):
    """Create a single review"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/reviews", 
                               json=review_data, headers=headers)
        return response.status_code in [200, 201], response
    except Exception as e:
        return False, str(e)

def update_review_date(token, review_id, new_date):
    """Update a review's created_at date"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/admin/reviews/{review_id}", 
                              json={"created_at": new_date.isoformat()}, 
                              headers=headers)
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ Error updating review date: {str(e)}")
        return False

def get_latest_review_id(token):
    """Get the latest review ID"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/admin/reviews?per_page=1", headers=headers)
        if response.status_code == 200:
            reviews = response.json().get("reviews", [])
            if reviews:
                return reviews[0]["id"]
        return None
    except Exception as e:
        print(f"❌ Error getting latest review: {str(e)}")
        return None

# Next 10 reviews to import (continuing from Familie Hoffmann onwards)
next_10_reviews = [
    {"name": "Familie Hoffmann", "content": "Drei Generationen auf dem Hausboot - es hat wunderbar geklappt! Großeltern, Eltern und Kinder hatten alle ihren Spaß. Opa beim Angeln, Oma in der Sauna, Kinder beim Schwimmen und wir beim Entspannen. Perfekt für große Familien!", "date": "23.06.2024"},
    {"name": "Daniel & Christin", "content": "Babymoon auf dem Hausboot - trotz Schwangerschaft perfekt! Die Ruhe, die gesunde Seeluft und die Entspannung waren genau das Richtige vor der Geburt. Das sanfte Schaukeln war sogar beruhigend. Ein wunderschöner Abschluss zu zweit!", "date": "16.06.2024"},
    {"name": "Senioren-WG Sonnenschein", "content": "Wir vier Senioren-Damen haben uns einen Traum erfüllt! Mit über 70 noch einmal etwas Neues wagen - das Hausboot war perfekt. Gemütlich, sicher und mit allem Komfort. Die Kaffeekränzchen auf dem Deck waren himmlisch!", "date": "09.06.2024"},
    {"name": "Grillmeister Frank", "content": "Als leidenschaftlicher Griller war der Bootsgriller ein Highlight! Frischer Fisch direkt aus dem See, perfekte Steaks mit Seeblick und dazu der Sonnenuntergang - Grillen auf dem Hausboot ist ein ganz besonderes Erlebnis!", "date": "02.06.2024"},
    {"name": "Wellness-Gruppe Harmonie", "content": "Wellness-Wochenende der besonderen Art! Die Sauna auf dem Boot, Meditation bei Sonnenaufgang und Yoga auf dem Deck haben Körper und Seele gut getan. Die Verbindung von Wasser und Entspannung ist einfach magisch!", "date": "26.05.2024"},
    {"name": "Familie Becker", "content": "Pfingstferien auf dem Hausboot mit Teenager-Kindern - überraschend harmonisch! Selbst unsere kritischen Teens waren begeistert. WLAN funktionierte für Social Media, aber die Natur hat dann doch gewonnen. Tolle Familienzeit!", "date": "19.05.2024"},
    {"name": "Ruheständler Wolfgang", "content": "Endlich Rente und das erste Mal auf einem Hausboot! Was für eine Entdeckung! Die Entschleunigung, die neuen Perspektiven und die Freiheit sind genau das, was ich im Ruhestand gesucht habe. Ein neues Hobby ist geboren!", "date": "12.05.2024"},
    {"name": "Studentengruppe Meeresbiologie", "content": "Studienfahrt mal anders! Das Hausboot als schwimmendes Labor zu nutzen war genial. Proben nehmen, Wassertiere beobachten und dabei den Komfort eines Hauses haben - perfekt für angehende Meeresbiologen!", "date": "05.05.2024"},
    {"name": "Ehepaar Goldene Hochzeit", "content": "50 Jahre Ehe auf dem Hausboot gefeiert - es war wunderschön! Die Ruhe, die Zweisamkeit und die romantische Atmosphäre haben uns an unsere Flitterwochen erinnert. Ein würdiger Rahmen für diesen besonderen Meilenstein!", "date": "28.04.2024"},
    {"name": "Hobbyköche United", "content": "Kochkurs auf dem Hausboot - einzigartig! Frischen Fisch zubereiten mit Seeblick, gemeinsam kochen in der gut ausgestatteten Küche und danit auf dem Deck genießen. Kulinarik und Natur in perfekter Harmonie!", "date": "21.04.2024"}
]

def main():
    print("🚀 Coco de Mer Reviews - Import Next 10 Reviews")
    print("=" * 60)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(next_10_reviews)}")
    print("Progress: 22/47 bereits importiert → 32/47 nach diesem Batch")
    print()
    
    # Get admin token
    print("🔐 Admin-Anmeldung...")
    token = get_admin_token()
    if not token:
        return
    
    print("✅ Admin-Anmeldung erfolgreich")
    print()
    
    imported_count = 0
    failed_count = 0
    
    for i, review in enumerate(next_10_reviews, 1):
        print(f"📝 Schritt {i:2d}/10: {review['name']}")
        
        # Parse original date
        original_date = parse_date(review["date"])
        if not original_date:
            print(f"   ❌ Ungültiges Datum: {review['date']}")
            failed_count += 1
            continue
        
        # Create review data
        review_data = {
            "name": review["name"],
            "content": review["content"],
            "rating": 5,  # Standard 5-Sterne Bewertung
            "created_at": original_date.isoformat(),
            "import_source": f"Gästebuch - {review['date']}"
        }
        
        # Create review with retry logic
        success = False
        retry_count = 0
        max_retries = 3
        
        while not success and retry_count < max_retries:
            success, response = create_review(token, review_data)
            
            if success:
                # Get the created review ID and update date
                review_id = get_latest_review_id(token)
                if review_id:
                    if update_review_date(token, review_id, original_date):
                        imported_count += 1
                        print(f"   ✅ Erstellt & Datum aktualisiert → {review['date']}")
                    else:
                        print(f"   ⚠️ Erstellt, aber Datum-Update fehlgeschlagen")
                        imported_count += 1  # Count as success anyway
                else:
                    print(f"   ⚠️ Erstellt, aber Review-ID nicht gefunden")
                    imported_count += 1  # Count as success anyway
            else:
                retry_count += 1
                error_msg = response.text if hasattr(response, 'text') else str(response)
                
                if "429" in error_msg or "Zu viele Anfragen" in error_msg:
                    wait_time = min(10 * retry_count, 30)  # Exponential backoff, max 30s
                    print(f"   ⏸️ Rate-Limit (Versuch {retry_count}/{max_retries}) - warte {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Fehler (Versuch {retry_count}/{max_retries}): {error_msg[:50]}")
                    if retry_count < max_retries:
                        time.sleep(2)
        
        if not success:
            failed_count += 1
            print(f"   ❌ Nach {max_retries} Versuchen fehlgeschlagen")
        
        # Progressive pause strategy
        if i % 3 == 0:  # After every 3rd review
            print(f"   ⏸️ Pause nach {i} Reviews (5s)...")
            time.sleep(5)
        else:
            time.sleep(2)  # Standard pause
        
        print()
    
    print("📊 Import-Zusammenfassung:")
    print(f"   ✅ Erfolgreich: {imported_count}/10")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/10")
    print(f"   📈 Gesamt-Progress: {22 + imported_count}/47 Reviews ({int((22 + imported_count) / 47 * 100)}%)")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} Reviews erfolgreich importiert!")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        
        if imported_count == 10:
            print("✨ Alle 10 Reviews erfolgreich! Bereit für die nächsten 15 Reviews.")
        else:
            print(f"⚠️ {10 - imported_count} Reviews sind fehlgeschlagen und können wiederholt werden.")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
