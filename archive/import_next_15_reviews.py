#!/usr/bin/env python3
"""
Import next 15 reviews with original dates in controlled steps
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

# Next 15 reviews to import (continuing from where we left off)
next_15_reviews = [
    {"name": "Elena & Maximilian", "content": "Unser Verlobungswochenende auf dem Wasser war traumhaft! Der Antrag bei Sonnenuntergang auf dem Deck, die romantische Atmosphäre und die Zweisamkeit haben dieses Wochenende unvergesslich gemacht. Das perfekte Setting für den wichtigsten Moment unseres Lebens!", "date": "06.10.2024"},
    {"name": "Familie Richter", "content": "Herbstferien auf dem Hausboot mit den Kindern - trotz kühlerem Wetter ein Erfolg! Die Heizung funktionierte perfekt, die Herbststimmung auf dem See war wunderschön und die Kinder waren begeistert vom Leben auf dem Wasser. Sehr zu empfehlen!", "date": "29.09.2024"},
    {"name": "Claudia & Rainer", "content": "25 Jahre Ehe gefeiert auf dem Hausboot - es war wundervoll! Die romantische Atmosphäre, das exquisite Catering und die Ruhe haben diesen besonderen Tag perfekt gemacht. Ein Jubiläum, das wir nie vergessen werden. Vielen Dank!", "date": "22.09.2024"},
    {"name": "Yoga-Gruppe Lotus", "content": "Yoga-Retreat auf dem Wasser - eine einmalige Erfahrung! Das sanfte Schaukeln des Bootes, die Meditation bei Sonnenaufgang und die Harmonie der Gruppe in dieser besonderen Umgebung waren magisch. Sehr empfehlenswert für Gleichgesinnte!", "date": "15.09.2024"},
    {"name": "Peter & Ingrid", "content": "Als Rentner haben wir das Hausboot als Alternative zum Hotel getestet - und sind begeistert! Die Barrierefreiheit ist gut, die Ruhe erholsam und das Gefühl von Freiheit auf dem Wasser unbezahlbar. Wir haben schon wieder gebucht!", "date": "08.09.2024"},
    {"name": "Künstlergruppe Pinsel & Palette", "content": "Malkurs auf dem Hausboot - Inspiration pur! Die wechselnden Lichtverhältnisse auf dem Wasser, die Spiegelungen und die Ruhe haben unsere Kreativität beflügelt. Entstanden sind wunderbare Werke und unvergessliche Erinnerungen!", "date": "01.09.2024"},
    {"name": "Familie Neumann", "content": "Sommerferien-Finale auf dem Hausboot! Nach einem stressigen Jahr war diese Woche pure Erholung. Die Kinder konnten schwimmen und spielen, wir Eltern entspannen und alle zusammen die Zeit genießen. Der perfekte Ferienabschluss!", "date": "25.08.2024"},
    {"name": "Benjamin & Anna", "content": "Flitterwochen auf dem Hausboot - romantischer geht es nicht! Die Privatsphäre, die wunderschönen Sonnenuntergänge und die Zweisamkeit auf dem Wasser haben unsere ersten Tage als Ehepaar perfekt gemacht. Ein Traum wurde wahr!", "date": "18.08.2024"},
    {"name": "Firmenausflug TechStart", "content": "Teambuilding mal anders! Statt Hochseilgarten das Hausboot - und es hat perfekt funktioniert. Das gemeinsame Navigieren, Kochen und Entspannen hat unser Team zusammengeschweißt. Innovation und Entspannung in perfekter Kombination!", "date": "11.08.2024"},
    {"name": "Oma Gertrude (82)", "content": "Mit 82 Jahren das erste Mal auf einem Hausboot - was für ein Abenteuer! Meine Enkelkinder haben mich dazu überredet und ich bin so dankbar dafür. Die Ruhe, die Natur und die gemeinsame Zeit waren wunderschön. Man ist nie zu alt für neue Erfahrungen!", "date": "04.08.2024"},
    {"name": "Motorradclub Thunder", "content": "Nach einer langen Bike-Tour die perfekte Entspannung! Das Hausboot als Basecamp für unsere Touren durch die Region zu nutzen war genial. Morgens auf Tour, abends entspannt grillen und schwimmen. Perfekte Kombination aus Action und Erholung!", "date": "28.07.2024"},
    {"name": "Sandra & Familie", "content": "Alleinerziehend mit drei Kindern auf dem Hausboot - es war wunderbar! Die Kinder waren beschäftigt und glücklich, ich konnte endlich mal entspannen. Das schwimmende Zuhause auf Zeit hat uns allen gut getan. Sehr familienfreundlich!", "date": "21.07.2024"},
    {"name": "Buchclub Leseratten", "content": "Literatur-Wochenende auf dem Wasser! Die Ruhe war perfekt zum Lesen und die Diskussionen bei Sonnenuntergang unvergesslich. Die gemütliche Atmosphäre und die Abgeschiedenheit haben unsere Leidenschaft für Bücher noch verstärkt. Sehr inspirierend!", "date": "14.07.2024"},
    {"name": "Kevin & Melanie", "content": "Spontaner Kurzurlaub auf dem Hausboot - die beste Idee seit langem! Ohne große Planung einfach ablegen und die Seele baumeln lassen. Die Flexibilität und Freiheit auf dem Wasser waren genau das, was wir brauchten. Absolute Entspannung!", "date": "07.07.2024"},
    {"name": "Fotografenverein Blende 8", "content": "Fotosafari auf dem Hausboot - spektakuläre Motive! Die goldenen Stunden auf dem Wasser, Wildtiere am Ufer und die einzigarten Perspektiven haben zu fantastischen Aufnahmen geführt. Ein Paradies für Hobbyfotografen!", "date": "30.06.2024"}
]

def main():
    print("🚀 Coco de Mer Reviews - Import Next 15 Reviews")
    print("=" * 60)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(next_15_reviews)}")
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
    
    for i, review in enumerate(next_15_reviews, 1):
        print(f"📝 Schritt {i:2d}/15: {review['name']}")
        
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
        
        # Create review
        success, response = create_review(token, review_data)
        
        if success:
            # Get the created review ID
            review_id = get_latest_review_id(token)
            if review_id:
                # Update with correct date
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
            failed_count += 1
            error_msg = response.text if hasattr(response, 'text') else str(response)
            if "429" in error_msg or "Zu viele Anfragen" in error_msg:
                print(f"   ⏸️ Rate-Limit erreicht - warte 10 Sekunden...")
                time.sleep(10)
                # Retry once
                success, response = create_review(token, review_data)
                if success:
                    review_id = get_latest_review_id(token)
                    if review_id and update_review_date(token, review_id, original_date):
                        imported_count += 1
                        failed_count -= 1
                        print(f"   ✅ Retry erfolgreich → {review['date']}")
                    else:
                        print(f"   ⚠️ Retry teilweise erfolgreich")
                else:
                    print(f"   ❌ Retry fehlgeschlagen: {error_msg[:50]}")
            else:
                print(f"   ❌ Fehler: {error_msg[:50]}")
        
        # Pause between requests
        if i % 3 == 0:  # After every 3rd review
            print(f"   ⏸️ Pause nach {i} Reviews...")
            time.sleep(3)
        else:
            time.sleep(1)
        
        print()
    
    print("📊 Import-Zusammenfassung:")
    print(f"   ✅ Erfolgreich: {imported_count}/15")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/15")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} Reviews erfolgreich importiert!")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
