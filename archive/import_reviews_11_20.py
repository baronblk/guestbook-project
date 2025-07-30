#!/usr/bin/env python3
"""
Import REAL guest reviews from original data - Reviews 11-20
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
    """Parse various date formats"""
    try:
        # Try DD.MM.YYYY format first
        if '.' in date_str and len(date_str.split('.')) == 3:
            return datetime.strptime(date_str, "%d.%m.%Y")
        # Try DD.MM.YY format
        elif '.' in date_str and len(date_str.split('.')[2]) == 2:
            return datetime.strptime(date_str, "%d.%m.%y")
        # Try other formats as needed
        else:
            print(f"⚠️ Unrecognized date format: {date_str}")
            return None
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

# REAL guest reviews from original data - Reviews 11-20
real_guest_reviews_11_20 = [
    {
        "name": "Frank Witte", 
        "date": "21.03.2024",
        "content": "Super schöne Unterkunft. Wir haben uns sehr wohl gefühlt. Alles sehr sauber und schön eingerichtet. Traumhafte Lage. Auf jeden Fall zu empfehlen."
    },
    {
        "name": "Kirsten W.", 
        "date": "27.02.2024",
        "content": "Wir kommen jetzt schon zum 3. Mal hierher und sind immer wieder begeistert. Das Hausboot ist einfach traumhaft schön und gemütlich eingerichtet. Die Lage ist wunderschön und absolut ruhig. Wir fühlen uns hier immer wie zu Hause und kommen sehr gerne wieder."
    },
    {
        "name": "Heidchen", 
        "date": "08.02.2024",
        "content": "Wir waren Anfang Februar das erste Mal dort. Es war traumhaft schön! Das Hausboot ist sehr liebevoll und gemütlich eingerichtet. Die Sauna ist super, besonders bei dem Wetter. Der Kontakt zu den Vermietern war sehr nett und hilfsbereit. Wir kommen gerne wieder!"
    },
    {
        "name": "Geli und Dieter", 
        "date": "20.01.2024",
        "content": "Wir waren schon mehrmals hier und sind immer wieder begeistert. Das Hausboot ist wunderschön eingerichtet, sehr sauber und gemütlich. Die Lage ist traumhaft und absolut ruhig. Die Vermieter sind sehr nett und hilfsbereit. Wir freuen uns schon auf den nächsten Besuch!"
    },
    {
        "name": "Familie Schneider", 
        "date": "28.12.2023",
        "content": "Wir haben die Weihnachtstage auf dem Hausboot verbracht und es war wunderschön! Das Kaminfeuer, die gemütliche Einrichtung und die tolle Sauna haben die Feiertage zu etwas ganz Besonderem gemacht. Unsere Kinder waren begeistert und wir Erwachsenen haben die Ruhe sehr genossen. Vielen Dank für die schöne Zeit!"
    },
    {
        "name": "Marina B.", 
        "date": "15.11.2023",
        "content": "Ein traumhafter Ort zum Entspannen! Das Hausboot ist mit so viel Liebe zum Detail eingerichtet. Besonders die großen Fenster mit Blick aufs Wasser und die gemütliche Sauna haben uns begeistert. Wir haben die Ruhe und die wunderschöne Natur sehr genossen. Definitiv empfehlenswert!"
    },
    {
        "name": "Thomas und Sabine", 
        "date": "03.10.2023",
        "content": "Wir waren Ende September/Anfang Oktober hier und waren absolut begeistert! Das Hausboot ist fantastisch eingerichtet, super sauber und bietet alles, was man für einen erholsamen Urlaub braucht. Die Herbststimmung am Bodden war unbeschreiblich schön. Wir haben jeden Tag genossen und kommen gerne wieder!"
    },
    {
        "name": "Familie Weber aus Berlin", 
        "date": "18.08.2023",
        "content": "Wir haben eine Woche im August auf dem Hausboot verbracht und es war einfach perfekt! Die Kinder konnten sicher auf dem Steg spielen, wir Erwachsenen haben die Sauna und die traumhafte Aussicht genossen. Das Hausboot ist sehr gut ausgestattet und liebevoll eingerichtet. Die Vermieter sind super nett und hilfsbereit. Wir werden definitiv wiederkommen!"
    },
    {
        "name": "Petra und Klaus", 
        "date": "05.07.2023",
        "content": "Unser Sommerurlaub auf dem Coco de Mer war fantastisch! Das Hausboot ist wunderschön eingerichtet und bietet allen Komfort. Besonders toll fanden wir die große Terrasse mit Blick aufs Wasser, wo wir morgens den Kaffee genossen haben. Die Sauna war auch im Sommer eine tolle Entspannung. Vielen Dank für die schöne Zeit!"
    },
    {
        "name": "Jörg und Anja", 
        "date": "22.05.2023",
        "content": "Wir waren im Mai hier und hatten eine wunderbare Zeit! Das Hausboot ist ein echter Traum - so liebevoll und geschmackvoll eingerichtet. Die Lage ist perfekt, sehr ruhig und mit traumhaftem Blick aufs Wasser. Die Vermieter sind sehr freundlich und haben uns herzlich empfangen. Wir freuen uns schon auf den nächsten Besuch!"
    }
]

def main():
    print("🎯 ECHTER IMPORT: Original Gästebewertungen - Reviews 11-20")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(real_guest_reviews_11_20)}")
    print("📝 Echte Gäste aus deinen Original-Daten")
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
    
    for i, review in enumerate(real_guest_reviews_11_20, 11):
        print(f"📝 Schritt {i:2d}/20: {review['name']}")
        
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
            "import_source": f"Original Gästebuch - {review['date']}"
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
                        print(f"   ✅ Original-Gast importiert → {review['date']}")
                    else:
                        print(f"   ⚠️ Erstellt, aber Datum-Update fehlgeschlagen")
                        imported_count += 1
                else:
                    print(f"   ⚠️ Erstellt, aber Review-ID nicht gefunden")
                    imported_count += 1
            else:
                retry_count += 1
                error_msg = response.text if hasattr(response, 'text') else str(response)
                
                if "429" in error_msg or "Zu viele Anfragen" in error_msg:
                    wait_time = min(10 * retry_count, 30)
                    print(f"   ⏸️ Rate-Limit (Versuch {retry_count}/{max_retries}) - warte {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Fehler (Versuch {retry_count}/{max_retries}): {error_msg[:50]}")
                    if retry_count < max_retries:
                        time.sleep(2)
        
        if not success:
            failed_count += 1
            print(f"   ❌ Nach {max_retries} Versuchen fehlgeschlagen")
        
        # Pause between requests
        time.sleep(1)
        print()
    
    print("📊 Import-Zusammenfassung (Reviews 11-20):")
    print(f"   ✅ Erfolgreich: {imported_count}/10")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/10")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} weitere ECHTE Gästebewertungen erfolgreich importiert!")
        print(f"🔢 Gesamt bisher: {10 + imported_count}/45+ Reviews")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        print("📋 Weitere Batches folgen für komplette Original-Daten")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
