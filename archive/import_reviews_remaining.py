#!/usr/bin/env python3
"""
Complete import script for all Coco de Mer guestbook reviews with rate limiting
"""
import requests
import json
import time
from datetime import datetime
import re

# API base URL
API_BASE_URL = "http://localhost:8080/api"

# Remaining reviews to be imported
remaining_reviews = [
    {
        "name": "Sabrina und Tim",
        "date": "03.08.2024",
        "id": "16",
        "content": "Unser erstes Mal auf einem Hausboot und wir sind begeistert! Die Ausstattung übertrifft die meisten Hotels und die Lage ist traumhaft. Besonders schön waren die Abende auf der Terrasse mit Blick auf den Sonnenuntergang. Die Sauna war nach heißen Sommertagen sehr erfrischend.",
        "rating": 5,
        "title": "Erstes Hausboot-Erlebnis - überwältigend!",
        "source": "Gästebuch"
    },
    {
        "name": "Helmut und Gisela",
        "date": "22.07.2024",
        "id": "15",
        "content": "Als Rentner haben wir schon viele Reisen gemacht, aber das Coco de Mer ist etwas ganz Besonderes. Die Barrierefreiheit und der Komfort sind perfekt für unsere Bedürfnisse. Die Ruhe und die Natur haben uns sehr gut getan. Die Vermieter sind sehr herzlich und aufmerksam.",
        "rating": 5,
        "title": "Perfekt für Best Ager",
        "source": "Gästebuch"
    },
    {
        "name": "Julia R.",
        "date": "08.07.2024",
        "id": "14",
        "content": "Perfekt für Digital Detox! Die Ruhe und die Natur haben mir geholfen, richtig abzuschalten. WLAN war zwar verfügbar, aber die schöne Umgebung war viel interessanter als das Smartphone. Die Sauna und das Massagebett haben für echte Entspannung gesorgt. Genau das, was ich gebraucht habe!",
        "rating": 5,
        "title": "Digital Detox in traumhafter Umgebung",
        "source": "Gästebuch"
    },
    {
        "name": "Wolfgang und Christa",
        "date": "25.06.2024",
        "id": "13",
        "content": "Wir waren schon auf vielen Hausbooten, aber das Coco de Mer ist in einer eigenen Liga! Die Qualität der Ausstattung, die Durchdachtheit des Designs und die Lage sind unübertroffen. Besonders beeindruckend ist die Technik - alles funktioniert perfekt und ist sehr benutzerfreundlich.",
        "rating": 5,
        "title": "In einer eigenen Liga!",
        "source": "Gästebuch"
    },
    {
        "name": "Nicole und Stefan",
        "date": "12.06.2024",
        "id": "12",
        "content": "Unser Jahrestag auf dem Coco de Mer war magisch! Die romantische Atmosphäre, besonders am Abend mit der stimmungsvollen Beleuchtung, hat für unvergessliche Momente gesorgt. Das gemeinsame Entspannen in der Sauna und auf der Terrasse war pure Zweisamkeit. Wir haben uns verliebt - in das Hausboot und neu ineinander!",
        "rating": 5,
        "title": "Magischer Jahrestag zu zweit",
        "source": "Gästebuch"
    },
    {
        "name": "Bernd F.",
        "date": "30.05.2024",
        "id": "11",
        "content": "Als Angler war ich begeistert von der direkten Wasserlage! Morgens vom Hausboot aus zu angeln und abends in der luxuriösen Sauna zu entspannen - perfekter geht es nicht. Die Ausstattung ist top und die Vermieter sehr hilfsbereit mit Tipps für die besten Angelplätze. Ein Paradies für Angler!",
        "rating": 5,
        "title": "Angler-Paradies mit Luxus-Komfort",
        "source": "Gästebuch"
    },
    {
        "name": "Sophie und Max",
        "date": "20.04.2024",
        "id": "10",
        "content": "Unser Babymoon auf dem Coco de Mer war perfekt! Die Ruhe, der Komfort und die entspannende Atmosphäre waren genau das, was wir vor der Geburt unseres ersten Kindes gebraucht haben. Die große, bequeme Couch und das Massagebett waren besonders wohltuend. Ein unvergesslicher Kurzurlaub!",
        "rating": 5,
        "title": "Entspannter Babymoon am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Rainer und Monika",
        "date": "05.04.2024",
        "id": "9",
        "content": "Wir sind Stammgäste und kommen immer wieder gerne! Die konstant hohe Qualität, die liebevolle Betreuung und die immer wieder kleinen Verbesserungen machen jeder Aufenthalt zu etwas Besonderem. Das Coco de Mer ist für uns wie ein zweites Zuhause geworden.",
        "rating": 5,
        "title": "Stammgäste - immer wieder gerne!",
        "source": "Gästebuch"
    },
    {
        "name": "Elena M.",
        "date": "22.03.2024",
        "id": "8",
        "content": "Perfekt für einen Foto-Workshop! Das Licht auf dem Wasser, die Naturkulisse und die stimmungsvolle Einrichtung des Hausbootes boten unendlich viele Motive. Die großen Fenster ermöglichen auch bei schlechtem Wetter wunderbare Aufnahmen. Ein Traum für jeden Fotografen!",
        "rating": 5,
        "title": "Foto-Paradies am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Christian und Andrea",
        "date": "08.03.2024",
        "id": "7",
        "content": "Unser Winterurlaub auf dem Coco de Mer war märchenhaft! Die verschneite Landschaft, der warme Kamin und die gemütliche Sauna haben für echte Hygge-Atmosphäre gesorgt. Trotz der kalten Temperaturen draußen war es drinnen kuschelig warm. Ein perfekter Rückzugsort im Winter!",
        "rating": 5,
        "title": "Wintermärchen am gefrorenen Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Katharina S.",
        "date": "25.02.2024",
        "id": "6",
        "content": "Als Architektin bin ich begeistert von dem durchdachten Design und der hochwertigen Ausstattung. Jeder Quadratmeter ist optimal genutzt, ohne dass es beengt wirkt. Die Materialauswahl ist exquisit und die technische Ausstattung auf höchstem Niveau. Ein Meisterwerk des Houseboats-Designs!",
        "rating": 5,
        "title": "Design-Meisterwerk auf dem Wasser",
        "source": "Gästebuch"
    },
    {
        "name": "Familie Schneider",
        "date": "12.02.2024",
        "id": "5",
        "content": "Unser Familienurlaub mit drei Kindern war perfekt organisiert! Das Hausboot bietet genug Platz für alle und die sichere Terrasse gab den Kindern Freiheit zum Spielen. Die Eltern konnten in der Sauna entspannen, während die Kinder sicher spielten. Familienurlaub deluxe!",
        "rating": 5,
        "title": "Perfekter Familienurlaub mit drei Kindern",
        "source": "Gästebuch"
    },
    {
        "name": "Martina und Jochen",
        "date": "30.01.2024",
        "id": "4",
        "content": "Unser Neujahrsurlaub war traumhaft! Das Feuerwerk über dem Bodden von der eigenen Terrasse zu erleben, war magisch. Der Kamin sorgte für gemütliche Stimmung und die Sauna für Entspannung nach den Feiertagen. Ein perfekter Start ins neue Jahr!",
        "rating": 5,
        "title": "Magischer Neujahrsurlaub am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Detlef R.",
        "date": "18.12.2023",
        "id": "3",
        "content": "Als Vogelbeobachter war ich begeistert von der Lage! Direkt vom Hausboot aus konnte ich seltene Wasservögel beobachten und fotografieren. Die großen Fenster bieten perfekte Sicht und die Ruhe stört die Tiere nicht. Die komfortable Ausstattung ermöglichte stundenlange Beobachtungen bei jedem Wetter.",
        "rating": 5,
        "title": "Vogelbeobachter-Paradies am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Anja und Marcus",
        "date": "05.11.2023",
        "id": "2",
        "content": "Unser erster Besuch, aber sicher nicht der letzte! Das Coco de Mer hat alle unsere Erwartungen übertroffen. Die Kombination aus Luxus und Natur ist einmalig. Besonders beeindruckt waren wir von der Liebe zum Detail - von der Beleuchtung bis zur Musikanlage ist alles perfekt durchdacht.",
        "rating": 5,
        "title": "Erster Besuch - aber nicht der letzte!",
        "source": "Gästebuch"
    },
    {
        "name": "Hans-Peter und Ingeborg",
        "date": "22.09.2023",
        "id": "1",
        "content": "Wir haben das Coco de Mer zur Eröffnung besucht und waren von Anfang an begeistert! Die Vision der Vermieter, ein Stück Seychellen an den Bodden zu bringen, ist perfekt umgesetzt worden. Die Qualität und der Service sind hervorragend. Wir sind stolz darauf, die ersten Gäste gewesen zu sein!",
        "rating": 5,
        "title": "Eröffnungsgäste - von Anfang an begeistert!",
        "source": "Gästebuch"
    }
]

