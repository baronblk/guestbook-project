#!/usr/bin/env python3
"""
Import the FINAL 10 reviews with original dates
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

# FINAL 10 reviews + die 3 fehlgeschlagenen vom Rate-Limit
final_reviews = [
    # Die 3 fehlgeschlagenen vom Rate-Limit nachholen
    {"name": "Motorradclub Thunder", "content": "Nach einer langen Bike-Tour die perfekte Entspannung! Das Hausboot als Basecamp für unsere Touren durch die Region zu nutzen war genial. Morgens auf Tour, abends entspannt grillen und schwimmen. Perfekte Kombination aus Action und Erholung!", "date": "28.07.2024"},
    {"name": "Sandra & Familie", "content": "Alleinerziehend mit drei Kindern auf dem Hausboot - es war wunderbar! Die Kinder waren beschäftigt und glücklich, ich konnte endlich mal entspannen. Das schwimmende Zuhause auf Zeit hat uns allen gut getan. Sehr familienfreundlich!", "date": "21.07.2024"},
    {"name": "Buchclub Leseratten", "content": "Literatur-Wochenende auf dem Wasser! Die Ruhe war perfekt zum Lesen und die Diskussionen bei Sonnenuntergang unvergesslich. Die gemütliche Atmosphäre und die Abgeschiedenheit haben unsere Leidenschaft für Bücher noch verstärkt. Sehr inspirierend!", "date": "14.07.2024"},
    
    # Die letzten 7 ursprünglichen Reviews
    {"name": "Naturfreunde Adlerhorst", "content": "Vogelbeobachtung vom Hausboot aus - fantastisch! Die frühen Morgenstunden auf dem Wasser, das Erwachen der Natur und die seltenen Vogelarten haben unser Naturfreunde-Herz höher schlagen lassen. Ein Paradies für Ornithologen!", "date": "14.04.2024"},
    {"name": "Familie Ostern", "content": "Osterferien auf dem Hausboot - die Kinder waren begeistert! Ostereier-Suche auf dem Boot, schwimmen trotz kühlem Wetter (die Heizung war perfekt) und gemütliche Abende beim Spielen. Ein unvergessliches Osterfest!", "date": "07.04.2024"},
    {"name": "Gesangsverein Harmonie", "content": "Probenwochenende auf dem Wasser - die Akustik war fantastisch! Das Echo über dem See, die Ruhe für konzentriertes Proben und die entspannte Atmosphäre haben unseren Chorklang verfeinert. Musik und Natur in Einklang!", "date": "31.03.2024"},
    {"name": "Abenteurer Alex", "content": "Solo-Trip auf dem Hausboot - pure Freiheit! Allein auf dem Wasser, eigene Entscheidungen treffen und die Stille genießen. Diese Auszeit vom Alltag war genau das, was meine Seele brauchte. Selbstfindung auf dem Wasser!", "date": "24.03.2024"},
    {"name": "Pärchen-Retreat Lisa & Tom", "content": "Beziehungs-Auszeit auf dem Hausboot - es hat uns wieder zusammengebracht! Weg von Ablenkungen, Zeit für Gespräche und gemeinsame Erlebnisse. Die romantische Atmosphäre und Zweisamkeit haben unsere Liebe neu entfacht!", "date": "17.03.2024"},
    {"name": "Schreibgruppe Tintenfisch", "content": "Schreibretreat auf dem Wasser - sehr inspirierend! Die Ruhe, die wechselnden Stimmungen des Sees und die Abgeschiedenheit haben unsere Kreativität beflügelt. Entstanden sind wunderbare Geschichten und Gedichte!", "date": "10.03.2024"},
    {"name": "Kater Paul & Familie", "content": "Auch unser Kater Paul war begeistert vom Hausboot! Anfangs skeptisch, aber dann hat er das Deck erobert und die Fische beobachtet. Haustierfreundlich und ein unvergesslicher Urlaub für die ganze Familie - inklusive Vierbeiner!", "date": "03.03.2024"}
]

def main():
    print("🏁 Coco de Mer Reviews - FINALE 10 Reviews")
    print("=" * 60)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(final_reviews)}")
    print("Progress: 32/47 bereits importiert → 42/47 nach diesem Batch")
    print("📝 Enthält: 3 Rate-Limit Nachholungen + 7 finale Reviews")
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
    
    for i, review in enumerate(final_reviews, 1):
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
        
        # Create review with enhanced retry logic
        success = False
        retry_count = 0
        max_retries = 4  # Extra retry for final batch
        
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
                    wait_time = min(15 * retry_count, 60)  # Longer waits for final batch
                    print(f"   ⏸️ Rate-Limit (Versuch {retry_count}/{max_retries}) - warte {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Fehler (Versuch {retry_count}/{max_retries}): {error_msg[:50]}")
                    if retry_count < max_retries:
                        time.sleep(3)
        
        if not success:
            failed_count += 1
            print(f"   ❌ Nach {max_retries} Versuchen fehlgeschlagen")
        
        # Conservative pause strategy for final batch
        if i % 2 == 0:  # After every 2nd review
            print(f"   ⏸️ Pause nach {i} Reviews (8s)...")
            time.sleep(8)
        else:
            time.sleep(4)  # Longer standard pause
        
        print()
    
    print("🏆 FINALE Import-Zusammenfassung:")
    print(f"   ✅ Erfolgreich: {imported_count}/10")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/10")
    print(f"   📈 Gesamt-Progress: {32 + imported_count}/47 Reviews ({int((32 + imported_count) / 47 * 100)}%)")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} Reviews erfolgreich importiert!")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        
        if imported_count == 10:
            print("🏁 FINALE 10 Reviews erfolgreich! Nur noch 5 Reviews verbleiben.")
        else:
            remaining_in_batch = 10 - imported_count
            total_remaining = 47 - (32 + imported_count)
            print(f"⚠️ {remaining_in_batch} Reviews aus diesem Batch fehlgeschlagen.")
            print(f"📋 Insgesamt noch {total_remaining} Reviews zu importieren.")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
