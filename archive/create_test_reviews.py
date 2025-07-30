#!/usr/bin/env python3
"""
Script zum Erstellen von Test-Bewertungen über die API
"""
import requests
import random
import json
import time
from datetime import datetime, timedelta

# API-Konfiguration
API_BASE_URL = "http://localhost:8000"
REVIEWS_ENDPOINT = f"{API_BASE_URL}/api/reviews"

# Test-Daten
NAMES = [
    "Anna Müller", "Max Schmidt", "Lisa Weber", "Tom Fischer", "Sarah Bauer",
    "Felix Wagner", "Emma Richter", "Paul Neumann", "Mia Hoffmann", "Leon Zimmermann",
    "Lena Braun", "Finn Krüger", "Lara Schulz", "Nils Köhler", "Julia König",
    "Tim Lehmann", "Nina Fuchs", "Jan Günther", "Maya Klein", "Luis Schwarz",
    "Zoe Weiß", "Ben Hartmann", "Eva Schröder", "Noah Lange", "Pia Schmitt",
    "Henri Peters", "Lea Hansen", "Elias Müller", "Amelie Werner", "Jonas Krause",
    "Sophie Friedrich", "David Meier", "Charlotte Wolf", "Alexander Jung", "Marie Hahn"
]

TITLES = [
    "Fantastische Erfahrung!", "Sehr empfehlenswert", "Top Service!",
    "Absolut begeistert", "Einfach perfekt", "Großartige Qualität",
    "Hervorragender Service", "Wunderbare Atmosphäre", "Exzellente Betreuung",
    "Traumhaft schön", "Rundum zufrieden", "Klasse gemacht!", 
    "Sehr professionell", "Überaus freundlich", "Einfach toll",
    "Mega gut!", "Super Erlebnis", "Wirklich beeindruckend",
    "Kann ich nur empfehlen", "Ausgezeichnet!", "Sehr zufrieden",
    "Tolle Qualität", "Perfekter Service", "Wunderbar!",
    "Excellent choice", "Amazing experience", "Outstanding quality",
    "Brilliant service", "Wonderful time", "Highly recommended",
    "Absolutely fantastic", "Great value", "Perfect execution",
    "Exceptional quality", "Superb experience"
]

COMMENTS = [
    "Ich bin wirklich begeistert von der Qualität und dem Service. Alles hat perfekt geklappt und die Mitarbeiter waren sehr freundlich und hilfsbereit. Kann ich nur weiterempfehlen!",
    "Eine wunderbare Erfahrung! Das Team war professionell und zuvorkommend. Die Qualität hat alle meine Erwartungen übertroffen. Gerne wieder!",
    "Fantastischer Service von Anfang bis Ende. Sehr kompetente Beratung und schnelle Umsetzung. Das Ergebnis spricht für sich!",
    "Absolute Spitzenklasse! Hier stimmt einfach alles - von der Beratung über die Ausführung bis hin zum Endergebnis. Vielen Dank!",
    "Ich war zunächst skeptisch, aber alle Zweifel wurden schnell ausgeräumt. Hervorragende Arbeit und faire Preise. Sehr zu empfehlen!",
    "Ein tolles Team mit viel Erfahrung und Kompetenz. Die Zusammenarbeit war unkompliziert und das Ergebnis einfach perfekt.",
    "Super zufrieden mit allem! Schnelle Bearbeitung, faire Preise und ein Ergebnis, das meine Erwartungen übertroffen hat.",
    "Professionell, freundlich und zuverlässig. Genau so stellt man sich guten Service vor. Kann ich uneingeschränkt empfehlen!",
    "Die Qualität ist wirklich herausragend. Man merkt, dass hier mit Leidenschaft und Expertise gearbeitet wird. Toll gemacht!",
    "Von der ersten Beratung bis zur finalen Umsetzung - alles perfekt! Das Team ist kompetent und sehr kundenorientiert.",
    "Ich bin rundum begeistert! Schnelle Abwicklung, top Qualität und ein sehr fairer Preis. Was will man mehr?",
    "Excellent service and outstanding quality! The team was very professional and delivered exactly what was promised.",
    "Amazing experience from start to finish. Great communication, timely delivery, and superb results. Highly recommended!",
    "The attention to detail is remarkable. Every aspect was handled with care and precision. Absolutely fantastic work!",
    "Outstanding professionalism and quality. The team exceeded all expectations and delivered exceptional results.",
    "Brilliant work and excellent customer service. Everything was handled smoothly and efficiently. Very impressed!",
    "Top-notch quality and service. The team was knowledgeable, friendly, and delivered exactly what we needed.",
    "Incredible attention to detail and superior craftsmanship. The final result is absolutely perfect!",
    "Exceptional quality and outstanding customer service. The entire process was smooth and professional.",
    "Amazing team with great expertise! They delivered beyond expectations and the quality is simply outstanding.",
    "Sehr gute Erfahrung gemacht. Das Team ist kompetent und arbeitet sehr sorgfältig. Das Ergebnis kann sich sehen lassen!",
    "Bin mit der Qualität sehr zufrieden. Alles wurde wie versprochen umgesetzt und der Service war erstklassig.",
    "Tolle Arbeit! Von der Planung bis zur Umsetzung lief alles reibungslos. Sehr empfehlenswert!",
    "Das Team hat wirklich gute Arbeit geleistet. Alles wurde termingerecht und in hoher Qualität abgeliefert.",
    "Sehr professionelle Herangehensweise und exzellente Umsetzung. Bin mit dem Ergebnis mehr als zufrieden!",
    "Kompetente Beratung und hervorragende Ausführung. Das Preis-Leistungs-Verhältnis stimmt absolut.",
    "Ein wirklich tolles Erlebnis! Das Team war sehr freundlich und hat hervorragende Arbeit geleistet.",
    "Alles hat perfekt geklappt. Schnelle Bearbeitung, faire Preise und ein Ergebnis, das überzeugt!",
    "Sehr zufrieden mit der gesamten Abwicklung. Professionell, zuverlässig und qualitativ hochwertig.",
    "Die Zusammenarbeit war unkompliziert und das Endergebnis ist einfach perfekt. Gerne wieder!",
    "Top Service und herausragende Qualität. Kann ich jedem wärmstens empfehlen!",
    "Das Team hat alle Erwartungen übertroffen. Sehr professionell und kundenorientiert.",
    "Exzellente Beratung und perfekte Umsetzung. Bin rundum begeistert vom Ergebnis!",
    "Wunderbare Erfahrung! Alles wurde wie besprochen umgesetzt und die Qualität ist erstklassig.",
    "Sehr empfehlenswert! Kompetentes Team, faire Preise und hervorragende Qualität."
]

