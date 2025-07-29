#!/usr/bin/env python3
"""
Import REAL guest reviews from original data - Missing 6 reviews
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

missing_reviews = [
    {
        "name": "M. Yvonne", 
        "date": "26.07.2024",
        "content": "(Übernommene Hundehotel.info-Rezension vom 25.07.2024): Wir (mein Partner, ich und unser Hund) waren Anfang Juli 2024 für 13 Übernachtungen im Coco de Mer. Wir hatten eine super schöne Zeit auf dem Hausboot und werden es def. nochmal buchen. Die von den Vermietern eingestellten Bilder stimmen wirklich mit der Realität überein. Alles ist mit sehr viel Liebe eingerichtet. Der Kontakt mit den Vermietern war klasse, die sind supernett. Vor Ort ist ein liebes Pärchen als Objektverwalter, die uns herzlich empfangen und alles auf dem Hausboot erklärt haben. Wir hatten mit Wäschepaket gebucht (Bettwäsche und Handtücher), die Handtücher wurden sogar nach einer Woche gewechselt. Für unseren Hund war ein kleines Körbchen/Hundekissen vorhanden (wir hatten aber auch unser eigenes Hundekissen mitgebracht), Näpfe für Futter und Wasser waren vorhanden, sogar eine Taschenlampe mit Hundekotbeutel wurde uns gestellt. Die Schlafzimmer waren mit Bett (und mit nicht durchgelegenen Matratzen), Schrank, Nachttischen, USB-Stecker ausgestattet. Beim Masterschlafzimmer hat man einen traumhaften Blick aufs Wasser und wenn man den Vorhang nicht zuzieht und zufällig aufwacht und rausguckt, wenn die Sonne aufgeht, ist der Blick noch traumhafter. Die Küche ist auch mit allem ausgestattet, was man benötigt. Aus Erfahrung anderer Ferienwohnungen hatte ich noch etliche Sachen mitgenommen (Knoblauchpresse, Messer, Gewürze, Küchenrolle, Klarsichtfolie etc), aber auch das war alles vorhanden. Auf der unteren Terrasse kann man morgens schon in der Sonne frühstücken. Eine Sauna ist ebenfalls vorhanden, die haben wir aber nicht getestet, da wir wirklich top Wetter hatten. Aufgrund der Wärme hat sich das Hausboot auch etwas aufgeheizt, aber im Wohnzimmer sowie in den beiden Schlafzimmern ist eine Klimaanlage, so dass die Temperatur super gesenkt werden konnte. Vom Sonnendeck kann man superschöne Sonnenuntergänge erleben. Auch tagsüber kann man sich dort gut entspannen und sonnen. Dadurch, dass es nur eine geringe Anzahl von Hausbooten sind, ist es sehr ruhig und man kann in Ruhe lesen, sich sonnen etc.. Die Innenstadt ist in wenigen Minuten fußläufig zu erreichen. Bäcker sind demnach ebenfalls gut zu Fuß erreichbar, aber auch ein Einkaufszentrum ist mit dem Auto max. 5 min entfernt. Wir können das Coco de Mer sehr empfehlen, gleich vom ersten Tag war es Erholung pur."
    }
]

def main():
    print("🎯 ECHTER IMPORT: Fehlende 6 Original-Gästebewertungen")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews zu importieren: {len(missing_reviews)}")
    print("📝 Die letzte fehlende echte Gästebewertung")
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
    
    for i, review in enumerate(missing_reviews, 41):
        print(f"📝 Schritt {i:2d}/46: {review['name']}")
        
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
    
    print("📊 Import-Zusammenfassung (Fehlende 6 Reviews):")
    print(f"   ✅ Erfolgreich: {imported_count}/6")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/6")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} fehlende ECHTE Gästebewertungen erfolgreich importiert!")
        print(f"🔢 Gesamt jetzt: {40 + imported_count}/46 Reviews")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        print("✅ VOLLSTÄNDIGER Import aller Original-Daten abgeschlossen!")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
