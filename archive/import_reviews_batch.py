#!/usr/bin/env python3
"""
Script to import reviews to the guestbook running at 192.168.2.12:3000
Imports reviews in batches of 10 with confirmation prompts
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://192.168.2.12:3000"
API_URL = f"{BASE_URL}/api"
BATCH_SIZE = 10

# Admin credentials for authentication
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "whHBJveMvwjs5a6p"

# Reviews data
REVIEWS_DATA = [
    {
        "name": "Andrea Ackermann",
        "email": "",
        "rating": 5,
        "title": "Ein so bequemes Bett mit Massagefunktion hatten wir noch nie!",
        "content": "Das Coco de Mer bietet einem alles, nein - es bietet noch mehr als man sich wünscht. Super sauber, liebevoll eingerichtet, sehr ruhig, aller mögliche technische Schnickschnack, den es heute so braucht, Sauna, Kamin und sogar 2 Hausengel, die einem willkommen heissen - sehr persönlich 😃 alles. Wenn man Erholung sucht, gerne gut isst, sich sportlich betätigen möchte, die Natur liebt, dann ist man hier richtig. Für uns am Schönsten war, dass wir unseren Pudel mitnehmen konnten. Solch hochwertige Unterkünfte sind für „Hündler" meist tabu. Für Badefans ist eher die nahe gelegene Ostsee, als der Bodden zu empfehlen. Alles ist genau so, wie in den Unterlagen beschrieben & auf die Tipps und Empfehlungen der Eigentümer ist Verlass. Mängel wären zu suchen! Wir kommen gerne wieder, trotz der langen Anreise.",
        "import_source": "google_reviews",
        "external_id": "45",
        "created_at": "2025-07-01T10:00:00"
    },
    {
        "name": "Falkenseeer",
        "email": "",
        "rating": 5,
        "title": "Sehr schönes Hausboot mit Wellness Oase!",
        "content": "Wir haben einen super Urlaub auf einem traumhaften Hausboot verbracht. Alles lief reibungslos und ist so wie in der Anzeige beschrieben.",
        "import_source": "google_reviews",
        "external_id": "44",
        "created_at": "2025-07-01T10:00:00"
    },
    {
        "name": "Gitta Fischer",
        "email": "",
        "rating": 5,
        "title": "Wiederholungsurlauber im sonnigen, aber kalten März 2025",
        "content": "Wir sind als \"Wiederholungurlauber\" im sonnigen, aber kalten März 2025 im wunderschönen Coco de Mer gewesen. Nach ausgiebigen Boddenwanderungen gibt es fast nicht schöneres, als in das warme Seychellenflair (Sauna) einzutauchen. Wie beim letzten Besuch war einfach alles wieder perfekt und nach unserem damaligen Hinweis, dass doch ein gemütlicher Lesesessel mit Blick auf das Wasser toll wäre, haben die Vermieter diesen Tipp prompt umgesetzt. Danke und bis bald.",
        "import_source": "google_reviews",
        "external_id": "43",
        "created_at": "2025-07-01T10:00:00"
    },
    {
        "name": "Meiwald Jan",
        "email": "",
        "rating": 5,
        "title": "Bereits zum 2. Mal - Erwartungen mehr als erfüllt",
        "content": "Bereits zum 2. Mal haben wir einen Kurzurlaub auf dem Coco de Mer verbracht. Wieder wurden unsere Erwartungen mehr als erfüllt. Wir haben die bequemen Betten, die frische Luft um die Nase auf den großzügigen Terrassen, die entspannende Sauna im kleinen Wellnessbereich und auch auch den neuen Lesestuhl vor den riesigen Fenstern sehr genossen. Durch die ebenerdigkeit fast aller Einrichtungen war der Aufenthalt auch für unseren sehbeeinträchtigten Bruder eine echte Erholung. Sehr gerne kommen wir wieder zu Euch.",
        "import_source": "manual_import",
        "external_id": "42",
        "created_at": "2025-01-28T10:00:00"
    },
    {
        "name": "Heiko Wolf",
        "email": "",
        "rating": 5,
        "title": "Schönes Silvester trotz schlechtem Wetter",
        "content": "Wie immer hatten wir, trotz schlechtem Wetter, einen schönen und gemütlichen Aufenthalt am Kaminfeuer. Wir haben das Silvester Feuerwerk von der Dachterrasse perfekt genossen 👍",
        "import_source": "google_reviews",
        "external_id": "41",
        "created_at": "2025-01-07T10:00:00"
    },
    {
        "name": "Gudrun, Manfred, Helga und Jürgen",
        "email": "",
        "rating": 5,
        "title": "320 Jahre Jubiläumsgeburtstage auf den Seychellen",
        "content": "Coco de Meer funktional und äußerst geschmackvoll, mit viel Liebe zum Detail, eingerichtete Bleibe - hier steckt echt Herzblut drin. Wer hätte gedacht, dass wir unsere Jubiläumsqeburtstage (320 Jahre) 3 Tage auf den Seychellen verbringen können! Wir haben die Zeit und die Annehmlichkeiten hier in vollen Umfang genossen. Sogar der „Seegang" wird, sonst nicht bemerkbar, mit den Lampen über dem Esstisch angezeigt. Das Wetter glich zwar nicht dem Indischen Ozean , aber wir haben eine tolle Darssrundfahrt gemacht u. waren sogar auf dem Leuchtturm . Den beiden „Jens'en " danken wir herzlich, wünschen alles gute , beste Gesundheit und Erholung bei den eigenen Auszeiten sowie weiterhin viele neugierige Gäste.",
        "import_source": "manual_import",
        "external_id": "40",
        "created_at": "2024-10-21T10:00:00"
    },
    {
        "name": "Abendstern",
        "email": "",
        "rating": 5,
        "title": "Rundum wohl gefühlt!",
        "content": "Wir haben uns rundum wohl gefühlt! Das „Hausboot" ist liebevoll eingerichtet und bietet alles was man im Urlaub braucht!",
        "import_source": "google_reviews",
        "external_id": "39",
        "created_at": "2024-08-27T10:00:00"
    },
    {
        "name": "M., Yvonne",
        "email": "",
        "rating": 5,
        "title": "Super schöne Zeit mit unserem Hund",
        "content": "Wir (mein Partner, ich und unser Hund) waren Anfang Juli 2024 für 13 Übernachtungen im Coco de Mer. Wir hatten eine super schöne Zeit auf dem Hausboot und werden es def. nochmal buchen. Die von den Vermietern eingestellten Bilder stimmen wirklich mit der Realität überein. Alles ist mit sehr viel Liebe eingerichtet. Der Kontakt mit den Vermietern war klasse, die sind supernett. Vor Ort ist ein liebes Pärchen als Objektverwalter, die uns herzlich empfangen und alles auf dem Hausboot erklärt haben. Wir hatten mit Wäschepaket gebucht (Bettwäsche und Handtücher), die Handtücher wurden sogar nach einer Woche gewechselt. Für unseren Hund war ein kleines Körbchen/Hundekissen vorhanden (wir hatten aber auch unser eigenes Hundekissen mitgebracht), Näpfe für Futter und Wasser waren vorhanden, sogar eine Taschenlampe mit Hundekotbeutel wurde uns gestellt.",
        "import_source": "hundehotel_info",
        "external_id": "38",
        "created_at": "2024-07-26T10:00:00"
    },
    {
        "name": "Kleene Maus",
        "email": "",
        "rating": 5,
        "title": "Erster Urlaub auf einem Hausboot - wie zu Hause gefühlt",
        "content": "Für uns war es der erste Urlaub auf einem Hausboot und wir haben uns sofort wie zu Hause gefühlt. Alles ist so liebevoll und bis ins kleinste Detail eingerichtet, so dass es einem an nichts fehlt. Das Hausboot ist perfekt geschnitten, somit finden hier bis zu 6 Personen bequem Platz. Auch unsere Vierbeiner waren herzlich willkommen und Sie haben sich sehr wohl gefühlt. Dank der Sauna und der großen Außenterrasse, mit einem wunderschönen Blick auf den Bodden, kann man das Hausboot zu jeder Jahreszeit genießen. Vielen lieben Dank für die tolle Auszeit und den herzlichen Empfang.",
        "import_source": "google_reviews",
        "external_id": "37",
        "created_at": "2024-07-11T10:00:00"
    },
    {
        "name": "Traumhafter Sonnenuntergang",
        "email": "",
        "rating": 5,
        "title": "Wunderschöne Unterkunft in traumhafter Lage",
        "content": "Eine wunderschöne Unterkunft in absolut ruhiger und traumhafter Lage! Ideal, um vom Alltag abzuschalten und ein romantisches Nest für Paare.",
        "import_source": "traumferienwohnungen",
        "external_id": "36",
        "created_at": "2024-05-21T10:00:00"
    }
]

def get_auth_token():
    """Login and get authentication token"""
    try:
        response = requests.post(f"{API_URL}/auth/login", json={
            "username": ADMIN_USERNAME,
            "password": ADMIN_PASSWORD
        })
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Successfully authenticated as {ADMIN_USERNAME}")
            return token
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return None

def import_review(review_data, token):
    """Import a single review"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Prepare review data for API
        api_data = {
            "name": review_data["name"],
            "email": review_data.get("email", ""),
            "rating": review_data["rating"],
            "title": review_data.get("title", ""),
            "content": review_data["content"],
            "import_source": review_data.get("import_source", "manual_import"),
            "external_id": review_data.get("external_id", ""),
            "is_approved": True,  # Auto-approve imported reviews
            "created_at": review_data.get("created_at", datetime.now().isoformat())
        }
        
        response = requests.post(f"{API_URL}/reviews/", json=api_data, headers=headers)
        
        if response.status_code == 201:
            review_id = response.json().get("id")
            print(f"  ✅ Imported: {review_data['name']} (ID: {review_id})")
            return True
        else:
            print(f"  ❌ Failed to import {review_data['name']}: {response.status_code}")
            print(f"     Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error importing {review_data['name']}: {e}")
        return False