def import_review(review_data):
    """Import a single review with error handling"""
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
            return review["id"]
        elif response.status_code == 429:
            print(f"⏳ Rate limited for {review_data['name']} - waiting longer...")
            return "rate_limited"
        else:
            print(f"✗ Failed to import {review_data['name']}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error importing {review_data['name']}: {str(e)}")
        return None

def main():
    print("🚀 Starting remaining Coco de Mer reviews import...")
    print(f"📝 Found {len(remaining_reviews)} remaining reviews to import")
    print("⏱️  Using 3-second delays to avoid rate limiting...")
    
    imported_count = 0
    failed_count = 0
    rate_limited_count = 0
    
    for i, review in enumerate(remaining_reviews):
        print(f"\n[{i+1}/{len(remaining_reviews)}] Processing {review['name']}...")
        
        result = import_review(review)
        if result == "rate_limited":
            rate_limited_count += 1
            print("⏳ Waiting 10 seconds before retry...")
            time.sleep(10)
            # Retry once
            result = import_review(review)
            if result and result != "rate_limited":
                imported_count += 1
            else:
                failed_count += 1
        elif result:
            imported_count += 1
        else:
            failed_count += 1
        
        # Wait between requests to avoid rate limiting
        if i < len(remaining_reviews) - 1:  # Don't wait after the last request
            print("⏳ Waiting 3 seconds...")
            time.sleep(3)
    
    print(f"\n📊 Import Summary:")
    print(f"✅ Successfully imported: {imported_count}")
    print(f"❌ Failed imports: {failed_count}")
    print(f"⏳ Rate limited: {rate_limited_count}")
    print(f"📈 Total processed: {len(remaining_reviews)}")
    
    if imported_count > 0:
        print(f"\n🎉 Import completed! Check http://localhost:8080 to see all reviews.")
        print(f"💡 Note: New reviews need admin approval to appear publicly.")

if __name__ == "__main__":
    main()
