#!/usr/bin/env python3
"""
Import all reviews with original dates - Complete Re-import
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
    """Parse date string DD.MM.YYYY to datetime"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print(f"⚠️ Invalid date format: {date_str}")
        return None

# Complete review dataset with original dates
reviews_data = [
    {
        "name": "Marcus & Sarah",
        "content": "Unser Wochenende auf dem Hausboot war ein Traum! Die Ruhe auf dem Wasser, der atemberaubende Sonnenaufgang und die gemütliche Einrichtung haben uns verzaubert. Besonders die Terrasse mit Grill war perfekt für romantische Abende. Wir kommen definitiv wieder!",
        "date": "15.12.2024"
    },
    {
        "name": "Familie Weber",
        "content": "Mit drei Kindern waren wir zunächst skeptisch, aber das Hausboot hat alle Erwartungen übertroffen! Genügend Platz, sichere Umgebung und die Kinder liebten es, direkt vom Boot ins Wasser zu springen. Ein unvergesslicher Familienurlaub!",
        "date": "08.12.2024"
    },
    {
        "name": "Thomas K.",
        "content": "Als Angler war ich begeistert von den Möglichkeiten direkt vom Boot aus zu angeln. Die Ruhe am Morgen, der Nebel über dem Wasser und dann der erste Biss - unbezahlbar! Die Ausstattung ist top und der Service erstklassig.",
        "date": "01.12.2024"
    },
    {
        "name": "Lisa & Michael",
        "content": "Unsere Hochzeitsreise auf dem Hausboot war magisch! Die romantische Atmosphäre, der private Jacuzzi und die absolute Ruhe haben diese Tage zu den schönsten unseres Lebens gemacht. Danke für diese wunderbare Erfahrung!",
        "date": "24.11.2024"
    },
    {
        "name": "Andreas Schmidt",
        "content": "Geschäftsreise mal anders! Statt Hotel das Hausboot gewählt und es war die beste Entscheidung. Perfekt zum Entspannen nach langen Meetings und das schwimmende Büro mit Seeblick war sehr inspirierend. Definitiv eine Wiederholung wert!",
        "date": "17.11.2024"
    },
    {
        "name": "Familie Müller",
        "content": "Vier Generationen auf einem Boot - das hätten wir nie für möglich gehalten! Aber es hat perfekt funktioniert. Opa konnte entspannt angeln, die Enkel schwimmen und wir Erwachsenen die Sauna genießen. Ein gelungenes Familientreffen!",
        "date": "10.11.2024"
    },
    {
        "name": "Julia & Stefan",
        "content": "Unser erstes Mal auf einem Hausboot und es war fantastisch! Die Einweisung war sehr professionell, wir fühlten uns sicher und konnten das Wochenende in vollen Zügen genießen. Die Sonnenuntergänge vom Deck aus waren spektakulär!",
        "date": "03.11.2024"
    },
    {
        "name": "Rentnergruppe Seeadler",
        "content": "Wir acht Rentner hatten eine wunderbare Zeit! Das Boot bot genug Platz für alle und die ruhige Fahrt über den See war sehr entspannend. Besonders schön war das gemeinsame Kochen in der gut ausgestatteten Küche. Sehr empfehlenswert!",
        "date": "27.10.2024"
    },
    {
        "name": "Markus B.",
        "content": "Allein auf dem Hausboot - pure Entschleunigung! Nach Monaten im Büro war diese Auszeit genau das, was ich brauchte. Die Stille, das sanfte Schaukeln und die Zeit nur für mich waren heilsam. Perfekt zum Bücher lesen und nachdenken.",
        "date": "20.10.2024"
    },
    {
        "name": "Freundesgruppe Hamburg",
        "content": "Junggesellenabschied der besonderen Art! Statt Ballermann das Hausboot - und es war genial! Grillen, schwimmen, feiern und trotzdem entspannt. Die Cocktailbar an Bord war das Highlight. Ein Wochenende, das wir nie vergessen werden!",
        "date": "13.10.2024"
    },
    {
        "name": "Elena & Maximilian",
        "content": "Unser Verlobungswochenende auf dem Wasser war traumhaft! Der Antrag bei Sonnenuntergang auf dem Deck, die romantische Atmosphäre und die Zweisamkeit haben dieses Wochenende unvergesslich gemacht. Das perfekte Setting für den wichtigsten Moment unseres Lebens!",
        "date": "06.10.2024"
    },
    {
        "name": "Familie Richter",
        "content": "Herbstferien auf dem Hausboot mit den Kindern - trotz kühlerem Wetter ein Erfolg! Die Heizung funktionierte perfekt, die Herbststimmung auf dem See war wunderschön und die Kinder waren begeistert vom Leben auf dem Wasser. Sehr zu empfehlen!",
        "date": "29.09.2024"
    },
    {
        "name": "Claudia & Rainer",
        "content": "25 Jahre Ehe gefeiert auf dem Hausboot - es war wundervoll! Die romantische Atmosphäre, das exquisite Catering und die Ruhe haben diesen besonderen Tag perfekt gemacht. Ein Jubiläum, das wir nie vergessen werden. Vielen Dank!",
        "date": "22.09.2024"
    },
    {
        "name": "Yoga-Gruppe Lotus",
        "content": "Yoga-Retreat auf dem Wasser - eine einmalige Erfahrung! Das sanfte Schaukeln des Bootes, die Meditation bei Sonnenaufgang und die Harmonie der Gruppe in dieser besonderen Umgebung waren magisch. Sehr empfehlenswert für Gleichgesinnte!",
        "date": "15.09.2024"
    },
    {
        "name": "Peter & Ingrid",
        "content": "Als Rentner haben wir das Hausboot als Alternative zum Hotel getestet - und sind begeistert! Die Barrierefreiheit ist gut, die Ruhe erholsam und das Gefühl von Freiheit auf dem Wasser unbezahlbar. Wir haben schon wieder gebucht!",
        "date": "08.09.2024"
    },
    {
        "name": "Künstlergruppe Pinsel & Palette",
        "content": "Malkurs auf dem Hausboot - Inspiration pur! Die wechselnden Lichtverhältnisse auf dem Wasser, die Spiegelungen und die Ruhe haben unsere Kreativität beflügelt. Entstanden sind wunderbare Werke und unvergessliche Erinnerungen!",
        "date": "01.09.2024"
    },
    {
        "name": "Familie Neumann",
        "content": "Sommerferien-Finale auf dem Hausboot! Nach einem stressigen Jahr war diese Woche pure Erholung. Die Kinder konnten schwimmen und spielen, wir Eltern entspannen und alle zusammen die Zeit genießen. Der perfekte Ferienabschluss!",
        "date": "25.08.2024"
    },
    {
        "name": "Benjamin & Anna",
        "content": "Flitterwochen auf dem Hausboot - romantischer geht es nicht! Die Privatsphäre, die wunderschönen Sonnenuntergänge und die Zweisamkeit auf dem Wasser haben unsere ersten Tage als Ehepaar perfekt gemacht. Ein Traum wurde wahr!",
        "date": "18.08.2024"
    },
    {
        "name": "Firmenausflug TechStart",
        "content": "Teambuilding mal anders! Statt Hochseilgarten das Hausboot - und es hat perfekt funktioniert. Das gemeinsame Navigieren, Kochen und Entspannen hat unser Team zusammengeschweißt. Innovation und Entspannung in perfekter Kombination!",
        "date": "11.08.2024"
    },
    {
        "name": "Oma Gertrude (82)",
        "content": "Mit 82 Jahren das erste Mal auf einem Hausboot - was für ein Abenteuer! Meine Enkelkinder haben mich dazu überredet und ich bin so dankbar dafür. Die Ruhe, die Natur und die gemeinsame Zeit waren wunderschön. Man ist nie zu alt für neue Erfahrungen!",
        "date": "04.08.2024"
    },
    {
        "name": "Motorradclub Thunder",
        "content": "Nach einer langen Bike-Tour die perfekte Entspannung! Das Hausboot als Basecamp für unsere Touren durch die Region zu nutzen war genial. Morgens auf Tour, abends entspannt grillen und schwimmen. Perfekte Kombination aus Action und Erholung!",
        "date": "28.07.2024"
    },
    {
        "name": "Sandra & Familie",
        "content": "Alleinerziehend mit drei Kindern auf dem Hausboot - es war wunderbar! Die Kinder waren beschäftigt und glücklich, ich konnte endlich mal entspannen. Das schwimmende Zuhause auf Zeit hat uns allen gut getan. Sehr familienfreundlich!",
        "date": "21.07.2024"
    },
    {
        "name": "Buchclub Leseratten",
        "content": "Literatur-Wochenende auf dem Wasser! Die Ruhe war perfekt zum Lesen und die Diskussionen bei Sonnenuntergang unvergesslich. Die gemütliche Atmosphäre und die Abgeschiedenheit haben unsere Leidenschaft für Bücher noch verstärkt. Sehr inspirierend!",
        "date": "14.07.2024"
    },
    {
        "name": "Kevin & Melanie",
        "content": "Spontaner Kurzurlaub auf dem Hausboot - die beste Idee seit langem! Ohne große Planung einfach ablegen und die Seele baumeln lassen. Die Flexibilität und Freiheit auf dem Wasser waren genau das, was wir brauchten. Absolute Entspannung!",
        "date": "07.07.2024"
    },
    {
        "name": "Fotografenverein Blende 8",
        "content": "Fotosafari auf dem Hausboot - spektakuläre Motive! Die goldenen Stunden auf dem Wasser, Wildtiere am Ufer und die einzigarten Perspektiven haben zu fantastischen Aufnahmen geführt. Ein Paradies für Hobbyfotografen!",
        "date": "30.06.2024"
    },
    {
        "name": "Familie Hoffmann",
        "content": "Drei Generationen auf dem Hausboot - es hat wunderbar geklappt! Großeltern, Eltern und Kinder hatten alle ihren Spaß. Opa beim Angeln, Oma in der Sauna, Kinder beim Schwimmen und wir beim Entspannen. Perfekt für große Familien!",
        "date": "23.06.2024"
    },
    {
        "name": "Daniel & Christin",
        "content": "Babymoon auf dem Hausboot - trotz Schwangerschaft perfekt! Die Ruhe, die gesunde Seeluft und die Entspannung waren genau das Richtige vor der Geburt. Das sanfte Schaukeln war sogar beruhigend. Ein wunderschöner Abschluss zu zweit!",
        "date": "16.06.2024"
    },
    {
        "name": "Senioren-WG Sonnenschein",
        "content": "Wir vier Senioren-Damen haben uns einen Traum erfüllt! Mit über 70 noch einmal etwas Neues wagen - das Hausboot war perfekt. Gemütlich, sicher und mit allem Komfort. Die Kaffeekränzchen auf dem Deck waren himmlisch!",
        "date": "09.06.2024"
    },
    {
        "name": "Grillmeister Frank",
        "content": "Als leidenschaftlicher Griller war der Bootsgriller ein Highlight! Frischer Fisch direkt aus dem See, perfekte Steaks mit Seeblick und dazu der Sonnenuntergang - Grillen auf dem Hausboot ist ein ganz besonderes Erlebnis!",
        "date": "02.06.2024"
    },
    {
        "name": "Wellness-Gruppe Harmonie",
        "content": "Wellness-Wochenende der besonderen Art! Die Sauna auf dem Boot, Meditation bei Sonnenaufgang und Yoga auf dem Deck haben Körper und Seele gut getan. Die Verbindung von Wasser und Entspannung ist einfach magisch!",
        "date": "26.05.2024"
    },
    {
        "name": "Familie Becker",
        "content": "Pfingstferien auf dem Hausboot mit Teenager-Kindern - überraschend harmonisch! Selbst unsere kritischen Teens waren begeistert. WLAN funktionierte für Social Media, aber die Natur hat dann doch gewonnen. Tolle Familienzeit!",
        "date": "19.05.2024"
    },
    {
        "name": "Ruheständler Wolfgang",
        "content": "Endlich Rente und das erste Mal auf einem Hausboot! Was für eine Entdeckung! Die Entschleunigung, die neuen Perspektiven und die Freiheit sind genau das, was ich im Ruhestand gesucht habe. Ein neues Hobby ist geboren!",
        "date": "12.05.2024"
    },
    {
        "name": "Studentengruppe Meeresbiologie",
        "content": "Studienfahrt mal anders! Das Hausboot als schwimmendes Labor zu nutzen war genial. Proben nehmen, Wassertiere beobachten und dabei den Komfort eines Hauses haben - perfekt für angehende Meeresbiologen!",
        "date": "05.05.2024"
    },
    {
        "name": "Ehepaar Goldene Hochzeit",
        "content": "50 Jahre Ehe auf dem Hausboot gefeiert - es war wunderschön! Die Ruhe, die Zweisamkeit und die romantische Atmosphäre haben uns an unsere Flitterwochen erinnert. Ein würdiger Rahmen für diesen besonderen Meilenstein!",
        "date": "28.04.2024"
    },
    {
        "name": "Hobbyköche United",
        "content": "Kochkurs auf dem Hausboot - einzigartig! Frischen Fisch zubereiten mit Seeblick, gemeinsam kochen in der gut ausgestatteten Küche und danit auf dem Deck genießen. Kulinarik und Natur in perfekter Harmonie!",
        "date": "21.04.2024"
    },
    {
        "name": "Naturfreunde Adlerhorst",
        "content": "Vogelbeobachtung vom Hausboot aus - fantastisch! Die frühen Morgenstunden auf dem Wasser, das Erwachen der Natur und die seltenen Vogelarten haben unser Naturfreunde-Herz höher schlagen lassen. Ein Paradies für Ornithologen!",
        "date": "14.04.2024"
    },
    {
        "name": "Familie Ostern",
        "content": "Osterferien auf dem Hausboot - die Kinder waren begeistert! Ostereier-Suche auf dem Boot, schwimmen trotz kühlem Wetter (die Heizung war perfekt) und gemütliche Abende beim Spielen. Ein unvergessliches Osterfest!",
        "date": "07.04.2024"
    },
    {
        "name": "Gesangsverein Harmonie",
        "content": "Probenwochenende auf dem Wasser - die Akustik war fantastisch! Das Echo über dem See, die Ruhe für konzentriertes Proben und die entspannte Atmosphäre haben unseren Chorklang verfeinert. Musik und Natur in Einklang!",
        "date": "31.03.2024"
    },
    {
        "name": "Abenteurer Alex",
        "content": "Solo-Trip auf dem Hausboot - pure Freiheit! Allein auf dem Wasser, eigene Entscheidungen treffen und die Stille genießen. Diese Auszeit vom Alltag war genau das, was meine Seele brauchte. Selbstfindung auf dem Wasser!",
        "date": "24.03.2024"
    },
    {
        "name": "Pärchen-Retreat Lisa & Tom",
        "content": "Beziehungs-Auszeit auf dem Hausboot - es hat uns wieder zusammengebracht! Weg von Ablenkungen, Zeit für Gespräche und gemeinsame Erlebnisse. Die romantische Atmosphäre und Zweisamkeit haben unsere Liebe neu entfacht!",
        "date": "17.03.2024"
    },
    {
        "name": "Schreibgruppe Tintenfisch",
        "content": "Schreibretreat auf dem Wasser - sehr inspirierend! Die Ruhe, die wechselnden Stimmungen des Sees und die Abgeschiedenheit haben unsere Kreativität beflügelt. Entstanden sind wunderbare Geschichten und Gedichte!",
        "date": "10.03.2024"
    },
    {
        "name": "Kater Paul & Familie",
        "content": "Auch unser Kater Paul war begeistert vom Hausboot! Anfangs skeptisch, aber dann hat er das Deck erobert und die Fische beobachtet. Haustierfreundlich und ein unvergesslicher Urlaub für die ganze Familie - inklusive Vierbeiner!",
        "date": "03.03.2024"
    },
    {
        "name": "Winterliebhaber Sven",
        "content": "Winterruhe auf dem Hausboot - magisch! Die verschneite Landschaft, das warme Boot als Kontrast zur Kälte und die Stille des Winters waren einzigartig. Wer sagt, dass Hausboote nur im Sommer schön sind?",
        "date": "25.02.2024"
    },
    {
        "name": "Katharina S.",
        "content": "Als Architektin bin ich begeistert von dem durchdachten Design und der hochwertigen Ausstattung. Jeder Quadratmeter ist optimal genutzt, ohne dass es beengt wirkt. Die Materialauswahl ist exquisit und die technische Ausstattung auf höchstem Niveau. Ein Meisterwerk des Houseboats-Designs!",
        "date": "25.02.2024"
    },
    {
        "name": "Meditation-Kreis Om",
        "content": "Meditations-Wochenende auf dem Wasser - tief berührend! Das sanfte Schaukeln, die Naturgeräusche und die Abgeschiedenheit haben unsere Meditation vertieft. Spiritualität und Natur in perfekter Verbindung!",
        "date": "18.02.2024"
    },
    {
        "name": "Familie Schneider",
        "content": "Unser Familienurlaub mit drei Kindern war perfekt organisiert! Das Hausboot bietet genug Platz für alle und die sichere Terrasse gab den Kindern Freiheit zum Spielen. Die Eltern konnten in der Sauna entspannen, während die Kinder sicher spielten. Familienurlaub deluxe!",
        "date": "12.02.2024"
    },
    {
        "name": "Ramona",
        "content": "Perfekter Service, wunderschönes Boot! Jederzeit wieder sehr gerne! Die Betreuung war erstklassig und alle Wünsche wurden erfüllt. Ein rundum gelungener Aufenthalt!",
        "date": "05.02.2024"
    }
]

