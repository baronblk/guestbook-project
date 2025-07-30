#!/usr/bin/env python3
"""
Import script for Coco de Mer guestbook reviews
"""
import requests
import json
from datetime import datetime
import re

# API base URL
API_BASE_URL = "http://localhost:8080/api"

# First 10 reviews as a test batch
reviews_data = [
    {
        "name": "Andrea Ackermann",
        "date": "01.07.2025",
        "id": "45",
        "content": "Ein so bequemes Bett mit Massagefunktion hatten wir noch nie! Das Coco de Mer bietet einem alles, nein - es bietet noch mehr als man sich wünscht. Super sauber, liebevoll eingerichtet, sehr ruhig, aller mögliche technische Schnickschnack, den es heute so braucht, Sauna, Kamin und sogar 2 Hausengel, die einem willkommen heissen - sehr persönlich 😃 alles. Wenn man Erholung sucht, gerne gut isst, sich sportlich betätigen möchte, die Natur liebt, dann ist man hier richtig. Für uns am Schönsten war, dass wir unseren Pudel mitnehmen konnten. Solch hochwertige Unterkünfte sind für „Hündler" meist tabu. Für Badefans ist eher die nahe gelegene Ostsee, als der Bodden zu empfehlen. Alles ist genau so, wie in den Unterlagen beschrieben & auf die Tipps und Empfehlungen der Eigentümer ist Verlass. Mängel wären zu suchen! Wir kommen gerne wieder, trotz der langen Anreise.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 30.06.25",
        "source": "Google"
    },
    {
        "name": "Falkenseeer",
        "date": "01.07.2025",
        "id": "44",
        "content": "Sehr schönes Hausboot mit Wellness Oase! Wir haben einen super Urlaub auf einem traumhaften Hausboot verbracht. Alles lief reibungslos und ist so wie in der Anzeige beschrieben.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 212.04.25",
        "source": "Google"
    },
    {
        "name": "Gitta Fischer",
        "date": "01.07.2025",
        "id": "43",
        "content": "Wir sind als 'Wiederholungurlauber' im sonnigen, aber kalten März 2025 im wunderschönen Coco de Mer gewesen. Nach ausgiebigen Boddenwanderungen gibt es fast nicht schöneres, als in das warme Seychellenflair (Sauna) einzutauchen. Wie beim letzten Besuch war einfach alles wieder perfekt und nach unserem damaligen Hinweis, dass doch ein gemütlicher Lesesessel mit Blick auf das Wasser toll wäre, haben die Vermieter diesen Tipp prompt umgesetzt. Danke und bis bald.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 17.03.25",
        "source": "Google"
    },
    {
        "name": "Meiwald Jan",
        "date": "28.01.2025",
        "id": "42",
        "content": "Bereits zum 2. Mal haben wir einen Kurzurlaub auf dem Coco de Mer verbracht. Wieder wurden unsere Erwartungen mehr als erfüllt. Wir haben die bequemen Betten, die frische Luft um die Nase auf den großzügigen Terrassen, die entspannende Sauna im kleinen Wellnessbereich und auch auch den neuen Lesestuhl vor den riesigen Fenstern sehr genossen. Durch die ebenerdigkeit fast aller Einrichtungen war der Aufenthalt auch für unseren sehbeeinträchtigten Bruder eine echte Erholung. Sehr gerne kommen wir wieder zu Euch.",
        "rating": 5,
        "title": "Zweiter Besuch - wieder perfekt",
        "source": "Gästebuch"
    },
    {
        "name": "Heiko Wolf",
        "date": "07.01.2025",
        "id": "41",
        "content": "Wie immer hatten wir, trotz schlechtem Wetter, einen schönen und gemütlichen Aufenthalt am Kaminfeuer. Wir haben das Silvester Feuerwerk von der Dachterrasse perfekt genossen 👍",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 06.01.25",
        "source": "Google"
    },
    {
        "name": "Gudrun, Manfred, Helga und Jürgen",
        "date": "21.10.2024",
        "id": "40",
        "content": "Coco de Meer funktional und äußerst geschmackvoll, mit viel Liebe zum Detail, eingerichtete Bleibe - hier steckt echt Herzblut drin. Wer hätte gedacht, dass wir unsere Jubiläumsgeburtstage (320 Jahre) 3 Tage auf den Seychellen verbringen können! Wir haben die Zeit und die Annehmlichkeiten hier in vollen Umfang genossen. Sogar der 'Seegang' wird, sonst nicht bemerkbar, mit den Lampen über dem Esstisch angezeigt. Das Wetter glich zwar nicht dem Indischen Ozean, aber wir haben eine tolle Darssrundfahrt gemacht u. waren sogar auf dem Leuchtturm. Den beiden 'Jens'en' danken wir herzlich, wünschen alles gute, beste Gesundheit und Erholung bei den eigenen Auszeiten sowie weiterhin viele neugierige Gäste. Helga, Jürgen, Gudrun und Manfred aus dem Erzgebirge.",
        "rating": 5,
        "title": "320 Jahre Jubiläumsgeburtstage auf den Seychellen",
        "source": "Gästebuch"
    },
    {
        "name": "Abendstern",
        "date": "27.08.2024",
        "id": "39",
        "content": "Wir haben uns rundum wohl gefühlt! Das 'Hausboot' ist liebevoll eingerichtet und bietet alles was man im Urlaub braucht!",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 26.08.24",
        "source": "Google"
    },
    {
        "name": "M., Yvonne",
        "date": "26.07.2024",
        "id": "38",
        "content": "Wir (mein Partner, ich und unser Hund) waren Anfang Juli 2024 für 13 Übernachtungen im Coco de Mer. Wir hatten eine super schöne Zeit auf dem Hausboot und werden es def. nochmal buchen. Die von den Vermietern eingestellten Bilder stimmen wirklich mit der Realität überein. Alles ist mit sehr viel Liebe eingerichtet. Der Kontakt mit den Vermietern war klasse, die sind supernett. Vor Ort ist ein liebes Pärchen als Objektverwalter, die uns herzlich empfangen und alles auf dem Hausboot erklärt haben.",
        "rating": 5,
        "title": "Übernommene Hundehotel.info-Rezension vom 25.07.2024",
        "source": "Hundehotel.info"
    },
    {
        "name": "Kleene Maus",
        "date": "11.07.2024",
        "id": "37",
        "content": "Für uns war es der erste Urlaub auf einem Hausboot und wir haben uns sofort wie zu Hause gefühlt. Alles ist so liebevoll und bis ins kleinste Detail eingerichtet, so dass es einem an nichts fehlt. Das Hausboot ist perfekt geschnitten, somit finden hier bis zu 6 Personen bequem Platz. Auch unsere Vierbeiner waren herzlich willkommen und Sie haben sich sehr wohl gefühlt. Dank der Sauna und der großen Außenterrasse, mit einem wunderschönen Blick auf den Bodden, kann man das Hausboot zu jeder Jahreszeit genießen. Vielen lieben Dank für die tolle Auszeit und den herzlichen Empfang.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 08.07.2024",
        "source": "Google"
    },
    {
        "name": "Traumhafter Sonnenuntergang",
        "date": "21.05.2024",
        "id": "36",
        "content": "Eine wunderschöne Unterkunft in absolut ruhiger und traumhafter Lage! Ideal, um vom Alltag abzuschalten und ein romantisches Nest für Paare.",
        "rating": 5,
        "title": "Übernommene Rezension von Traumfereinwohnungen.de vom 26.04.24",
        "source": "Traumfereinwohnungen.de"
    }
]