def main():
    print("🔄 Guestbook Review Import Tool")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print(f"Reviews to import: {len(REVIEWS_DATA)}")
    print(f"Batch size: {BATCH_SIZE}")
    print("")
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Import in batches
    total_imported = 0
    total_failed = 0
    
    for i in range(0, len(REVIEWS_DATA), BATCH_SIZE):
        batch = REVIEWS_DATA[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        
        print(f"\\n📦 Batch {batch_num}: Importing {len(batch)} reviews...")
        print("-" * 40)
        
        batch_success = 0
        batch_failed = 0
        
        for review in batch:
            if import_review(review, token):
                batch_success += 1
                total_imported += 1
                time.sleep(0.5)  # Small delay between requests
            else:
                batch_failed += 1
                total_failed += 1
        
        print(f"\\n📊 Batch {batch_num} Results:")
        print(f"   ✅ Successful: {batch_success}")
        print(f"   ❌ Failed: {batch_failed}")
        
        # Ask for confirmation to continue (except for last batch)
        if i + BATCH_SIZE < len(REVIEWS_DATA):
            print(f"\\n⏳ Continue with next batch? (y/n): ", end="")
            response = input().strip().lower()
            if response != 'y' and response != 'yes':
                print("🛑 Import cancelled by user")
                break
    
    print(f"\\n🎉 Import Complete!")
    print(f"=" * 50)
    print(f"✅ Total imported: {total_imported}")
    print(f"❌ Total failed: {total_failed}")
    print(f"🌐 Check your guestbook: {BASE_URL}")

if __name__ == "__main__":
    main()
