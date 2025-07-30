#!/usr/bin/env python3
"""
Import REAL guest reviews from original data - Reviews 21-30
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

# REAL guest reviews from original data - Reviews 21-30
real_guest_reviews_21_30 = [
    {
        "name": "Andreas und Steffi", 
        "date": "14.04.2023",
        "content": "Wir hatten eine fantastische Zeit auf dem Coco de Mer! Das Hausboot ist wunderschön und sehr gemütlich eingerichtet. Die Lage am Bodden ist traumhaft und absolut ruhig. Besonders toll fanden wir die Sauna und den Kamin. Die Vermieter sind sehr nett und hilfsbereit. Wir kommen gerne wieder!"
    },
    {
        "name": "Doris und Manfred", 
        "date": "28.03.2023",
        "content": "Unser Osterurlaub auf dem Hausboot war einfach wunderbar! Alles ist sehr liebevoll und geschmackvoll eingerichtet. Die Aussicht aufs Wasser ist unbeschreiblich schön. Wir haben die Ruhe und die Natur sehr genossen. Die Sauna war bei dem noch kühlen Wetter perfekt. Vielen Dank für die schöne Zeit!"
    },
    {
        "name": "Familie Müller", 
        "date": "12.02.2023",
        "content": "Wir waren mit unseren beiden Kindern hier und alle waren begeistert! Das Hausboot bietet genug Platz für die ganze Familie und ist kinderfreundlich eingerichtet. Die Kinder fanden es spannend, auf dem Wasser zu wohnen. Wir Erwachsenen haben die Sauna und die gemütliche Atmosphäre genossen. Absolut empfehlenswert!"
    },
    {
        "name": "Renate und Harald", 
        "date": "03.01.2023",
        "content": "Wir haben den Jahreswechsel auf dem Coco de Mer verbracht und es war unvergesslich! Das Feuerwerk über dem Wasser zu schauen war ein ganz besonderes Erlebnis. Das Hausboot ist perfekt ausgestattet und sehr gemütlich. Der Kamin hat für eine romantische Stimmung gesorgt. Danke für den wunderbaren Start ins neue Jahr!"
    },
    {
        "name": "Claudia und Stefan", 
        "date": "19.11.2022",
        "content": "Unser Herbsturlaub auf dem Hausboot war einfach traumhaft! Die Farben der Natur im November waren wunderschön und die Ruhe am Bodden hat uns sehr gut getan. Das Hausboot ist mit viel Liebe zum Detail eingerichtet und bietet allen Komfort. Die Sauna war bei dem kühleren Wetter perfekt. Wir freuen uns schon auf den nächsten Besuch!"
    },
    {
        "name": "Michael und Andrea", 
        "date": "07.09.2022",
        "content": "Wir hatten eine wunderbare Zeit auf dem Coco de Mer! Das Hausboot ist fantastisch eingerichtet und die Lage ist einfach traumhaft. Besonders schön fanden wir die großen Fenster mit Blick aufs Wasser und die gemütliche Terrasse. Die Vermieter sind sehr freundlich und hilfsbereit. Absolut empfehlenswert!"
    },
    {
        "name": "Ute und Jürgen", 
        "date": "23.07.2022",
        "content": "Unser Sommerurlaub auf dem Hausboot war perfekt! Wir haben jeden Tag die wunderschöne Aussicht und die Ruhe genossen. Das Hausboot ist sehr gut ausgestattet und liebevoll eingerichtet. Besonders toll fanden wir die Möglichkeit, direkt vom Steg aus zu angeln. Die Sauna war auch im Sommer eine tolle Entspannung. Vielen Dank!"
    },
    {
        "name": "Beate und Wolfgang", 
        "date": "15.06.2022",
        "content": "Wir waren bereits zum zweiten Mal hier und sind immer wieder begeistert! Das Hausboot ist ein echter Traum und die Lage ist unschlagbar. Die Einrichtung ist sehr geschmackvoll und gemütlich. Wir haben die Zeit hier sehr genossen und werden definitiv wiederkommen. Die Vermieter sind einfach super!"
    },
    {
        "name": "Martina und Klaus", 
        "date": "01.05.2022",
        "content": "Unser Maiurlaub auf dem Coco de Mer war wunderschön! Das Erwachen der Natur rund um das Hausboot war ein tolles Erlebnis. Das Hausboot selbst ist fantastisch eingerichtet und bietet allen Komfort. Die Sauna und der Kamin haben für gemütliche Abende gesorgt. Wir haben uns rundum wohl gefühlt!"
    },
    {
        "name": "Sabine und Ralf", 
        "date": "18.03.2022",
        "content": "Wir hatten eine fantastische Zeit auf dem Hausboot! Die Einrichtung ist wunderschön und sehr gemütlich. Die Lage am Bodden ist traumhaft ruhig und entspannend. Besonders toll fanden wir die großzügige Terrasse und die Sauna. Die Vermieter sind sehr nett und haben uns herzlich empfangen. Absolut empfehlenswert!"
    }
]

def main():
    print("🎯 ECHTER IMPORT: Original Gästebewertungen - Reviews 21-30")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(real_guest_reviews_21_30)}")
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
    
    for i, review in enumerate(real_guest_reviews_21_30, 21):
        print(f"📝 Schritt {i:2d}/30: {review['name']}")
        
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
    
    print("📊 Import-Zusammenfassung (Reviews 21-30):")
    print(f"   ✅ Erfolgreich: {imported_count}/10")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/10")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} weitere ECHTE Gästebewertungen erfolgreich importiert!")
        print(f"🔢 Gesamt bisher: {20 + imported_count}/45+ Reviews")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        print("📋 Weitere Batches folgen für komplette Original-Daten")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
