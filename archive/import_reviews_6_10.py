#!/usr/bin/env python3
"""
Import REAL guest reviews from original data - Next 5 reviews (6-10)
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

# REAL guest reviews from original data - Reviews 6-10
real_guest_reviews_6_10 = [
    {
        "name": "Gudrun, Manfred, Helga und Jürgen", 
        "date": "21.10.2024",
        "content": "Coco de Mer funktional und äußerst geschmackvoll, mit viel Liebe zum Detail, eingerichtete Bleibe - hier steckt echt Herzblut drin. Wer hätte gedacht, dass wir unsere Jubiläumsgeburtstage (320 Jahre) 3 Tage auf den Seychellen verbringen können! Wir haben die Zeit und die Annehmlichkeiten hier in vollen Umfang genossen. Sogar der Seegang wird, sonst nicht bemerkbar, mit den Lampen über dem Esstisch angezeigt. Das Wetter glich zwar nicht dem Indischen Ozean, aber wir haben eine tolle Darssrundfahrt gemacht und waren sogar auf dem Leuchtturm. Den beiden Jensen danken wir herzlich, wünschen alles gute, beste Gesundheit und Erholung bei den eigenen Auszeiten sowie weiterhin viele neugierige Gäste. Helga, Jürgen, Gudrun und Manfred aus dem Erzgebirge."
    },
    {
        "name": "Abendstern", 
        "date": "26.08.2024",
        "content": "Wir haben uns rundum wohl gefühlt! Das Hausboot ist liebevoll eingerichtet und bietet alles was man im Urlaub braucht!"
    },
    {
        "name": "M., Yvonne", 
        "date": "25.07.2024",
        "content": "Wir (mein Partner, ich und unser Hund) waren Anfang Juli 2024 für 13 Übernachtungen im Coco de Mer. Wir hatten eine super schöne Zeit auf dem Hausboot und werden es def. nochmal buchen. Die von den Vermietern eingestellten Bilder stimmen wirklich mit der Realität überein. Alles ist mit sehr viel Liebe eingerichtet. Der Kontakt mit den Vermietern war klasse, die sind supernett. Vor Ort ist ein liebes Pärchen als Objektverwalter, die uns herzlich empfangen und alles auf dem Hausboot erklärt haben. Wir hatten mit Wäschepaket gebucht (Bettwäsche und Handtücher), die Handtücher wurden sogar nach einer Woche gewechselt."
    },
    {
        "name": "Kleene Maus", 
        "date": "08.07.2024",
        "content": "Für uns war es der erste Urlaub auf einem Hausboot und wir haben uns sofort wie zu Hause gefühlt. Alles ist so liebevoll und bis ins kleinste Detail eingerichtet, so dass es einem an nichts fehlt. Das Hausboot ist perfekt geschnitten, somit finden hier bis zu 6 Personen bequem Platz. Auch unsere Vierbeiner waren herzlich willkommen und Sie haben sich sehr wohl gefühlt. Dank der Sauna und der großen Außenterrasse, mit einem wunderschönen Blick auf den Bodden, kann man das Hausboot zu jeder Jahreszeit genießen. Vielen lieben Dank für die tolle Auszeit und den herzlichen Empfang."
    },
    {
        "name": "Traumhafter Sonnenuntergang", 
        "date": "26.04.2024",
        "content": "Eine wunderschöne Unterkunft in absolut ruhiger und traumhafter Lage! Ideal, um vom Alltag abzuschalten und ein romantisches Nest für Paare."
    }
]

def main():
    print("🎯 ECHTER IMPORT: Original Gästebewertungen - Reviews 6-10")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews to import: {len(real_guest_reviews_6_10)}")
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
    
    for i, review in enumerate(real_guest_reviews_6_10, 6):
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
    
    print("📊 Import-Zusammenfassung (Reviews 6-10):")
    print(f"   ✅ Erfolgreich: {imported_count}/5")
    print(f"   ❌ Fehlgeschlagen: {failed_count}/5")
    print()
    
    if imported_count > 0:
        print(f"🎉 {imported_count} weitere ECHTE Gästebewertungen erfolgreich importiert!")
        print(f"🔢 Gesamt bisher: {5 + imported_count}/45+ Reviews")
        print("🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
        print("📋 Weitere Batches folgen für komplette Original-Daten")
    else:
        print("❌ Keine Reviews importiert!")

if __name__ == "__main__":
    main()
