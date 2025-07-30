#!/usr/bin/env python3
"""
Simple review import script for Coco de Mer guestbook
Run this to import your reviews in batches
"""

import requests
import json
import time

# Configuration
GUESTBOOK_URL = "http://192.168.2.12:3000"
ADMIN_USER = "admin" 
ADMIN_PASS = "whHBJveMvwjs5a6p"

# First 10 reviews to import
reviews_batch_1 = [
    {
        "name": "Andrea Ackermann",
        "rating": 5,
        "title": "Ein so bequemes Bett mit Massagefunktion hatten wir noch nie!",
        "content": "Das Coco de Mer bietet einem alles, nein - es bietet noch mehr als man sich wünscht. Super sauber, liebevoll eingerichtet, sehr ruhig, aller mögliche technische Schnickschnack, den es heute so braucht, Sauna, Kamin und sogar 2 Hausengel, die einem willkommen heissen - sehr persönlich alles. Wenn man Erholung sucht, gerne gut isst, sich sportlich betätigen möchte, die Natur liebt, dann ist man hier richtig. Für uns am Schönsten war, dass wir unseren Pudel mitnehmen konnten. Solch hochwertige Unterkünfte sind für Hündler meist tabu. Für Badefans ist eher die nahe gelegene Ostsee, als der Bodden zu empfehlen. Alles ist genau so, wie in den Unterlagen beschrieben und auf die Tipps und Empfehlungen der Eigentümer ist Verlass. Mängel wären zu suchen! Wir kommen gerne wieder, trotz der langen Anreise."
    },
    {
        "name": "Falkenseeer",
        "rating": 5,
        "title": "Sehr schönes Hausboot mit Wellness Oase!",
        "content": "Wir haben einen super Urlaub auf einem traumhaften Hausboot verbracht. Alles lief reibungslos und ist so wie in der Anzeige beschrieben."
    },
    {
        "name": "Gitta Fischer",
        "rating": 5,
        "title": "Wiederholungsurlauber im sonnigen, aber kalten März 2025",
        "content": "Wir sind als Wiederholungurlauber im sonnigen, aber kalten März 2025 im wunderschönen Coco de Mer gewesen. Nach ausgiebigen Boddenwanderungen gibt es fast nicht schöneres, als in das warme Seychellenflair (Sauna) einzutauchen. Wie beim letzten Besuch war einfach alles wieder perfekt und nach unserem damaligen Hinweis, dass doch ein gemütlicher Lesesessel mit Blick auf das Wasser toll wäre, haben die Vermieter diesen Tipp prompt umgesetzt. Danke und bis bald."
    },
    {
        "name": "Meiwald Jan",
        "rating": 5,
        "title": "Bereits zum 2. Mal - Erwartungen mehr als erfüllt",
        "content": "Bereits zum 2. Mal haben wir einen Kurzurlaub auf dem Coco de Mer verbracht. Wieder wurden unsere Erwartungen mehr als erfüllt. Wir haben die bequemen Betten, die frische Luft um die Nase auf den großzügigen Terrassen, die entspannende Sauna im kleinen Wellnessbereich und auch auch den neuen Lesestuhl vor den riesigen Fenstern sehr genossen. Durch die ebenerdigkeit fast aller Einrichtungen war der Aufenthalt auch für unseren sehbeeinträchtigten Bruder eine echte Erholung. Sehr gerne kommen wir wieder zu Euch."
    },
    {
        "name": "Heiko Wolf",
        "rating": 5,
        "title": "Schönes Silvester trotz schlechtem Wetter",
        "content": "Wie immer hatten wir, trotz schlechtem Wetter, einen schönen und gemütlichen Aufenthalt am Kaminfeuer. Wir haben das Silvester Feuerwerk von der Dachterrasse perfekt genossen."
    }
]

def login():
    """Login and get token"""
    try:
        response = requests.post(f"{GUESTBOOK_URL}/api/auth/login", json={
            "username": ADMIN_USER,
            "password": ADMIN_PASS
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def import_review(review, token):
    """Import one review"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "name": review["name"],
            "rating": review["rating"],
            "title": review["title"],
            "content": review["content"],
            "email": "",
            "is_approved": True
        }
        
        response = requests.post(f"{GUESTBOOK_URL}/api/reviews/", json=data, headers=headers)
        
        if response.status_code == 201:
            print(f"✅ {review['name']} - imported successfully")
            return True
        else:
            print(f"❌ {review['name']} - failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ {review['name']} - error: {e}")
        return False

def main():
    print("🔄 Importing first 5 reviews to Coco de Mer Guestbook")
    print("=" * 60)
    print(f"Target: {GUESTBOOK_URL}")
    print()
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without login")
        return
    
    print("✅ Login successful")
    print()
    
    # Import reviews
    success_count = 0
    for i, review in enumerate(reviews_batch_1, 1):
        print(f"[{i}/{len(reviews_batch_1)}] Importing: {review['name'][:30]}...")
        if import_review(review, token):
            success_count += 1
        time.sleep(1)  # Pause between imports
    
    print()
    print("🎉 Import completed!")
    print(f"✅ Successfully imported: {success_count}/{len(reviews_batch_1)} reviews")
    print(f"🌐 Check your guestbook: {GUESTBOOK_URL}")

if __name__ == "__main__":
    main()
