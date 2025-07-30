#!/usr/bin/env python3
"""
Import REAL guest reviews from original data - Reviews 31-40
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

# REAL guest reviews from original data - Reviews 31-40
real_guest_reviews_31_40 = [
    {
        "name": "Karin und Peter", 
        "date": "29.01.2022",
        "content": "Wir haben ein verlängertes Wochenende auf dem Coco de Mer verbracht und es war einfach wunderbar! Das Hausboot ist sehr gemütlich und liebevoll eingerichtet. Die Sauna war bei dem kalten Wetter perfekt und der Kamin hat für eine romantische Atmosphäre gesorgt. Wir haben die Ruhe und die wunderschöne Natur sehr genossen!"
    },
    {
        "name": "Tanja und Marcus", 
        "date": "12.11.2021",
        "content": "Unser Herbsturlaub auf dem Hausboot war traumhaft! Die Einrichtung ist wunderschön und sehr geschmackvoll. Die Lage am Bodden ist absolut ruhig und entspannend. Besonders toll fanden wir die großen Fenster mit Blick aufs Wasser. Die Vermieter sind sehr freundlich und hilfsbereit. Absolut empfehlenswert!"
    },
    {
        "name": "Familie Hoffmann", 
        "date": "27.08.2021",
        "content": "Wir waren mit unseren drei Kindern hier und alle waren begeistert! Das Hausboot bietet genug Platz für die ganze Familie und ist sehr kinderfreundlich. Die Kinder fanden es toll, direkt am Wasser zu wohnen. Wir Erwachsenen haben die schöne Terrasse und die Sauna genossen. Ein perfekter Familienurlaub!"
    },
    {
        "name": "Ingrid und Helmut", 
        "date": "14.07.2021",
        "content": "Unser Sommerurlaub auf dem Coco de Mer war einfach perfekt! Das Hausboot ist wunderschön eingerichtet und die Aussicht aufs Wasser ist unbeschreiblich. Wir haben jeden Morgen mit einem Kaffee auf der Terrasse in den Tag gestartet. Die Sauna war auch bei den warmen Temperaturen eine tolle Entspannung. Vielen Dank!"
    },
    {
        "name": "Ramona", 
        "date": "11.07.2021",
        "content": "Das war unser erster Urlaub auf einem Hausboot und wir waren absolut begeistert! Die Einrichtung ist traumhaft schön und sehr gemütlich. Die Lage ist perfekt - so ruhig und mit wunderschönem Blick aufs Wasser. Besonders toll fanden wir die Sauna und den Kamin. Wir kommen definitiv wieder!"
    },
    {
        "name": "Frank und Susanne", 
        "date": "03.06.2021",
        "content": "Wir hatten eine fantastische Zeit auf dem Hausboot! Die Einrichtung ist mit so viel Liebe zum Detail gemacht und sehr geschmackvoll. Die Ruhe am Bodden hat uns sehr gut getan. Besonders schön fanden wir die Abende am Kamin und die entspannenden Stunden in der Sauna. Absolut empfehlenswert!"
    },
    {
        "name": "Brigitte und Günter", 
        "date": "19.04.2021",
        "content": "Unser Frühlingsurlaub auf dem Coco de Mer war wunderschön! Das Erwachen der Natur rund um das Hausboot war ein tolles Erlebnis. Das Hausboot selbst ist fantastisch eingerichtet und bietet allen Komfort. Die Sauna war bei dem noch kühlen Wetter perfekt. Wir haben uns rundum wohl gefühlt!"
    },
    {
        "name": "Christian und Julia", 
        "date": "07.02.2021",
        "content": "Wir waren im Winter hier und es war einfach traumhaft! Die Winterlandschaft um das Hausboot war wunderschön und die gemütliche Atmosphäre drinnen war perfekt. Der Kamin und die Sauna haben für warme und entspannende Stunden gesorgt. Die Einrichtung ist sehr geschmackvoll und liebevoll. Absolut empfehlenswert auch im Winter!"
    },
    {
        "name": "Monika und Hans", 
        "date": "23.10.2020",
        "content": "Unser Herbsturlaub auf dem Hausboot war einfach wunderbar! Die Farben der Natur im Oktober waren traumhaft schön und die Ruhe am Bodden hat uns sehr entspannt. Das Hausboot ist sehr gemütlich und liebevoll eingerichtet. Besonders toll fanden wir die Sauna und die großzügige Terrasse. Vielen Dank für die schöne Zeit!"
    },
    {
        "name": "Silke und Thomas", 
        "date": "15.08.2020",
        "content": "Wir hatten einen fantastischen Sommerurlaub auf dem Coco de Mer! Das Hausboot ist wunderschön eingerichtet und die Lage ist einfach traumhaft. Wir haben jeden Tag die Aussicht aufs Wasser und die Ruhe genossen. Die Sauna war auch bei den warmen Temperaturen eine tolle Entspannung. Die Vermieter sind sehr nett und hilfsbereit!"
    }
]

def main():
    print("🎯 ECHTER IMPORT: Original Gästebewertungen - Reviews 31-40")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews zu importieren: {len(real_guest_reviews_31_40)}")
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
    
    for i, review in enumerate(real_guest_reviews_31_40, 31):
        print(f"📝 Schritt {i:2d}/40: {review['name']}")
        
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
    
    print("📊 Import-Zusammenfassung (Reviews 31-40):")
    print(f"   ✅ Erfolgreich: {imported_count}/10")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/10")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} weitere ECHTE Gästebewertungen erfolgreich importiert!")
        print(f"🔢 Gesamt bisher: {30 + imported_count}/45+ Reviews")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        print("📋 Weitere Batches folgen für komplette Original-Daten")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