EMAILS = [
    "anna.mueller@email.com", "max.schmidt@test.de", "lisa.weber@mail.com",
    "tom.fischer@example.org", "sarah.bauer@web.de", "felix.wagner@gmail.com",
    "emma.richter@yahoo.de", "paul.neumann@hotmail.com", "mia.hoffmann@outlook.de",
    "leon.zimmermann@gmx.de", "lena.braun@t-online.de", "finn.krueger@freenet.de",
    "lara.schulz@posteo.de", "nils.koehler@tutanota.com", "julia.koenig@protonmail.com",
    "tim.lehmann@mailbox.org", "nina.fuchs@web.de", "jan.guenther@gmail.com",
    "maya.klein@yahoo.com", "luis.schwarz@hotmail.de", "zoe.weiss@outlook.com",
    "ben.hartmann@gmx.at", "eva.schroeder@mail.at", "noah.lange@email.at",
    "pia.schmitt@live.de", "henri.peters@icloud.com", "lea.hansen@me.com",
    "elias.mueller@aol.com", "amelie.werner@zoho.com", "jonas.krause@yandex.com",
    "sophie.friedrich@fastmail.com", "david.meier@rocketmail.com", 
    "charlotte.wolf@mail.ru", "alexander.jung@inbox.com", "marie.hahn@rediffmail.com"
]

def create_test_review(index):
    """Erstellt eine Test-Bewertung"""
    
    # Zufällige Daten auswählen
    name = NAMES[index % len(NAMES)]
    email = EMAILS[index % len(EMAILS)] if random.choice([True, False, True]) else None  # 2/3 haben E-Mail
    rating = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 5, 15, 25])[0]  # Mehr hohe Bewertungen
    title = random.choice(TITLES) if random.choice([True, False]) else None  # 50% haben Titel
    content = COMMENTS[index % len(COMMENTS)]
    
    review_data = {
        "name": name,
        "rating": rating,
        "content": content
    }
    
    if email:
        review_data["email"] = email
    if title:
        review_data["title"] = title
    
    return review_data

def create_reviews():
    """Erstellt 35 Test-Bewertungen mit Pausen zwischen den Anfragen"""
    print("🚀 Erstelle 35 Test-Bewertungen (mit Pausen für Rate-Limiting)...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    rate_limited_count = 0
    
    for i in range(35):
        try:
            review_data = create_test_review(i)
            
            response = requests.post(
                REVIEWS_ENDPOINT,
                json=review_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                success_count += 1
                print(f"✅ Review {i+1:2d}: {review_data['name']} - {review_data['rating']}⭐")
                # Kurze Pause zwischen erfolgreichen Anfragen
                time.sleep(0.5)
                
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"⏳ Review {i+1:2d}: Rate-Limit erreicht - warte 65 Sekunden...")
                time.sleep(65)  # Warte etwas mehr als 1 Minute
                
                # Nochmal versuchen
                response = requests.post(
                    REVIEWS_ENDPOINT,
                    json=review_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    success_count += 1
                    print(f"✅ Review {i+1:2d}: {review_data['name']} - {review_data['rating']}⭐ (nach Wartezeit)")
                    time.sleep(0.5)
                else:
                    error_count += 1
                    print(f"❌ Review {i+1:2d}: Immer noch Fehler {response.status_code}")
            else:
                error_count += 1
                print(f"❌ Review {i+1:2d}: Fehler {response.status_code} - {response.text[:100]}")
                
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"❌ Review {i+1:2d}: Verbindungsfehler - {str(e)[:100]}")
        except Exception as e:
            error_count += 1
            print(f"❌ Review {i+1:2d}: Unbekannter Fehler - {str(e)[:100]}")
    
    print("-" * 60)
    print(f"✅ Erfolgreich erstellt: {success_count}")
    print(f"⏳ Rate-Limit erreicht: {rate_limited_count} mal")
    print(f"❌ Fehler: {error_count}")
    print(f"📊 Gesamt: {success_count + error_count}")
    
    if success_count > 0:
        print(f"\n🎉 {success_count} Test-Bewertungen wurden erfolgreich erstellt!")
        print(f"📱 Frontend: http://localhost:3000")
        print(f"🔧 API: {REVIEWS_ENDPOINT}")

if __name__ == "__main__":
    try:
        # Zuerst testen ob die API erreichbar ist
        response = requests.get(f"{API_BASE_URL}/api/reviews", timeout=5)
        if response.status_code == 200:
            print("✅ API ist erreichbar")
            create_reviews()
        else:
            print(f"❌ API antwortet mit Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Kann API nicht erreichen: {e}")
        print("💡 Stelle sicher, dass das Backend läuft: docker-compose up -d")
