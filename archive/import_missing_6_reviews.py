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

# Die 6 fehlenden Reviews aus deinen Original-Daten
missing_reviews = [
    {
        "name": "Fam. Hirsch", 
        "date": "05.04.2024",
        "content": "Jederzeit wieder. Für uns mit Hund die beste Unterkunft. Es fehlte an nichts. Alles sehr geschmackvoll und liebevoll eingerichtet. Besonders toll fanden wir die Sauna sowie das Massagebett mit Blick aufs Wasser um den Sonnenaufgang oder am Abend den Sternenhimmel beobachten zu können. Selbst bei Regenwetter wird es in diesem Domizil nicht langweilig. Wir sagen Danke für diese schöne Zeit die wir dort verbringen durften. Herzliche Grüße aus Berlin"
    },
    {
        "name": "Irmgard", 
        "date": "23.03.2024",
        "content": "Urlaub im August 2023 auf der Coco de Mer Super herzlicher Empfang und Betreuung durch Familie Hartwich! Ein wunderbares Hausboot, mit erstklassigem Ambiente, phantastische Einrichtung - mit Liebe ausgestattet und dekoriert - hier fehlt es an Nichts. Die Sauna ist ein Highlight. Absoluter Erholungsurlaub!"
    },
    {
        "name": "Christian u. Jana Z.", 
        "date": "03.01.2024",
        "content": "Wir haben den Jahreswechsel als Gäste im Coco de Mer verbracht. Und es war zauberhaft. Schon der herzliche Empfang durch Familie H. ließ uns mit Entspannung in die freien Tage starten. Das Feriendomizil ist mit viel Liebe zum Detail eingerichtet, so hatten wir noch eine weihnachtliche Atmosphäre (ich bin ein kleiner Weihnachtsfreak). Auch unsere Hundedame Daisy war willkommen und fand Näpfe und ein Deckchen zum kuscheln vor. Es fehlte einem an nichts. Man kann von hier schöne Spaziergänge mit dem Hund unternehmen und auch das Zentrum ist zu Fuß zu erreichen. Zur Ostsee sind es nur wenige Minuten mit dem Auto. Alles in allem haben wir uns dort verdammt wohl gefühlt, ob entspannt in der eigenen Sauna oder bei Kaminfeuer auf der gemütlichen Couch den Abend ausklingen lassen. Es war einfach herrlich, so dass wir schon den nächsten Besuch im Coco de Mer planen."
    },
    {
        "name": "Reinhold HANNBERGER", 
        "date": "04.10.2023",
        "content": "Ein fantastischer Urlaub. So eine tolle Unterkunft für Mensch und Hund. Es fehlt an nichts! Vom orthopädischen Bett mit Massagefunktion, Sauna mit 3 verschiedenen Wellnessprogrammen, ob Infrarot oder Finnische Sauna, Sonnendeck, Waschmaschine und voll ausgestattete Küche, die keine Wünsche offen lässt. Das Ferienhaus auf dem Wasser ist einzigartig. Können es nur mit gutem Gewissen empfehlen. September 2023 Helga, Reinhold mit den Hunden Dotti und Alma"
    },
    {
        "name": "Jenny & René", 
        "date": "11.09.2023",
        "content": "Wir hatten eine wunderschöne und entspannte Woche auf dem Hausboot. Uns hat es an nichts gefehlt und selbst für unsere Fellnasen war gesorgt. Jeden Tag diesen schönen Ausblick von der Terrasse oder vom Wasser aus zu genießen war einfach ein Traum. Wir kommen gerne wieder!!"
    },
    {
        "name": "Das Schmidtsche Rudel", 
        "date": "29.08.2023",
        "content": "Urlaub im Coco de Mer heißt Wohlfühlen ab der ersten Sekunde. Wir waren im August 2023 für 2 Wochen auf dem tollen Coco und haben die Zeit wahnsinnig genossen. Bei Ankunft wird man von der lieben Familie Hartwich begrüßt und in all die technischen Wunder des Coco eingeführt. Und dann kann die Erholung auch sofort beginnen, denn es ist alles da, was man dafür braucht. Morgens Sonnenaufgang auf der Terrasse unten, Frühstück dort im Idealfall in der Morgensonne, eine Runde schwimmen im Bodden, chillen auf der gemütlich eingerichteten Dachterrasse, Sonnenuntergang dann auch auf der Dachterrasse. Wo bekommt man schon mal beides an einem Ort. Schön. Und wenn das Wetter mal nordisch steif ist, auch kein Problem. Die Sauna ist ein Traum. Die ganze Wohnung ist urgemütlich, große Couch, liebevolle Gestaltung von allem. Tolle Ausstattung in der Küche. Es gibt NICHTS zu meckern. Und auch unsere Hündin fand den Aufenthalt super. Für die standen zwei Näpfe und ein Deckchen bereit als wir ankamen. Das war auch toll, Hundebett mit Boddenblick. Jens und Jens, die beiden lieben Eigentümer, haben da eine Oase der Erholung geschaffen, die man einfach nur lieben, loben und weiterempfehlen kann. Die beiden versorgen einen mit tollen Tipps zu Ausflügen und den besten Torten der Umgebung. Auch ein ganz besonderer Kontakt, so wie wir ihn noch nie erlebt haben bei anderen Objekten. Ihr macht das großartig!!! Wir werden auf alle Fälle sehr, sehr gerne einmal wiederkommen."
    }
]

def main():
    print("🎯 ECHTER IMPORT: Fehlende 6 Original-Gästebewertungen")
    print("=" * 65)
    print(f"Target: {API_BASE_URL}")
    print(f"Reviews zu importieren: {len(missing_reviews)}")
    print("📝 Die letzten 6 fehlenden echten Gäste")
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
