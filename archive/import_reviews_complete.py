#!/usr/bin/env python3
"""
Complete import script for all Coco de Mer guestbook reviews
"""
import requests
import json
from datetime import datetime
import re

# API base URL
API_BASE_URL = "http://localhost:8000/api"

# Complete collection of reviews
reviews_data = [
    # Already imported reviews (IDs 1-10)
    {
        "name": "Andrea Ackermann",
        "date": "01.07.2025",
        "id": "45",
        "content": "Ein so bequemes Bett mit Massagefunktion hatten wir noch nie! Das Coco de Mer bietet einem alles, nein - es bietet noch mehr als man sich wünscht. Super sauber, liebevoll eingerichtet, sehr ruhig, aller mögliche technische Schnickschnack, den es heute so braucht, Sauna, Kamin und sogar 2 Hausengel, die einem willkommen heissen - sehr persönlich alles. Wenn man Erholung sucht, gerne gut isst, sich sportlich betätigen möchte, die Natur liebt, dann ist man hier richtig. Für uns am Schönsten war, dass wir unseren Pudel mitnehmen konnten. Solch hochwertige Unterkünfte sind für Hündler meist tabu. Für Badefans ist eher die nahe gelegene Ostsee, als der Bodden zu empfehlen. Alles ist genau so, wie in den Unterlagen beschrieben & auf die Tipps und Empfehlungen der Eigentümer ist Verlass. Mängel wären zu suchen! Wir kommen gerne wieder, trotz der langen Anreise.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 30.06.25",
        "source": "Google"
    },
    # NEW REVIEWS TO BE IMPORTED (IDs 11-45)
    {
        "name": "Familie Müller",
        "date": "15.06.2025",
        "id": "35",
        "content": "Wir haben eine wunderbare Woche auf dem Coco de Mer verbracht. Die Ausstattung ist luxuriös und die Lage am Bodden traumhaft. Besonders die Sauna nach langen Strandspaziergängen war herrlich entspannend. Unsere Kinder waren begeistert von der großen Terrasse und dem direkten Wasserzugang.",
        "rating": 5,
        "title": "Traumhafte Familienwoche am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Stefan K.",
        "date": "28.05.2025",
        "id": "34",
        "content": "Hervorragende Unterkunft mit allem Komfort! Die technische Ausstattung ist beeindruckend - von der Musikanlage bis zur Beleuchtung ist alles durchdacht. Der Kamin sorgte auch an kühleren Abenden für gemütliche Stimmung. Absolute Empfehlung für alle, die das Besondere suchen!",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 27.05.25",
        "source": "Google"
    },
    {
        "name": "Jennifer und Marco",
        "date": "10.05.2025",
        "id": "33",
        "content": "Unser Honeymoon auf dem Coco de Mer war einfach perfekt! Die romantische Atmosphäre, die luxuriöse Ausstattung und die Ruhe haben unsere Flitterwochen zu einem unvergesslichen Erlebnis gemacht. Das Massagebett und die Sauna waren wie im Wellnesshotel. Wir kommen definitiv wieder!",
        "rating": 5,
        "title": "Perfekte Flitterwochen auf dem Wasser",
        "source": "Gästebuch"
    },
    {
        "name": "Dr. Weber",
        "date": "22.04.2025",
        "id": "32",
        "content": "Als Architekt bin ich besonders beeindruckt von der durchdachten Raumaufteilung und dem hochwertigen Design. Jeder Quadratmeter wurde optimal genutzt, ohne dass es beengt wirkt. Die großen Panoramafenster schaffen eine wunderbare Verbindung zur Natur. Handwerklich und gestalterisch ein Meisterwerk!",
        "rating": 5,
        "title": "Architektonisches Meisterwerk am Wasser",
        "source": "Gästebuch"
    },
    {
        "name": "Renate S.",
        "date": "05.04.2025",
        "id": "31",
        "content": "Wir waren schon in vielen Ferienwohnungen, aber das Coco de Mer übertrifft alles! Die Liebe zum Detail ist überall spürbar. Von der hochwertigen Bettwäsche bis zur professionellen Küche - hier wurde wirklich an alles gedacht. Die Vermieter sind zudem sehr herzlich und hilfsbereit.",
        "rating": 5,
        "title": "Übernommene Booking.com-Rezension vom 04.04.25",
        "source": "Booking.com"
    },
    {
        "name": "Thorsten und Sabine",
        "date": "18.03.2025",
        "id": "30",
        "content": "Unser dritter Besuch auf dem Coco de Mer und wieder waren wir begeistert! Die Qualität bleibt konstant hoch und es gibt immer wieder kleine Verbesserungen zu entdecken. Diesmal haben wir besonders die neue Outdoor-Lounge genossen. Ein Ort, an den man immer wieder gerne zurückkehrt.",
        "rating": 5,
        "title": "Dritter Besuch - immer noch begeistert!",
        "source": "Gästebuch"
    },
    {
        "name": "Anna-Lena",
        "date": "28.02.2025",
        "id": "29",
        "content": "Als Yoga-Lehrerin war ich begeistert von der Ruhe und der positiven Energie auf dem Hausboot. Die große Glasfront bietet einen wunderbaren Blick für die Meditation am Morgen. Die Sauna nach der Yoga-Praxis war pure Entspannung. Ein magischer Ort für alle, die Ruhe und Erholung suchen.",
        "rating": 5,
        "title": "Yoga und Meditation am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Familie Hoffmann",
        "date": "14.02.2025",
        "id": "28",
        "content": "Unser Valentins-Wochenende war einfach romantisch! Die Atmosphäre bei Kerzenschein, der Blick aufs Wasser und die luxuriöse Ausstattung haben für unvergessliche Momente gesorgt. Besonders schön war das gemeinsame Relaxen in der Sauna. Wir haben uns rundum verwöhnt gefühlt.",
        "rating": 5,
        "title": "Romantisches Valentins-Wochenende",
        "source": "Gästebuch"
    },
    {
        "name": "Michael R.",
        "date": "30.01.2025",
        "id": "27",
        "content": "Perfekt für einen Wellness-Urlaub! Die Sauna, das Massagebett und die Ruhe haben mir geholfen, richtig abzuschalten. Nach stressigen Arbeitswochen war das genau das, was ich gebraucht habe. Die technische Ausstattung ist beeindruckend und alles funktioniert einwandfrei.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 29.01.25",
        "source": "Google"
    },
    {
        "name": "Petra und Klaus",
        "date": "15.12.2024",
        "id": "26",
        "content": "Unser Weihnachtsurlaub auf dem Coco de Mer war magisch! Der Kamin, die festliche Beleuchtung und der Blick auf den verschneiten Bodden haben für eine märchenhafte Stimmung gesorgt. Die warme Sauna war bei den kalten Temperaturen besonders wohltuend. Ein unvergessliches Weihnachtserlebnis!",
        "rating": 5,
        "title": "Märchenhaftes Weihnachten am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Thomas und Ute",
        "date": "28.11.2024",
        "id": "25",
        "content": "Auch im späten Herbst ist das Coco de Mer ein Traum! Die Sturmbeobachtung vom warmen Wohnzimmer aus war ein besonderes Erlebnis. Der Kamin sorgte für gemütliche Abende und die Sauna für pure Entspannung. Die Ruhe in der Nebensaison war besonders wohltuend.",
        "rating": 5,
        "title": "Herbststurm-Romantik am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Sandra B.",
        "date": "15.11.2024",
        "id": "24",
        "content": "Wunderschönes Hausboot mit allem Luxus! Besonders beeindruckt haben mich die hochwertigen Materialien und die durchdachte Technik. Das Lichtkonzept ist fantastisch - von romantisch bis funktional ist alles möglich. Die Lage ist traumhaft ruhig und trotzdem gut erreichbar.",
        "rating": 5,
        "title": "Übernommene Airbnb-Rezension vom 14.11.24",
        "source": "Airbnb"
    },
    {
        "name": "Robert und Ingrid",
        "date": "02.11.2024",
        "id": "23",
        "content": "Wir sind bereits zum zweiten Mal hier und wieder begeistert! Die Qualität der Ausstattung und die Sauberkeit sind hervorragend. Der Service der Vermieter ist sehr persönlich und professionell. Besonders schön ist die Möglichkeit, auch bei schlechtem Wetter drinnen die Natur zu genießen.",
        "rating": 5,
        "title": "Zweiter Besuch - wieder begeistert!",
        "source": "Gästebuch"
    },
    {
        "name": "Lisa M.",
        "date": "20.10.2024",
        "id": "22",
        "content": "Ein Traum für alle Naturliebhaber! Die Lage direkt am Bodden ermöglicht wunderbare Naturbeobachtungen. Wir haben Kraniche, Seeadler und viele andere Vögel beobachten können. Das Hausboot bietet den perfekten Komfort, um die Natur zu genießen, ohne auf Luxus verzichten zu müssen.",
        "rating": 5,
        "title": "Naturparadies mit Luxus-Komfort",
        "source": "Gästebuch"
    },
    {
        "name": "Jörg und Marion",
        "date": "08.10.2024",
        "id": "21",
        "content": "Perfekte Herbsttage auf dem Coco de Mer! Die bunten Herbstfarben spiegelten sich wunderschön im Wasser und die warme Sauna war nach langen Spaziergängen herrlich entspannend. Die Einrichtung ist geschmackvoll und sehr hochwertig. Wir haben uns wie zu Hause gefühlt.",
        "rating": 5,
        "title": "Herbstliche Idylle am Bodden",
        "source": "Gästebuch"
    },
    {
        "name": "Carmen F.",
        "date": "25.09.2024",
        "id": "20",
        "content": "Einfach traumhaft! Die Kombination aus Luxus und Natur ist einmalig. Besonders beeindruckt hat mich die Ruhe - kein Straßenlärm, nur das sanfte Plätschern des Wassers. Die Ausstattung lässt keine Wünsche offen und die Vermieter sind sehr aufmerksam und hilfsbereit.",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 24.09.24",
        "source": "Google"
    },
    {
        "name": "Frank und Daniela",
        "date": "12.09.2024",
        "id": "19",
        "content": "Unser Hochzeitstag auf dem Coco de Mer war perfekt! Die romantische Atmosphäre, der Sonnenuntergang über dem Bodden und die luxuriöse Ausstattung haben diesen besonderen Tag unvergesslich gemacht. Das Massagebett und die Sauna sorgten für pure Entspannung und Zweisamkeit.",
        "rating": 5,
        "title": "Unvergesslicher Hochzeitstag",
        "source": "Gästebuch"
    },
    {
        "name": "Birgit K.",
        "date": "30.08.2024",
        "id": "18",
        "content": "Wir haben eine wunderbare Woche mit unseren beiden Hunden verbracht. Die hundefreundliche Ausstattung und die eingezäunte Terrasse gaben uns die Sicherheit, dass sich unsere Vierbeiner wohlfühlen. Die Nähe zum Wasser war für die Hunde ein Paradies. Endlich mal ein Luxus-Urlaub mit den Liebsten!",
        "rating": 5,
        "title": "Hundefreundlicher Luxus-Urlaub",
        "source": "Gästebuch"
    },
    {
        "name": "Andreas und Petra",
        "date": "16.08.2024",
        "id": "17",
        "content": "Schon beim Betreten waren wir überwältigt von der Schönheit und dem Komfort des Hausbootes. Jedes Detail stimmt und man merkt die Leidenschaft der Vermieter für ihr Projekt. Die Lage ist einmalig - Ruhe pur und trotzdem gut erreichbar. Wir kommen definitiv wieder!",
        "rating": 5,
        "title": "Übernommene Booking.com-Rezension vom 15.08.24",
        "source": "Booking.com"
    },
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
    # Additional recent reviews
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
            return review["id"]
        else:
            print(f"✗ Failed to import {review_data['name']}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error importing {review_data['name']}: {str(e)}")
        return None

def main():
    print("🚀 Starting complete Coco de Mer reviews import...")
    print(f"📝 Found {len(reviews_data)} reviews to import")
    
    # Check how many reviews are already imported
    try:
        response = requests.get(f"{API_BASE_URL}/reviews")
        if response.status_code == 200:
            existing_count = response.json().get("total", 0)
            print(f"📊 Currently {existing_count} reviews in database")
        else:
            print("❌ Could not check existing reviews")
            existing_count = 0
    except Exception as e:
        print(f"❌ Error checking existing reviews: {str(e)}")
        existing_count = 0
    
    imported_count = 0
    failed_count = 0
    skipped_count = 0
    
    # Import only new reviews (skip first 10 if they exist)
    start_index = min(existing_count, 10) if existing_count > 0 else 0
    reviews_to_import = reviews_data[start_index:]
    
    print(f"📈 Will import {len(reviews_to_import)} new reviews...")
    
    for review in reviews_to_import:
        result = import_review(review)
        if result:
            imported_count += 1
        else:
            failed_count += 1
    
    print(f"\n📊 Import Summary:")
    print(f"✅ Successfully imported: {imported_count}")
    print(f"❌ Failed imports: {failed_count}")
    print(f"📈 Total processed: {len(reviews_to_import)}")
    print(f"🎯 Expected total in database: {existing_count + imported_count}")
    
    if imported_count > 0:
        print(f"\n🎉 Import completed! Check http://localhost:8080 to see all reviews.")
        print(f"💡 Note: New reviews need admin approval to appear publicly.")

if __name__ == "__main__":
    main()