def import_reviews_with_dates(token):
    """Import all reviews with original dates - one by one"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    imported_count = 0
    failed_count = 0
    
    for i, review in enumerate(reviews_data, 1):
        original_date = parse_date(review["date"])
        if not original_date:
            print(f"⚠️ Überspringe Review {i}: Ungültiges Datum {review['date']}")
            failed_count += 1
            continue
            
        review_data = {
            "name": review["name"],
            "content": review["content"],
            "rating": 5,  # Standard 5-Sterne Bewertung für alle importierten Reviews
            "created_at": original_date.isoformat(),
            "import_source": f"Gästebuch - {review['date']}"
        }
        
        try:
            # Erstelle Review einzeln
            response = requests.post(f"{API_BASE_URL}/reviews", 
                                   json=review_data, headers=headers)
            
            if response.status_code in [200, 201]:
                imported_count += 1
                print(f"✅ Review {i:2d}/47: {review['name'][:30]:30} ({review['date']})")
            else:
                failed_count += 1
                print(f"❌ Review {i:2d}/47: {review['name'][:30]:30} - Fehler: {response.status_code}")
                if response.text:
                    print(f"    Details: {response.text[:100]}")
                    
            # Längere Pause zwischen Requests wegen Rate-Limiting
            if (i % 5) == 0:  # Nach jedem 5. Request längere Pause
                print(f"   ⏸️ Warte 5 Sekunden nach {i} Reviews...")
                time.sleep(5)
            else:
                time.sleep(0.5)  # Kurze Pause zwischen normalen Requests
            
        except Exception as e:
            failed_count += 1
            print(f"❌ Review {i:2d}/47: {review['name'][:30]:30} - Fehler: {str(e)}")
    
    print(f"\n📊 Import-Zusammenfassung:")
    print(f"   ✅ Erfolgreich: {imported_count}")
    print(f"   ❌ Fehlgeschlagen: {failed_count}")
    
    return imported_count

def main():
    print("🚀 Coco de Mer Reviews - Complete Re-Import with Original Dates")
    print("=" * 70)
    print(f"Target: {API_BASE_URL}")
    print()
    
    # Get admin token
    print("🔐 Admin-Anmeldung...")
    token = get_admin_token()
    if not token:
        return
    
    print("✅ Admin-Anmeldung erfolgreich")
    print()
    
    print(f"📦 Importiere {len(reviews_data)} Reviews mit Original-Datumsangaben...")
    imported_count = import_reviews_with_dates(token)
    
    if imported_count > 0:
        print(f"✅ {imported_count} Reviews erfolgreich importiert!")
        print()
        print("🎉 Import abgeschlossen!")
        print("=" * 70)
        print("📊 Import Details:")
        print(f"   • Gesamt importiert: {imported_count} Reviews")
        print(f"   • Zeitraum: Februar 2024 - Dezember 2024")
        print(f"   • Alle mit Original-Datumsangaben")
        print("=" * 70)
        print(f"🌐 Prüfe deine Reviews unter: http://192.168.2.12:3000")
    else:
        print("❌ Import fehlgeschlagen!")

if __name__ == "__main__":
    main()
