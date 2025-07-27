#!/usr/bin/env python3
"""
Script zum direkten Erstellen von Test-Bewertungen in der Datenbank
(umgeht das API Rate-Limiting für Testzwecke)
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Pfad für Import hinzufügen
sys.path.append('/Users/renesuss/Development/Tools/src/guestbook-project/backend')

# Backend-Module importieren
from app.database import SessionLocal, engine
from app.models import Base, Review
from app.schemas import RatingEnum

# Test-Daten (gleiche wie im API-Script)
TEST_DATA = {
    "names": [
        "Anna Müller", "Max Schmidt", "Lisa Weber", "Tom Fischer", "Sarah Bauer",
        "Felix Wagner", "Emma Richter", "Paul Neumann", "Mia Hoffmann", "Leon Zimmermann",
        "Lena Braun", "Finn Krüger", "Lara Schulz", "Nils Köhler", "Julia König",
        "Tim Lehmann", "Nina Fuchs", "Jan Günther", "Maya Klein", "Luis Schwarz",
        "Zoe Weiß", "Ben Hartmann", "Eva Schröder", "Noah Lange", "Pia Schmitt",
        "Henri Peters", "Lea Hansen", "Elias Müller", "Amelie Werner", "Jonas Krause",
        "Sophie Friedrich", "David Meier", "Charlotte Wolf", "Alexander Jung", "Marie Hahn"
    ],
    
    "titles": [
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
    ],
    
    "comments": [
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
        "Ein wirklich tolles Erlebnis! Das Team war sehr freundlich und hat hervorragende Arbeit geleistet."
    ],
    
    "emails": [
        "anna.mueller@email.com", "max.schmidt@test.de", "lisa.weber@mail.com",
        "tom.fischer@example.org", "sarah.bauer@web.de", "felix.wagner@gmail.com",
        "emma.richter@yahoo.de", "paul.neumann@hotmail.com", "mia.hoffmann@outlook.de",
        "leon.zimmermann@gmx.de", "lena.braun@t-online.de", "finn.krueger@freenet.de",
        "lara.schulz@posteo.de", "nils.koehler@tutanota.com", "julia.koenig@protonmail.com",
        "tim.lehmann@mailbox.org", "nina.fuchs@web.de", "jan.guenther@gmail.com",
        "maya.klein@yahoo.com", "luis.schwarz@hotmail.de", "zoe.weiss@outlook.com",
        "ben.hartmann@gmx.at", "eva.schroeder@mail.at", "noah.lange@email.at",
        "pia.schmitt@live.de", "henri.peters@icloud.com", "lea.hansen@me.com"
    ]
}

def create_database_reviews(count=25):
    """Erstellt Reviews direkt in der Datenbank"""
    print(f"🚀 Erstelle {count} Test-Bewertungen direkt in der Datenbank...")
    print("-" * 60)
    
    # Datenbankverbindung
    db = SessionLocal()
    success_count = 0
    
    try:
        for i in range(count):
            # Zufällige Daten generieren
            name = random.choice(TEST_DATA["names"])
            email = random.choice(TEST_DATA["emails"]) if random.choice([True, False, True]) else None
            rating = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 5, 15, 25])[0]
            title = random.choice(TEST_DATA["titles"]) if random.choice([True, False]) else None
            content = random.choice(TEST_DATA["comments"])
            
            # Zufälliges Datum in den letzten 30 Tagen
            days_ago = random.randint(0, 30)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            # Review-Objekt erstellen
            review = Review(
                name=name,
                email=email,
                rating=rating,
                title=title,
                content=content,
                created_at=created_at,
                is_approved=True,
                is_featured=random.choice([True, False, False, False])  # 25% featured
            )
            
            db.add(review)
            success_count += 1
            
            # Status anzeigen
            stars = "⭐" * rating
            featured = " 🌟" if review.is_featured else ""
            print(f"✅ Review {i+1:2d}: {name} - {rating}{stars}{featured}")
        
        # Alle Änderungen committen
        db.commit()
        print("-" * 60)
        print(f"🎉 {success_count} Test-Bewertungen erfolgreich in der Datenbank erstellt!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Fehler beim Erstellen der Reviews: {e}")
    finally:
        db.close()

def show_stats():
    """Zeigt Statistiken der Reviews"""
    db = SessionLocal()
    try:
        total_reviews = db.query(Review).count()
        featured_reviews = db.query(Review).filter(Review.is_featured == True).count()
        
        ratings_stats = {}
        for rating in [1, 2, 3, 4, 5]:
            count = db.query(Review).filter(Review.rating == rating).count()
            ratings_stats[rating] = count
        
        print("\n📊 Review-Statistiken:")
        print("-" * 30)
        print(f"Gesamt: {total_reviews}")
        print(f"Featured: {featured_reviews}")
        print("\n🌟 Bewertungen:")
        for rating, count in ratings_stats.items():
            stars = "⭐" * rating
            print(f"  {rating} {stars}: {count}")
        
        print(f"\n📱 Frontend: http://localhost:3000")
        print(f"🔧 API: http://localhost:8000/api/reviews")
        
    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Statistiken: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    try:
        # 25 zusätzliche Reviews erstellen (haben bereits ~12)
        create_database_reviews(25)
        show_stats()
    except Exception as e:
        print(f"❌ Allgemeiner Fehler: {e}")
        print("💡 Stelle sicher, dass das Backend läuft und die Datenbank erreichbar ist")