def parse_date(date_str):
    """Parse German date format to ISO format"""
    try:
        # Parse DD.MM.YYYY format
        day, month, year = date_str.split('.')
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except:
        return "2024-01-01"  # fallback date

def import_review(review_data):
    """Import a single review"""
    # Prepare the review data for API
    api_data = {
        "name": review_data["name"],
        "email": f"import_{review_data['id']}@coco-de-mer.de",  # Generate email
        "rating": review_data["rating"],
        "title": review_data["title"],
        "content": review_data["content"]
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/reviews", json=api_data)
        if response.status_code == 200:
            review = response.json()
            print(f"✓ Imported: {review_data['name']} (ID: {review['id']})")
            
            # Update the review to set it as approved and set custom created_at
            admin_update = {
                "is_approved": True,
                "created_at": parse_date(review_data["date"]),
                "import_source": review_data.get("source", "Import"),
                "external_id": review_data["id"]
            }
            
            # Note: This would require admin API access
            # For now, we'll just mark them as imported
            return review["id"]
        else:
            print(f"✗ Failed to import {review_data['name']}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error importing {review_data['name']}: {str(e)}")
        return None

def main():
    print("🚀 Starting Coco de Mer reviews import...")
    print(f"📝 Found {len(reviews_data)} reviews to import")
    
    imported_count = 0
    failed_count = 0
    
    for review in reviews_data:
        result = import_review(review)
        if result:
            imported_count += 1
        else:
            failed_count += 1
    
    print(f"\n📊 Import Summary:")
    print(f"✅ Successfully imported: {imported_count}")
    print(f"❌ Failed imports: {failed_count}")
    print(f"📈 Total reviews: {len(reviews_data)}")
    
    if imported_count > 0:
        print(f"\n🎉 Import completed! Check http://localhost:8080 to see the reviews.")

if __name__ == "__main__":
    main()
